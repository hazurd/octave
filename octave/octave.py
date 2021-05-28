import datetime as dt
import json
import requests
import os

def fetch_neows_feed(s, e):
    params = {
        'api_key': API_KEY,
        'start_date': s,
        'end_date': e
    }
    return requests.get(FEED_API, params=params).json()

def get_occurrences(neos):
    occurrences = []
    for dates in neos.values():
        for neo in dates:
            occurrences.append(neo)
    return occurrences

def get_close_approach_data(o):
    return o.get('close_approach_data')[0]

def answer(occurrences):
    cad = get_close_approach_data(occurrences)
    ans['name'] = occurrences.get('name')
    ans['id'] = occurrences.get('id')
    ans['close_approach_date_full'] = cad.get('close_approach_date_full')
    print(json.dumps(ans, indent=2))

ans = {}
API_KEY = os.getenv('NASA_API_KEY')
FEED_API = "https://api.nasa.gov/neo/rest/v1/feed"
STRFTIME = "%Y-%m-%d"

"""
1 Retrieve and display: name, id, close_approach_date_full
for asteroids with approach dates between October 31st 2019 and November 2nd 2019 (inclusive):
"""
start_date = dt.datetime(2019, 10, 31).strftime(STRFTIME)
end_date = dt.datetime(2019, 11, 2).strftime(STRFTIME)
neos = fetch_neows_feed(start_date, end_date).get('near_earth_objects')
for i in get_occurrences(neos):
    answer(i)

"""
2 ƒor asteroids with approach dates between
September 10th 2020 and September 17th 2020(inclusive) calculate:
The velocity, in kilometers_per_second, of the fastest asteroid for the period.
The velocity, in kilometers_per_second, of the slowest asteroid for the period
The mean velocity (in kilometers_per_second) of all asteroids in the period.
The median velocity (in kilometers_per_second) of all asteroids in the period.
Note: no numpy.
"""
start_date = dt.datetime(2020, 9, 10).strftime(STRFTIME)
end_date = dt.datetime(2020, 9, 17).strftime(STRFTIME)
neos = fetch_neows_feed(start_date, end_date).get('near_earth_objects')
kmps = []
float_list = []
for i in get_occurrences(neos):
    cad = get_close_approach_data(i)
    rel_velocity = cad.get('relative_velocity')
    kmps.append(rel_velocity.get('kilometers_per_second'))

for i in kmps:
    float_list.append(float(i))
float_list.sort()
n = len(float_list)
slowest = float_list[0]
fastest = float_list[-1]
# Mean and Median provided by geeksforgeeks.org/finding-mean-median-mode-in-python-without-libraries/
mean = sum(float_list) / len(float_list)
if n % 2 == 0:
    median1 = float_list[n//2]
    median2 = float_list[n//2 - 1]
    median = (median1 + median2)/2
else:
    median = float_list[n//2]
print(f"\nslowest: {slowest}, fastest: {fastest}, mean: {mean}, median: {median}\n")

"""
3 Find the three most recent (from today) asteroid approaches where the is_potentially_hazardous_asteroid flag is set to true.
"""
today = dt.datetime.today().strftime(STRFTIME)
start_date = today
end_date = today
now = dt.datetime.now().strftime('%H:%M')
hours = []
neos = fetch_neows_feed(start_date, end_date).get('near_earth_objects')
print("3 or less latest 'is_potentially_hazardous_asteroid' cases today")

for i in get_occurrences(neos):
    if i.get('is_potentially_hazardous_asteroid'):
        cad = get_close_approach_data(i)
        hours.append(cad.get('close_approach_date_full').split()[1])
most_recent = sorted(hours)
if len(most_recent) > 3:
    print(most_recent[-3])
else:
    print(most_recent)
