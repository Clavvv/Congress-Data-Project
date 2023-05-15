from configparser import ConfigParser
import os

#config parser for psycopg2 database connection.
#reads an ini file turns it into a dictionary and returns it 

def config(filename= str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+("\database.ini"), section= 'postgresql'):

    parser= ConfigParser()

    parser.read(filename)


    db= {}

    if parser.has_section(section):
        params= parser.items(section)

        for p in params:
            db[p[0]]= p[1]

    else:
        raise Exception(f'SECTION {section} NOT FOUND IN THE {filename} FILE')

    return db


if __name__ == '__main__':

    config()





