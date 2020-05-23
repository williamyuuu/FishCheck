import arrow
import requests
from KeyManager import KeyManager

class SwellCheck:

    sg_key = KeyManager("sg_keys").get_key()
    param = "swellHeight,swellPeriod"

    def __init__(self, lat=37.4435478, lng=-122.4729689):
        self.lat = lat
        self.lng = lng

    def get_tides(self):
        # Get first hour of today
        start = arrow.now().floor('hour')

        # Get last hour of today
        end = arrow.now().ceil('day')
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
        json_data = response.json()
        #print(json_data)

        print(f'{"DATE / TIME":^20}||{"NOAA SWELL":^18}||{"SG SWELL":^18}||')
        for item in json_data["hours"]:
            arrtime = arrow.get(item["time"])
            time = arrtime.to("local").format("MM/DD/YYYY hh:mm A")
            noaaSwell = item["swellHeight"]["noaa"]*3.281
            sgSwell = item["swellHeight"]["sg"]*3.281
            noaaPer = item["swellPeriod"]["noaa"]
            sgPer = item["swellPeriod"]["sg"]

            #print(f"{time} ||  {noaaSwell:0<4}  |  {noaaWave:0<4}  ||  {sgSwell:0<4}  |  {sgWave:0<4}  ||")
            print(f"{time} ||{noaaSwell:>6.2f}ft @ {noaaPer:<4.2f}s  ||{sgSwell:>6.2f}ft @ {sgPer:<4.2f}s  ||")