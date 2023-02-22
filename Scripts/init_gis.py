import os
from sqlalchemy import *
from geoalchemy2 import Geometry, WKTElement
import pandas as pd
import geopandas as gpd
import json
import glob
import re


def init_gis():

    dir_path= str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    #Reading and parsing json to populate db connection credentials
    params= json.load(open(dir_path+"\GIS_DB.json"))
    user= params['username']
    pwd= params['password']
    host= params['host']
    port= params['socket']
    database= params['database']

    #creating database connection engine
    engine= create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{database}')

    #getting filepaths for shapefiles
    gis_path= f"{dir_path}/GIS"
    gis_files= glob.glob(f"{gis_path}/**/*.shp", recursive=True)
    names= set([])

    for file in gis_files:

        #cleaning the file path strings to use as table names
        #using regex to create homogenous naming scheme
        #removing the directory paths preceeding the file name

        table_name= file.split(gis_path)[1]

        #separating the county and district files and filtering string to use as table names 
        if (bool(re.match('.US', table_name))):
            expression= r'.\w.\w\d(?=[th])'
            result= re.search(expression, table_name)
            name= str(result.group(0))
        
        elif (bool(re.match('.tl', table_name))):
            expression= r'\d..\d'
            result= re.search(expression, table_name)
            name= str(result.group(0)+"_county")


        

        #read in shapefile
        gdf= gpd.read_file(file)
        
        #creating table and uploading to PostGIS
        gdf.to_postgis(con= engine, name= name, if_exists= 'replace', schema= 'public')


if __name__ == "__main__":
    init_gis()