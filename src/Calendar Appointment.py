#Implementation of the calendar exercise is done by the help of Google calendar api.
# The credentials are saved in this file
#If the API is not working, the code can also be verified by uncommenting the direct input variables from Line 124 to Line 130 passsed to the function ----> find_meeting_slots
#Comment the lines from Line 142 to 167
import datetime
from http import client
import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pytz

import utils.FreeTimeSlots as ft
import utils.ChangeTimeArrayFormat as ct
import utils.utility as util
import utils.MeetingSlots as meet



# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Google Calendar - Assignment'

def getCredentials():
    creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())
    return creds

# ## Method to get the Working hours
def getWorkingHours(credentials, email):
  try:
      service = build("calendar", "v3", credentials=credentials)
      # Call the Calendar API
      events_result = (
          service.events()
          .list(
              calendarId= email,
              singleEvents = True,
              orderBy = "startTime",
              showDeleted = False,
              # timeMax= '2023-02-29T23:00:00+01:00',
              # timeMin= '2023-02-12T00:00:00+01:00',
              eventTypes=['workingLocation'],
          )
          .execute()
      )
      events = events_result.get("items", [])
      if not events:
        print("No upcoming events found.")
        return
      else:
        # Get today's date
        today = datetime.date.today()
        events_result_str = json.dumps(events_result, indent=4)
        # Parse the JSON string
        data = json.loads(events_result_str)
        workingHours = util.readJsonProperties(data, today)
        return workingHours
  except HttpError as error:
        print(f"An error occurred: {error}")
    


## Method to get the working hours
def getBusyHoursOfCoworker(credentials, start_time, end_time, email):
    credentials = getCredentials()
    try:
        service = build("calendar", "v3", credentials=credentials)
        body = {
            "timeMin": start_time.isoformat(),
            "timeMax": end_time.isoformat(),
            "timeZone": 'UTC',
            "items": [{"id": email}]
        }
        eventsResult = service.freebusy().query(body=body).execute()
        return eventsResult
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def getEvents(credentials):
  try:
      service = build("calendar", "v3", credentials=credentials)
      page_token = None
      while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            print(calendar_list)
            for calendar_list_entry in calendar_list["items"]:
                print(calendar_list_entry["summary"])
            page_token = calendar_list.get("nextPageToken")
            if not page_token:
                break

  except client.AccessTokenRefreshError:
        print(
            "The credentials have been revoked or expired, please re-run"
            "the application to re-authorize."
        )

def main():
    #Uncomment the part if the calendar api is not returning any result
    #start here
    # yourWorkingHours =  ['09:30', '19:30']
    # coWorkerWorkingHours =  ['09:00', '18:30']
    # yourCalendar = [('10:00', '11:00'), ('12:00', '13:00'), ('17:30', '18:00')]
    # coWorkerCalendar =  [('09:30', '10:30'), ('13:00', '15:00'), ('16:00', '16:30')]
    # meetingDuration = 30
    # free_time_slot_for_self =  [('09:30', '10:00'), ('11:00', '12:00'), ('13:00', '17:30'), ('18:00', '19:30')]
    # free_time_slot_for_coworker =  [('09:00', '09:30'), ('10:30', '13:00'), ('15:00', '16:00'), ('16:30', '18:30')]
    #end here
    
    
    
    tz = pytz.timezone('UTC')
    credentials = getCredentials()
    selfEmail = "peenal.gupta@srh-heidelberg.org"
    coWorkerEmail = "peenal.gupta@quantumdatasolutions.org" #test account for the assignment 
    
    # Get the working Hours 
    yourWorkingHours = getWorkingHours(credentials, selfEmail)
    coWorkerWorkingHours = getWorkingHours(credentials, coWorkerEmail)
    print("YourWorkingHours : ",yourWorkingHours)
    print("YourCoWorkersWorkingHours : ",coWorkerWorkingHours)
    
    today = datetime.date.today()
    the_datetime_start = tz.localize(datetime.datetime.combine(today, datetime.time(0, 0, 0)))
    the_datetime_end = tz.localize(datetime.datetime.combine(today, datetime.time(23, 59, 59)))
    
    #Get the Calendar events
    freebusy_info_colleague = getBusyHoursOfCoworker(credentials, the_datetime_start, the_datetime_end, coWorkerEmail)
    freebusy_info_self = getBusyHoursOfCoworker(credentials, the_datetime_start, the_datetime_end, selfEmail)
    coWorkerCalendar = ct.convert_to_simple_tuples(freebusy_info_colleague['calendars'][coWorkerEmail])
    yourCalendar = ct.convert_to_simple_tuples(freebusy_info_self['calendars'][selfEmail])
    print("YourCalendar :", yourCalendar)
    print("YourCoWorkersCalendar : ", coWorkerCalendar)
 
    # Calculate free time
    free_time_slot_for_self = ft.calculate_free_time(yourWorkingHours[0], yourWorkingHours[1],yourCalendar)
    free_time_slot_for_coworker = ft.calculate_free_time(coWorkerWorkingHours[0], coWorkerWorkingHours[1],coWorkerCalendar)
    
    meetingDuration = int(input("Enter the meeting duration in minutes: "))
    # Get Available slots 
    available_meeting_slots = meet.find_meeting_slots(free_time_slot_for_self, free_time_slot_for_coworker, meetingDuration)
    print("Meeting Duration:", meetingDuration)
    print("Available Meeting Slots: ",available_meeting_slots)
    

if __name__ == "__main__":
  main()
  
  
  
# Time Complexity:  O(n^2)

# The time complexity of the find_meeting_slots function is O(n^2), where n is the number of time slots for both the user and the coworker. 
# This is because the function compares each of the user's time slots with each of the coworker's time slots to find overlapping periods.

# Space Complexity: O(n)

# The space complexity of the find_meeting_slots function is O(n), where n is the number of time slots for both the user and the coworker. 
# This is because the function creates a new list to store the common meeting slots, and the size of this list can be at most n.