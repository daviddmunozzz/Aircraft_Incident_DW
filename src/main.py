import utilities
import pandas as pd
import time

    
def transform(df):
    # Las fechas que aparecen incompletas las formatea como 01-JAN-YYYY
    df['Incident_Date'] = df['Incident_Date'].apply(lambda x: x.replace('??', '01').replace('???', 'JAN'))

    # Elimina las filas duplicadas
    df = df.drop_duplicates()

    # Limpia los datos de la columna "Time" a únicamente la hora
    df.loc[:, "Time"] = df["Time"].astype(str).str.extract(r'(\d{2}:\d{2})')

    # Limpia los datos de la columna "Aircraft_First_Flight" a únicamente el año
    df.loc[:, "Aircaft_First_Flight"] = df["Aircaft_First_Flight"].astype(str).str.extract(r"(\d{4})")

    # Sutituye los valores nulos por "-"
    df.loc[:, :] = df.fillna("-")

    # Limpia los datos de la columna "Location" eliminando los puntos suspensivos al final del texto y los espacios en blanco al principio y al final del texto
    df.loc[:, "Incident_Location"] = df["Incident_Location"].apply(utilities.clean_location)    

    # Añade columnas

    df[["Fatalities_Crew", "Occupants_Crew"]] = df["Onboard_Crew"].apply(lambda x: pd.Series(utilities.extract_values(x)))
    df[["Fatalities_Passengers", "Occupants_Passengers"]] = df["Onboard_Passengers"].apply(lambda x: pd.Series(utilities.extract_values(x)))

    df[['Departure_Airport_Name', 'Departure_Airport_IATA', 'Departure_Airport_ICAO', 'Departure_Airport_Country']] = df['Departure_Airport'].apply(utilities.extract_airport_info)
    df[['Destination_Airport_Name', 'Destination_Airport_IATA', 'Destination_Airport_ICAO', 'Destination_Airport_Country']] = df['Destination_Airport'].apply(utilities.extract_airport_info)


    for index, row in df.iterrows():
        print(f"Fila {index}:")
        for column in df.columns:
            print(f"{column}: {row[column]}")
            time.sleep(1)
    

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