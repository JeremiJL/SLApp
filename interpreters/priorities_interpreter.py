from .interpreter import Interpreter
from .time_of_day import TimeOfDay

import datetime

class PrioritiesInterpreter(Interpreter):
    
    def __init__(self, project_configuration, schedule):
        super().__init__(project_configuration, schedule=schedule)

        self.day = self.create_day_time_of_day_object()
        self.night = self.create_night_time_of_day_object()
        
        self.time_of_day_maps_time_factor = self.fill_time_of_day_maps_time_factor_dictionary()
        self.priority_maps_max_completion_time_per_ticket = self.fill_priority_maps_max_completion_time_per_ticket_dictionary()
        self.priority_maps_max_completion_time_per_month = self.fill_priority_maps_max_completion_time_per_month_dictionary()
        
        
    def interpret_shedule_according_to_contract_rules(self):
        interpreted_shedule = self.schedule_before_interpretation
        
        for ticket in interpreted_shedule.tickets:
            ticket.full_completion_time = self.calculate_ticket_completion_time(ticket)
            ticket.exceeds_maximum_time = self.check_if_ticket_does_exceed_maximum_completion_time(ticket)
        
        interpreted_shedule.total_time_of_completion_in_month_per_priority = self.calculate_total_time_of_completion_in_month_per_priority(interpreted_shedule)    
        
        return interpreted_shedule
    
    def calculate_total_time_of_completion_in_month_per_priority(self, interpreted_schedule):
        priority_maps_total_time_of_completion = self.make_dictionary_mapping_priority_with_total_time_of_completion_in_month()
        
        for ticket in interpreted_schedule.tickets:
            if ticket.priority in priority_maps_total_time_of_completion.keys():
                priority_maps_total_time_of_completion[ticket.priority] += ticket.full_completion_time
        
        return priority_maps_total_time_of_completion
        
    def make_dictionary_mapping_priority_with_total_time_of_completion_in_month(self):
        priority_maps_total_time_of_completion = self.priority_maps_max_completion_time_per_month
        
        for priority in priority_maps_total_time_of_completion.keys():
            priority_maps_total_time_of_completion[priority] = 0
            
        return priority_maps_total_time_of_completion

    def check_if_ticket_does_exceed_maximum_completion_time(self, ticket):
        
        if ticket.priority not in self.priority_maps_max_completion_time_per_ticket:
            return False
        if ticket.full_completion_time > self.priority_maps_max_completion_time_per_ticket[ticket.priority]:
            return True
        else:
            return False
    
    def create_day_time_of_day_object(self):
        start_of_day = self.fetch_time_when_day_starts()
        end_of_day = self.fetch_time_when_day_ends()
        
        day = TimeOfDay(start_of_day, end_of_day)
        return day
    
    def fetch_time_when_day_starts(self):
        hour = int(self.project_configuration['agreement']['day_schedule']['start_of_day']['hour'])
        minutes = int(self.project_configuration['agreement']['day_schedule']['start_of_day']['minutes'])
        
        start_of_day = datetime.time(hour,minutes)
        return start_of_day
    
    def fetch_time_when_day_ends(self):
        hour = int(self.project_configuration['agreement']['day_schedule']['end_of_day']['hour'])
        minutes = int(self.project_configuration['agreement']['day_schedule']['end_of_day']['minutes'])
        
        end_of_day = datetime.time(hour,minutes)
        return end_of_day
    
    def create_night_time_of_day_object(self):
        if (self.day == None):
            self.day = self.create_day_time_of_day_object()
        
        start_of_night = self.day.end
        end_of_night = self.day.start
        
        night = TimeOfDay(start_of_night, end_of_night)
        return night
            
    def fill_time_of_day_maps_time_factor_dictionary(self):        
        time_of_day_maps_time_factor = dict()
        time_of_day_maps_time_factor[self.day] = self.fetch_day_time_factor()
        time_of_day_maps_time_factor[self.night] = self.fetch_night_time_factor()
        
        return time_of_day_maps_time_factor
    
    def fetch_day_time_factor(self):
        factor = self.project_configuration['agreement']['day_time_factor']
        return factor
    
    def fetch_night_time_factor(self):
        factor = self.project_configuration['agreement']['night_time_factor']
        return factor
    
    def fill_priority_maps_max_completion_time_per_ticket_dictionary(self):
        priority_maps_max_time = self.project_configuration['agreement']['priorities_total_time_map_per_ticket']
        return priority_maps_max_time
    
    def fill_priority_maps_max_completion_time_per_month_dictionary(self):
        priority_maps_max_time = self.project_configuration['agreement']['priorities_total_time_map_per_month']
        return priority_maps_max_time
        
    def calculate_ticket_completion_time(self, ticket):
        total_completion_time = 0
        for interval in ticket.time_intervals_on_side_of_contractor:
            total_completion_time += self.calculate_interval_time(interval)
        
        return total_completion_time
    
    def calculate_interval_time(self, interval):
        total_interval_time = self.calculate_night_part_of_interval(interval) + self.calculate_day_part_of_interval(interval)
        return total_interval_time
    
    def calculate_night_part_of_interval(self, interval):
        
        time_zone = interval.start.tzinfo
        year = interval.start.year
        month = interval.start.month
        day = interval.start.day
        hour = self.night.start.hour
        minute = self.night.start.minute
        start_of_night_on_given_day = datetime.datetime(year=year, month=month,day=day, hour=hour, minute=minute,tzinfo=time_zone)
        
        hour = self.night.end.hour
        minute = self.night.end.minute
        end_of_night_on_given_day = datetime.datetime(year=year, month=month,day=day, hour=hour, minute=minute, tzinfo=time_zone)
        end_of_night_on_given_day += datetime.timedelta(days=1)
        
        total_night_part_time = 0
        
        while start_of_night_on_given_day <= interval.end:
            
            if start_of_night_on_given_day <= interval.start <= end_of_night_on_given_day:
                start_of_night_part_of_interval = interval.start
            else:
                start_of_night_part_of_interval = start_of_night_on_given_day
            
            if end_of_night_on_given_day <= interval.end:
                end_of_night_part_interval = end_of_night_on_given_day
            else:
                end_of_night_part_interval = interval.end
                
            total_night_part_time += self.calculate_factored_time_difference_in_minutes(start_of_night_part_of_interval
                            ,end_of_night_part_interval, self.night)
                
            start_of_night_on_given_day += datetime.timedelta(days=1)
            end_of_night_on_given_day += datetime.timedelta(days=1)
    
        return total_night_part_time
    
    def calculate_day_part_of_interval(self, interval):
        
        active_days_of_week = self.fetch_working_days_of_week()
        time_zone = interval.start.tzinfo
        year = interval.start.year
        month = interval.start.month
        day = interval.start.day
        hour = self.day.start.hour
        minute = self.day.start.minute
        start_of_day_on_given_day = datetime.datetime(year=year, month=month,day=day, hour=hour, minute=minute,tzinfo=time_zone)
        
        hour = self.day.end.hour
        minute = self.day.end.minute
        end_of_day_on_given_day = datetime.datetime(year=year, month=month,day=day, hour=hour, minute=minute, tzinfo=time_zone)
        
        total_day_part_time = 0
        
        while start_of_day_on_given_day <= interval.end:
            
            if start_of_day_on_given_day.isoweekday() in active_days_of_week:
                if start_of_day_on_given_day <= interval.start <= end_of_day_on_given_day:
                    start_of_day_part_of_interval = interval.start
                else:
                    start_of_day_part_of_interval = start_of_day_on_given_day
                
                if end_of_day_on_given_day <= interval.end:
                    end_of_day_part_interval = end_of_day_on_given_day
                else:
                    end_of_day_part_interval = interval.end
                
                total_day_part_time += self.calculate_factored_time_difference_in_minutes(start_of_day_part_of_interval
                                ,end_of_day_part_interval, self.day)
            
            start_of_day_on_given_day += datetime.timedelta(days=1)
            end_of_day_on_given_day += datetime.timedelta(days=1)
    
        return total_day_part_time
    
    def fetch_working_days_of_week(self):
        working_days_of_week_list = self.project_configuration['agreement']['working_days_of_week']
        return working_days_of_week_list
    
    def calculate_factored_time_difference_in_minutes(self, start_date_time, end_date_time, time_of_day):
        difference_in_minutes = self.calculate_time_difference_in_minutes(start_date_time, end_date_time)
        difference_factored = difference_in_minutes * self.time_of_day_maps_time_factor[time_of_day]
        
        return difference_factored
    
    def calculate_time_difference_in_minutes(self, start_date_time, end_date_time):
        difference = end_date_time - start_date_time
        difference_in_minutes = difference.seconds / 60
        
        return difference_in_minutes