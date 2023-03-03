from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from connect import make_connection
import os


def match_dates():
    #will create key:value pairs for each table so that I can match the corresponding county table to the congressional district tables
    #before I perform a spatial join within POSTGIS

    kv= {}

    def get_gis_tables():
        
        #returns all public schema table names in the database

        #specifies the config filepath for the connection function
        config_path= str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+("\GIS_DB.ini")

        #the query
        metaquery= """SELECT table_schema, table_name FROM information_schema.tables
                        where table_schema = 'public' order by table_name;"""

        #query returned as list of tuples
        res= make_connection(query= metaquery, default_path= config_path)

        #slicing the query to get rid of default PostGIS geometry and spatial tables
        return res[:-3]


    def make_dates():
        #creates an iterator that gives the start/end date for each congress 
        #eg. 2013-01-03 begins Congress 111 2015-01-03 begins congress 112 AND ends congress 111
        end_date= date(datetime.today().year, datetime.today().month, datetime.today().day) 
        current_date= date(2009, 1, 3)

        while current_date < end_date:
            yield current_date
            current_date+= relativedelta(years=+ 2)

    
    tables= get_gis_tables()

    for each in make_dates():



    





    return None


if __name__ == '__main__':
    match_dates()
