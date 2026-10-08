from .txt_visualizer import TxtVisualizer
from domain.decidim.decidim_ticket import DecidimTicket

class DecidimTxtVisualizer(TxtVisualizer):
    
    def __init__(self, project_configuration, computed_schedule, contractor_schedule):
        super().__init__(project_configuration=project_configuration, computed_schedule=computed_schedule, contractor_schedule=contractor_schedule)
    
    
    def add_comparison_between_two_tickets(self, info_as_string, computed_ticket, contractor_ticket):
        
        intervals_list_from_computed_schedule = computed_ticket.time_intervals_on_side_of_contractor
        
        info_as_string += self.build_new_line_of_info("ID Zgłoszenia", computed_ticket.ticket_id, contractor_ticket.ticket_id)
        
        info_as_string += self.build_new_line_of_info("Priorytet", computed_ticket.priority, contractor_ticket.priority)
        
        info_as_string += self.build_new_line_of_info("Poziom istotności", computed_ticket.importance_level, contractor_ticket.importance_level)
        
        info_as_string += self.build_new_line_of_info("Data utworzenia", computed_ticket.creation_date_time, contractor_ticket.creation_date_time)
        
        info_as_string += self.build_new_line_of_info("Data zamknięcia", computed_ticket.closure_date_time, contractor_ticket.closure_date_time)
        
        info_as_string += self.build_new_line_of_info("Czas rozwiązania", computed_ticket.full_completion_time, contractor_ticket.full_completion_time)
        
        info_as_string += self.build_new_line_of_info("Wykroczenie czasowe", computed_ticket.exceeds_maximum_time, contractor_ticket.exceeds_maximum_time)
        
        info_as_string += self.build_new_line_of_info("Link do zgłoszenia", computed_ticket.url, contractor_ticket.url)
        
        info_as_string += "\n\nInterwały czasowe zgłoszenia:\n"
        
        for interval in intervals_list_from_computed_schedule:
            info_as_string += str("\n> Start : " + str(interval.start)).ljust(60)
            info_as_string += "> Koniec : " + str(interval.end)
        
        return info_as_string