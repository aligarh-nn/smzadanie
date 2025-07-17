import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

TOKEN = config['YANDEX']['OAUTH_TOKEN']
TABLE_ID = config['YANDEX']['TABLE_ID']

def append_row(data):
    url = f"https://api.mds.yandex.net/v1/spreadsheets/{TABLE_ID}/tables/Sheet1/rows"
    headers = {
        "Authorization": f"OAuth {TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json={"values": data}, headers=headers)
    return response.status_code, response.text