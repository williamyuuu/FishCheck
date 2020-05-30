from WeatherCheck import WeatherCheck
from SwellCheck import SwellCheck


if __name__ == "__main__":
    wc = WeatherCheck()
    sc = SwellCheck()

    wc.set_display_amount(3)
    wc.checkForecast()
    sc.set_amount(3)
    sc.print_swells()