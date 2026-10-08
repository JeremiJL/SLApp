from ..collector import Collector

from docx import Document

class PiuwCollector(Collector):
    
    def __init__(self, project_configuration, file_name, month, year):
        super().__init__(project_configuration)
        
        self.file_name = file_name
        self.month = month
        self.year = year
        
    def get_month(self):
        return self.month
    
    def get_year(self):
        return self.year
    
    def get_project_name(self):
        return self.project_configuration['project_name']
        
    def collect_tickets_data(self):
        raport_file_path = self.get_raport_path_name()
        raport_as_records_list = self.fetch_raport_as_records_list(raport_file_path)
        return raport_as_records_list
       
    def get_raport_path_name(self):
        full_path_name = self.file_name
        return full_path_name
    
    def fetch_raport_as_records_list(self, file_path):
        word_document = Document(file_path)
        
        records_list = []
        for table in word_document.tables:
            for row in table.rows:
                record = []
                
                for cell in row.cells:
                    content = cell.text
                    content = self.format_docx_cell_content(content)
                    record.append(content)
                    
                records_list.append(record)
        
        records_list = self.remove_table_headers(records_list)
        return records_list
    
    def remove_table_headers(self, records_list):
        return records_list[3:]
        
    def format_docx_cell_content(self, content):
        content = str(content).replace('\xa0', ' ')
        return content
                