import os
import pandas as pd



def load(dataset):
    df = pd.read_csv(dataset, header=0, delimiter=",")

    # Las fechas que aparecen incompletas las formatea como 01-JAN-YYYY
    df['Incident_Date'] = df['Incident_Date'].apply(lambda x: x.replace('??', '01').replace('???', 'JAN'))

    # Elimina las filas duplicadas
    df = df.drop_duplicates()

    # Limpia los datos de la columna "Time" a únicamente la hora
    df["Time"] = df["Time"].astype(str).str.extract(r'(\d{1,2}:\d{2})')

    # Sutituye los valores nulos por "-"
    df.fillna("-", inplace=True)



   # print(df.dtypes)
   # print(df["Onboard_Total"]) --> Ex: Fatalities: 0 / Occupants: 7 Transformar en bbdd
   # print(df.isnull().sum())
   # filas_dup = df[df.duplicated()]
    print(df.isnull().sum())




            
def main():
    dataset = "../data/Aircraft_Incident_Dataset.csv"
    load(dataset)

if __name__ == "__main__":
    main()