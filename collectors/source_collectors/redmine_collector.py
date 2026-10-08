from ..collector import Collector
from services.date_service import get_number_of_days_in_a_month

from datetime import date
import requests
import xmltodict
from math import ceil

class RedmineCollector(Collector):
    
    def __init__(self, project_configuration, api_key, month, year, data_format):
        super().__init__(project_configuration)
        self.api_key = api_key
        self.month = month
        self.year = year
        self.fetched_data_format = data_format
        
        # redmine does not accept value greater than 100
        self.portion_of_data_records_collected_in_one_request = 100
        
    def get_month(self):
        return self.month
    
    def get_year(self):
        return self.year
    
    def get_project_name(self):
        project_name = self.project_configuration['project_name']
        return project_name
      
    def collect_tickets_data(self):
        tickets_id_list = self.collect_id_of_all_tickets_within_month()
        tickets_as_dictionaries = []
        
        for ticket_id in tickets_id_list:
            ticket_xml_content_with_journal = self.collect_specific_ticket_with_journal(ticket_id)
            ticket_as_dictionary = self.convert_single_xml_ticket_into_dictionary(ticket_xml_content_with_journal)
            
            tickets_as_dictionaries.append(ticket_as_dictionary)
        
        return tickets_as_dictionaries
        
    def collect_list_of_all_members_involved_in_project(self):
        list_of_all_members = self.collect_multiple_records_from_redmine(request_data_function=self.make_request_for_members_involved_in_project)        
        return list_of_all_members
    
    def collect_all_closed_tickets_from_whole_month_without_journals(self):
        tickets_list = self.collect_multiple_records_from_redmine(request_data_function=self.make_request_for_all_closed_tickets_in_whole_month)
        # if type(tickets_list) != list():
        #     single_element = tickets_list
        #     tickets_list = []
        #     tickets_list.append(single_element)
        return tickets_list
    
    def collect_id_of_all_tickets_within_month(self):
        tickets_list = self.collect_all_closed_tickets_from_whole_month_without_journals()
        
        tickets_id_list = []
        for ticket in tickets_list:
            print(ticket)
            tickets_id_list.append(ticket['id'])
            
        return tickets_id_list
    
    def collect_specific_ticket_with_journal(self, ticket_identifier):
        endpoint = self.get_endpoint_for_specific_issue(ticket_identifier)
        parameters = self.get_request_parameters_for_single_issue()
        
        response = requests.get(endpoint, params=parameters, verify=False)
        response_content = self.get_response_textual_content_as_string(response)
        return response_content
    
    def collect_multiple_records_from_redmine(self, request_data_function):
        
        response_xml_content = request_data_function()
        number_of_iterations = self.get_number_of_requests_necessary_to_collect_all_data(response_xml_content)
        
        list_of_all_records = []
        offset = 0
        
        for _ in range(0, number_of_iterations):
            
            records_xml_content = request_data_function(offset=offset)
            records_as_dictionary = xmltodict.parse(records_xml_content)
            records_as_list_from_single_request = self.unwrap_response_into_list(records_as_dictionary)
            
            list_of_all_records += records_as_list_from_single_request 
            
            offset += self.portion_of_data_records_collected_in_one_request
        
        return list_of_all_records
      
    def make_request_for_members_involved_in_project(self, offset=0):
        endpoint = self.get_endpoint_for_list_of_memebers_involved_in_project()
        parameters = self.get_request_parameters_for_members_involved_in_project(offset=offset)
        
        response = requests.get(endpoint, params=parameters, verify=False)
        response_content = self.get_response_textual_content_as_string(response)
    
        return response_content
    
    def make_request_for_all_closed_tickets_in_whole_month(self, offset=0):
        endpoint = self.get_endpoint_for_all_issues_in_whole_month()
        parameters = self.get_request_parameters_for_all_issues_in_whole_month(offset=offset)
        
        response = requests.get(endpoint, params=parameters, verify=False)
        response_content = self.get_response_textual_content_as_string(response)
        return response_content
    
    def unwrap_response_into_list(self, wrapped_response_as_dict):
        half_way_throught_unwrapped_response = self.unwrap_response_into_dict(wrapped_response_as_dict)
        last_key = [key for key in half_way_throught_unwrapped_response.keys()][-1]
        unwrapped_response_as_list = half_way_throught_unwrapped_response[last_key]
        
        return unwrapped_response_as_list
    
    def unwrap_response_into_dict(self, wrapped_response_as_dict):
        one_and_only_key = [key for key in wrapped_response_as_dict.keys()][0]
        response_as_dict = wrapped_response_as_dict[one_and_only_key]
        
        return response_as_dict
        
    def get_number_of_requests_necessary_to_collect_all_data(self, xml_response_content):
        wrapped_response_as_dict =  xmltodict.parse(xml_response_content)
        response_as_dict = self.unwrap_response_into_dict(wrapped_response_as_dict)
        
        limit_of_data_records_in_single_request = int(response_as_dict['@limit'])
        total_number_of_data_records = int(response_as_dict['@total_count'])
        
        number_of_requests_necessary_to_collect_all_data_records = total_number_of_data_records / limit_of_data_records_in_single_request
        number_of_requests_necessary_to_collect_all_data_records = ceil(number_of_requests_necessary_to_collect_all_data_records)
        
        return number_of_requests_necessary_to_collect_all_data_records
    
    def convert_single_xml_ticket_into_dictionary(self, ticket_xml_content):
        ticket_dictionary = xmltodict.parse(ticket_xml_content)['issue']
        return ticket_dictionary
    
    def get_endpoint_for_specific_issue(self, issue_id):
        issue_endpoint = self.project_configuration['api']['endpoints']['single_issue']
        specific_issue_endpoint = issue_endpoint  + str(issue_id)
        endpoint_url = self.add_data_format_tag_to_url(specific_issue_endpoint)
        return endpoint_url
    
    def get_endpoint_for_list_of_memebers_involved_in_project(self):
        members_list_endpoint = self.project_configuration['api']['endpoints']['members']
        endpoint_url = self.add_data_format_tag_to_url(members_list_endpoint)
        return endpoint_url
    
    def get_endpoint_for_all_issues_in_whole_month(self):
        multiple_issues_endpoint = self.project_configuration['api']['endpoints']['multiple_issues']
        endpoint_url = self.add_data_format_tag_to_url(multiple_issues_endpoint)
        return endpoint_url
    
    def add_data_format_tag_to_url(self, url):
        url_with_data_format_tag = url + "." + self.fetched_data_format
        return url_with_data_format_tag
    
    def get_response_textual_content_as_string(self, response):
        return response.text
    
    def get_request_parameters_for_single_issue(self):
        return {"key" : str(self.api_key), "include" : "journals"}

    def get_request_parameters_for_all_issues_in_whole_month(self, offset = 0):
        first_day_of_month_date = date(self.year, self.month, 1)
        last_day_of_month_date = date(self.year, self.month, get_number_of_days_in_a_month(self.month, self.year))
        month_interval_parameter = '><' + str(first_day_of_month_date) + "|" + str(last_day_of_month_date)
        return {"key" : self.api_key, "status_id" : "closed" , "closed_on" : month_interval_parameter, "limit" : self.portion_of_data_records_collected_in_one_request, 'offset' : offset}
        
    def get_request_parameters_for_members_involved_in_project(self, offset = 0):
        return {"key" : self.api_key, "limit" : self.portion_of_data_records_collected_in_one_request, 'offset' : offset}
   