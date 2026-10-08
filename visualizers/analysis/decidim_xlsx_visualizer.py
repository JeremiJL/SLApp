from visualizers.analysis.xlsx_visualizer import XlsxVisualizer
from domain.decidim.decidim_ticket import DecidimTicket

class DecidimXlslxVisualizer(XlsxVisualizer):
    
    def __init__(self, project_configuration, computed_schedule, contractor_schedule):
        super().__init__(project_configuration, computed_schedule, contractor_schedule)
        
    def get_table_headers_ordered_list(self):
        headers = ["Strona", "ID zgłoszenia", "Priorytet zgłoszenia", "Poziom istotości", "Data utworzenia", "Data zamknięcia", "Czas rozwiązania zgłoszenia", "Wykroczenie czasowe", "Różnica", "Komentarz", "Link"]
        return headers
    
    def create_null_ticket(self):
        ticket = DecidimTicket(None, None, None, None, None, None, None, None, None)
        return ticket
    
    def write_comparison_between_two_tickets(self, computed_ticket, contractor_ticket, row_index, collumn_index):
        self.write_comparison_between_ticket_id(computed_ticket, contractor_ticket, row_index, collumn_index + 1)
        self.write_comparison_between_ticket_priority(computed_ticket, contractor_ticket, row_index, collumn_index + 2)
        self.write_comparison_between_ticket_importance_level(computed_ticket, contractor_ticket, row_index, collumn_index + 3)
        self.write_comparison_between_ticket_creation_date(computed_ticket, contractor_ticket, row_index, collumn_index + 4)
        self.write_comparison_between_ticket_closure_date(computed_ticket, contractor_ticket, row_index, collumn_index + 5)
        self.write_comparison_between_ticket_completion_time(computed_ticket, contractor_ticket, row_index, collumn_index + 6)
        self.write_comparison_between_ticket_exceeds_max_time(computed_ticket, contractor_ticket, row_index, collumn_index + 7)
        
        self.write_ticket_differences(computed_ticket, contractor_ticket, row_index, collumn_index + 8)
        self.write_ticket_comment(computed_ticket, contractor_ticket, row_index, collumn_index + 9)
        self.write_ticket_api_end_point_url(computed_ticket, row_index, collumn_index + 10)
        
    def write_comparison_between_ticket_importance_level(self, computed_ticket, contractor_ticket, row, collumn):
        self.write_row_of_data(row, collumn, computed_ticket.importance_level, contractor_ticket.importance_level)