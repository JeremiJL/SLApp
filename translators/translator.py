from domain.schedule import Schedule
from domain.ticket import Ticket

from abc import ABC, abstractmethod


class Translator(ABC):
    
    def __init__(self, project_configuration, data_collector):
        self.project_configuration = project_configuration
        self.data_collector = data_collector
        
    def get_schedule(self):
        year = self.data_collector.get_year()
        month = self.data_collector.get_month()
        project_name = self.data_collector.get_project_name()
        tickets = self.get_tickets()
        
        schedule = Schedule(month=month, year=year, tickets=tickets, project_name=project_name)
        return schedule
    
    def create_ticket_representation(self, ticket_data):
        ticket_id = self.extract_ticket_id(ticket_data)
        ticket_creation_date = self.extract_ticket_creation_date_time(ticket_data)
        ticket_closure_date = self.extract_ticket_closure_date_time(ticket_data)
        ticket_time_intervals_on_side_of_contractor = self.extract_time_intervals_on_side_of_contractor(ticket_data, ticket_creation_date, ticket_closure_date)
        ticket_full_completion_time = self.extract_ticket_full_completion_time(ticket_data)
        ticket_exceeds_time = self.extract_ticket_exceeds_maximum_time(ticket_data)
 
        ticket = Ticket(ticket_id=ticket_id, creation_date_time=ticket_creation_date, 
                                   closure_date_time=ticket_closure_date, time_intervals=ticket_time_intervals_on_side_of_contractor,
                                   full_completion_time=ticket_full_completion_time, exceeds_maximum_time=ticket_exceeds_time)
        return ticket
    
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
    def extract_time_intervals_on_side_of_contractor(self, ticket_data, creation_date_time, ticket_closure_date):
        pass
    
    @abstractmethod
    def extract_ticket_exceeds_maximum_time(self, ticket_data):
        pass
    
    