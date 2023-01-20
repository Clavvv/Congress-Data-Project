from connect import make_connection
from api import call_vote_by_date
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
from api import daily_api

def handle_api(y= None, m= None, byMonth= False, Daily= False, *args):

    if byMonth:
        pyson= call_vote_by_date(y, m)
        return pyson

    elif Daily:

        pyson= daily_api()
        if len(pyson) == 0:
            return None
        return pyson



def write_insertions(json_arry):

    commands= []
    for i, item in enumerate(json_arry):
        x= json.dumps(item)
        x= x.replace("'", "''")
        command= f"""INSERT INTO raw_data VALUES ({i}, '{x}');"""
        commands.append(command)

    return commands

def monthly_schedule():
    end= date(datetime.today().year, datetime.today().month, 1)
    current= date(2014, 1, 1)
    end+= relativedelta(months=+1)

    while current < end:
        yield current
        current+= relativedelta(months=+ 1)



def build_db():

    create_table= f"""CREATE TABLE IF NOT EXISTS raw_data (
            id integer NOT NULL,
            data jsonb
            );"""

    queries= [create_table]

    f= "%Y-%m"
    for each in monthly_schedule():
        yr, mth= datetime.strftime(each, f).split('-')
        sql_statement= write_insertions(handle_api(yr, mth, byMonth= True))
        queries.extend(sql_statement)

    return queries





if __name__ == '__main__':
    make_connection(build_db())

