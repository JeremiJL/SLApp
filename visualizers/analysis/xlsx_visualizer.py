from .analysis_visualizer import AnalysisVisualizer
from domain.piuw.piuw_ticket import PiuwTicket

import xlsxwriter
import math

class XlsxVisualizer(AnalysisVisualizer):
    
    def __init__(self, project_configuration, computed_schedule, contractor_schedule):
        super().__init__(project_configuration=project_configuration, computed_schedule=computed_schedule, contractor_schedule=contractor_schedule)
        
        self.cell_formats_dictionary = {}
        self.workbook = self.create_excel_workbook()
        self.worksheet = self.create_worksheet_in_given_workbook(self.workbook)
        
    def get_output_file_name(self):
        output_file_name = super().get_output_file_name()
        output_file_name_with_extension = output_file_name + ".xlsx"
        return output_file_name_with_extension
    def visualize(self):
        
        self.cell_formats_dictionary = self.set_cell_formats_dictionary_for_workbook()
        self.write_summary()
        self.write_table_headers()
        self.write_table_content()
        self.format_collumns_width_so_that_text_fits_them()
        
        self.save_workbook_file()
        
    def format_collumns_width_so_that_text_fits_them(self):
        self.worksheet.autofit()
        
    def create_excel_workbook(self):
        workbook_path = self.get_output_file_path()
        workbook = xlsxwriter.Workbook(workbook_path, options={'remove_timezone': True})   
        return workbook
        
    def create_worksheet_in_given_workbook(self, workbook):
        worksheet = workbook.add_worksheet('Analiza')
        return worksheet
    
    def save_workbook_file(self):
        self.workbook.close()
        
    def set_cell_formats_dictionary_for_workbook(self):
        computed_data_format = self.workbook.add_format()
        computed_data_format.set_bg_color('#A5CBDC')
        computed_data_format.set_align('center')
        computed_data_format.set_align('vcenter')
        computed_data_format.set_border(1)
        
        raport_data_format = self.workbook.add_format()
        raport_data_format.set_bg_color('#F28E89')
        raport_data_format.set_align('center')
        raport_data_format.set_align('vcenter')
        raport_data_format.set_border(1)
        
        alarming_format = self.workbook.add_format()
        alarming_format.set_bg_color('#DBCD86')
        alarming_format.set_align('center')
        alarming_format.set_align('vcenter')
        alarming_format.set_border(1)
        
        danger_format = self.workbook.add_format()
        danger_format.set_bg_color('#D9879B')
        danger_format.set_align('center')
        danger_format.set_align('vcenter')
        danger_format.set_border(1)
        
        positive_format = self.workbook.add_format()
        positive_format.set_bg_color('#86DB90')
        positive_format.set_align('center')
        positive_format.set_align('vcenter')
        positive_format.set_border(1)
        
        neutral_format = self.workbook.add_format()
        neutral_format.set_bg_color('#D4D4D4')
        neutral_format.set_align('center')
        neutral_format.set_align('vcenter')
        neutral_format.set_border(1)
        
        formats_dictionary = {"computed_data" : computed_data_format, "raport_data" : raport_data_format, 'alarming' : alarming_format, 'danger' : danger_format, 'positive' : positive_format, 'neutral': neutral_format}
        return formats_dictionary
           
    def write_summary(self):
        year  = self.computed_schedule.year
        month = self.computed_schedule.month
        project_name = self.computed_schedule.project_name
        number_of_closed_tickets = len(self.computed_schedule.tickets)
        number_of_tickets_in_raport = len(self.contractor_schedule.tickets)
        number_of_missing_tickets = self.calculate_number_of_missing_tickets()
        
        neutral_cell_format = self.cell_formats_dictionary['neutral']
        computed_cell_format = self.cell_formats_dictionary['computed_data']
        raport_cell_format = self.cell_formats_dictionary['raport_data']
        
        self.worksheet.write(0,0,'Projekt')
        self.worksheet.write(1,0,project_name, neutral_cell_format)
        
        self.worksheet.write(0,1,'Rok')
        self.worksheet.write(1,1,year, neutral_cell_format)
        
        self.worksheet.write(0,2,'Miesiąc')
        self.worksheet.write(1,2,month, neutral_cell_format)
        
        self.worksheet.write(0,4,'Liczba zamkniętych zgłoszeń')
        self.worksheet.write(1,4,number_of_closed_tickets, computed_cell_format)
        
        self.worksheet.write(0,5,'Liczba zgłoszeń w raporcie')
        self.worksheet.write(1,5,number_of_tickets_in_raport, raport_cell_format)
        
        self.worksheet.write(0,6,'Liczba brakujących zgłoszeń w raporcie')
        self.worksheet.write(1,6,number_of_missing_tickets, neutral_cell_format)
        
    def get_table_headers_ordered_list(self):
        headers = ["Strona", "ID zgłoszenia", "Priorytet zgłoszenia", "Data utworzenia", "Data zamknięcia", "Czas rozwiązania zgłoszenia", "Wykroczenie czasowe", "Różnica", "Komentarz", "Link"]
        return headers
            
    def write_table_headers(self):
        collumn_index = 0
        row_destined_for_headers = 4
        
        headers = self.get_table_headers_ordered_list()
        
        for header, collumn_index in zip(headers, range(collumn_index, collumn_index +  len(headers))):
            self.worksheet.write(row_destined_for_headers, collumn_index, header)
        
    def write_table_content(self):
        tickets_from_computed_schedule = self.get_sorted_tickets_by_ticket_id(self.computed_schedule.tickets)
        tickets_from_contractor_schedule = self.get_sorted_tickets_by_ticket_id(self.contractor_schedule.tickets)
        
        id_maps_computed_ticket = self.generate_a_map_from_ticket_id(tickets_from_computed_schedule)
        id_maps_contractor_ticket = self.generate_a_map_from_ticket_id(tickets_from_contractor_schedule)

        collumn_index = 0
        row_index = 5
        rows_used_to_display_data_in_one_iteration = 2
        space_between_every_iteration = 1
        
        for ticket_id in id_maps_computed_ticket.keys():
            
            self.write_row_headers(row_index, collumn_index)
            
            if ticket_id in id_maps_contractor_ticket.keys():
                computed_ticket = id_maps_computed_ticket[ticket_id]
                contractor_ticket = id_maps_contractor_ticket[ticket_id]

            else:
                computed_ticket = id_maps_computed_ticket[ticket_id]
                contractor_ticket = self.create_null_ticket()
                
            self.write_comparison_between_two_tickets(computed_ticket, contractor_ticket, row_index, collumn_index)
                
            row_index += rows_used_to_display_data_in_one_iteration + space_between_every_iteration
    
    def write_comparison_between_two_tickets(self, computed_ticket, contractor_ticket, row_index, collumn_index):
        self.write_comparison_between_ticket_id(computed_ticket, contractor_ticket, row_index, collumn_index + 1)
        self.write_comparison_between_ticket_priority(computed_ticket, contractor_ticket, row_index, collumn_index + 2)
        self.write_comparison_between_ticket_creation_date(computed_ticket, contractor_ticket, row_index, collumn_index + 3)
        self.write_comparison_between_ticket_closure_date(computed_ticket, contractor_ticket, row_index, collumn_index + 4)
        self.write_comparison_between_ticket_completion_time(computed_ticket, contractor_ticket, row_index, collumn_index + 5)
        self.write_comparison_between_ticket_exceeds_max_time(computed_ticket, contractor_ticket, row_index, collumn_index + 6)
        
        self.write_ticket_differences(computed_ticket, contractor_ticket, row_index, collumn_index + 7)
        self.write_ticket_comment(computed_ticket, contractor_ticket, row_index, collumn_index + 8)
        self.write_ticket_api_end_point_url(computed_ticket, row_index, collumn_index + 9)
               
    def calculate_number_of_missing_tickets(self):
        computed_ticket_id_map = self.generate_a_map_from_ticket_id(self.computed_schedule.tickets)
        contractor_ticket_id_map = self.generate_a_map_from_ticket_id(self.contractor_schedule.tickets)
        
        number_of_missing_tickets = 0
        for ticket_id in computed_ticket_id_map:
            if ticket_id not in contractor_ticket_id_map:
                number_of_missing_tickets += 1
                
        return number_of_missing_tickets
    
    def create_null_ticket(self):
        ticket = PiuwTicket(None, None, None, None, None, None, None, None)
        return ticket
        
    def write_row_of_data(self, row, collumn, computed_data, contractor_data):
        self.write_computed_data(row, collumn, computed_data)
        self.write_raport_data(row + 1, collumn, contractor_data)
    
    def write_computed_data(self, row, collumn, data):
        cell_format = self.cell_formats_dictionary['computed_data']
        self.worksheet.write(row, collumn, data, cell_format)
        
    def write_raport_data(self, row, collumn, data):
        
        if data != None:
            cell_format = self.cell_formats_dictionary['raport_data']
            self.worksheet.write(row, collumn, data, cell_format)
        else:
            cell_format = self.cell_formats_dictionary['neutral']
            self.worksheet.write(row, collumn, "Brak danych", cell_format)
                       
    def write_row_headers(self, row, collumn):
        self.write_row_of_data(row, collumn, "SLApp", "Raport")
    
    def write_comparison_between_ticket_id(self, computed_ticket, contractor_ticket, row, collumn):
        self.write_row_of_data(row, collumn, computed_ticket.ticket_id, contractor_ticket.ticket_id)
            
    def write_comparison_between_ticket_priority(self, computed_ticket, contractor_ticket, row, collumn):
        self.write_row_of_data(row, collumn, computed_ticket.priority, contractor_ticket.priority)
    
    def write_comparison_between_ticket_creation_date(self, computed_ticket, contractor_ticket, row, collumn):
        computed_date_time_formatted = self.format_date_time_for_visualization(computed_ticket.creation_date_time)
        raport_date_time_formatted = self.format_date_time_for_visualization(contractor_ticket.creation_date_time)
        self.write_row_of_data(row, collumn, computed_date_time_formatted, raport_date_time_formatted)
    
    def write_comparison_between_ticket_closure_date(self, computed_ticket, contractor_ticket, row, collumn):
        computed_date_time_formatted = self.format_date_time_for_visualization(computed_ticket.closure_date_time)
        raport_date_time_formatted = self.format_date_time_for_visualization(contractor_ticket.closure_date_time)
        self.write_row_of_data(row, collumn, computed_date_time_formatted, raport_date_time_formatted)
    
    def write_comparison_between_ticket_completion_time(self, computed_ticket, contractor_ticket, row, collumn):
        computed_completion_time_formatted = self.format_completion_time_for_visualization(computed_ticket.full_completion_time)
        raport_completion_time_formatted = self.format_completion_time_for_visualization(contractor_ticket.full_completion_time)
        self.write_row_of_data(row, collumn, computed_completion_time_formatted, raport_completion_time_formatted)  
    
    def write_comparison_between_ticket_exceeds_max_time(self, computed_ticket, contractor_ticket, row, collumn):
        computed_ticket_exceeds_time_as_string = computed_ticket.exceeds_maximum_time
        contractor_ticket_exceeds_time_as_string = contractor_ticket.exceeds_maximum_time
        self.write_row_of_data(row, collumn, computed_ticket_exceeds_time_as_string, contractor_ticket_exceeds_time_as_string)    
         
    def write_ticket_differences(self, computed_ticket, contractor_ticket, row, collumn):
        
        try:
            difference_value = self.compute_difference_value(computed_ticket, contractor_ticket)
            
            if (difference_value > self.get_significant_threshold_value_of_differences_between_computed_and_raported_time()):
                cell_format = self.cell_formats_dictionary['alarming']
            else:
                cell_format = self.cell_formats_dictionary['positive']
                
            text = "Różnica w obliczeniach wynosi " + str(difference_value) + " minut"
        except:
            cell_format = self.cell_formats_dictionary['danger']
            text = "Nie można obliczyć różnicy."
             
        self.worksheet.merge_range(row, collumn, row + 1, collumn, text, cell_format)
    
    def write_ticket_comment(self, computed_ticket, contractor_ticket, row, collumn):
        
        if contractor_ticket.ticket_id != None:
            difference_value = self.compute_difference_value(computed_ticket, contractor_ticket)
            
            if (difference_value > self.get_significant_threshold_value_of_differences_between_computed_and_raported_time()):
                cell_format = self.cell_formats_dictionary['alarming']
                comment_content = "Różnica jest istotna - sprawdź zgłoszenie manualnie!"
            else:
                cell_format = self.cell_formats_dictionary['positive']
                comment_content = "Wyliczenia zgadzają się z raportem."
        else:
            cell_format = self.cell_formats_dictionary['danger']
            comment_content = "Zgłoszenie jest nieobecne w raporcie wykonawcy."
            
        self.worksheet.merge_range(row, collumn, row + 1, collumn, comment_content, cell_format)
    
    def write_ticket_api_end_point_url(self, computed_ticket, row, collumn):
        computed_ticket_url = str(computed_ticket.url)
        cell_format = self.cell_formats_dictionary['neutral']
        self.worksheet.merge_range(row, collumn, row + 1, collumn, computed_ticket_url, cell_format)
                
    def format_completion_time_for_visualization(self, completion_time):
        if completion_time != None:
            completion_time_rounded = round(completion_time, 0)
            return completion_time_rounded
        else:
            return completion_time
        
    def format_date_time_for_visualization(self, date_time):
        if date_time != None:
            format = '%d-%m-%y %H:%M'
            formatted_date = date_time.strftime(format)
            return formatted_date
        else:
            return None
        