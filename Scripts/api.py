import requests as req
import os
import json
from psycopg2.extras import Json
from psycopg2.extensions import register_adapter
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_api_key():

    key_path= str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+("\API.ini")
    with open(key_path) as file:
        file= file.read().strip('\n')
        api_key= file.split(': ')[1]

    return api_key



def call_vote_by_date(year, month):

    api_key= get_api_key()

    url= f"https://api.propublica.org/congress/v1/house/votes/{year}/{month}.json"

    api_head= {'X-API-Key': api_key}

    response= req.get(url, headers= api_head)
    r_json= response.json()
    parsed_json= r_json['results']['votes']

    return parsed_json

def daily_api():
    #retrieves API key from API.ini and then calls api to retrieve today's roll call votes
    #returns json parsed as python dictionary dtype

    api_key= get_api_key()
    today= datetime.today()
    strf_today= today.strftime("%Y-%m-%d")


    url= f"https://api.propublica.org/congress/v1/house/votes/{strf_today}/{strf_today}.json"
    api_head= {'X-API-Key': api_key}

    response= req.get(url, headers= api_head)
    r_json= response.json()
    parsed_json= r_json['results']['votes']

    return parsed_json

def get_bill_data():

    api_key= get_api_key()

    return parse_json


if __name__ == '__main__':

    test_dates= ['2014', '02']
    #call_vote_by_date(*test_dates)
