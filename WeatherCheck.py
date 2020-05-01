import requests
import datetime
from KeyManager import KeyManager
#yo

class WeatherCheck:

    api_key = KeyManager().get_key_rotate()
    URL = "http://api.openweathermap.org/data/2.5/"
    units = "imperial"               # Fahrenheit = imperial / Celcius = metric / Default: Kelvins

    amount = "8"        # Number of forecasts (by 3 hours)

    def __init__(self, lat="37.4435478", lon="-122.4729689"): #Half Moon Bay
        self.lat = lat
        self.lon = lon

    def __get_json(self, check_type):
        self.check_type = check_type
        response = requests.get(f"{self.URL}{self.check_type}?lat={self.lat}&lon={self.lon}&units={self.units}"
                                f"&cnt={self.amount}&appid={self.api_key}")
        return response.json()

    def _get_datetime(self, time):
        # %I instead of %H for 12hrs, %p for AM/PM, converts from epoch to local
        output = datetime.datetime.fromtimestamp(time).strftime('%Y/%m/%d %I:%M %p')
        return output


    #To set your own key or premium key. To bypass the use of KeyManager
    def set_api_key(self, key):
        self.api_key = key

    def set_display_amount(self, num):
        self.amount = num

    def set_units(self, units = "imperial"):
        self.units = units

    # check current weather,temp,location, pressure, wind speed for Half Moon Bay
    def checkWeather(self):
        data = self.__get_json("weather")

        location = data["name"]
        weather = data["weather"][0]["main"]
        temp = data["main"]["temp"]
        pressure = data["main"]["pressure"]
        windSpeed = data["wind"]["speed"]
        print(f"Condition for {location.upper()}:\n|-"
              f"Weather: {weather.upper()} \n|-"
              f"Temperature: {temp} F°\n|-"
              f"Wind Speed: {windSpeed} mph\n")
        print(f"{self.URL}weather?lat={self.lat}&lon={self.lon}&units={self.units}&appid={self.api_key}")

    # check forecast for Half Moon Bay
    def checkForecast(self):
        data = self.__get_json("forecast")

        location = data["city"]["name"]

        count = 0

        print("============================")
        print(f"    {location.upper()}")
        print("============================")

        for item in data["list"]:
            weather = item["weather"][0]["main"]
            temp = item["main"]["temp"]
            pressure = item["main"]["pressure"]
            windSpeed = item["wind"]["speed"]
            dt = item["dt"]

            count += 1
            print("Forecast", "{:>2}".format(str(count)), end=" || ")

            print(self._get_datetime(dt), end=" || ")

            print(f" {temp:0<5} F° || {windSpeed:>5} mph || {weather:^8} || {pressure} ||")
        sunrise = data["city"]["sunrise"]
        sunset = data["city"]["sunset"]
        print(f"Sunrise: {self._get_datetime(sunrise):>22}")
        print(f"Sunset:  {self._get_datetime(sunset):>22}")
        print(f"{self.URL}forecast?lat={self.lat}&lon={self.lon}&units={self.units}&cnt={self.amount}&appid={self.api_key}")

