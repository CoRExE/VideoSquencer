import os
from jinja2 import Template
import tempfile
import shutil


class HTMLReportWriter:
    def __init__(self, folder_path, report_name, metadata=None):
        self.folder_path = folder_path
        self.report_name = report_name
        self.metadata = metadata
        self.temp_dir = tempfile.mkdtemp()

    def write_report(self):

        index_page = Template(open(r'templates/index.html', 'r').read())
        index_result = index_page.render(report_name=self.report_name, content=self.generate_cards())

        with open(self.temp_dir + '/index.html', 'w') as f:
            f.write(index_result)

        self.generate_lists(self.folder_path)

        for file in os.listdir(self.temp_dir):
            shutil.move(self.temp_dir + '/' + file, self.folder_path + '/' + file)

        shutil.rmtree(self.temp_dir)

    def generate_cards(self):
        result = ""

        card_component = Template(open(r'templates/card.html', 'r').read())

        for folder in os.listdir(self.folder_path):
            if os.path.isdir(self.folder_path + '/' + folder):
                result += self.generate_card(card_component, folder)

        return result

    def generate_card(self, component, folder):
        return component.render(folder=folder,
                                filename=self.metadata[folder]['name'],
                                filesize=self.metadata[folder]['size'],
                                last_modified=self.metadata[folder]['modified'],
                                md5=self.metadata[folder]['md5'],
                                number_frames=len(os.listdir(self.folder_path + '/' + folder)),
                                folder_dest=folder + '.html'
                                )

    def generate_lists(self, folder):
        for unfolder in os.listdir(folder):
            if os.path.isdir(folder + '/' + unfolder):
                self.generate_list(unfolder)

    def generate_list(self, folder):
        result = ""

        list_component = Template(open(r'templates/frame_list.html', 'r').read())

        compt = 0
        for file in os.listdir(self.folder_path + '/' + folder):
            if file.endswith(".jpg") or file.endswith(".png"):
                if compt == 5:
                    result += "</tr>\n<tr>"
                    compt = 0
                else:
                    result += ("<td><img src='" + folder + "/" + file + "'>" +
                               "<a href='" + folder + "/" + file + "' target='_blank'>" + file + "</a>" + "</td>\n")
                    compt += 1
        result += "</tr>"

        with open(self.temp_dir + '/' + folder + '.html', 'w') as f:
            f.write(list_component.render(title=folder, images=result))
