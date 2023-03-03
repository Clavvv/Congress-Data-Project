from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from connect import make_connection
import os


def match_dates():
    #two sessions per congress, starting on jan 3 ending on jan 3 the following year
    # eg.) 111th -> Jan 6, 2009 -> session 1 end [dec 23, 2009] -> congress end [dec 22 2010] 112 start [jan 5 2011]

    kv= {}

    def get_gis_tables():
        config_path= str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+("\GIS_DB.ini")

        metaquery= """select table_name from information_scheme.tables
                        where table_scheme = 'public'"""



        res= make_connection(query= [metaquery], gis=1, confpath= config_path)

        input()
        for each in res:
            print(res)
            input()


    get_gis_tables()



        


    def make_dates():
        end_date= date(datetime.today().year, datetime.today().month, datetime.today().day) 
        current_date= date(2009, 1, 3)

        while current_date < end_date:
            yield current_date
            current_date+= relativedelta(years=+ 2)

    





    return None


if __name__ == '__main__':
    match_dates()
