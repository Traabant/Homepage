from scripts.getWeather import GetWeather

# This script is run every our by scheduler

# downloads ands saves pollution
GetWeather().get_pollution()

