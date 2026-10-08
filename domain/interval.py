class Interval:

    def __init__(self):
        self.start = None
        self.end = None
        
    def set_start_date_time(self, start_date_time):
        self.start = start_date_time
        
    def set_end_date_time(self, end_date_time):
        self.end = end_date_time
    
    def get_difference_between_start_end_in_minutes(self):
        
        if (self.end is not None and self.start is not None):
            difference = self.end - self.start
            return int(difference.seconds / 60)
        
        else:
            raise Exception('Interval object not complete yet!')
