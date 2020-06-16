from WeatherCheck import WeatherCheck
from SwellCheck import SwellCheck
import arrow


def print_conditions():
    wc = WeatherCheck("forecast")
    sc = SwellCheck()

    wc.set_display_amount(3)
    sc.set_amount(5)

    source = "sg"
    interval = 3

    # noaa or sg
    height = sc.get_swell_data(source, "swellHeight", interval)
    period = sc.get_swell_data(source, "swellPeriod", interval)

    for x in range(len(height)):
        print(height[x],"ft @",period[x],"s")

def test():
    wc = WeatherCheck("forecast")
    wc.set_display_amount(8)
    print(wc.get_wind_speed())
    print(wc.get_location())
    wc.set_units("metrics")
    print(wc.get_wind_speed())
    wc.set_units("imperial")
    print(wc.get_wind_speed())

def broken_key():
    wc = WeatherCheck("forecast")
    wc.set_api_key("randomapitkeythatwontwork")
    wc.set_new_data()
    print(wc.get_link())

if __name__ == "__main__":
    # print_conditions()
    test()
    # broken_key()