from connect import insert
import pandas as pd
import json
from init_db import handle_api
from parse import roll_call_parse
from datetime import datetime

def daily_update():

    json_arry= handle_api(Daily= True)
    data= roll_call_parse(json_arry)
    now= datetime.now()

    if isinstance(data, pd.DataFrame):
        insert(data)

        with open('log.txt', 'w') as file:
            file.write(f'Status: 200 => {now.strftime("%Y%M%D")}\n')

    else:
        with open('log.txt', 'w') as file:
            file.write(f'Status: 204 => {now.strftime("%Y%M%D")}\n')


if __name__ == '__main__':
    daily_update()
