# Razer

## About

Razer es el proyecto individual N° 1 para SoyHenry. Se trata del desarrollo de una API con el framework FastAPI, que realiza determinadas consultas sobre datasets brindados previamente. La temática es de carreras de Fórmula 1, y posteriormenta se deployará en un servidor de Heroku. Para este caso utilizaremos Pandas.

## Enlace

<<https://razer-umazz.herokuapp.com/user-guide>>

## Códigos

### Cvser.py

Este pequeño código convierte en archivos .csv los datasets en .json para su posterior utilización. En caso de no tener lista la carpeta 'csvs' debe ejecutarse antes.

### Main.py

Contiene todo lo necesario para la ejecución de la API.

## Data

### Original_data

Contiene todos los datasets brindados por Henry, aunque algunos no serán utilizados.

### Csvs

COntiene en formato .csv los datasets que utilizaremos.

### ETL

Los datos ya están limpios, por lo que nos dedicaremos al armado de la API y las conexiones entre tablas.
