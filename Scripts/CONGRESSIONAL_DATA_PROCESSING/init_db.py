from connect import insert
from api import call_vote_by_date
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
from api import daily_api
from parse import roll_call_parse
import pandas as pd

def handle_api(y= None, m= None, byMonth= False, Daily= False, *args):

    if byMonth:
        pyson= call_vote_by_date(y, m)
        if len(pyson) == 0:
            return None
        return pyson

    elif Daily:

        pyson= daily_api()
        if len(pyson) == 0:
            return None

        return pyson

def monthly_schedule():
    end= date(datetime.today().year, datetime.today().month, 1)
    current= date(2014, 1, 1)
    end+= relativedelta(months=+1)

    while current < end:
        yield current
        current+= relativedelta(months=+ 1)


def build_db():

    f= "%Y-%m"
    for each in monthly_schedule():
        yr, mth= datetime.strftime(each, f).split('-')
        data= roll_call_parse(handle_api(yr, mth, byMonth= True))

        if isinstance(data, pd.DataFrame):
            insert(data)







if __name__ == '__main__':
    build_db()

