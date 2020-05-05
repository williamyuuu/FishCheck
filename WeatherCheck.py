import requests
import datetime
from KeyManager import KeyManager

class WeatherCheck:

    api_key = KeyManager().get_key_rotate()
    URL = "http://api.openweathermap.org/data/2.5/"
    units = "imperial"               # Fahrenheit = imperial / Celcius = metric / Default: Kelvins

    amount = "8"        # Number of forecasts (by 3 hours)

    def __init__(self, lat="37.4435478", lon="-122.4729689", city= None, state= None, zip= None, country="US"): #Half Moon Bay

        self.lat = str(lat) # ±90
        self.lon = str(lon) # ±180
        self.city = str(city)
        self.state = str(state)
        self.zip = str(zip) # format check positive num
        self.country = str(country) # defaults to US

    def __get_json(self, check_type):
        self.check_type = check_type
        response = requests.get(f"{self.URL}{self.check_type}?lat={self.lat}&lon={self.lon}&units={self.units}"
                                f"&cnt={self.amount}&appid={self.api_key}")
        return response.json()

    def __error_check(self, data):
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
            quit()


    def _get_datetime(self, time):
        # %I instead of %H for 12hrs, %p for AM/PM, converts from epoch to local
        output = datetime.datetime.fromtimestamp(time).strftime('%Y/%m/%d %I:%M %p')
        return output

    def _get_inMg(self, hpa):
         return hpa * 0.02953

    def _get_inMg_quality(self, inMg):
        if 29.75 <= inMg <= 30.45:
            quality = "VERY GOOD"
        elif (29.65 <= inMg <= 29.74) or (30.46 <= inMg <= 30.94):
            quality = "GOOD"
        else:
            quality = "POOR"

        return quality

    #To set your own key or premium key. To bypass the use of KeyManager
    def set_api_key(self, key):
        self.api_key = key

    def set_display_amount(self, num):
        self.amount = str(num)

    def set_units(self, units):
        self.units = units

    # check current weather,temp,location, pressure, wind speed for Half Moon Bay
    def checkWeather(self):
        data = self.__get_json("weather")
        self.__error_check(data)
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
        print(f"{self.URL}weather?lat={self.lat}&lon={self.lon}&units={self.units}&appid={self.api_key}")
        # print(self.zip)
        # print(self.city)
        # print(self.state)

    # check forecast for Half Moon Bay
    def checkForecast(self):
        data = self.__get_json("forecast")
        self.__error_check(data)
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
        print(f"{self.URL}forecast?lat={self.lat}&lon={self.lon}&units={self.units}&cnt={self.amount}&appid={self.api_key}")

