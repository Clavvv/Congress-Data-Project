from configparser import ConfigParser



def config(filename= '/Users/Ryan/Desktop/CongressAPP/database.ini', section= 'postgresql'):

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





