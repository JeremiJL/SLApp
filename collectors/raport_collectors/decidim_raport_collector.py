from ..collector import Collector

import pandas

class DecidimCollector(Collector):
    
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
        raport_as_data_frame = self.fetch_raport_as_data_frame(raport_file_path)
        return raport_as_data_frame
       
    def get_raport_path_name(self):
        full_path_name = self.file_name
        return full_path_name
    
    def fetch_raport_as_data_frame(self, file_path):
        raport_as_data_frame = pandas.read_excel(file_path, sheet_name=1)    
        return raport_as_data_frame