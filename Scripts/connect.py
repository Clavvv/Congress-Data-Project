import os
import psycopg2
from psycopg2.extras import execute_values
from config import config
import io
import geopandas as gpd
import pandas as pd
import csv
from sqlalchemy import create_engine, text
from sqlalchemy.types import BigInteger, Text, Boolean, Float

def make_connection(query, default_path= None):
    conn= None
    response= None

    try:
        
        if not default_path:
            params= config(filename= str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+("\CD_Database.ini"))

        else:
           params= config(str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+("\GIS_DB.ini"))



        #print('CONNECTING TO THE POSTGRESQL DATABASE...')
        conn= psycopg2.connect(**params)

        cursor= conn.cursor()

        #print('PostgreSQL database version:')

        cursor.execute('SELECT version()')
        db_version= cursor.fetchone()
        #print(db_version)



        cursor.execute(query)
        response= cursor.fetchall()




        cursor.close()
        conn.commit()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn != None:
            conn.close()
            print('DATABSE CONNECTION CLOSED.')

    return response

def insert_member_info(dataframe):
    engine = None
    try:
        params = config()
        print('CONNECTING TO THE POSTGRESQL DATABASE...')
        engine = create_engine(f"postgresql://{params['user']}:{params['password']}@{params['host']}:5432/{params['database']}")
        
        conn= engine.connect()
        result= conn.execute(text('select version();'))
        print(result.fetchone())
        
        table_name = 'member_info'
        
        column_types = {
            'int64': BigInteger,
            'float64': Float(precision=53),
            'object': Text,
            'bool': Boolean
        }
        column_definitions = {column: column_types[str(dtype)] for column, dtype in dataframe.dtypes.items()}
        
        dataframe.to_sql(table_name, engine, if_exists='append', index=False, dtype=column_definitions, chunksize=1000)
        
        print('DATA INSERTED SUCCESSFULLY INTO POSTGRESQL DATABASE')
    except Exception as error:
        print(f'ERROR: {error}')
    finally:
        if engine is not None:
            engine.dispose()
            print('DATABASE CONNECTION CLOSED.')

    return None


'''def insert_member_info(dataframe):

    conn= None

    try:
        params= config()

        print('CONNECTING TO THE POSTGRESQL DATABASE...')
        conn= psycopg2.connect(**params)

        cursor= conn.cursor()

        print('PostgreSQL database version:')

        cursor.execute('SELECT version()')
        db_version= cursor.fetchone()
        print(db_version)

        table_name= 'member_info'

        columns= list(dataframe.columns)
        dtypes= [f"bigint" if dt == 'int64'  else
                     'double precision' if dt == 'float64' else
                      'text' if dt == 'object' else
                       'boolean' if dt == 'bool' else
                        dt for dt in dataframe.dtypes]

        print(columns, ' IS THE LIST OF COLUMNS')
        print(dtypes, ' IS THE LIST OF DATA TYPES')
        input()

        create_table_query= f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join([f"{c} {dt}" for c, dt in zip(columns, dtypes)])});'

        cursor.execute(create_table_query)

        vals= [tuple(x) for x in dataframe.to_records(index=False)]

        execute_values(cursor, f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s", vals)

        conn.commit()
        cursor.close()

    

    except(Exception, psycopg2.DatabaseError) as error:
        print(f'ERORR: {error}')

    finally:
        if conn != None:
            conn.close()
            print('DATABSE CONNECTION CLOSED.')

    return None'''

def insert_roll_call(dataframe):
    
    conn= None

    try:
        params= config()

        print('CONNECTING TO THE POSTGRESQL DATABASE...')
        conn= psycopg2.connect(**params)

        cursor= conn.cursor()

        print('PostgreSQL database version:')

        cursor.execute('SELECT version()')
        db_version= cursor.fetchone()
        print(db_version)

        cursor.execute("""CREATE TABLE IF NOT EXISTS house_roll_call (
                            congress smallint,
                            chamber text,
                            session smallint,
                            roll_call smallint,
                            source text,
                            vote_uri text,
                            question text,
                            description text,
                            vote_type text,
                            date date,
                            time time,
                            result text,
                            bill_id text,
                            number text,
                            sponsor_id text,
                            api_url text,
                            title text,
                            latest_action text);""")

        columns= dataframe.columns

        rows= dataframe.values

        string_buffer= io.StringIO()

        dataframe.to_csv(string_buffer, sep='\t', header=False, index=False)

        string_buffer.seek(0)

        data= string_buffer.getvalue()

        cursor.copy_from(string_buffer, 'house_roll_call', null='')

        conn.commit()
        cursor.close()

    

    except(Exception, psycopg2.DatabaseError) as error:
        print('ERORR')

    finally:
        if conn != None:
            conn.close()
            print('DATABSE CONNECTION CLOSED.')

    return None


if __name__ == '__main__':
    insert_roll_call(None, None)
