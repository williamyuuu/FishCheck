import arrow
import requests
from KeyManager import KeyManager

class SwellCheck:

    sg_key = KeyManager("sg_keys").get_key()
    amount = 8
    hour_range = 24
    start = 0

    def __init__(self, lat=37.4435478, lng=-122.4729689, param="swellHeight,swellPeriod"):
        self.lat = lat
        self.lng = lng
        self.param = param

    def get_json(self):
        # Get first hour of today
        start = arrow.now()

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

        return response.json()

    def get_start_point(self):
        json_data = self.get_json()

        for item in range(0, 4):
            arrtime = arrow.get(json_data["hours"][item]["time"])
            utc_hour = arrtime.format("HH")

            if (int(utc_hour) % 3 == 0):
                start = item

        self.start = start
        return start

    def set_amount(self, amount):
        self.amount = amount
        self.hour_range = ((self.amount+1) * 3) + self.start

    def print_swells(self):
        json_data = self.get_json()
        start = self.get_start_point()
        print(f'{"DATE / TIME":^20}||{"NOAA SWELL":^19}||{"SG SWELL":^20}||')

        for x in range(start, self.hour_range, 3):
            arrtime = arrow.get(json_data["hours"][x]["time"])
            time = arrtime.to("local").format("MM/DD/YYYY hh:mm A")
            noaaSwell = json_data["hours"][x]["swellHeight"]["noaa"] * 3.281
            sgSwell = json_data["hours"][x]["swellHeight"]["sg"] * 3.281
            noaaPer = json_data["hours"][x]["swellPeriod"]["noaa"]
            sgPer = json_data["hours"][x]["swellPeriod"]["sg"]

            # print(f"{time} ||  {noaaSwell:0<4}  |  {noaaWave:0<4}  ||  {sgSwell:0<4}  |  {sgWave:0<4}  ||")
            print(f"{time} ||{noaaSwell:>6.2f}ft @ {noaaPer:>5.2f}s  ||{sgSwell:>6.2f}ft @ {sgPer:>5.2f}s  ||")


    def print_hourly_swells(self):
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

