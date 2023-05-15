from connect import query, export_to_database
from datetime import datetime, date
from api import custom_url
from parse import roll_call_parse


def validate_daily_entry():

    today= datetime.today().date()


    try:
        if query('SELECT date from house_roll_call order by date desc limit 1;')[0][0] == today:
            return True

        else:
            return False

    except:

        return False


def repair_database():

    today= datetime.today().date()
    strf_today= today.strftime("%Y-%m-%d")
    last_successful_ingestion= query('SELECT date from house_roll_call order by date desc limit 1;')[0][0].strftime("%Y-%m-%d")

    url= f"https://api.propublica.org/congress/v1/house/votes/{last_successful_ingestion}/{strf_today}.json"

    missing_data_json_array= custom_url(url)['results']['votes']

    export_to_database('house_roll_call', roll_call_parse(missing_data_json_array))




if __name__ == '__main__':
    repair_database()