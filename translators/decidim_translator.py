from .translator import Translator
from domain.decidim.decidim_schedule import DecidimSchedule
from domain.decidim.decidim_ticket import DecidimTicket
from .date_formatter import format_date_as_string_to_date_object_with_present_time_zone

from abc import abstractmethod 

class DecidimTranslator(Translator):
    
    def __init__(self, project_configuration, data_collector):
        self.project_configuration = project_configuration
        self.data_collector = data_collector
        
    def get_schedule(self):
        year = self.data_collector.get_year()
        month = self.data_collector.get_month()
        project_name = self.data_collector.get_project_name()
        tickets = self.get_tickets()
        
        schedule = DecidimSchedule(month=month, year=year, tickets=tickets, project_name=project_name)
        return schedule
      
    def get_tickets(self):
        if self.are_there_any_tickets_in_given_month():
            return self.create_all_tickets_representations()
        else:
            return []
        
    @abstractmethod    
    def are_there_any_tickets_in_given_month(self):
        pass
        
    @abstractmethod
    def create_all_tickets_representations(self):
        pass
    
    def create_ticket_representation(self, ticket_data):
        ticket_id = self.extract_ticket_id(ticket_data)
        ticket_creation_date = format_date_as_string_to_date_object_with_present_time_zone(self.extract_ticket_creation_date_time(ticket_data))
        ticket_closure_date = format_date_as_string_to_date_object_with_present_time_zone(self.extract_ticket_closure_date_time(ticket_data))
        ticket_time_intervals_on_side_of_contractor = self.extract_time_intervals_on_side_of_contractor(ticket_data, ticket_creation_date, ticket_closure_date)
        ticket_full_completion_time = self.extract_ticket_full_completion_time(ticket_data)
        ticket_exceeds_time = self.extract_ticket_exceeds_maximum_time(ticket_data)
        ticket_priority = self.format_ticket_priority(self.extract_ticket_priority(ticket_data))
        ticket_importance_level = self.extract_ticket_importance_level(ticket_data)
        ticket_url = self.extract_ticket_url(ticket_data)
        
        ticket = DecidimTicket(ticket_id=ticket_id, creation_date_time=ticket_creation_date, url=ticket_url,
                                   closure_date_time=ticket_closure_date, time_intervals=ticket_time_intervals_on_side_of_contractor,
                                   priority=ticket_priority, importance_level=ticket_importance_level,
                                   full_completion_time=ticket_full_completion_time, exceeds_maximum_time=ticket_exceeds_time)
        return ticket
    
    def format_ticket_priority(self, ticket_priority):
        return str(ticket_priority[-1])
    
    @abstractmethod
    def extract_ticket_id(self, ticket_data):
        pass

    @abstractmethod
    def extract_ticket_creation_date_time(self, ticket_data):
        pass
    
    @abstractmethod
    def extract_ticket_closure_date_time(self, ticket_data):
       pass
   
    @abstractmethod
    def extract_ticket_full_completion_time(self, ticket_data):
        pass

    @abstractmethod
    def extract_ticket_priority(self, ticket_data):
        pass
    
    @abstractmethod
    def extract_ticket_importance_level(self, ticket_data):
        pass
    
    @abstractmethod
    def extract_time_intervals_on_side_of_contractor(self, ticket_data, creation_date_time, ticket_closure_date):
        pass
    
    @abstractmethod
    def extract_ticket_exceeds_maximum_time(self, ticket_data):
        pass
    
    def extract_ticket_url(self, ticket_data):
        url_for_single_ticket = self.get_single_ticket_endpoint()
        ticket_id = self.extract_ticket_id(ticket_data)
        url_for_this_specific_ticket = str(url_for_single_ticket) + str(ticket_id)
        return url_for_this_specific_ticket
    
    def get_single_ticket_endpoint(self):
        return self.project_configuration['api']['endpoints']['single_issue']