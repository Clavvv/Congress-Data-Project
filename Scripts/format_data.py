import json
from api import daily_api
from connect import make_connection
from init_db import write_insertions, handle_api
import pandas as pd
import numpy as np


def parse(json_arr):
    nan= np.nan
    rows= []
    bills= []

    for j in json_arr:
        bills.append(j['bill'])
        del j['bill']
        rows.append(j)


    df= pd.DataFrame.from_dict(rows, orient='columns')
    df2=pd.DataFrame.from_dict(bills, orient='columns')
    final= pd.merge(df, df2, left_index=True, right_index=True)
    final.drop(['republican', 'independent', 'democratic'], axis=1, inplace=True)

    return





    return None









if __name__ == "__main__":
    r= handle_api(byMonth= True, y='2023', m='01')
    parse(r)

