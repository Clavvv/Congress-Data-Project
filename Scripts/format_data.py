import json
from api import daily_api
from connect import make_connection
from init_db import write_insertions, handle_api
import pandas as pd
import numpy as np


def parse(json_arr):
    nan= np.nan
    rows= []

    for j in json_arr:
        rows.append(j)

    df= pd.DataFrame.from_dict(rows, converters={'bill':parse()}, orient='columns')





    return





    return None









if __name__ == "__main__":
    r= handle_api(Daily= True)
    parse(r)

