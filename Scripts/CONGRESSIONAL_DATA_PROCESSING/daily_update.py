from connect import insert
import json
from init_db import handle_api
from parse import roll_call_parse

def daily_update():

    json_arry= handle_api(Daily= True)
    data= roll_call_parse(json_arry)

    if isinstance(data, pd.DataFrame):
        insert(data)
        print("data updated successfully...")

    elsE:
        print("AN ERROR OCCURRED!")


if __name__ == '__main__':
    daily_update()
