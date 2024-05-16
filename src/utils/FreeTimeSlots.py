from datetime import datetime, timedelta


def format_time_in_hrs_min(timestring):
    dt_object = datetime.fromisoformat(timestring)
    # Convert to a string with only hours and minutes
    hours_minutes_format = dt_object.strftime('%H:%M')
    return hours_minutes_format


def parse_time(t):
    # Parse a 'HH:MM' string into a datetime object.
    return datetime.strptime(t, '%H:%M')

def format_time(dt):
    #Format a datetime object into a 'HH:MM' string.
    return dt.strftime('%H:%M')

def calculate_free_time(start, end, booked):
    free_slots = []
    booked = sorted(booked, key=lambda x: x[0])  # Sort booked times by start time
    current_time = parse_time(start)

    for start_booked, end_booked in booked:
        start_booked_dt = parse_time(start_booked)
        end_booked_dt = parse_time(end_booked)

        # If there's free time before the booked slot, add it to the free times
        if current_time < start_booked_dt:
            free_slots.append((format_time(current_time), format_time(start_booked_dt)))
        
        # Update current_time to the end of the booked slot
        current_time = max(current_time, end_booked_dt)
    
    # Check for free time after the last booked slot until the end time
    end_dt = parse_time(end)
    if current_time < end_dt:
        free_slots.append((format_time(current_time), format_time(end_dt)))
    
    return free_slots

