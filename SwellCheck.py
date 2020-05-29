import arrow
import requests
from KeyManager import KeyManager

class SwellCheck:

    sg_key = KeyManager("sg_keys").get_key()
    hour_range = 24

    def __init__(self, lat=37.4435478, lng=-122.4729689, param="swellHeight,swellPeriod"):
        self.lat = lat
        self.lng = lng
        self.param = param

    def get_json(self):
        # Get first hour of today
        start = arrow.now().floor('hour')

        # Get last hour of shifted range
        end = arrow.now().shift(hours=self.hour_range).ceil('hour')

        response = requests.get(
            'https://api.stormglass.io/v2/weather/point',
            params={
                'lat': self.lat,
                'lng': self.lng,
                'params': self.param,
                'source': 'noaa,sg',
                'start': start.to('UTC').timestamp,  # Convert to UTC timestamp
                'end': end.to('UTC').timestamp  # Convert to UTC timestamp
            },
            headers={
                'Authorization': self.sg_key
            }
        )

        # Do something with response data.
        return response.json()
        #print(json_data)

    def set_hour_range(self, hour_range):
        self.hour_range = hour_range

    def print_swells(self):
        json_data = self.get_json()
        print(f'{"DATE / TIME":^20}||{"NOAA SWELL":^18}||{"SG SWELL":^20}||')
        for item in json_data["hours"]:
            arrtime = arrow.get(item["time"])
            time = arrtime.to("local").format("MM/DD/YYYY hh:mm A")
            noaaSwell = item["swellHeight"]["noaa"]*3.281
            sgSwell = item["swellHeight"]["sg"]*3.281
            noaaPer = item["swellPeriod"]["noaa"]
            sgPer = item["swellPeriod"]["sg"]

            #print(f"{time} ||  {noaaSwell:0<4}  |  {noaaWave:0<4}  ||  {sgSwell:0<4}  |  {sgWave:0<4}  ||")
            print(f"{time} ||{noaaSwell:>6.2f}ft @ {noaaPer:>5.2f}s  ||{sgSwell:>6.2f}ft @ {sgPer:>5.2f}s  ||")

    def test_swells(self):
        json_data = self.get_json()

        for item in json_data["hours"]:
            arrtime = arrow.get(item["time"])
