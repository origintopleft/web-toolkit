import datetime
import json
import logging

import requests

from . import error

openweather_api_key = "2925f0e48e2ee50e2d78770977eee603"

ts_weatherupdate = datetime.datetime.now()
dat_weather = None
dat_geodata = None

def get_geodata():
    global dat_geodata
    logging.info("getting geolocation data")
    # http://api.openweathermap.org/geo/1.0/direct?q=Everett,wa,us&limit=1&appid=2925f0e48e2ee50e2d78770977eee603
    owmreq = requests.get("http://api.openweathermap.org/geo/1.0/direct", params={
        "q": "Everett,wa,us",
        "limit": 1,
        "appid": openweather_api_key
    })

    if owmreq.ok:
        dat_geodata = owmreq.json()[0]
    else:
        guestcheck_token = error.init_error()
        logging.error("{0} error getting geocaching data".format(owmreq.status_code))
        logging.error("guestcheck token: {0}".format(guestcheck_token))

def refresh_data(tdelta):
    global ts_weatherupdate
    global dat_weather

    if dat_weather == None or ts_weatherupdate + datetime.timedelta(**tdelta) < datetime.datetime.now():
        logging.info("refreshing weather data")
        owmreq = requests.get("https://api.openweathermap.org/data/2.5/weather", params={
            "lat": dat_geodata["lat"],
            "lon": dat_geodata["lon"],
            "units": "imperial",
            "appid": openweather_api_key
        })

        if owmreq.ok:
            incoming_data = owmreq.json()
            if incoming_data["cod"] == 200:
                ts_weatherupdate = datetime.datetime.now()
                dat_weather = incoming_data
                logging.info("weather information is most current as of this message")
            else:
                guestcheck_token = error.init_error()
                logging.error("API code {0} getting weather information (API itself OK)".format(incoming_data["cod"]))
                logging.error("guestcheck token: {0}".format(guestcheck_token))
        else:
            guestcheck_token = error.init_error()
            logging.error("{0} error getting weather information".format(owmreq.status_code))
            logging.error("guestcheck token: {0}".format(guestcheck_token))