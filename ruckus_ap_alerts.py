#!/usr/local/bin/python3
import datetime, requests, json, os, time
from dotenv import load_dotenv
load_dotenv(verbose=True)

ruckusapi_url = os.environ['ruckusapi_url']
username = os.environ['username']
password = os.environ['password']

ruckus_auth = {
    "username": username,
    "password": password,
    "timeZoneUtcOffset": "-05:00"
}

sz_headers = {
    'Content-type': 'application/json;charset=UTF-8',
    'Connection': 'keep-alive'
              }

def ruckus_login():
    sz_logon_url = f"{ruckusapi_url}/session"
    session = requests.session()
    r = session.post(sz_logon_url, data=json.dumps(ruckus_auth), headers=sz_headers)
    r = session.get(sz_logon_url)
    if r.status_code == 200:
        return session
    else:
        quit()

def get_events(session):
    payload = "{\n  \"limit\": 100\n}"
    response = session.post(os.environ['ruckusapi_url'] + "/alert/alarm/list", data=payload, headers=sz_headers, verify=False)

    return response

session = ruckus_login()

events = get_events(session)

event_list = events.json()['list']

for event in event_list:
    epoch_time = (event['insertionTime'] / 1000)
    readable_time = time.strftime("%a, %m/%d/%y, %I:%M:%S %p %Z", time.localtime(epoch_time))
    print ('AP Alarm Detected:',str(event['activity']),'\nTime:',str(readable_time))

# print(json.dumps(events.json()['list'], sort_keys=True, indent=4))
