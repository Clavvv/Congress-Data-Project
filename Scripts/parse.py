import json
import numpy as np
import pandas as pd


def roll_call_parse(json_arr):

    if json_arr == None:
        return None

    nan= np.nan
    rows= []
    bills= []

    #unnesting the json and saving the bill information to row
    for j in json_arr:
        bills.append(j['bill'])
        del j['bill']
        rows.append(j)


    #adding the data from the lists into the dataframe 
    vote_data= pd.DataFrame.from_dict(rows, orient='columns')
    bill_data=pd.DataFrame.from_dict(bills, orient='columns')

    #combining the data from the inner json to the rest of the data 

    combined_data= pd.merge(vote_data, bill_data, left_index=True, right_index=True)

    #dropping collumns I don't care about
    if 'ammendment' in combined_data.columns:
        combined_data.drop(['republican', 'independent', 'democratic', 'total', 'url', 'question_text', 'amendment'], axis=1, inplace=True)

    else:
        combined_data.drop(['republican', 'independent', 'democratic', 'total', 'url', 'question_text'], axis=1, inplace=True)

    return combined_data

def misconduct_parse(dataframe):
    df= dataframe.replace('X', 1)
    df= df.fillna(0)
    return df

def member_info_parse(raw_json):


    members_dataframe= pd.DataFrame(raw_json['results'][0]['members'])

    print(members_dataframe.head(3))


    return None


if __name__ == "__main__":
    member_info_parse()

