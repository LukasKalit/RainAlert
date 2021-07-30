import requests
import json
from dotenv import load_dotenv
import smtplib
import os
load_dotenv()

print(os.environ)
MAIN_MAIL = os.getenv("HOST_MAIL")
PASSWORD = os.getenv("HOST_PASSWORD")
DESTINATION_MAIL = os.getenv("DESTINATION_MAIL")
APP_ID_WEATHER = os.getenv("APP_ID_WEATHER")


OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
params = {
    "lat": 52.229675,
    "lon": 21.012230,
    "appid": APP_ID_WEATHER,
    "exclude": "current,minutely,daily"
}
response = requests.get(OWM_Endpoint, params=params)
response.raise_for_status()

weather_data = response.json()
with open("weather_data.json", "w") as data_file:
    json.dump(weather_data, data_file, indent=4)

will_rain = False

only_hour_dict = weather_data["hourly"]
for item in only_hour_dict[:12]:

    if item["weather"][0]["id"] < 800:
        will_rain = True

if will_rain:
    print("Take umbrella")
    with smtplib.SMTP("smtp.gmail.com") as smtp:
        smtp.starttls()
        smtp.login(user=MAIN_MAIL, password=PASSWORD)
        smtp.sendmail(MAIN_MAIL, DESTINATION_MAIL, msg="Subject:Weather today\n\nTake umbrella, today will raining")



