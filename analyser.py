import collectors
import collectors.raport_collectors
import collectors.raport_collectors.decidim_raport_collector
import collectors.raport_collectors.piuw_raport_collector
import collectors.source_collectors
import collectors.source_collectors.piuw_collector
import collectors.source_collectors.redmine_collector
import interpreters.priorities_interpreter
import translators
import interpreters
import translators.raport
import translators.raport.decidim_raport_translator
import translators.raport.piuw_raport_translator
import translators.source
import translators.source.decidim_source_translator
import translators.source.piuw_source_translator
import visualizers.analysis.analysis_visualizer
import visualizers.analysis.decidim_txt_visualizer
import visualizers
import visualizers.analysis.decidim_xlsx_visualizer
import visualizers.analysis.txt_visualizer
import visualizers.analysis.xlsx_visualizer
from exceptions.analyser_exception import AnalyserException
from exceptions.collector_exception import CollectorException
import visualizers.protocol
import visualizers.protocol.piuw_visualizer
from services.configuration_provider import get_project_configuration

class Analyser:
    
    def __init__(self, api_key, year, month, project_identifier, raport_file_pathname):
        self.api_key = api_key
        self.year = year
        self.month = month
        self.project_identifier = project_identifier
        self.raport_file_pathname = raport_file_pathname
        
        self.project_configuration = get_project_configuration(project_identifier)
        
        self.interpreted_schedule = None
        self.contractor_schedule = None
        
    def analyze(self):
        self.interpret_source_data()
        self.translate_raport_data()
        
    def interpret_source_data(self):
        try:
            match self.project_identifier:
                case 'B':
                    self.interpret_source_data_of_b_project()
                case 'A':
                    self.interpret_source_data_of_a_project()
                case 'C':
                    self.interpret_source_data_of_c_project()
                case 'D':
                    self.interpret_source_data_of_d_project()
        except Exception:
            cause_of_exception = "Niepoprawny klucz dostępu API."
            advice_on_how_to_solve_it = "Upewnij się, że podałeś właściwy klucz dostępu API."
            raise CollectorException(cause=cause_of_exception, advice=advice_on_how_to_solve_it)
        
    def translate_raport_data(self):
        try:
            match self.project_identifier:
                case 'A':
                    self.translate_raport_data_of_a_project()
                case 'B':
                    self.translate_raport_data_of_b_project()
                case 'C':
                    self.translate_raport_data_of_c_project()
                case 'D':
                    self.translate_raport_data_of_d_project()
        except Exception:
            cause_of_exception = "Nieporawny format raportu wykonawcy."
            advice_on_how_to_solve_it = "Upewnij się, że plik który podałeś to właściwy raport wykonawcy."
            raise CollectorException(cause=cause_of_exception, advice=advice_on_how_to_solve_it)
            
    def export_analysis(self, output_file_format):
        
        match self.project_identifier:
            case 'B':
                output_file_path = self.export_b_project_analysis(output_file_format)
            case 'A':
                output_file_path = self.export_a_project_analysis(output_file_format)
            case 'C':
                output_file_path = self.export_c_project_analysis(output_file_format)
            case 'D':
                output_file_path = self.export_piuw_project_analysis(output_file_format)
                
        return output_file_path
    
    def export_protocol(self):
        
        match self.project_identifier:
            case 'D':
                output_file_path = self.export_d_project_protocol()
                
        return output_file_path
         
    def interpret_source_data_of_d_project(self):
        
        # 1 collect raw data from sorce
        source_collector = collectors.source_collectors.piuw_collector.PiuwCollector(self.project_configuration, month=self.month, year=self.year, api_key=self.api_key, data_format='xml')
        # 2 translate raw date into interpretable objects
        source_translator = translators.source.piuw_source_translator.PiuwTranslator(self.project_configuration, source_collector)
        # 3 interpret schedule objects
        schedule_before_interpretation = source_translator.get_schedule()
        source_interpreter = interpreters.priorities_interpreter.PrioritiesInterpreter(self.project_configuration, schedule_before_interpretation)
        self.interpreted_schedule = source_interpreter.get_interpreted_shedule()

    def translate_raport_data_of_d_project(self):
    
        # 5 collect raw data from contractor's raport
        raport_collector = collectors.raport_collectors.piuw_raport_collector.PiuwCollector(project_configuration=self.project_configuration, file_name=self.raport_file_pathname, month=self.month, year=self.year)
        # 6 translate raw date into interpretable objects
        raport_translator = translators.raport.piuw_raport_translator.PiuwRaportTranslator(self.project_configuration, raport_collector)
        self.contractor_schedule = raport_translator.get_schedule()
    
    def export_piuw_project_analysis(self, output_file_format):
        
        # compare and visualize
        match output_file_format:
            case 'XLSX':
                visualizer = visualizers.analysis.xlsx_visualizer.XlsxVisualizer(self.project_configuration, contractor_schedule=self.contractor_schedule, computed_schedule=self.interpreted_schedule)
            case 'TXT':
                visualizer = visualizers.analysis.txt_visualizer.TxtVisualizer(self.project_configuration, computed_schedule=self.interpreted_schedule, contractor_schedule=self.contractor_schedule)

        visualizer.visualize()
        visualization_output_file_pathname = visualizer.get_output_file_path()
        
        return visualization_output_file_pathname
    
    def export_d_project_protocol(self):
        visualizer = visualizers.protocol.piuw_visualizer.PiuwProtocolVisualizer(self.project_configuration, computed_schedule=self.interpreted_schedule, contractor_schedule=self.contractor_schedule)
        visualizer.visualize()
        visualization_output_file_pathname = visualizer.get_output_file_path()
        
        return visualization_output_file_pathname
    
    def interpret_source_data_of_a_project(self):
        return self.interpret_source_data_of_decidim_project()
    
    def translate_raport_data_of_a_project(self):
        return self.translate_raport_data_of_decidim_project()
    
    def export_a_project_analysis(self,output_file_format):
        return self.export_decidim_project_analysis(output_file_format)
    
    def interpret_source_data_of_b_project(self):
        return self.interpret_source_data_of_decidim_project()
    
    def translate_raport_data_of_b_project(self):
        return self.translate_raport_data_of_decidim_project()
    
    def export_b_project_analysis(self,output_file_format):
        return self.export_decidim_project_analysis(output_file_format)
    
    def interpret_source_data_of_c_project(self):
        return self.interpret_source_data_of_decidim_project()
    
    def translate_raport_data_of_c_project(self):
        return self.translate_raport_data_of_decidim_project()
    
    def export_c_project_analysis(self,output_file_format):
        return self.export_decidim_project_analysis(output_file_format)
    
    def interpret_source_data_of_decidim_project(self):
        
        # 1 collect raw data from sorce
        source_collector = collectors.source_collectors.redmine_collector.RedmineCollector(self.project_configuration, month=self.month, year=self.year, api_key=self.api_key, data_format='xml')
        # 2 translate raw date into interpretable objects
        source_translator = translators.source.decidim_source_translator.DecidimSourceTranslator(self.project_configuration, source_collector)
        # 3 interpret schedule objects
        schedule_before_interpretation = source_translator.get_schedule()
        source_interpreter = interpreters.priorities_interpreter.PrioritiesInterpreter(self.project_configuration, schedule_before_interpretation)
        self.interpreted_schedule = source_interpreter.get_interpreted_shedule()

    def translate_raport_data_of_decidim_project(self):
        
        # 5 collect raw data from contractor's raport
        raport_collector = collectors.raport_collectors.decidim_raport_collector.DecidimCollector(project_configuration=self.project_configuration, file_name=self.raport_file_pathname, month=self.month, year=self.year)
        # 6 translate raw date into interpretable objects
        raport_translator = translators.raport.decidim_raport_translator.DecidimRaportTranslator(self.project_configuration, raport_collector)
        self.contractor_schedule = raport_translator.get_schedule()

    def export_decidim_project_analysis(self, output_file_format):
        
        # compare and visualize
        match output_file_format:
            case 'XLSX':
                visualizer = visualizers.analysis.decidim_xlsx_visualizer.DecidimXlslxVisualizer(self.project_configuration, contractor_schedule=self.contractor_schedule, computed_schedule=self.interpreted_schedule)
            case 'TXT':
                visualizer = visualizers.analysis.decidim_txt_visualizer.DecidimTxtVisualizer(self.project_configuration, contractor_schedule=self.contractor_schedule, computed_schedule=self.interpreted_schedule)

        visualizer.visualize()
        visualization_output_file_pathname = visualizer.get_output_file_path()
        
        return visualization_output_file_pathname
    
    
    def get_number_of_analyzed_tickets(self):
        return len(self.interpreted_schedule.tickets)
    
    def get_number_of_tickets_that_does_not_match(self):
        return self.get_number_of_analyzed_tickets() - self.get_number_of_matching_tickets()
    
    def get_number_of_matching_tickets(self):
        visualizer = visualizers.analysis.txt_visualizer.TxtVisualizer(self.project_configuration, contractor_schedule=self.contractor_schedule, computed_schedule=self.interpreted_schedule)
        number_of_matching_tickets = visualizer.get_number_of_correctly_analysed_tickets()
        return number_of_matching_tickets