from WeatherCheck import WeatherCheck
from SwellCheck import SwellCheck
import arrow


def print_conditions():
    wc = WeatherCheck()
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



if __name__ == "__main__":
    print_conditions()