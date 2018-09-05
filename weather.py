import json
import requests
import os
import time
# from slackclient import SlackClient
from slacker import Slacker

def get_token():
    file_dir = os.path.dirname(__file__)
    token_path = os.path.join(file_dir, '../weather-slack-bot/slack.json')
    with open(token_path, 'r') as fp:
        token = json.load(fp)['token']
        return token

sc = Slacker(get_token())

def slack_get():
    r = sc.channels.history('CC7HD3TS5',count=1)
    r_text = r.body['messages'][0]['text']
    return r_text

def get_weather(cityname):
    return requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid=78df9f2f039e30df1a3ecc3b9591e231&units=metric')

data = get_weather(slack_get())
weather_data = json.loads(data.text)
print(weather_data)

def data_do():
    w_list = weather_data['weather'][0]['description']
    w_name = weather_data['name']
    w_main = weather_data['main']
    name = '查詢地點:' + ' ' + w_name + '\n'
    temp = '\n現在溫度:' + ' ' + str(round(w_main['temp'])) + '度' + '，' + w_list
    result = name + temp 
    return result


def slack_post():
    sc.chat.post_message('#general', data_do())

with open('weather_data.json', 'w') as file:
    json.dump(weather_data, file, indent=10)
    file.close()


slack_post()
