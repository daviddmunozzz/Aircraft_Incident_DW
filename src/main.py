import os
import pandas as pd
import re

def clean_location(text):
    if pd.isna(text):
        return text
    text = re.sub(r"\.{3}$", "", text) # Elimina los puntos suspensivos al final del texto
    text = re.sub(r"^\s*(near|whitin)\s+", "", text) # Elimina "near" y "whitin" al principio del texto
    return text.strip() # Elimina los espacios en blanco al principio y al final del texto

def transform(df):
    # Las fechas que aparecen incompletas las formatea como 01-JAN-YYYY
    df['Incident_Date'] = df['Incident_Date'].apply(lambda x: x.replace('??', '01').replace('???', 'JAN'))

    # Elimina las filas duplicadas
    df = df.drop_duplicates()

    # Limpia los datos de la columna "Time" a únicamente la hora
    df["Time"] = df["Time"].astype(str).str.extract(r'(\d{2}:\d{2})')

    # Limpia los datos de la columna "Aircraft_First_Flight" a únicamente el año
    df["Aircaft_First_Flight"] = df["Aircaft_First_Flight"].astype(str).str.extract(r"(\d{4})")

    # Sutituye los valores nulos por "-"
    df.fillna("-", inplace=True)

    print(df["Aircaft_First_Flight"])
    

def extract(dataset):
    df = pd.read_csv(dataset, header=0, delimiter=",")

    return df


def load(df):


   # print(df.dtypes)
   # print(df["Onboard_Total"]) --> Ex: Fatalities: 0 / Occupants: 7 Transformar en bbdd
   # print(df.isnull().sum())
   # filas_dup = df[df.duplicated()]
    print(df.isnull().sum())




            
def main():
    dataset = "../data/Aircraft_Incident_Dataset.csv"
    df = extract(dataset)
    df = transform(df)

if __name__ == "__main__":
    main()