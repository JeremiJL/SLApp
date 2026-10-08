from ..translator import Translator
from domain.piuw.piuw_schedule import PiuwSchedule
from domain.piuw.piuw_ticket import PiuwTicket
from .tools.redmine_intervals_extractor import IntervalsExtractor
from ..date_formatter import format_date_as_string_to_date_object_with_present_time_zone

class PiuwTranslator(Translator):
    
    def __init__(self, project_configuration, data_collector):
        super().__init__(project_configuration, data_collector)
        
        self.intervals_extractor = IntervalsExtractor(project_configuration=project_configuration, data_collector=data_collector)
        
        
    def get_tickets(self):
        if self.are_there_any_tickets_in_given_month():
            return self.create_all_tickets_representations()
        else:
            return []
        
    def are_there_any_tickets_in_given_month(self):
        return True
        
    def create_all_tickets_representations(self):
        
        tickets_as_dictionaries_list = self.data_collector.collect_tickets_data()
        ticket_representations = []
        
        for ticket_as_dictionary in tickets_as_dictionaries_list:
            ticket_representations.append(self.create_ticket_representation(ticket_as_dictionary))
            
        return ticket_representations
        
    def create_ticket_representation(self, ticket_data):
        ticket_id = self.extract_ticket_id(ticket_data)
        ticket_creation_date = format_date_as_string_to_date_object_with_present_time_zone(self.extract_ticket_creation_date_time(ticket_data))
        ticket_closure_date = format_date_as_string_to_date_object_with_present_time_zone(self.extract_ticket_closure_date_time(ticket_data))
        ticket_time_intervals_on_side_of_contractor = self.extract_time_intervals_on_side_of_contractor(ticket_data, ticket_creation_date, ticket_closure_date)
        ticket_full_completion_time = self.extract_ticket_full_completion_time(ticket_data)
        ticket_exceeds_time = self.extract_ticket_exceeds_maximum_time(ticket_data)
        ticket_priority = self.extract_ticket_priority(ticket_data)
        ticket_url = self.extract_ticket_url(ticket_data)
        
        ticket = PiuwTicket(ticket_id=ticket_id, creation_date_time=ticket_creation_date, priority=ticket_priority, url=ticket_url,
                                   closure_date_time=ticket_closure_date, time_intervals=ticket_time_intervals_on_side_of_contractor,
                                   full_completion_time=ticket_full_completion_time, exceeds_maximum_time=ticket_exceeds_time)
        
        return ticket
    
    def extract_ticket_id(self, ticket_as_dictionary):
        ticket_id = ticket_as_dictionary['id']
        ticket_id_as_integer = int(ticket_id)
        return ticket_id_as_integer

    def extract_ticket_creation_date_time(self, ticket_as_dictionary):
        date_as_string = ticket_as_dictionary['created_on']
        return date_as_string
    
    def extract_ticket_closure_date_time(self, ticket_as_dictionary):
        closure_date_as_string = ticket_as_dictionary['closed_on']
        
        if closure_date_as_string == None:
            closure_date_as_string = ticket_as_dictionary['updated_on']    
            
        return closure_date_as_string
    
    def extract_ticket_priority(self, ticket_as_dictionary):
        priority_full_name = ticket_as_dictionary['tracker']['@name']
        priority_code = priority_full_name[-1]
        return priority_code
    
    def extract_ticket_url(self, ticket_as_dictionary):
        url_for_single_ticket = self.get_single_ticket_endpoint()
        ticket_id = self.extract_ticket_id(ticket_as_dictionary)
        url_for_this_specific_ticket = str(url_for_single_ticket) + str(ticket_id)
        return url_for_this_specific_ticket
    
    def get_single_ticket_endpoint(self):
        return self.project_configuration['api']['endpoints']['single_issue']
    
    def extract_time_intervals_on_side_of_contractor(self, ticket_as_dictionary, creation_date_time, ticket_closure_date):
        return self.intervals_extractor.extract_time_intervals_on_side_of_contractor(ticket_as_dictionary, creation_date_time, ticket_closure_date)

    def extract_ticket_exceeds_maximum_time(self, ticket_data):
        return None
    
    def extract_ticket_full_completion_time(self, ticket_data):
        return None
    
    