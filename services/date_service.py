from datetime import datetime, timedelta

def get_current_day():
    return datetime.now().day

def get_current_month():
    return datetime.now().month

def get_last_day_of_previous_month():
    current_date = datetime.now()
    number_of_days = current_date.day
    date_month_before = current_date - timedelta(number_of_days)
    return date_month_before

def get_year_of_previous_month():
    date_month_before = get_last_day_of_previous_month()
    previous_year = date_month_before.year
    return previous_year

def get_next_month(month=get_current_month()):
    return (month + 1) % 12

def get_previous_month(month=get_current_month()):
    return (month - 1) % 12

def get_number_of_days_in_a_month(month, year):
    if (month == 2) and ((year % 4 == 0) or ((year % 100 == 0) and (year % 400 == 0))):
        return 29
    elif month == 2:
        return 28
    elif month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    else:
        return 30

def get_month_name(month_number):
    
    month_name = None
    match(month_number):
        case 1: month_name = "Styczeń" 
        case 2: month_name = "Luty"
        case 3: month_name = "Marzec"
        case 4: month_name = "Kwiecień"
        case 5: month_name = "Maj"
        case 6: month_name = "Czerwiec"
        case 7: month_name = "Lipiec"
        case 8: month_name = "Sierpień"
        case 9: month_name = "Wrzesień"
        case 10: month_name = "Październik"
        case 11: month_name = "Listopad"
        case 12: month_name = "Grudzień"
    
    return month_name