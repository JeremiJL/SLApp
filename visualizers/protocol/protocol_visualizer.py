from visualizers.visualizer import Visualizer

from abc import abstractmethod

class ProtocolVisualizer(Visualizer):
    
    def get_output_file_name(self):
        output_file_name = super().get_output_file_name()
        output_file_name += "-protokół"
        return output_file_name
    
    def get_output_file_directory(self):
        output_file_directory = self.project_configuration['path_names']['output']['protocol']
        return output_file_directory
    
    @abstractmethod
    def visualize(self):
        pass