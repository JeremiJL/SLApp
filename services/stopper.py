from datetime import datetime

start = None

def start_stopper():
    global start
    start = datetime.now()
    
def end_stopper():
    end = datetime.now()
    delta = end - start
    delta_in_seconds = delta.seconds
    return str(Time(delta_in_seconds))

class Time:
    def __init__(self, seconds):
        self.seconds = seconds
        
    def __str__(self) -> str:
        minutes = self.get_minutes()
        seconds = self.get_seconds_modulo()
        if minutes > 0:
            return str(minutes) + " minut i " + str(seconds) + " sekund"
        else:
            return str(seconds) + " sekund"
        
    def get_minutes(self):
        return int(self.seconds / 60)
        
    def get_seconds_modulo(self):
        return self.seconds % 60