import os
import psycopg2
from config import config
import io
import pandas as pd
import csv

def make_connection(query= []):
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


        for item in query:
            cursor.execute(item)


        cursor.close()
        conn.commit()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn != None:
            conn.close()
            print('DATABSE CONNECTION CLOSED.')

    return None


def insert(dataframe):
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

        cursor.execute("""CREATE TABLE IF NOT EXISTS roll_call_data (
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
        cursor.copy_from(string_buffer, 'roll_call_data', null='')

        conn.commit()
        cursor.close()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn != None:
            conn.close()
            print('DATABSE CONNECTION CLOSED.')

    return None



if __name__ == '__main__':
    test_df= pd.DataFrame(test_df)
    insert(test_df)
