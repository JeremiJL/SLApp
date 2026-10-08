class Ticket:

    def __init__(self, ticket_id, creation_date_time, closure_date_time, time_intervals, full_completion_time, priority, url):
        self.ticket_id = ticket_id
        self.creation_date_time = creation_date_time
        self.closure_date_time = closure_date_time
        self.time_intervals_on_side_of_contractor = time_intervals
        self.full_completion_time = full_completion_time
        self.priority = priority
        self.url = url