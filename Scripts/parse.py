import json
import numpy as np
import pandas as pd


def roll_call_parse(json_arr):

    if json_arr == None:
        return None

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
    final.drop(['republican', 'independent', 'democratic', 'total', 'url', 'question_text'], axis=1, inplace=True)

    return final


if __name__ == "__main__":
    roll_call_parse()

