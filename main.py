#Razer PI01 API Uriel Mazzucco

import json
import pandas as pd                              #Importamos lo necesario
from fastapi import FastAPI

app = FastAPI()                                  #Creamos la API

data_path = 'Datasets/'              #Establecemos la ubicación de los datasets

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

circuits.drop(['lat','lng','alt'],axis=1,inplace=True)
drivers.drop(['number','code','dob'],axis=1,inplace=True)
races.drop(['time','date'],axis=1,inplace=True)
lista = ['number','grid','position','positionText','laps','time','milliseconds','fastestLap','fastestLapTime','fastestLapSpeed','statusId']
results.drop(lista,axis=1,inplace=True)                         #Eliminamos columnas que no necesitamos


@app.get("/")                                                   #Mensaje de bienvenida
def home():
    welcome_msg = {'Te damos la bienvenida a Razer':'Prueba agregando */user-guide* (sin asteriscos) en la barra de direcciones'}
    return welcome_msg


@app.get('/about')                                              #Breve reseña de la API
def about():
    about_msg = 'Razer es el PI 01 de Uriel Mazzucco para Henry'
    return about_msg

@app.get('/user-guide')                                         #Guía del Usuario
def user_guide():
    usr_guide = {
    'Código':'Consulta',
    '/most-raced-year':'Año en que se realizaron más carreras carreras',
    '/most-first-place':'Piloto que salió en primer lugar más veces',
    '/most-raced-circuit':'Nombre del circuito más corrido',
    '/most-points':'Piloto con mayor cantidad de puntos totales, utilizando un constructor estadounidense o británico',
    '/about':'Sobre Razer',
    '/datasets':'Lista de datasets con los que hemos trabajado (en bruto)',
    '/datasets/data':'Devuelve el dataset *data* (utilizar sin asteriscos) que queremos consultar',
    '/docs':'Documentación realizada automáticamente por FastAPI',
    '/':'Mensaje de Bienvenida'
    }    
    return usr_guide


@app.get('/datasets/{data}')                                    #Obtenemos un dataset
def get_dataset(data:str):
    return datasets[data]


@app.get('/datasets')                                           #Obtenemos la lista de datasets
def get_datasets_stat():
    return {'datasets':list(datasets.keys())}


@app.get('/most-raced-year')                                    #Obtenemos el año con más carreras
def get_most_raced_year():
    sorted_years = races.groupby('year').count().sort_values('raceId',ascending=False)
    year = int(sorted_years.index[0])
    return {'El año en que se realizaron más carreras carreras es':year}

@app.get('/most-raced-circuit')                                 #Obtenemos el circuito con más carreras
def get_most_rc():
    sorted_circuits = races.groupby('circuitId').count().sort_values('raceId',ascending=False)
    most_raced_circuit_id = sorted_circuits.index[0]
    aux = str(circuits.loc[circuits['circuitId']==most_raced_circuit_id]['name'].values)
    most_rc = aux.strip('[').strip(']').strip("'")
    return {'El circuito donde se realizaron más carreras es':most_rc}

@app.get('/most-first-place')                                   #Obtenemos el piloto que más veces salió 1ro
def get_best_driver():
    first_places = results.loc[results['positionOrder']==1]
    driverId = first_places.groupby('driverId').count().sort_values('positionOrder',ascending=False).index[0]
    driver = str(drivers[drivers['driverId']==1]['name'].values)
    part = driver.strip('[').strip(']').strip('{').strip('}').replace("forename",'').replace("surname",'')
    best_driver = part.replace("'",'').replace(":",'').replace(" ",'').replace(",",' ')
    return {'El piloto que salió en primer lugar más veces es:':best_driver}

@app.get('/most-points')                                        #Obtenemos el piloto que más veces salió 1ro
def get_most_points():
    id_constructores = constructors.loc[(constructors['nationality']=='British') | (constructors['nationality']=='American')]['constructorId'].to_list()
    carreras = results.loc[(results['constructorId'].isin(id_constructores))]
    sorted = carreras.groupby('driverId').sum('points').sort_values('points',ascending=False)
    most_points_id = sorted.index[0]
    points = int(sorted.iloc[0]['points'])
    piloto = str(drivers[drivers['driverId']==most_points_id]['name'].values)
    best_pil = piloto.replace("[{'forename': '","").replace("', 'surname': '"," ").replace("'}]","")
    return {'El piloto con mayor cantidad de puntos totales, utilizando un constructor estadounidense o británico es':best_pil}


#uvicorn main:app --reload on terminal launches the api
#api on http://127.0.0.1:8000
