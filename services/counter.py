from services.configuration_provider import get_project_configuration

from datetime import timedelta

configuration = get_project_configuration('COUNTER')
serialized_records_pathname = configuration['path']['serialized_records_codes']
serialized_count_of_correctly_analysed_tickets_pathname = configuration['path']['serialized_count_of_correctly_analyzed_tickets']

def get_time_saved(number_of_tickets_analyzed):
    number_of_minutes_per_one_ticket = 5
    total_sum_of_minutes_saved = number_of_tickets_analyzed * number_of_minutes_per_one_ticket
    time_saved_representation = str(Time(total_sum_of_minutes_saved))
    return time_saved_representation

def get_total_time_saved():
    number_of_tickets_analyzed = get_count_of_correctly_analysed_tickets()
    return get_time_saved(number_of_tickets_analyzed)
    
def get_generated_analysis_counter_value():
    records = get_records_as_hash_set()
    return len(records)

def get_count_of_correctly_analysed_tickets():
    serialized_count_of_correctly_analysed_tickets_pathname = configuration['path']['serialized_count_of_correctly_analyzed_tickets']
    count_of_correctly_analyzed_tickets = 0
    with open(serialized_count_of_correctly_analysed_tickets_pathname, "r") as counter_file:
        line = counter_file.readline()
        count_of_correctly_analyzed_tickets = int(line.strip())
    return count_of_correctly_analyzed_tickets

def increment_correctly_analysed_tickets_counter(number_of_correctly_analyzed_tickets):
    old_value = get_count_of_correctly_analysed_tickets()
    new_value = old_value + number_of_correctly_analyzed_tickets
    update_count_of_correctly_analysed_tickets(new_value)
    
def update_count_of_correctly_analysed_tickets(new_value):
    with open(serialized_count_of_correctly_analysed_tickets_pathname, "w") as counter_file:
        counter_file.write(str(new_value))

def increment_counters(year, month, project, number_of_correctly_analyzed_tickets):
    encoded_record = encode_record(year, month, project)
    set_of_records = get_records_as_hash_set()
    
    if encoded_record not in set_of_records:
        increment_correctly_analysed_tickets_counter(number_of_correctly_analyzed_tickets)
    
    set_of_records.add(encoded_record)
    write_updated_records(set_of_records)

def get_records_as_hash_set():
    records_as_set = set()
    with open(serialized_records_pathname, "r") as records_as_file:
        for line in records_as_file.readlines():
            record = line.strip()
            records_as_set.add(record)
    return records_as_set

def write_updated_records(set_of_records):
    with open(serialized_records_pathname, "w") as records_as_file:
        for encoded_record in set_of_records:
            records_as_file.write(str(encoded_record) + "\n")

def encode_record(year, month, project):
    encoded_record = str(year) + "-" + str(month) + "-" + str(project)
    return encoded_record

class Time:
    def __init__(self, minutes):
        self.minutes = minutes
        
    def __str__(self) -> str:
        hours = self.get_hours()
        minutes = self.get_minutes_modulo()
        if hours > 0:
            return str(hours) + " godzin i " + str(minutes) + " minut"
        else:
            return str(minutes) + " minut"
        
    def get_hours(self):
        return int(self.minutes / 60)
        
    def get_minutes_modulo(self):
        return self.minutes % 60
    