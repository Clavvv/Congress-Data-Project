import os
import psycopg2
from psycopg2.extras import execute_values
from config import config
import io
import geopandas as gpd
import pandas as pd
import csv
from sqlalchemy import create_engine, text, URL
from sqlalchemy.types import BigInteger, Text, Boolean, Float


def export_to_database(table_name, dataframe):

    try:
        params= config()
        url_obj= URL.create(
            "postgresql+psycopg2",
            username= params['user'],
            password= params['password'],
            host= params['host'],
            database= params['database'],
        )

        engine= create_engine(url_obj)

        dataframe.to_sql(table_name, engine, if_exists='append', index=False)
        print('Success')

    except(Exception, psycopg2.DatabaseError) as error:
        print('ERORR:', error)

    return None


def query(q, default_path=None):
    conn= None
    response= None

    try:
        if not default_path:
            params= config(filename=str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + ("\database.ini"))
        else:
            params= config(str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + ("\GIS_DB.ini"))

        conn= psycopg2.connect(**params)
        cursor= conn.cursor()

        if q.upper().startswith('SELECT'):
            cursor.execute(q)
            response= cursor.fetchall()
        else:
            cursor.execute(q)
            conn.commit()

        cursor.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('DATABASE CONNECTION CLOSED.')

    return response