from .redmine_collector import RedmineCollector
from services.date_service import get_number_of_days_in_a_month

from datetime import date

class PiuwCollector(RedmineCollector):
    
    def __init__(self, project_configuration, api_key, month, year, data_format):
        super().__init__(project_configuration, api_key, month, year, data_format)
        
    def get_request_parameters_for_all_issues_in_whole_month(self, offset = 0):
        first_day_of_month_date = date(self.year, self.month, 1)
        last_day_of_month_date = date(self.year, self.month, get_number_of_days_in_a_month(self.month, self.year))
        month_interval_parameter = '><' + str(first_day_of_month_date) + "|" + str(last_day_of_month_date)
        
        return {"key" : self.api_key, "status_id" : "3,5", "updated_on" : month_interval_parameter, "limit" : self.portion_of_data_records_collected_in_one_request, 'offset' : offset}