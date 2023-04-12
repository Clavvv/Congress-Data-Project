import os
import glob
from connect import insert_roll_call
from api import call_vote_by_date
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
from api import daily_api
from parse import roll_call_parse, misconduct_parse
import pandas as pd

def handle_api(y= None, m= None, byMonth= False, Daily= False, *args):


    #specifies whether api will access data for 30day/monthly increments or daily
    if byMonth:
        pyson= call_vote_by_date(y, m)
        if len(pyson) == 0:
            return None
        return pyson

    elif Daily:

        #this is used by the dailyupdate function to call the propublica api
        #dtype Pyson => Dict
        pyson= daily_api()
        if len(pyson) == 0:
            return None

        return pyson

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


if __name__ == '__main__':
    build_db()


