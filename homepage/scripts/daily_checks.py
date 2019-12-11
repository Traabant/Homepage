from check_event import CheckEents
from getWeather import GetWeather
from radarData import radarData

# This script is run once a day by scheduler


# downloads and checks for new events on kindergarden website 
CheckEents()

# download Data for weatehr and pollution
weather = GetWeather()
weather.get_weather()
weather.get_pollution()

# Downloads ands saves radar images from yesterday 
radarData().yesterdays_radar_data()
