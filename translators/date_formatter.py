from datetime import datetime
from dateutil import tz as time_zone_calculator

def format_date_as_string_to_date_object_with_present_time_zone(date_as_string):
        if date_as_string != None:
                present_time_zone = time_zone_calculator.gettz('Europe / Berlin')
                date_as_iso = datetime.fromisoformat(date_as_string)
                date_with_present_time_zone = date_as_iso.astimezone(present_time_zone)
                return date_with_present_time_zone
        else:
                return None