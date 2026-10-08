from .. import ticket

class DecidimTicket(ticket.Ticket):

    def __init__(self, ticket_id, creation_date_time, closure_date_time, time_intervals, priority, importance_level, url, full_completion_time = None, exceeds_maximum_time = None):
        super().__init__(ticket_id=ticket_id, creation_date_time=creation_date_time, time_intervals=time_intervals, priority=priority,
                         closure_date_time=closure_date_time, full_completion_time=full_completion_time, url=url)
        
        # poziom istotności - according to contract's nomenclature
        self.importance_level = importance_level
        # wykroczenie poza maksymalny czas naprawy - according to contract's nomenclature
        self.exceeds_maximum_time = exceeds_maximum_time
        
        
        