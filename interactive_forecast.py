import common
import datetime
import logging


def main():
  zip_code = setZipcode()
  while(True):    
    option = raw_input('Please select one of the following: \n 1) Current temperature. \n 2) Forecast over the next 3 days. \n 3) Is it a good day? \n 4) Reset Zipcode. \n 5) Exit \n Enter your choice: ')

    if option == '1':
      currentTemp(zip_code)
    elif option == '2':
      three_day_forecast(zip_code)
    elif option == '3':
      good_day(zip_code)
    elif option == '4':
      zip_code = setZipcode()
    elif option == '5':
      exit()
    else:
      print 'Please select a valid option from the choices'


def setZipcode():
  return raw_input('Please enter the Zipcode of the forecast you would like to see: ')


def currentTemp(zip_code):
  request = common.checkCache(zip_code, True)
  if request:
    current_temp = parseTemp_(request)
  else:
    request = common.request_helper(common.CURRENT_CONDITIONS, zip_code)
    current_temp = parseTemp_(request)
    common.writeCache(request, zip_code)
  print 'current temperature for %s is %s' % (zip_code, current_temp)


"""Prints the next 3 day forecast based off provided zip code."""
def three_day_forecast(zip_code):
  request = common.checkCache(zip_code + 'forecast')
  if request:
    forecast = parseAndPrintForecast_(request)
  else:
    request = common.request_helper(common.FORECAST, zip_code)
    forecast = parseAndPrintForecast_(request)
    common.writeCache(request, zip_code + 'forecast')


"""Prints whether or not today will have nice weather."""
def good_day(zip_code):
  request = common.checkCache(zip_code + 'good_day', True)
  if request:
    parseAndPrintGoodDay_(request)
  else:
    request = common.request_helper(common.GOOD_DAY, zip_code)
    common.writeCache(request, zip_code + 'good_day')
    parseAndPrintGoodDay_(request)


"""Parses JSON for the hours leading up to 9pm today and evaluates whether or
   not the weather meets the "good day" criteria(Sunny and less than or 
   equal to 68)."""
def parseAndPrintGoodDay_(request_json):
  now = datetime.datetime.now()
  if (now.hour < 9 or now.hour > 21):
    print 'The hours of 9am to 9pm have already passed try back tomorrow.'
  else:
    # Check the hours between now and 9pm.
    try:
      r_base = request_json['hourly_forecast']
    except KeyError as details:
      logging.error('Unable to parse JSON check zipcode %s' % details)
    else: 
     for x in range(21 - now.hour):
      if (r_base[x]['wx'] == 'Sunny' and 
          int(r_base[x]['feelslike']['english']) <= 68):
        print 'Nice weather for %s with a Temp of %s ' % (
          r_base[x]['FCTTIME']['pretty'], r_base[x]['feelslike']['english'])
      else:
        print 'Weather is not sunny or hotter than 68 degrees for %s.' % (
            r_base[x]['FCTTIME']['pretty'])
 

"""Parses and prints the forecast for the next 3 days.""" 
def parseAndPrintForecast_(request_json):
  try:
    r_base = request_json['forecast']['simpleforecast']['forecastday']
  except KeyError as details:
    logging.error('Unable to parse forecast due to invalid JSON %s' % details)
  else:
    print '%-*s %-*s %-*s %-*s %-*s' %(10, 'Day', 
                                       10, 'Temp(High)',
                                       10, 'Temp(Low)',
                                       10, 'Wind(MPH)',
                                       10,'Conditions')
    print '-------------------------------------------------------'
    for x in range (1,4):
      print '%-*s %-*s %-*s %-*s %-*s' % (10,r_base[x]['date']['weekday'],
                                          10,r_base[x]['high']['fahrenheit'],
                                          10,r_base[x]['low']['fahrenheit'],
                                          10,r_base[x]['avewind']['mph'],
                                          10,r_base[x]['conditions'])


def parseTemp_(request_json):
  try:
    temp = request_json['current_observation']['temp_f']
  except KeyError as details:
    logging.error('Unable to parse temp due to invalid JSON %s' % details)
  else:
    return temp

if __name__ == "__main__":
    main()