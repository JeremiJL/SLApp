from ..schedule import Schedule

class DecidimSchedule(Schedule):
    
    def __init__(self, month, year, tickets, project_name):
        super().__init__(month, year, tickets, project_name)

        # skumulowany czas niedostępności usługi - according to contract's nomenclature
        self.total_time_of_completion_in_month_per_priority = dict()