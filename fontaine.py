import urllib
import urllib2
from bs4 import BeautifulSoup
import json
from meeting import Meeting
import csv
from datetime import date
import calendar

def do():
  #So, this is how it goes
  #1, loop through years so we know what year we're passing in
  #2, loop through pages referencing the year for date

  this_year = date.today().year 

  meetings = []
  for year in range(2014, this_year+1):
    page_count = get_page_count(year)
    print(page_count)
    #page_count = 4

    for page in range(0, page_count + 1):
      print("printing page: " + str(page))
      response = make_server_call(year, page)
      html_data = format_server_response_to_json(response)
      meetings = meetings + parse_data_into_meetings(html_data, year)

  write_csv_from_meetings(meetings)

#Functions

def make_server_call(year, page):
  url = 'https://ec.europa.eu/commission/views/ajax_en'
  values = {'view_name' : 'agenda',
            'view_display_id' : 'list',
            'page' : str(page),
            'date_filter[min][date]' : "01/01/"+str(year),
            'date_filter[max][date]' : "31/12/"+str(year)
           }
  print(values)
  
  data = urllib.urlencode(values)
  req = urllib2.Request(url, data)
  response = urllib2.urlopen(req)
  the_page = response.read()
  return the_page

def format_server_response_to_json(response):

  json1_data = json.loads(response)

  html_data = json1_data[1]['data']
  return html_data
  
def parse_data_into_meetings(data, year):
  soup = BeautifulSoup(data)
  meetings = soup.find_all(class_="listing-item")

  meetings_array = []
  for meeting in meetings:
    #if the month is two, just take the first
    month = meeting.find(class_='month').get_text()
    spans_multiple_months = False
    if len(month) > 3:
      month = month.split()[0]
      spans_multiple_months = True

    #if day is a range we have to split it, get the first date, and then set length
    day = 0
    #default length
    length = 1
    day_text = meeting.find(class_='day').get_text().encode('utf-8')
    if len(day_text) > 2:
      day_text_parts = day_text.split("-")
      day = int(day_text_parts[0])

      if(spans_multiple_months == False):
        length = int(day_text_parts[1]) - int(day_text_parts[0])
      else:
        month_number = Meeting.number_for_month_name(month)
        number_of_days_in_month = calendar.monthrange(year, month_number)
        length = int(day_text_parts[1]) + (number_of_days_in_month[1] - int(day_text_parts[0]))
    else: 
      day = int(day_text)
            
    text = meeting.find(class_='views-field-field-activity-link').get_text()
    name = meeting.find("span", class_='field-content').get_text()
    meeting_object = Meeting(name, text, year, month, day, length)

    meetings_array.append(meeting_object)

  for meeting in meetings_array:
    print meeting.name + " : " + meeting.date_as_string() + " : " + meeting.text
  return meetings_array

def write_csv_from_meetings(meetings):
  with open('meetings.csv', 'wb') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=',')
      spamwriter.writerow(["Date", "Length", "Name", "Text"])
      for meeting in meetings:
          spamwriter.writerow(meeting.list_representation())
     
def get_page_count(year):
  data = make_server_call(year, 0)
  html_data = format_server_response_to_json(data)
  #Find the page count here
  soup = BeautifulSoup(html_data)
  total = soup.find(class_="pager-current-combo-total").find("em").get_text().lstrip().rstrip()
  return int(total)

do()