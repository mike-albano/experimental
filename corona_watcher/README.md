Does an HTTP GET using Python Requests (pip3 install requests).

Usage example, for state of Colorado:
```
python3 corona_tracker.py co
```

Stick a sound file and uncomment the following line, if you also want to play a sound (OSX Only):
```
Line 32: # os.popen('open sound.mp3')
```
Default is to perform the GET every 1 minute; feel free to change the following to increase/decrease that:
```
Line 43: time.sleep(60)  # Perform the check every 60s
```
If you want to track something other than positive cases, change the 'parse_data' function and 'initial_num' variables around to suite your needs.

Uses the data from: [https://covidtracking.com/api/](https://covidtracking.com/api/)
