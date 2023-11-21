import requests
import json
import time
from datetime import datetime
import urllib.error, urllib.parse, urllib.request
import ezgmail, os

API_KEY = ''

request_url = ('https://maps.googleapis.com/maps/api/directions/json'+
    '?departure_time=now'+
    '&origin=225+Presidential+Way+Woburn+MA'+
    '&destination=242+Ridge+Road+Marshfield+MA'+
    '&key='+API_KEY)

#One line key code for URL:
#https://maps.googleapis.com/maps/api/directions/json?departure_time=now&origin=225+Presidential+Way+Woburn+MA&destination=242+Ridge+Road+Marshfield+MA&key=AIzaSyDDCQZAUgunU7Ud_2v6jAhSx3taBCy0_u0


def send_email(traffic_duration, route):
    # Confirm the Trip summary 
    email_body = (route + ' now takes ' + traffic_duration)
    ezgmail.send('ndriscoll20@gmail.com', 'Traffic notification', email_body)
    # Sleep now through the end of the time period so we don't send another notification until tomorrow
    time.sleep(12000)

if __name__ == "__main__":
    while True: 
        # Check every 5 mins
        time.sleep(300)

        # Only check between 5 & 8 PM
        if time.localtime()[3] > 17 & time.localtime()[3] < 20:
            req = requests.get(request_url)
            json_obj = req.json()

            # Get the traffic duration
            traffic_duration = json_obj['routes'][0]['legs'][0]['duration_in_traffic']['text']
            
            # 'I-93 S and MA-3 S' is one of the responses
            route = json_obj['routes'][0]['summary'] 
            
            #TO DO: do this better
            if 'hours' in traffic_duration:
                # Not sending if multiple hours
                continue
            elif 'mins' in traffic_duration & 'hour' not in traffic_duration:
                dt = datetime.datetime(traffic_duration, '%M mins')
                send_email(traffic_duration, route)                
            elif 'mins' in traffic_duration & 'hour' in traffic_duration:
                dt = datetime.datetime(traffic_duration, '%H hour %M mins')
                if dt.minute < 15:
                    # Only Send Email if under an hour and 15
                    send_email(traffic_duration, route)
                else:
                    continue
            elif 'min' in traffic_duration & 'hour' in traffic_duration:
                # Corner case, 1 hour 1 minute
                dt = datetime.datetime(traffic_duration, '%H hour %M min')
                send_email(traffic_duration, route)

            

            
            

            
