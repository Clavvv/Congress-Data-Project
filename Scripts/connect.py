import os
import psycopg2
from config import config

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






if __name__ == '__main__':
    make_connection()
