from abc import ABC, abstractmethod

class Collector(ABC):
    
    def __init__(self, project_configuration):
        self.project_configuration = project_configuration
        
    @abstractmethod
    def collect_tickets_data(self):
        pass
    
    @abstractmethod
    def get_project_name(self):
        pass
    
    @abstractmethod
    def get_month(self):
        pass
    
    @abstractmethod
    def get_year(self):
        pass