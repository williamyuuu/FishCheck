import arrow
import requests
from KeyManager import KeyManager


class SwellCheck:

    sg_key = KeyManager("sg_keys").get_key_rotate()
    amount = 8
    hour_range = 24
    start = 0
    status = 1                          # Indicates whether an updated json is available

    def __init__(self, lat=37.4435478, lng=-122.4729689, param="swellHeight,swellPeriod"):
        self.lat = lat
        self.lng = lng
        self.param = param

    # PRIVATE FUNCTIONS
    def __get_json(self):
        # Get first hour of today
        start = arrow.now().ceil('hour')

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
        self.json_data = response.json()

    # sets self.start next quarterly hour in UTC
    def __start_point(self):
        json_data = self.json_data

        for item in range(0, 3):
            arrtime = arrow.get(json_data["hours"][item]["time"])
            utc_hour = arrtime.format("HH")

            if (int(utc_hour) % 3 == 0):
                start = item
                self.start = start

    # update status to identify a new json is available after setting new parameters -- for setter functions
    def __set_status(self):
        if self.status != 1:
            self.status = 1

    # checks to see if new json is available and then resets status after getting new json -- for getter functions
    def __check_status(self):
        if self.status == 1:
            self.__get_json()
            self.status = 0

    # SETTERS
    # Set the amount of data that will be given.
    def set_amount(self, amount):
        self.amount = amount
        #Hour range is dynamic, according to the set amount, making sure the range is large enough
        self.hour_range = ((self.amount) * 3) + self.start
        self.__set_status()

    # GETTERS
    # returns array of swell periods by swell type given : returns array meter/seconds
    def get_swell_data(self, swell_type ="noaa", dataType ="swellHeight", pattern = 3):
        self.__check_status()
        json_data = self.json_data
        self.__start_point()
        value = []

        for x in range(self.start, self.hour_range, int(pattern)):
            value.append('{:.2f}'.format(json_data["hours"][x][dataType][swell_type]))

        return value

    # returns array of swell height by swell type given : returns array in units of ft
    def get_swell_height(self, swell_type="noaa", pattern = 3):
        self.__check_status()
        json_data = self.json_data
        self.__start_point()
        value = []

        for x in range(self.start, self.hour_range, int(pattern)):
            value.append('{:.2f}'.format(json_data["hours"][x]["swellHeight"][swell_type] * 3.281))

        return value

    # returns array of swell periods by swell type given : returns array in units of seconds
    def get_swell_period(self, swell_type="noaa", pattern = 3):
        self.__check_status()
        json_data = self.json_data
        self.__start_point()
        value = []

        for x in range(self.start, self.hour_range, int(pattern)):
            value.append('{:.2f}'.format(json_data["hours"][x]["swellPeriod"][swell_type] * 3.281))

        return value

    # PRINTERS
    # prints swells in 3 hour intervals
    def print_swells(self):
        json_data = self.json_data
        self.__start_point()
        print(f'{"DATE / TIME":^20}||{"NOAA SWELL":^19}||{"SG SWELL":^19}||')

        for x in range(self.start, self.hour_range, 3):
            arrtime = arrow.get(json_data["hours"][x]["time"])
            time = arrtime.to("local").format("MM/DD/YYYY hh:mm A")
            noaaSwell = json_data["hours"][x]["swellHeight"]["noaa"] * 3.281
            sgSwell = json_data["hours"][x]["swellHeight"]["sg"] * 3.281
            noaaPer = json_data["hours"][x]["swellPeriod"]["noaa"]
            sgPer = json_data["hours"][x]["swellPeriod"]["sg"]

            # print(f"{time} ||  {noaaSwell:0<4}  |  {noaaWave:0<4}  ||  {sgSwell:0<4}  |  {sgWave:0<4}  ||")
            print(f"{time} ||{noaaSwell:>6.2f}ft @ {noaaPer:>5.2f}s  ||{sgSwell:>6.2f}ft @ {sgPer:>5.2f}s  ||")

    # prints swells in hourly intervals
    def print_hourly_swells(self):
        json_data = self.json_data
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

