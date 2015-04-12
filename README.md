# Weather-API
This is a script that will compute and print the average temperature for the last seven days for San Jose, CA.

## Approach
The approach taken for this script was to use the free API at http://api.wunderground.com. This API gives free access to historical weather information and had good documentation.

### Language
The language chosen for this script was to use Python. Python is an easy to read language which has many built-in libraries that makes accomplishing a task like this fun. 

### Implementation

The urllib2 library was used for creating a connection to the remote api and returning the request. The request will be converted to json which will allow the programmer to extract information in a standard way. This will also make reading and writing the request to a file easy.

In order to save time on repeated calls and API quota the requests will be saved to disk. This allows for faster execution of the script in the event that the requests have been made already. Assuming this script was to be ran every day it would only require 1 new API call to be made per day for the past week's temperature. Because the requests in the interactive script are testing realtime information there is a variable in common.py that will set a threshold, and a flag in checkCache_ to determine whether or not the API should be called. 


