from dateutil.parser import parse
def readJsonProperties(jsonObject, today):
    # print("Inside the function readJsonProperties: ",jsonObject)
    # Initialize an empty list to hold working hours for today
    WorkingHours = []
    event_date = None
    # # Extract and format the start and end times for today's date
    for item in jsonObject.get("items", []):
        start_dateTime = item.get("start", {}).get("dateTime")
        # Parse the dateTime to get the date
        if start_dateTime is not None:
            event_date = parse(start_dateTime).date()
        else:
            event_date = start_dateTime
        if event_date == today:
            # Parse and format the start and end times
            start_time = parse(start_dateTime).strftime('%H:%M')
            end_time = parse(item.get("end", {}).get("dateTime")).strftime('%H:%M')

            # Update the YourWorkingHours list
            WorkingHours = [start_time, end_time]
            # print("YourWorkingHours: ",WorkingHours)
    return WorkingHours
    # print("YourWorkingHours: ",YourWorkingHours)