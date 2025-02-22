import os
import pandas as pd



def load(dataset):
    df = pd.read_csv(dataset, header=0, delimiter=",")
    # Las fechas que aparecen incompletas las formatea como 01-JAN-YYYY
    df['Incident_Date'] = df['Incident_Date'].apply(lambda x: x.replace('??', '01').replace('???', 'JAN'))
    # Elimina las filas duplicadas
    df = df.drop_duplicates()

   # print(df.dtypes)
   # print(df["Onboard_Total"]) --> Ex: Fatalities: 0 / Occupants: 7 Transformar en bbdd
   # print(df.isnull().sum())
   # filas_dup = df[df.duplicated()]
   # print(filas_dup)




            
def main():
    dataset = "../data/Aircraft_Incident_Dataset.csv"
    load(dataset)

if __name__ == "__main__":
    main()