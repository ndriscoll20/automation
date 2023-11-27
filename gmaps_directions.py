import requests
import json
import time
from datetime import datetime
import urllib.error, urllib.parse, urllib.request
import ezgmail, os

f = open(r'/home/nick/python/api.json')
data = json.load(f)
API_KEY = data['apikey']

request_url = ('https://maps.googleapis.com/maps/api/directions/json'+
    '?departure_time=now'+
    '&origin=225+Presidential+Way+Woburn+MA'+
    '&destination=242+Ridge+Road+Marshfield+MA'+
    '&key='+API_KEY)

def check_token():
    tok = r'/home/nick/python/token.json'
    
    try: 
        f = open(tok)
        data = json.load(f)
        tok_time = time.strptime(data['token_expiry'], '%Y-%m-%dT%H:%M:%SZ')
        # If token is expired, delete token & re-initialize
        if time.localtime() > tok_time:
            os.remove('/home/nick/python/token.json')
            ezgmail.init()
    except: 
        ezgmail.init()

def send_email(route, traffic_duration):
    # Confirm the Trip summary 
    email_body = ('As of ' + time.strftime('%H:%m:%S') + ' ' + route + ' now takes ' + traffic_duration)
    ezgmail.send('ndriscoll20@gmail.com', 'Traffic notification', email_body)
    # Sleep now through the end of the time period so we don't send another notification until tomorrow
    print('Email Sent: '+ time.strftime('%H:%m:%S'))
    time.sleep(12000)

def test_email():
    email_body = 'Testing sending emails with python'
    ezgmail.send('ndriscoll20@gmail.com', 'Test Numero Uno', email_body)

def get_traffic_duration():
    req = requests.get(request_url)
    json_obj = req.json()
    # Get the traffic duration
    traffic_duration = json_obj['routes'][0]['legs'][0]['duration_in_traffic']['text']
    
    # 'I-93 S and MA-3 S' is one of the responses
    route = json_obj['routes'][0]['summary'] 

    return route, traffic_duration
        
def main():
    while True: 
        # Check every 5 mins
        time.sleep(300)

        # Only check between 5 & 8 PM
        if time.localtime()[3] > 17 & time.localtime()[3] < 20:
            check_token()

            route, traffic_duration = get_traffic_duration()
            
            #TO DO: do this better using durations or time deltas
            if 'hours' in traffic_duration:
                # Not sending if multiple hours
                continue
            elif 'mins' in traffic_duration & 'hour' not in traffic_duration:
                dt = datetime.datetime(traffic_duration, '%M mins')
                send_email(route, traffic_duration)             
            elif 'mins' in traffic_duration & 'hour' in traffic_duration:
                dt = datetime.datetime(traffic_duration, '%H hour %M mins')
                if dt.minute < 15:
                    # Only Send Email if under an hour and 15
                    send_email(route, traffic_duration)
                else:
                    continue
            elif 'min' in traffic_duration & 'hour' in traffic_duration:
                # Corner case, 1 hour 1 minute
                dt = datetime.datetime(traffic_duration, '%H hour %M min')
                send_email(route, traffic_duration)

if __name__ == "__main__":
    main() 
    
    
    # Unit Tests
    #test_email()
    # route, traffic_duration = get_traffic_duration()
    # send_email(route, traffic_duration)

            
            

            
