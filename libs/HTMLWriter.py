import os
from jinja2 import Template


class HTMLReportWriter:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def write_report(self, report_name):

        # TODO : Générer le Report Hors dossier et le déplacer une fois fini

        if not os.path.exists(self.folder_path + '/report'):
            os.mkdir(self.folder_path + '/report')

        # Read the index.html template
        with open('./template/index.html', 'r') as file:
            index_template_content = file.read()

        # Create a Jinja2 template object for index.html
        index_template = Template(index_template_content)

        # Render the index.html template with the report data
        index_result = index_template.render(report_name=report_name, content=self.generate_cards(self.folder_path))

        # Write the rendered index.html to the report folder
        with open(self.folder_path + '/report/index.html', 'w') as file:
            file.write(index_result)

    def generate_cards(self, folder_path):
        content = ""

        for nom_fichier in os.listdir(folder_path):
            chemin_fichier = folder_path + '/' + nom_fichier
            if os.path.isdir(chemin_fichier):
                content += self.generate_card(chemin_fichier)
                self.generate_list(chemin_fichier)

        return content

    @staticmethod
    def generate_card(folder):
        # Read the frame_list.html template
        with open(r'./template/card.html', 'r') as file:
            card_template_content = file.read()

        # Create a Jinja2 template object for frame_list.html
        card_template = Template(card_template_content)

        # Render the frame_list.html template with the report data
        return card_template.render(folder=folder, number_files=len(os.listdir(folder)),
                                    folder_dest="frame_list_" + folder.split('/')[-1] + ".html")

    def generate_list(self, folder):
        # TODO : Générer les Listes dans le Report
        pass
