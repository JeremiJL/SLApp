from ..decidim_translator import DecidimTranslator
from domain.interval import Interval
from .tools.redmine_intervals_extractor import IntervalsExtractor

from datetime import datetime


class DecidimSourceTranslator(DecidimTranslator):
      
    def __init__(self, project_configuration, data_collector):
        super().__init__(project_configuration, data_collector)
        
        self.intervals_extractor = IntervalsExtractor(project_configuration=project_configuration, data_collector=data_collector)
                
                
    def are_there_any_tickets_in_given_month(self):
        return True
            
    def create_all_tickets_representations(self):
        
        tickets_as_dictionaries_list = self.data_collector.collect_tickets_data()
        ticket_representations = []
        
        for ticket_as_dictionary in tickets_as_dictionaries_list:
            ticket_representations.append(self.create_ticket_representation(ticket_as_dictionary))
            
        return ticket_representations
                
    def extract_ticket_id(self, ticket_as_dictionary):
        ticket_id = ticket_as_dictionary['id']
        ticket_id_as_integer = int(ticket_id)
        return ticket_id_as_integer

    def extract_ticket_creation_date_time(self, ticket_as_dictionary):
        date_as_string = ticket_as_dictionary['created_on']
        return date_as_string
    
    def extract_ticket_closure_date_time(self, ticket_as_dictionary):
        date_as_string = ticket_as_dictionary['closed_on']
        return date_as_string
    
    def extract_ticket_full_completion_time(self, ticket_data_as_dictionary):
        return None
        
    def extract_ticket_priority(self, ticket_as_dictionary):
        ticket_priority = ticket_as_dictionary['custom_fields']['custom_field'][2]['value']
        return ticket_priority
    
    def extract_ticket_importance_level(self, ticket_as_dictionary):
        ticket_importance_level = ticket_as_dictionary['custom_fields']['custom_field'][1]['value']
        return ticket_importance_level
    
    def extract_ticket_exceeds_maximum_time(self, ticket_as_dictionary):
        return None
    
    def extract_time_intervals_on_side_of_contractor(self, ticket_as_dictionary, creation_date_time, ticket_closure_date):
        return self.intervals_extractor.extract_time_intervals_on_side_of_contractor(ticket_as_dictionary, creation_date_time, ticket_closure_date)