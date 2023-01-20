from connect import make_connection
import json
from api import daily_api
from init_db import write_insertions, handle_api

def daily_update():

    json_arry= handle_api(Daily= True)

    if json_arry == None:
        print("no votes occurred today...come back tomorrow and try again :)")
        return

    else:
        make_connection(write_insertions(json_arry))
        print("data updated successfully...")



if __name__ == '__main__':
    daily_update()
