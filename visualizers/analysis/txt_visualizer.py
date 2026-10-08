from .analysis_visualizer import AnalysisVisualizer
from domain.ticket import Ticket

class TxtVisualizer(AnalysisVisualizer):
    
    def __init__(self, project_configuration, computed_schedule, contractor_schedule):
        super().__init__(project_configuration=project_configuration, computed_schedule=computed_schedule, contractor_schedule=contractor_schedule)
           
    def visualize(self):
        file_path = self.get_output_file_path()
        summarization_content = self.get_summarization_info_as_string()
        
        with open(file=file_path, mode="w") as output:
            output.write(summarization_content)
            
    def get_output_file_name(self):
        output_file_name = super().get_output_file_name()
        output_file_name_with_extension = output_file_name + ".txt"
        return output_file_name_with_extension
    
    def get_summarization_info_as_string(self):
        
        header_info_as_string = self.add_header_info()
        info_about_unavailability_per_priority_as_string = self.add_info_about_unavailability_per_priority()
        comparison_between_raport_data_and_computed_data_as_string = self.add_comparison_between_raport_data_and_computed_data()
        
        final_info_as_string = header_info_as_string + info_about_unavailability_per_priority_as_string + comparison_between_raport_data_and_computed_data_as_string
        
        return final_info_as_string
    
    def add_header_info(self):
        year  = self.computed_schedule.year
        month = self.computed_schedule.month
        project_name = self.computed_schedule.project_name
        
        number_of_tickets_collected = len(self.computed_schedule.tickets)
        number_of_tickets_in_raport = len(self.contractor_schedule.tickets)
        number_of_missing_tickets = self.get_number_of_missing_tickets()
        
        header_info_as_string = "Analiza dla " + project_name + " za " + str(year) + "/" + str(month) + "\n\n" 
        header_info_as_string += "Liczba zgłoszeń pobranych ze źródła : " + str(number_of_tickets_collected) + "\n"
        header_info_as_string += "Liczba zgłoszeń obecnych w raporcie Wykonawcy : " + str(number_of_tickets_in_raport) + "\n"
        header_info_as_string += "Liczba brakujących zgłoszeń w raporcie Wykonawcy : " + str(number_of_missing_tickets) + "\n"
        
        return header_info_as_string
        
    def add_info_about_unavailability_per_priority(self):
        info_about_unavailability_per_priority_as_string = "\nSumaryczna niedostępność per priorytet : "
        
        summed_unavailability_per_project = self.computed_schedule.total_time_of_completion_in_month_per_priority
        
        for priority, summed_time in zip(summed_unavailability_per_project.keys(), summed_unavailability_per_project.values()):
            info_about_unavailability_per_priority_as_string += self.build_new_line_of_info(priority, summed_time, "Brak danych")
            
        return info_about_unavailability_per_priority_as_string
        
    def add_comparison_between_raport_data_and_computed_data(self):
        info_as_string = "\n\Analiza SLApp:".ljust(58) + "Analiza Wykonawcy:\n"
        
        tickets_from_computed_schedule = self.get_sorted_tickets_by_ticket_id(self.computed_schedule.tickets)
        tickets_from_contractor_schedule = self.get_sorted_tickets_by_ticket_id(self.contractor_schedule.tickets)
        
        id_maps_computed_ticket = self.generate_a_map_from_ticket_id(tickets_from_computed_schedule)
        id_maps_contractor_ticket = self.generate_a_map_from_ticket_id(tickets_from_contractor_schedule)
                
        for ticket_id in id_maps_computed_ticket.keys():
            
            if ticket_id in id_maps_contractor_ticket.keys():
                computed_ticket = id_maps_computed_ticket[ticket_id]
                contractor_ticket = id_maps_contractor_ticket[ticket_id]
            else:
                computed_ticket = id_maps_computed_ticket[ticket_id]
                contractor_ticket = self.create_null_ticket()
                
            info_as_string = self.add_comparison_between_two_tickets(info_as_string, computed_ticket, contractor_ticket)
                
            info_as_string += "\n\n"
        
        return info_as_string
            
    def add_comparison_between_two_tickets(self, info_as_string, computed_ticket, contractor_ticket):
        
        intervals_list_from_computed_schedule = computed_ticket.time_intervals_on_side_of_contractor
        
        info_as_string += self.build_new_line_of_info("ID Zgłoszenia", computed_ticket.ticket_id, contractor_ticket.ticket_id)
        
        info_as_string += self.build_new_line_of_info("Priorytet", computed_ticket.priority, contractor_ticket.priority)
        
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
            
    def build_new_line_of_info(self, component_header, computed_schedule_component, contractor_schedule_component):
        info_as_string = str("\n" + component_header + ": ").ljust(30)
        info_as_string += str(computed_schedule_component).ljust(30)
        
        info_as_string += str(component_header + ": ").ljust(30)
        info_as_string += str(contractor_schedule_component)
        
        return info_as_string
          
    def get_number_of_missing_tickets(self):
        computed_ticket_id_map = self.generate_a_map_from_ticket_id(self.computed_schedule.tickets)
        contractor_ticket_id_map = self.generate_a_map_from_ticket_id(self.contractor_schedule.tickets)
        
        number_of_missing_tickets = 0
        for ticket_id in computed_ticket_id_map:
            if ticket_id not in contractor_ticket_id_map:
                number_of_missing_tickets += 1
                
        return number_of_missing_tickets
    
    def create_null_ticket(self):
        ticket = Ticket("Brak danych", "Brak danych", "Brak danych", "Brak danych", "Brak danych", "Brak danych", "Brak danych")
        return ticket
