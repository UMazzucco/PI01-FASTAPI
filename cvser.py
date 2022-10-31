import json
import pandas as pd                              #Importamos lo necesario
import os

data_path = 'original_data/'              #Establecemos la ubicación de los datasets

with open(data_path+'constructors.json', encoding = 'utf-8') as file:
        dict_aux = [json.loads(line) for line in file]

constructors = pd.DataFrame.from_dict(dict_aux)            #Importamos Constructores

with open(data_path+'drivers.json', encoding = 'utf-8') as file:
        dict_aux = [json.loads(line) for line in file]

drivers = pd.DataFrame.from_dict(dict_aux)                      #Importamos Conductores

with open(data_path+'results.json', encoding = 'utf-8') as file:
        dict_aux = [json.loads(line) for line in file]

results = pd.DataFrame.from_dict(dict_aux)                  #Importamos Resultados

constructors.to_csv('csvs/constructors.csv',index=False,sep=',') #Guardamos los datframes en csvs
drivers.to_csv('csvs/drivers.csv',index=False,sep=',')
results.to_csv('csvs/results.csv',index=False,sep=',')

os.system('mv original_data/circuits.json csvs/')
os.system('mv original_data/races.json csvs/')