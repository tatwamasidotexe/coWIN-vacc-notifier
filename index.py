import requests

from datetime import datetime, timedelta
import time
from pygame import mixer 

import json

print("blahblahblah testing.")

age = 55
pincodes = ["751013", "751031", "750017", "751016", "751017", "751051"]
within = 10 # no. of days within which we want a slot

flag = 'y'

today = datetime.today()

# list of all the dates we want to check availability for
list_of_datetimes = [today + timedelta(days = i) for i in range(within)]

dates_to_check = [i.strftime("%d-%m-%Y") for i in list_of_datetimes]

while True :
    count = 0
    for pincode in pincodes:
        for date in dates_to_check :
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, date)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
            response = requests.get(URL, headers = header)

            if response.ok :
                # storing the huge data received as response from CoWIN server in a json
                response_json = response.json()

                if response_json["centers"] :
                    if(flag == 'y') :
                        for center in response_json["centers"] :
                            for session in center["sessions"] :
                                if session["min_age_limit"] <= age and session["available_capacity"] > 0 :
                                    print("Pincode: "+ pincode)
                                    print(f"\t Available on: {date}")
                                    print("\t"+ center["name"])
                                    print(f"\t"+ center["block_name"])
                                    print(f"\t Price: "+ center["fee_type"])
                                    print(f"\t Availability: "+ str(session["available_capacity"]))

                                    if session["vaccine"] != "" :
                                        print(f"\t Vaccine type: "+ session["vaccine"])
                                    print('\n')

                                    count+=1
                else :
                    print("No response :((")
    
    if count :
        mixer.init()
        mixer.music.load('mixkit-happy-bells-notification-937.wav')
        mixer.music.play()
        print("\nAh. The sweet taste of success.")
        print("Search completed!")
    else :
        print("No slots found, sorry :(")

    dt = datetime.now() + timedelta(minutes=3)

    while datetime.now() < dt:
        time.sleep(1)