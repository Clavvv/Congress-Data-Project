from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from connect import make_connection


def match_dates():
    #two sessions per congress, starting on jan 3 ending on jan 3 the following year
    # eg.) 111th -> Jan 6, 2009 -> session 1 end [dec 23, 2009] -> congress end [dec 22 2010] 112 start [jan 5 2011]

    kv= {}


    def make_dates():
        end_date= date(datetime.today().year, datetime.today().month, datetime.today().day) 
        current_date= date(2013, 1, 3)

        while current_date < end_date:
            yield current_date
            current_date+= relativedelta(years=+ 2)



    





    return None


if __name__ == '__main__':
    match_dates()
