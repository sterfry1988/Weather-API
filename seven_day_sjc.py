import datetime
import common

# In your own scripting language of choice, create a solution for the following questions. Your code should be well commented. Final solution should include: the approach, your script, and the output results.

# Write a script that gets historical average (or mean) temperature of San Jose, California over the past seven days.
# Write a script that takes user input for a zip code and can show any of the user-selected following features - current temperature, forecast over the next 3 days, and whether or not today is a good day to get out of the house (assume sunny at an ambient 68F, no higher, between 9am-9pm).


"""Makes requests for the average temperature for the last seven days. Will then average the average temperatures and print them to the console."""
def main():
  today = datetime.date.today()
  temperatures = {}
  #Start the range at 1 and go to 8 to ensure we go back 7 days.
  for x in range(1,8):
    #Take today and subtract x days, this allows requests to be made in the past.
    request_date = (today - datetime.timedelta(days=x))

    # Check to see if there is an existing saved request for this day.
    request = common.checkCache(request_date.isoformat()) 
    if (request):
      temp = parseTemp_(request)
    else:        
        request = common.request_helper(common.SJC_HISTORY_URL, request_date.strftime('%Y%m%d'))
        temp = parseTemp_(request)
        common.writeCache(request, request_date.isoformat())
    temperatures[request_date] = temp
  
  #Sum all the temperatures and then divide them by the count of temperatures.
  avg_temp = sum(temperatures.values()) / len(temperatures.values())
  print 'The average temperature in San Jose for the last 7 days is %d' % avg_temp


"""Parses out the average temperature from the request json."""
def parseTemp_(request_json):
  try:
    temp = int(request_json['history']['dailysummary'][0]['meantempi'])
  except KeyError as details:
    print 'Unable to parse temp due to invalid JSON %s' % details
  else:
    return temp

if __name__ == "__main__":
    main()