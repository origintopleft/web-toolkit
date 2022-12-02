import datetime
import json
import logging

import flask
import requests

from . import core, error

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

def refresh_data(**tdelta):
    global ts_weatherupdate
    global dat_weather

    if dat_geodata == None:
        get_geodata()

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

def generate_result():
    return {
        # standard response
        "ts": ts_weatherupdate.timestamp()
    }

@core.app.route("/weather/suntimes")
def get_suntimes():
    # sunrise/sunset times don't change frequently, or if they do, not by enough to matter.
    refresh_data(hours=16)

    result_data = generate_result()
    result_data["sunrise"] = dat_weather["sys"]["sunrise"]
    result_data["sunset"]  = dat_weather["sys"]["sunset"]

    return flask.Response(json.dumps(result_data), content_type="application/json")

@core.app.route("/weather/temperature")
def get_temperature():
    refresh_data(minutes=15)

    result_data = generate_result()
    result_data["min"]      = dat_weather["main"]["temp_min"]
    result_data["max"]      = dat_weather["main"]["temp_max"]
    result_data["current"]  = dat_weather["main"]["temp"]
    result_data["feels"]    = dat_weather["main"]["feels_like"]

    return flask.Response(json.dumps(result_data), content_type="application/json")