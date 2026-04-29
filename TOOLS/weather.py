import argparse as ap
import requests
import rich

apikey = "" # put api key here if you want weather
url  = "https://api.worldweatheronline.com/premium/v1/weather.ashx"

parser = ap.ArgumentParser(description='get the weather for an area')
parser.add_argument('--prompt')
args = parser.parse_args()
prompt = args.prompt

prompt = prompt.split(' in ')[1]
print(prompt)

def get_weather(location):
    params = {
        "key":apikey,
        "q":location,
        "format": "json",
        "includelocation":"yes",
        "cc":"yes",
        
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["data"]
weather = get_weather(f"{prompt}")
print(weather["current_condition"][0]["temp_F"], "F")
