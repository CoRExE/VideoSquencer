import os
from jinja2 import Template


class HTMLReportWriter:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def write_report(self, report_name, folder_path):
        if not os.path.exists(self.folder_path + '/report'):
            os.mkdir(self.folder_path + '/report')

        # Read the index.html template
        with open('../template/index.html', 'r') as file:
            index_template_content = file.read()

        # Create a Jinja2 template object for index.html
        index_template = Template(index_template_content)

        # Render the index.html template with the report data
        index_result = index_template.render(report_name=report_name, content=self.generate_cards(folder_path))

        # Write the rendered index.html to the report folder
        with open(self.folder_path + '/report/index.html', 'w') as file:
            file.write(index_result)

    def generate_cards(self, folder_path):
        pass

    def generate_card(self, folder_name, folder_path):
        pass
