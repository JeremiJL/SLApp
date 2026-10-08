from domain.interval import Interval
from ...date_formatter import format_date_as_string_to_date_object_with_present_time_zone

from datetime import datetime
from dateutil import tz as time_zone_calculator

class IntervalsExtractor():
      
    def __init__(self, project_configuration, data_collector):
        
        self.project_configuration = project_configuration
        self.data_collector = data_collector
        
        self.our_team_employees = []
        self.contractor_team_employees = []
        
        self.assign_employess_to_teams()
        
        self.test()
                
    def extract_time_intervals_on_side_of_contractor(self, ticket_as_dictionary, creation_date_time, ticket_closure_date):
        
        assignement_and_status_list = self.get_journals_assignement_and_status_info(ticket_as_dictionary)
        
        intervals_list = []
        first_interval = Interval()
        first_interval.set_start_date_time(creation_date_time)
        intervals_list.append(first_interval)
        
        for assignement in assignement_and_status_list:
            latest_interval = intervals_list[-1]
            
            if self.is_responsibility_passed_back_to_us(assignement, latest_interval):
                end_date_time = self.fetch_date_time_from_assignement(assignement)
                latest_interval.set_end_date_time(end_date_time)
            
            if self.is_responsibility_passed_to_contractor(assignement, latest_interval):
                start_date_time = self.fetch_date_time_from_assignement(assignement)
                new_interval = Interval()
                new_interval.set_start_date_time(start_date_time)
                intervals_list.append(new_interval)
        
        last_interval = intervals_list[-1]
        last_interval = self.set_last_issue_end_time_if_it_does_not_have_any(last_interval, ticket_closure_date)
        
        return intervals_list
    
    def set_last_issue_end_time_if_it_does_not_have_any(self, last_interval, ticket_closure_date):
        interval = last_interval
        if interval.end == None:
            interval.set_end_date_time(ticket_closure_date)
        return interval
    
    def fetch_date_time_from_assignement(self, assignement):
        date_as_string = str(assignement['time_of_creation'])
        date_time_with_present_time_zone = format_date_as_string_to_date_object_with_present_time_zone(date_as_string)
        return date_time_with_present_time_zone

    def is_responsibility_passed_to_contractor(self, assignement, latest_interval):
        old_assignee = assignement['old_assignee']
        new_assignee = assignement['new_assignee']
        new_status = assignement['new_status']
        is_previous_interval_closed = (latest_interval.end != None)
        statuses_representing_interval_halt = self.fetch_statuses_representing_interval_halt()
        
        if is_previous_interval_closed == False:
            return False
        
        if new_status != None and int(new_status) in statuses_representing_interval_halt:
            return False
    
        if old_assignee in self.our_team_employees and new_assignee in self.contractor_team_employees:
            return True
        else:
            return False
    
    def is_responsibility_passed_back_to_us(self, assignement, latest_interval):
        old_assignee = assignement['old_assignee']
        new_assignee = assignement['new_assignee']
        new_status = assignement['new_status']
        is_previous_interval_closed = (latest_interval.end != None)
        statuses_representing_interval_halt = self.fetch_statuses_representing_interval_halt()
        
        if is_previous_interval_closed == True:
            return False
        
        if new_status != None and int(new_status) in statuses_representing_interval_halt:
            return True
                
        if old_assignee in self.contractor_team_employees and new_assignee in self.our_team_employees:
            return True
        else:
            return False
    
    def get_journals_assignement_and_status_info(self, ticket_as_dictionary):
        
        journals_list = ticket_as_dictionary['journals']['journal']
        journals_list = self.convert_sigle_record_as_dictionary_into_list(journals_list)
        formatted_assignement_info_list = []
        
        for journal in journals_list:
            self.fetch_information_about_assignement_and_status(journal, formatted_assignement_info_list)
            
        assignement_info_list_sorted_by_date = sorted(formatted_assignement_info_list, key=lambda dictionary: dictionary['time_of_creation'])
        return assignement_info_list_sorted_by_date
         
    def fetch_information_about_assignement_and_status(self, journal, formatted_assignement_info_list):
        
        if self.is_journal_a_standalone_massage(journal):
        
            details = journal['details']['detail']
            details = self.convert_sigle_record_as_dictionary_into_list(details)
            
            time_of_creation = datetime.fromisoformat(journal['created_on'])
            new_assignee = self.fetch_new_assignee_id(details)
            old_assignee = self.fetch_old_assignee_id(details)
            new_status = self.fetch_new_status_id(details)

            formatted_info = {'time_of_creation' : time_of_creation, 'new_assignee' : new_assignee, 'old_assignee' : old_assignee, 'new_status' : new_status}                    
            formatted_assignement_info_list.append(formatted_info)
                
    def is_journal_a_standalone_massage(self, journal):
        
        if 'detail' in journal['details'].keys():
            return True
        else:
            return False
    
    def fetch_new_assignee_id(self, details):
        for detail in details:
            if self.is_detail_representing_assignement_data(detail):
                return detail['new_value']
        return None
    
    def fetch_old_assignee_id(self, details):
        for detail in details:
            if self.is_detail_representing_assignement_data(detail):
                    return detail['old_value']
                
        return None
    
    def fetch_new_status_id(self, details):
        for detail in details:
            if self.is_detail_representing_status_data(detail):
                return detail['new_value']
        return None
    
    def is_detail_representing_assignement_data(self, detail):
        if detail['@name'] == 'assigned_to_id':
            return True
        else:
            return False
        
    def is_detail_representing_status_data(self, detail):
        if detail['@name'] == 'status_id':
            return True
        else:
            return False
        
    def convert_sigle_record_as_dictionary_into_list(self, records):
        if type(records) == type(dict()):
                single_record = records
                records = []
                records.append(single_record)  
                            
        return records
    
    def assign_employess_to_teams(self):
        try:
            self.assign_employees_to_teams_via_list_from_configuration_file()
        except:
            self.assign_employees_to_teams_via_members_roles()
        finally:
            if len(self.our_team_employees) == 0 or len(self.contractor_team_employees) == 0:
                 self.assign_employees_to_teams_via_members_roles()
    
    def assign_employees_to_teams_via_list_from_configuration_file(self):
        self.our_team_employees = self.project_configuration['api']['team_members']['our_team']
        self.contractor_team_employees = self.project_configuration['api']['team_members']['contractor_team']
        
    def assign_employees_to_teams_via_members_roles(self):
        
        employees_list = self.data_collector.collect_list_of_all_members_involved_in_project()
            
        role_id_of_our_team = self.get_role_id_of_our_team()
        role_id_of_contractor_team = self.get_role_id_of_cotractor_team()
    
        for employee in employees_list:
            
            if self.is_employee_a_real_record(employee):
                
                employee_roles_list = self.get_employee_roles_as_list(employee)
                employee_id = self.get_employee_id(employee)
                
                if role_id_of_contractor_team in employee_roles_list:
                    self.contractor_team_employees.append(employee_id)

                elif role_id_of_our_team in employee_roles_list:
                    self.our_team_employees.append(employee_id)
                
    def is_employee_a_real_record(self, employee):
        if 'user' in employee.keys():
            return True
        else:
            return False
                
    def get_role_id_of_a_team(self, team_identifier):
        role_id = self.project_configuration['api']['role_id_of_teams'][team_identifier]
        role_id_as_integer = int(role_id)
        return role_id_as_integer
        
    def get_role_id_of_our_team(self):
        return self.get_role_id_of_a_team('our_team')
    
    def get_role_id_of_cotractor_team(self):
        return self.get_role_id_of_a_team('contractor_team')
    
    def get_employee_roles_as_list(self, employee):
        
        collection_of_roles = employee['roles']['role']
        
        if type(collection_of_roles) == type(list()):
            return self.get_multiple_roles_of_employee(collection_of_roles)
        
        elif type(collection_of_roles) == type(dict()):
            return self.get_single_role_of_employee(collection_of_roles)
    
    def get_multiple_roles_of_employee(self, list_of_roles_as_dictionaries):
        roles_list = []
        for role in list_of_roles_as_dictionaries:
            roles_list.append(self.extract_role_id(role))
            
        return roles_list
    
    def extract_role_id(self, role):
        return int(role['@id'])
    
    def get_single_role_of_employee(self, role_as_dictionary):
        roles_list = []
        role = self.extract_role_id(role_as_dictionary)
        roles_list.append(role)
        return roles_list
                
    def get_employee_id(self, employee):
        return employee['user']['@id']
    
    def fetch_statuses_representing_interval_halt(self):
       return (self.project_configuration['api']['status_id']['halt'])
    
    def test(self):
        print(self.contractor_team_employees)
        print(self.our_team_employees)