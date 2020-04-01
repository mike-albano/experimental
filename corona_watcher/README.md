Does an HTTP GET using Python Requests, plays a sound depending on result.

pip3 install -r requirements.txt

Usage example, for state of Colorado:
```
python3 corona_tracker.py co
```

Stick a sound file and uncomment the following line, if you also want to play a sound (OSX Only):
```
Line 32: # os.popen('open sound.mp3')
```
Default is to perform the GET every 5 minutes; feel free to change the following to increase/decrease that:
```
Line 43: time.sleep(300)  # Perform the check every 5m
```
If you want to track something other than positive cases, change the 'parse_data' function and 'initial_num' variables around to suite your needs.

Uses the data from: [https://covidtracking.com/api/](https://covidtracking.com/api/)
