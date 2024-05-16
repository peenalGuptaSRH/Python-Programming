# function to convert the hours to minutes 
def convertHoursToMinutes(time_str):
    #Converts time string in 'HH:MM' format to minutes.
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

#function to fing the available meeting slots
def find_meeting_slots(your_slots, coworker_slots, duration):
    #Finds the common meeting slots between the user and the coworker.
    common_slots = []

    # Convert all time slots to minutes for easier comparison.
    your_slots_in_minutes = [(convertHoursToMinutes(start), convertHoursToMinutes(end)) for start, end in your_slots]
    coworker_slots_in_minutes = [(convertHoursToMinutes(start), convertHoursToMinutes(end)) for start, end in coworker_slots]

    # Compare your free time slots with your coworker's to find overlapping periods.
    for your_start, your_end in your_slots_in_minutes:
        for coworker_start, coworker_end in coworker_slots_in_minutes:
            # Find the overlap between your free time and your coworker's.
            start = max(your_start, coworker_start)
            end = min(your_end, coworker_end)

            # If there is enough time for the meeting in the overlapping slot, add it to the common slots list.
            if (end - start) >= duration:
                common_slots.append((start, end))

    # Convert common slots back to 'HH:MM' format.
    available_meeting_slots_formatted = [(f'{start // 60:02d}:{start % 60:02d}', f'{end // 60:02d}:{end % 60:02d}') for start, end in common_slots]

    return available_meeting_slots_formatted