from datetime import datetime
import pytz

def convert_to_simple_tuples(busy_times):
    # Convert an array of busy times from ISO 8601 format to simple ('HH:MM', 'HH:MM') tuples.
    simple_times = []
    for slot in busy_times['busy']:
        # Parse the ISO 8601 date-time strings
        start_dt = datetime.strptime(slot['start'], '%Y-%m-%dT%H:%M:%SZ')
        end_dt = datetime.strptime(slot['end'], '%Y-%m-%dT%H:%M:%SZ')
        
        # Optionally convert to another timezone, here keeping as UTC
        # If you need to convert to another timezone, apply the conversion here
        
        # Format times into 'HH:MM'
        start_time = start_dt.strftime('%H:%M')
        end_time = end_dt.strftime('%H:%M')
        
        simple_times.append((start_time, end_time))
    
    return simple_times
