import requests
import datetime
from KeyManager import KeyManager

class WeatherCheck:

    api_key = KeyManager("wc_keys").get_key_rotate()
    URL = "http://api.openweathermap.org/data/2.5/"
    units = "imperial"               # Fahrenheit = imperial / Celcius = metric / Default: Kelvins

    amount = "8"        # Number of forecasts (by 3 hours)

    # Default lat/lon is Half Moon Bay
    # Requires check_type "weather" or "forecast"
    def __init__(self, check_type, lat="37.4435478", lon="-122.4729689", city = "de_City", state = "de_State", zip = "de_Zip", country="US"):

        # if either value passes coordinate boundaries, resets to default
        if float(lat) < -90 or float(lat) > 90 or float(lon) < -180 or float(lon) > 180:
            print("Coordinates out of range, default to Half Moon Bay")
            self.lat = "37.4435478"
            self.lon = "-122.4729689"
        else:
            self.lat = str(lat) # ±90
            self.lon = str(lon) # ±180

        self.city = str(city)
        self.state = str(state)
        self.zip = str(zip) # format check positive num
        self.country = str(country) # defaults to US
        self.json_data, self.link = self.__get_json(check_type)

    # PRIVATE FUNCTIONS
    # private class to get json : returns link and json file
    def __get_json(self, check_type):
        self.check_type = check_type
        website = f"{self.URL}{self.check_type}?"

        # if not default, prioritizes a call with zip, leads with 0 if less than 5 digits
        if self.zip != "de_Zip":
            link = f"{website}&units={self.units}&cnt={self.amount}&zip={self.zip:0>5},{self.country}&appid={self.api_key}"
        # if not default, calls with city
        elif self.city != "de_City":
            # replaces spaces in city names with %20
            self.city = self.city.replace(" ", "%20")
            link = f"{website}&units={self.units}&cnt={self.amount}&q={self.city},{self.state}&appid={self.api_key}"
        # using coords or default lon/lat
        else:
            link = f"{website}&lat={self.lat}&lon={self.lon}&units={self.units}&cnt={self.amount}&appid={self.api_key}"

        response = requests.get(link)
        self.__error_check(response.json())
        return response.json(), link

    # checks error codes and writes into ERROR_LOG with details
    def __error_check(self, data):
        #catches error codes leading with 4 and writes to ERROR_LOG.log
        if (str(data["cod"])[0:1] == "4"):
            f = open("ERROR_LOG.log", "a+")
            f.write(f'{datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")}\n'
                    f'ak={self.api_key} '
                    f'la={self.lat} '
                    f'lo={self.lon} '
                    f'ci={self.city} '
                    f's={self.state} '
                    f'z={self.zip} '
                    f'co={self.country}\n'
                    f'{data["cod"]} {data["message"]}\n\n')
            f.close()
            print(f'ERROR: {data["cod"]}\n{data["message"]}')
            quit()

    # Converts EPOCH/UNIX time to Local Time
    def _get_datetime(self, time):
        # %I instead of %H for 12hrs, %p for AM/PM, converts from epoch to local
        output = datetime.datetime.fromtimestamp(time).strftime('%Y/%m/%d %I:%M %p')
        return output

    # Converts hpa to inMg
    def _get_inMg(self, hpa):
        return hpa * 0.02953

    # Water pressure range for quality of fishing
    def _get_inMg_quality(self, inMg):
        if 29.75 <= inMg <= 30.45:
            quality = "VERY GOOD"
        elif (29.65 <= inMg <= 29.74) or (30.46 <= inMg <= 30.94):
            quality = "GOOD"
        else:
            quality = "POOR"

        return quality

    # SETTERS
    # To set your own key or premium key. To bypass the use of KeyManager
    def set_api_key(self, key):
        self.api_key = key

    # sets the amount to display into API call
    def set_display_amount(self, num):
        self.amount = str(num)

    # sets the unity type to display into API call : imperial, metrics, Kelvins
    def set_units(self, units):
        self.units = units

    # GETTERS
    # get name of location / station : returns a string
    def get_location(self):
        if self.check_type == "weather":
            return self.json_data["name"]
        elif self.check_type == "forecast":
            return self.json_data["city"]["name"]

    # get weather condition : returns string or list of strings
    def get_weather(self):
        if self.check_type == "weather":
            return self.json_data["weather"][0]["main"]
        elif self.check_type == "forecast":
            values = []
            for item in self.json_data["list"]:
                values.append(item["weather"][0]["main"])
            return values

    # get temperature depending on units provided earlier : returns 2float or list of 2floats
    def get_temp(self):
        if self.check_type == "weather":
            return '{:.2f}'.format(self.json_data["main"]["temp"])
        elif self.check_type == "forecast":
            values = []
            for item in self.json_data["list"]:
                values.append('{:.2f}'.format(item["main"]["temp"]))
            return values

    # get pressure in units of inMg : returns 2float or list of 2floats
    def get_inMg(self):
        if self.check_type == "weather":
            return '{:.2f}'.format(self._get_inMg(self.json_data["main"]["pressure"]))
        elif self.check_type == "forecast":
            values = []
            for item in self.json_data["list"]:
                values.append('{:.2f}'.format(self._get_inMg(item["main"]["pressure"])))
            return values

    # get wind speed in mph : returns 2float or list of 2floats
    def get_wind_speed(self):
        if self.check_type == "weather":
            return '{:.2f}'.format(self.json_data["wind"]["speed"])
        elif self.check_type == "forecast":
            values = []
            for item in self.json_data["list"]:
                values.append('{:.2f}'.format(self._get_inMg(item["wind"]["speed"])))
            return values

    # get sunrise in local time AM/PM : returns a string
    def get_sunrise(self):
        if self.check_type == "weather":
            return self._get_datetime(self.json_data["sys"]["sunrise"])
        elif self.check_type == "forecast":
            return self._get_datetime(self.json_data["city"]["sunrise"])

    # get sunset in local time AM/PM : returns a string
    def get_sunset(self):
        if self.check_type == "weather":
            return self._get_datetime(self.json_data["sys"]["sunset"])
        elif self.check_type == "forecast":
            return self._get_datetime(self.json_data["city"]["sunset"])

    # get link of the API call : returns a string
    def get_link(self):
        return self.link

    # PRINTERS
    # prints current weather, location name/weather/temp/wind/pressure/pressure quality
    def checkWeather(self):
        data, link = self.__get_json("weather")
        location = data["name"]
        weather = data["weather"][0]["main"]
        temp = data["main"]["temp"]
        inMg = self._get_inMg(data["main"]["pressure"])
        windSpeed = data["wind"]["speed"]
        print("============================")
        print(f"{location.upper():^28}")
        print("============================")
        print(f"Weather: {weather.upper()} \n"
              f"Temperature: {temp:>5.2f} F°\n"
              f"Wind Speed: {windSpeed:>5.2f} mph\n"
              f"Pressure: {inMg:>5.2f} inMg\n"
              f"Pressure Quality: {self._get_inMg_quality(inMg)}")
        sunrise = data["sys"]["sunrise"]
        sunset = data["sys"]["sunset"]
        print(f"Sunrise: {self._get_datetime(sunrise):>22}")
        print(f"Sunset:  {self._get_datetime(sunset):>22}")
        print(link)

    # prints forecast, location name/date time/temp/wind/weather/pressure/pressure quality
    def checkForecast(self):
        data, link = self.__get_json("forecast")
        location = data["city"]["name"]

        count = 0

        print("============================")
        print(f"{location.upper():^28}")
        print("============================")
        print(f'{"FORECAST":^12}||{"DATE/TIME":^21}||{"TEMP":^11}||{"WIND":^11}||{"WEATHER":^12}||'
              f'{"inMg":^7}||{"QUALITY":^11}')
        print("------------||---------------------||-----------||-----------||------------||-------||-----------")
        for item in data["list"]:
            weather = item["weather"][0]["main"]
            # weather = item["weather"][0]["description"]
            temp = item["main"]["temp"]
            inMg = self._get_inMg(item["main"]["pressure"])
            windSpeed = item["wind"]["speed"]
            dt = item["dt"]

            count += 1
            print("Forecast", "{:>2}".format(str(count)), end=" || ")

            print(self._get_datetime(dt), end=" || ")

            print(f" {temp:>5.2f} F° || {windSpeed:>5.2f} mph || {weather:^10} || {inMg:>5.2f} || {self._get_inMg_quality(inMg)}")
        sunrise = data["city"]["sunrise"]
        sunset = data["city"]["sunset"]
        print(f"Sunrise: {self._get_datetime(sunrise):>22}")
        print(f"Sunset:  {self._get_datetime(sunset):>22}")
        print(link)

