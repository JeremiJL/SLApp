from .protocol_visualizer import ProtocolVisualizer
from services.date_service import get_next_month, get_number_of_days_in_a_month, get_month_name, get_current_day

from docxtpl import DocxTemplate

class PiuwProtocolVisualizer(ProtocolVisualizer):
    
    def __init__(self, project_configuration, contractor_schedule, computed_schedule):
        super().__init__(project_configuration, contractor_schedule, computed_schedule)
        
    def get_output_file_name(self):
        output_file_name = super().get_output_file_name()
        output_file_name_with_extension = output_file_name + ".docx"
        return output_file_name_with_extension
    
    def visualize(self):
        output_file_path = self.get_output_file_path()
        self.create_protocol_as_docx(output_file_path)

    def create_protocol_as_docx(self, output_file_path):
        protocol_template_pathname = self.get_protocol_template_pathname()
        document = DocxTemplate(protocol_template_pathname)
        document = self.set_document_variables_values(document)
        document.save(output_file_path)
        
    def set_document_variables_values(self, document):
        variables_and_values = self.create_document_variables()
        self.save_document_variables_names_in_reference_file(variables_and_values.keys())
        
        document.render(variables_and_values)
        return document
    
    def create_document_variables(self):
        month = self.computed_schedule.month
        month_name = get_month_name(month)
        next_month = get_next_month(month)
        year = self.computed_schedule.year
        number_of_days_in_month = get_number_of_days_in_a_month(month, year)
        day = get_current_day()
        
        variables_and_values = { 'MONTH' : month, 'MONTH_NAME' : month_name, 'NEXT_MONTH' : next_month, 'YEAR' : year,
                  'NUMBER_OF_DAYS_IN_MONTH' : number_of_days_in_month, 'DAY' : day}
        
        return variables_and_values
    
    def save_document_variables_names_in_reference_file(self, variables_names):
        protocol_available_variables_pathname = self.get_protocol_available_variables_pathname()
        
        with open(protocol_available_variables_pathname, "w") as variables_names_file:
            for variable_name in variables_names:
                variable_in_jinja_format = "{{ " + variable_name + " }}"
                variables_names_file.write(variable_in_jinja_format + "\n")
    
    def get_protocol_available_variables_pathname(self):
        protocol_available_variables_pathname = self.project_configuration['path_names']['output']['available_variables_for_protocols']
        return protocol_available_variables_pathname
        
    def get_protocol_template_pathname(self):
        protocol_template_pathname = self.project_configuration['path_names']['input']['protocol']
        return protocol_template_pathname
    