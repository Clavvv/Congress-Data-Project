from connect import query
from datetime import datetime, date
from api import custom_url


def validate_daily_entry():

    today= datetime.today().date()


    try:
        if query('SELECT date from house_roll_call order by date desc limit 1;')[0][0] == today:
            return True

        else:
            return False

    except:

        return False

def testApiResponse():


    edge1= '2023-01-06'

    date= '2023-05-10'
    testing_url= f'https://api.propublica.org/congress/v1/house/votes/{date}/{date}.json'
    
    res= custom_url(testing_url)

    whitelist= ['congress', 'chamber', 'session', 'roll_call', 'source', 'vote_uri', 'question', 
                'description', 'vote_type', 'date', 'time', 'result', 'bill', 'sponsor_id',
                'api_url', 'title', 'latest_action']


    #   x= {k:v for key, value in zip(arr1, arr2}

    json_arr= res['results']['votes']

    formattedJson= {}


    for json in json_arr:

        for key in whitelist:

            if key == 'bill':

                formattedJson[key]= json['bill'][key]

            else:
                formattedJson[key]= json[key]



        print(formattedJson)

        input()




if __name__ == '__main__':
    testApiResponse()