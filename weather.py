import json
import requests
import os
from slackclient import SlackClient

def get_token():
    file_dir = os.path.dirname(__file__)
    token_path = os.path.join(file_dir, '../weather-slack-bot/slack.json')
    with open(token_path, 'r') as fp:
        token = json.load(fp)['token']
        return token

def get_weather(cityname):
    return requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid=78df9f2f039e30df1a3ecc3b9591e231&units=metric').json()

weather_data = get_weather('Taipei')
data = json.dumps(weather_data)

def data_do():
    w_list = weather_data.get('weather')
    w_name = weather_data.get('name')
    w_main = weather_data.get('main')
    name = '查詢地點:' + w_name + '\n'
    temp = '\n現在溫度:' + str(round(w_main['temp'])) + '度'
    
    result = name + temp
    print(type(w_list))
    return result
data_do()


def slack():
    slack_token = get_token()
    param = {
        'token': slack_token,
        'channel': '#general',
        'text': data_do(),
    }   
    r = requests.get('https://slack.com/api/chat.postMessage', params=param)

# slack()


with open('weather_data.json', 'w') as file:
    json.dump(weather_data, file, indent=10)
    file.close()
