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
        cd_query= r"""SELECT table_name FROM information_schema.tables
                        where table_schema = 'public' and table_name like '%cd%' order by table_name;"""
        
        county_query= r"""select table_name from information_schema.tables
                            where table_schema = 'public' and table_name like '%county%' order by table_name;"""


        #query returned as list of tuples
        res= [make_connection(query= cd_query, default_path= config_path), make_connection(query= county_query, default_path= config_path)]

        #slicing the query to get rid of default PostGIS geometry and spatial tables
        return res


    #matches the correct congress to the correct county data shapefiles
    #gets all tables from GIS database
    tables= get_gis_tables()
    #splits the list into congressional districts (cd) and counties (queue)
    queue= tables[1][1:]
    cd= tables[0][1:]

    #matches them, if you were to look this up it would appear wrong. Congress 111 ran from 2009 - 2011 however, it ended on Jan 03 2011 so yearly 2011 data should not be counted
    for district in cd:
        kv[district[0]]= [queue[0][0], queue[1][0]]
        queue.pop(0)
        queue.pop(0)


    print(kv)
















if __name__ == '__main__':
    match_dates()
