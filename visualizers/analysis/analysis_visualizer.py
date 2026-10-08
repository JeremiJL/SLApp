from visualizers.visualizer import Visualizer

class AnalysisVisualizer(Visualizer):
    
    def get_output_file_name(self):
        output_file_name = super().get_output_file_name()
        output_file_name += "-analiza"
        return output_file_name
    
    def get_output_file_directory(self):
        output_file_directory = self.project_configuration['path_names']['output']['analysis']
        return output_file_directory
    
    def get_sorted_tickets_by_ticket_id(self, ticket_list):
        return sorted(ticket_list, key=lambda ticket: ticket.ticket_id)
    
       
    def get_number_of_correctly_analysed_tickets(self):
        
        correctly_ananalysed_tickets_count  = 0
        id_maps_computed_ticket = self.generate_a_map_from_ticket_id(self.computed_schedule.tickets)
        id_maps_contractor_ticket = self.generate_a_map_from_ticket_id(self.contractor_schedule.tickets)
        
        for ticket_id in id_maps_computed_ticket.keys():
            if ticket_id in id_maps_contractor_ticket.keys():
                computed_ticket = id_maps_computed_ticket[ticket_id]
                contractor_ticket = id_maps_contractor_ticket[ticket_id]
                difference = self.compute_difference_value(computed_ticket, contractor_ticket)
                treshold = self.get_significant_threshold_value_of_differences_between_computed_and_raported_time()
                if difference < treshold:
                    correctly_ananalysed_tickets_count += 1
                    
        return correctly_ananalysed_tickets_count
                    
    def generate_a_map_from_ticket_id(self, tickets_list):
        id_maps_ticket = dict()
        for ticket in tickets_list:
            id_maps_ticket[ticket.ticket_id] = ticket
        return id_maps_ticket
                         
    def compute_difference_value(self, computed_ticket, contractor_ticket):
            computed_time = computed_ticket.full_completion_time
            raport_time = contractor_ticket.full_completion_time
            
            absolute_difference = abs(computed_time - raport_time)
            rounded_difference = round(absolute_difference,1)
            return rounded_difference
        
    def get_significant_threshold_value_of_differences_between_computed_and_raported_time(self):
        significant_threshold = self.project_configuration['agreement']['significant_threshold']
        return significant_threshold