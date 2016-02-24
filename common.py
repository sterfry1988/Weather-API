from datetime import datetime
import json
import logging
import os
import urllib2 
# API key used for http://api.wunderground.com
API_KEY = 'your key here'
API_URL = 'http://api.wunderground.com/api/'
CACHE_AGE = 3 * 60 * 60 # 3 hours in seconds
# URL to request the historical temperatures for San Jose. Note that only 30 days in the past can be retrieved. 
SJC_HISTORY_URL = API_URL + API_KEY + '/history_%s/q/CA/San_Jose.json' 


CURRENT_CONDITIONS = API_URL + API_KEY + '/conditions/q/%s.json'
GOOD_DAY = API_URL + API_KEY + '/hourly/q/%s.json'
FORECAST = API_URL + API_KEY + '/forecast/q/%s.json'


"""urllib2 wrapper to help handle all requests. Accepts a URL and a param where the param is most likely going to be a ZIP code."""
def request_helper(url, param):
  try:
    request = urllib2.urlopen(url % param)
  except urllib2.URLerror as details:
    logging.error('Unable to open spefied url %s details %s '(url, details))
  else:
    return json.loads(request.read())


"""Writes request json to file for future caching."""
def writeCache(request, request_key):
  with open(request_key, 'w') as cachefile:
    json.dump(request, cachefile)


"""Returns request file from disk or None. If refresh is specific the file will be checked for staleness and refreshed if the cache threshold is met."""
def checkCache(request_key, refresh=None):
  try:
    f = open(request_key, 'r')
  except IOError as details:
    logging.info('unable to open %s ' % details)
    return None
  else:
    # Evaluate if the cache is stale. 
    if refresh:
      cache_age = datetime.fromtimestamp(os.path.getmtime(request_key))
      if (datetime.now() - cache_age).seconds > CACHE_AGE:
        logging.info('Cache was outside of age threshold, returning None.')
        return None
    return json.loads(f.read())
