import json
import requests
import datetime

# In your own scripting language of choice, create a solution for the following questions. Your code should be well commented. Final solution should include: the approach, your script, and the output results.

# Write a script that gets historical average (or mean) temperature of San Jose, California over the past seven days.
# Write a script that takes user input for a zip code and can show any of the user-selected following features - current temperature, forecast over the next 3 days, and whether or not today is a good day to get out of the house (assume sunny at an ambient 68F, no higher, between 9am-9pm).


# API key used for http://api.wunderground.com
API_KEY = '98218564ac42bf29'

#URL to request the historical temperatures for San Jose. Note that only 30 days in the past can be retrieved. 
SJC_HISTORY_URL = 'http://api.wunderground.com/api/' + API_KEY + '/history_%s/q/CA/San_Jose.json' 


"""Makes requests for the average temperature for the last seven days. Will then average the average temperatures and print them to the console."""
def makeRequests():
  today = datetime.date.today()
  temperatures = {}
  #Start the range at 1 and go to 8 to ensure we go back 7 days.
  for x in range(1,8):
    #Take today and subtract x days, this allows requests to be made in the past.
    request_date = (today - datetime.timedelta(days=x))

    # Check to see if there is an existing saved request for this day.
    request = _checkCache(request_date.isoformat()) 
    if (request):
      temp = parseTemp_(request)
    else:      
      try:
        print 'Request for %s was not cached, requesting via api.' % request_date
        request = requests.get(SJC_HISTORY_URL % request_date.strftime('%Y%m%d'))
      except requests.exceptions.ConnectionError() as details:
        print 'Error occured requesting from API:%s' % details
        print 'Check your API quota and API key.'
      else:
        temp = parseTemp_(request.json())
        _writeCache(request.json(), request_date.isoformat())
    temperatures[request_date] = temp
  
  #Sum all the temperatures and then divide them by the count of temperatures.
  avg_temp = sum(temperatures.values()) / len(temperatures.values())
  print 'The average temperature in San Jose for the last 7 days is %d' % avg_temp


"""Writes request json to file for future caching."""
def _writeCache(request, request_date):
  with open(request_date, 'w') as cachfile:
    json.dump(request, cachfile)


"""Returns request file from disk or None."""
def _checkCache(request):
  try:
    f = open(request, 'r')
  except IOError as details:
    print 'Error occured, unable to open cache, requesting from API, details of error:%s.' % details
    return None
  else:
    return json.loads(f.read())

"""Parses out the average temperature from the request json."""
def parseTemp_(request_json):
  try:
    temp = int(request_json['history']['dailysummary'][0]['meantempi'])
  except KeyError as details:
    print 'Unable to parse temp due to invalid JSON %s' % details
  else:
    return temp
