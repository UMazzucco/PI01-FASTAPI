#Razer PI01 API#

import json
import pandas as pd                              #Importamos lo necesario
from fastapi import FastAPI


app = FastAPI()                                  #Creamos la API

data_path = 'PI01_DATA02/Datasets/'              #Establecemos la ubicación de los datasets

datasets = {}                                    #Creamos un diccionario con la información



circuits = pd.read_csv(data_path + 'circuits.csv')                         #Importamos Circuitos
dict_aux = circuits.to_dict('records')
datasets['circuits']=dict_aux

races = pd.read_csv(data_path + 'races.csv')                               #Importamos Carreras
dict_aux = races.to_dict('records')
datasets['races']=dict_aux


with open(data_path+'constructors.json', encoding = 'utf-8') as file:
    dict_aux = [json.loads(line) for line in file]
    datasets['constructors']= dict_aux

constructors = pd.DataFrame.from_dict(datasets['constructors'])            #Importamos Constructores

with open(data_path+'drivers.json', encoding = 'utf-8') as file:
    dict_aux = [json.loads(line) for line in file]
    datasets['drivers']= dict_aux

drivers = pd.DataFrame.from_dict(datasets['drivers'])                      #Importamos Conductores

with open(data_path+'results.json', encoding = 'utf-8') as file:
    dict_aux = [json.loads(line) for line in file]
    datasets['results']= dict_aux

results = pd.DataFrame.from_dict(datasets['results'])                      #Importamos Resultados


@app.get("/")                                                   #Mensaje de bienvenida
def home():
    welcome_msg = 'Bienvenid@ a Razer'
    return welcome_msg


@app.get('/about')                                              #Breve reseña de la API
def about():
    about_razer = {
    'Este es el proyecto 01 de Uriel Mazzucco':'Que nos dirá \n',
    'Año con más carreras':'/most-raced-year',
    'Piloto con mayor cantidad de primeros puestos':'/most-first-place',
    'Nombre del circuito más corrido':'/most-raced-circuit',
    'Piloto con mayor cantidad de puntos totales cuyo constructor sea estadounidense o británico':'/most-points'
    }    
    return about_razer


@app.get('/dataset/{data}')                                     #Obtenemos un dataset
def get_dataset(data:str):
    return datasets[data]


@app.get('/datasets')                                           #Obtenemos la lista de datasets
def get_datasets_stat():
    return {'datasets':list(datasets.keys())}


@app.get('/most-raced-year')                                    #Obtenemos el año con más carreras
def get_most_raced_year():
    sorted_years = races.groupby('year').count().sort_values('raceId',ascending=False)
    year = int(sorted_years.index[0])
    return {'El año con más carreras es:':year}

@app.get('/most-raced-circuit')                                 #Obtenemos el circuito con más carreras
def get_most_rc():
    sorted_circuits = races.groupby('circuitId').count().sort_values('raceId',ascending=False)
    most_raced_circuit_id = sorted_circuits.index[0]
    aux = str(circuits.loc[circuits['circuitId']==most_raced_circuit_id]['name'].values)
    most_rc = aux.strip('[').strip(']').strip("'")
    return {'El circuito con más carreras es:':most_rc}

@app.get('/most-first-place')                                   #Obtenemos el piloto que más veces salió 1ro
def get_best_driver():
    first_places = results.loc[results['positionOrder']==1]
    driverId = first_places.groupby('driverId').count().sort_values('positionOrder',ascending=False).index[0]
    driver = str(drivers[drivers['driverId']==1]['name'].values)
    part = driver.strip('[').strip(']').strip('{').strip('}').replace("forename",'').replace("surname",'')
    best_driver = part.replace("'",'').replace(":",'').replace(" ",'').replace(",",' ')
    return {'El piloto que más veces salió en primer puesto es:':best_driver}

@app.get('/most-points')                                        #Obtenemos el piloto que más veces salió 1ro
def get_most_points():
    id_constructores = constructors.loc[(constructors['nationality']=='British') | (constructors['nationality']=='American')]['constructorId'].to_list()
    carreras = results.loc[(results['constructorId'].isin(id_constructores))]
    most_points_id = carreras.groupby('driverId').sum('points').sort_values('points',ascending=False).index[0]
    piloto = str(drivers[drivers['driverId']==most_points_id]['name'].values)
    part =piloto.strip('[').strip(']').strip('{').strip('}').replace("forename",'').replace("surname",'')
    best_pil = part.replace("'",'').replace(":",'').replace(" ",'').replace(",",' ')
    return {'El piloto de fabricante estadounidense o británico con más puntos es:':best_pil}



#uvicorn razer:app --reload launches the api
#api on http://127.0.0.1:8000