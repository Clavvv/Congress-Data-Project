from connect import export_to_database
import pandas as pd
import json
from init_db import handle_api
from parse import roll_call_parse
from datetime import datetime
from test_suite import validate_daily_entry

def daily_update():

    #array of nested json returned from api
    #data is unnested and formatted to be uploaded to database
    #when function is run (everyday around 9:00pm PST via Windows Task Scheduler) log.txt updates with a status code and the current date
    #NOTE: if the log.txt is not updating make sure that your windows task scheduler is running the task from this directory, defualt directory 
    #is Sys32 or wherever the scheduler is located
    json_arry= handle_api(Daily= True)
    data= roll_call_parse(json_arry)
    now= datetime.today()

    if isinstance(data, pd.DataFrame):

        export_to_database('house_roll_call' , data)

        if validate_daily_entry(): 

            with open('log.txt', 'a') as file:
                file.write(f'Status: 200 Data Retrieved and Ingested Successfully => {now.strftime(r"%Y-%m-%d")}\n')

        else:

            with open('log.txt', 'a') as file:
                file.write(f'Status: 500 Data Retrieved but Not Ingested to Database => {now.strftime(r"%Y-%m-%d")}\n')


    #conditional to catch None type responses from api
    #Occurs when there are no new roll call votes for that day in congress
    else:
        with open('log.txt', 'a') as file:
            file.write(f'Status: 204 => No New Data to Process {now.strftime(r"%Y-%m-%d")}\n')

if __name__ == "__main__":
    daily_update()
