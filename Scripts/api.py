import requests as req
import os
import json
from psycopg2.extras import Json
from psycopg2.extensions import register_adapter
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_api_key():
    '''
    locates, reads and parses the api key for ProPublica Congressional Data API from a .ini file 

    Returns
    -------
    str
        api key for the ProPublica Congressional Data API

    See Also
    --------
    handle_api : arbitrator for api calls
    call_vote_by_date : fetches congressional roll call data on a monthly time scale and is used to initiate database
    daily_api : fetches today's congressional roll call vote data via the ProPublica api
    '''

    key_path= str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+("\API.ini")
    with open(key_path) as file:
        file= file.read().strip('\n')
        api_key= file.split(': ')[1]

    return api_key



def call_vote_by_date(year, month):
    '''
    calls the ProPublica roll call api and returns a Python dictionary of all roll call votes occurring in a particular month as specified by
    the year and month parameters. 

    Parameters
    ----------
    year : str
        Year parameter to specify timeframe in API call

    month : str
        Month parameter to specify timeframe in API call

    Returns
    -------
    dict
        reformatted json of a single month's roll call data

    See Also
    --------
    handle_api : arbitrator for api calls
    daily_api : fetches today's congressional roll call vote data via the ProPublica api
    monthly_schedule : generator for dates on monthly basis for api call starting in 2013 ending on current date
    roll_call_parse : formats Json reposnse from api response and returns a Pandas DataFrame
    build_db : assembles the database by orchestrating API calls, parsing functions and establishing database connection
    get_api_key : fetches api key from .ini folder, used by all functions accessing the ProPublica API
    ProPublica API Documentation : https://projects.propublica.org/api-docs/congress-api/
    '''

    api_key= get_api_key()

    url= f"https://api.propublica.org/congress/v1/house/votes/{year}/{month}.json"

    api_head= {'X-API-Key': api_key}

    response= req.get(url, headers= api_head)
    r_json= response.json()
    parsed_json= r_json['results']['votes']

    return parsed_json

def daily_api():
    '''
    Fetches today's congressional roll call vote data via the ProPublica api
        and must be used in conjunction with a scheduler/orchestrator in order to run on a daily-basis.
        If no roll call votes occurred today, function returns dtype: None

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A json formatted Python dictionary containing data of today's roll call votes

        None 
            When no votes occurred today

        See Also
        --------
        call_vote_by_date : fetches congressional roll call data on a monthly time scale and is used to initiate database
        handle_api : arbitrator for api calls
        roll_call_parse : formats Json reposnse from api response and returns a Pandas DataFrame
        get_api_key : fetches api key from .ini folder, used by all functions accessing the ProPublica API
        ProPublica API Documentation : https://projects.propublica.org/api-docs/congress-api/
        '''

    api_key= get_api_key()
    today= datetime.today()
    strf_today= today.strftime("%Y-%m-%d")


    url= f"https://api.propublica.org/congress/v1/house/votes/{strf_today}/{strf_today}.json"
    api_head= {'X-API-Key': api_key}

    response= req.get(url, headers= api_head)
    r_json= response.json()
    parsed_json= r_json['results']['votes']

    return parsed_json


if __name__ == '__main__':
    test_dates= ['2014', '02']
    call_vote_by_date(*test_dates)
