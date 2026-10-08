from ..decidim_translator import DecidimTranslator

from datetime import datetime
from dateutil import tz as time_zone_calculator

class DecidimRaportTranslator(DecidimTranslator):
    
    def __init__(self, project_configuration, data_collector):
        super().__init__(project_configuration, data_collector)
             
    def are_there_any_tickets_in_given_month(self):
        return True         
 
    def create_all_tickets_representations(self):
        
        tickets_as_data_frame = self.data_collector.collect_tickets_data()
        
        tickets_list = []
        for _, ticket_as_row in tickets_as_data_frame.iterrows():
            tickets_list.append(self.create_ticket_representation(ticket_as_row))
        
        return tickets_list
        
    def extract_ticket_id(self, ticket_as_row_of_data_frame):
        ticket_id = ticket_as_row_of_data_frame['ID Redmine']
        return ticket_id
    
    def extract_ticket_creation_date_time(self, ticket_as_row_of_data_frame):
        date_as_string = ticket_as_row_of_data_frame['Data utworzenia']
        return date_as_string
    
    def extract_ticket_closure_date_time(self, ticket_as_row_of_data_frame):
        date_as_string = ticket_as_row_of_data_frame['Data zamknięcia']
        return date_as_string
    
    def extract_time_intervals_on_side_of_contractor(self, ticket_as_row_of_data_frame, ticket_creation_date, ticket_closure_date):
        return []
    
    def extract_ticket_priority(self, ticket_as_row_of_data_frame):
        ticket_priority = ticket_as_row_of_data_frame['Poziomy niedostępności']
        return ticket_priority
    
    def format_date_as_string_to_date_object_with_present_time_zone(self, date_as_string):
        present_time_zone = time_zone_calculator.gettz('Europe / Berlin')
        date_as_iso = datetime.fromisoformat(date_as_string)
        date_with_present_time_zone = date_as_iso.astimezone(present_time_zone)
        return date_with_present_time_zone
    
    def extract_ticket_importance_level(self, ticket_as_row_of_data_frame):
        ticket_importance_level = ticket_as_row_of_data_frame['Poziom istotności']
        return ticket_importance_level
    
    def extract_ticket_full_completion_time(self, ticket_as_row_of_data_frame):
        ticket_completion_time = ticket_as_row_of_data_frame['Czas naprawy']
        return ticket_completion_time
    
    def extract_ticket_exceeds_maximum_time(self, ticket_as_row_of_data_frame):
        does_ticket_exceeds_maximum_time_as_string = ticket_as_row_of_data_frame['Przekroczenie']
        
        if (does_ticket_exceeds_maximum_time_as_string == 'TAK'):
            return True
        else:
            return False