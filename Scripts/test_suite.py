from connect import make_connection
from datetime import datetime, date


def validate_daily_entry():

    today= datetime.today().date()

    if make_connection('SELECT date from house_roll_call order by date desc limit 1;')[0][0] == today:
        return True

    else:
        return False


if __name__ == '__main__':
    validate_daily_entry()