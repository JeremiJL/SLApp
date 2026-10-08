from abc import ABC, abstractmethod

class Visualizer(ABC):
    
    def __init__(self, project_configuration, contractor_schedule, computed_schedule):
        self.project_configuration = project_configuration
        
        self.computed_schedule = computed_schedule
        self.contractor_schedule = contractor_schedule
           
    @abstractmethod
    def visualize(self):
        pass
    
    def get_output_file_path(self):
        output_file_directory = self.get_output_file_directory()
        output_file_name = self.get_output_file_name()
        
        output_file_path = output_file_directory + output_file_name
        return output_file_path
    
    @abstractmethod
    def get_output_file_directory(self):
        pass
    
    def get_output_file_name(self):
        project_name = self.computed_schedule.project_name
        month = self.computed_schedule.month
        year = self.computed_schedule.year
        
        output_file_name = str(project_name) + "-" + str(month) + "-" + str(year)
        return output_file_name
    