from configparser import ConfigParser
import os



def config(filename= str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+("\CD_Database.ini"), section= 'postgresql'):

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





