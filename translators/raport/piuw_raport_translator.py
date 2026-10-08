from ..translator import Translator
from ..date_formatter import format_date_as_string_to_date_object_with_present_time_zone
from domain.piuw.piuw_ticket import PiuwTicket

class PiuwRaportTranslator(Translator):
    
    def __init__(self, project_configuration, data_collector):
        super().__init__(project_configuration, data_collector)
        
    def get_tickets(self):
        raw_tickets_list_data = self.data_collector.collect_tickets_data()
        tickets_representations = []
        for raw_ticket in raw_tickets_list_data:
            translated_ticket = self.create_ticket_representation(raw_ticket)
            tickets_representations.append(translated_ticket)
            
        return tickets_representations
    
    def create_ticket_representation(self, ticket_data):
        ticket_id = self.extract_ticket_id(ticket_data)
        ticket_creation_date = format_date_as_string_to_date_object_with_present_time_zone(self.extract_ticket_creation_date_time(ticket_data))
        ticket_closure_date = format_date_as_string_to_date_object_with_present_time_zone(self.extract_ticket_closure_date_time(ticket_data))
        ticket_time_intervals_on_side_of_contractor = self.extract_time_intervals_on_side_of_contractor(ticket_data, ticket_creation_date, ticket_closure_date)
        ticket_full_completion_time = self.extract_ticket_full_completion_time(ticket_data)
        ticket_exceeds_time = self.extract_ticket_exceeds_maximum_time(ticket_data)
        ticket_priority = self.extract_ticket_priority(ticket_data)
        ticket_url = self.extract_ticket_url(ticket_data)
 
        ticket = PiuwTicket(ticket_id=ticket_id, creation_date_time=ticket_creation_date, url=ticket_url, priority=ticket_priority,
                                   closure_date_time=ticket_closure_date, time_intervals=ticket_time_intervals_on_side_of_contractor,
                                   full_completion_time=ticket_full_completion_time, exceeds_maximum_time=ticket_exceeds_time)
        return ticket
    
    
    def extract_ticket_id(self, ticket_data):
        ticket_id = ticket_data[2]
        ticket_as_integer = int(ticket_id)
        return ticket_as_integer
    
    def extract_ticket_priority(self, ticket_data):
        ticket_priority = ticket_data[3]
        return ticket_priority

    def extract_ticket_creation_date_time(self, ticket_data):
        ticket_creation_date = ticket_data[0]
        return ticket_creation_date
    
    def extract_ticket_closure_date_time(self, ticket_data):
       ticket_closure_date = None
       return ticket_closure_date
   
    def extract_ticket_full_completion_time(self, ticket_data):
        ticket_completion_time = ticket_data[7]
        completion_time_as_integer = int(ticket_completion_time)
        return completion_time_as_integer

    def extract_time_intervals_on_side_of_contractor(self, ticket_data, creation_date_time, ticket_closure_date):
        return None
    
    def extract_ticket_exceeds_maximum_time(self, ticket_data):
        amount_of_minutes_that_exceed_max_time = ticket_data[8]
        does_ticket_exceeds_time = (int(amount_of_minutes_that_exceed_max_time) > 0)
        return does_ticket_exceeds_time
    
    def extract_ticket_url(self, ticket_data):
        url_for_single_ticket = self.get_single_ticket_endpoint()
        ticket_id = self.extract_ticket_id(ticket_data)
        url_for_this_specific_ticket = str(url_for_single_ticket) + str(ticket_id)
        return url_for_this_specific_ticket
    
    def get_single_ticket_endpoint(self):
        return self.project_configuration['api']['endpoints']['single_issue']