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
    sc = SwellCheck()
    print(sc.get_time())

def broken_key():
    wc = WeatherCheck("forecast")
    wc.set_api_key("randomapitkeythatwontwork")
    print(wc.get_link())

if __name__ == "__main__":
    # print_conditions()
    # test()
    broken_key()