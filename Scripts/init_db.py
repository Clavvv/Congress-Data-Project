import os
import glob
from connect import insert_roll_call, make_connection
from api import call_vote_by_date, daily_api, custom_url
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
from parse import roll_call_parse, misconduct_parse, member_info_parse
import pandas as pd

def handle_api(url= None, byMonth= False, Daily= False, y= None, m= None, *args):

    if byMonth:
        pyon= call_vote_by_date(y, m)
        if len(pyon) == 0:
            return None
        return pyon

    elif Daily:

        #this is used by the dailyupdate function to call the propublica api
        #dtype Pyson => Dict
        pyon= daily_api()
        if len(pyon) == 0:
            return None

        return pyon

    else:

        pyon= custom_url(url)

        if len(pyon) == 0:
            return None

        return pyon

        

    


def monthly_schedule():
    #creates generator for each month starting from 2014 and ending on current date
    #to change the earliest database entries change the current date var prior to loop
    #NOTE: changing the starting date may change the api response format and/or quality, verify with propublica docs
    #URL= https://projects.propublica.org/api-docs/congress-api/
    end= date(datetime.today().year, datetime.today().month, 1)
    current= date(2014, 1, 1)
    end+= relativedelta(months=+1)

    while current < end:
        yield current
        current+= relativedelta(months=+ 1)

def fetch_misconduct():
    url= 'https://raw.githubusercontent.com/govtrack/misconduct/master/misconduct-instances.csv'
    raw_df= pd.read_csv(url, index_col=0)
    

    return misconduct_parse(raw_df).to_csv('congressional_misconduct.csv')






def build_db():

    #assembles the database by making calls to the api using the insert() function
    #parsing from json to tabular format done with pandas
    f= "%Y-%m"
    for each in monthly_schedule():
        yr, mth= datetime.strftime(each, f).split('-')
        data= roll_call_parse(handle_api(yr, mth, byMonth= True))

        if isinstance(data, pd.DataFrame):
            insert_roll_call(data)

    


    
    return

def build_member_info():
    curr_cong= make_connection('SELECT congress from house_roll_call order by date desc limit 1;')[0][0]


    url= 'https://api.propublica.org/congress/v1/117/house/members.json'


    for cong in range(113, curr_cong+1):
        api_url= f'https://api.propublica.org/congress/v1/{cong}/house/members.json'

        data= pd.DataFrame(handle_api(url= api_url)['results'][0]['members'])







if __name__ == '__main__':

    build_member_info()



