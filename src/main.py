import utilities
import pandas as pd
import time
import sqlite3
from config import DATABASE_PATH

    
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
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    for index, row in df.iterrows():

        cursor.execute('''
                INSERT OR IGNORE INTO Dim_Fecha (fecha, dia_semana, dia, mes, anio)
                VALUES (?,?,?,?,?)
                ''', (row['Incident_Date'], row['Date'].split()[0], row['Arit'].split("-")[0], 
                      row['Arit'].split("-")[1], row['Arit'].split("-")[2]))
        cursor.execute('''
                SELECT fecha_id FROM Dim_Fecha WHERE fecha = ?
                ''', (row['Incident_Date']))
        fecha_id = cursor.fetchone()[0]
        
        cursor.execute('''
                INSERT OR IGNORE INTO Dim_Aeronave (modelo, registro, motores, primer_vuelo)  
                VALUES (?,?,?,?)
                ''', (row['Aircraft_Model'], row['Aircraft_Registration'],
                      row['Aircraft_Engines'], row['Aircaft_First_Flight']))
        cursor.execute('''
                SELECT aeronave_id FROM Dim_Aeronave WHERE modelo = ? AND registro = ?
                ''', (row['Aircraft_Model'], row['Aircraft_Registration']))
        aeronave_id = cursor.fetchone()[0]
        
        cursor.execute('''
                INSERT OR IGNORE INTO Dim_Aeropuerto (nombre, codigo_iata, codigo_icao, pais)
                VALUES (?,?,?,?)
                ''', (row["Departure_Airport_Name"], row["Departure_Airport_IATA"],
                      row["Departure_Airport_ICAO"], row["Departure_Airport_Country"]))   
        cursor.execute('''
                SELECT aeropuerto_id FROM Dim_Aeropuerto WHERE nombre = ?
                ''', (row["Departure_Airport_Name"]))
        aeropuerto_salida_id = cursor.fetchone()[0]

        cursor.execute('''
                INSERT OR IGNORE INTO Dim_Aeropuerto (nombre, codigo_iata, codigo_icao, pais)
                VALUES (?,?,?,?)
                ''', (row["Destination_Airport_Name"], row["Destination_Airport_IATA"],
                      row["Destination_Airport_ICAO"], row["Destination_Airport_Country"]))
        cursor.execute('''
                SELECT aeropuerto_id FROM Dim_Aeropuerto WHERE nombre = ?
                ''', (row["Destination_Airport_Name"]))
        aeropuerto_destino_id = cursor.fetchone()[0]
        
        cursor.execute('''
                INSERT OR IGNORE INTO Dim_Categoria_Incidente (categoria)
                VALUES (?)
                ''', (row["Incident_Category"]))
        cursor.execute('''
                SELECT categoria_id FROM Dim_Categoria_Incidente WHERE categoria = ?
                ''', (row["Incident_Category"]))
        categoria_id = cursor.fetchone()[0]
        
        cursor.execute('''
                INSERT OR IGNORE INTO Dim_Causa_Incidente (causa)
                VALUES (?)
                ''', (row["Incident_Cause(es)"]))
        cursor.execute('''
                SELECT causa_id FROM Dim_Causa_Incidente WHERE causa = ?
                ''', (row["Incident_Cause(es)"]))
        causa_id = cursor.fetchone()[0]
        
        cursor.execute('''
                INSERT OR IGNORE INTO Dim_Tipo_Dano (tipo_dano)
                VALUES (?)
                ''', (row["Aircaft_Damage_Type"]))
        cursor.execute('''
                SELECT tipo_dano_id FROM Dim_Tipo_Dano WHERE tipo_dano = ?
                ''', (row["Aircaft_Damage_Type"]))
        tipo_dano_id = cursor.fetchone()[0]
        
        cursor.execute('''
                INSERT OR IGNORE INTO Dim_Fase_Vuelo (fase)
                VALUES (?)
                ''', (row["Aircraft_Phase"]))
        cursor.execute('''
                SELECT fase_id FROM Dim_Fase_Vuelo WHERE fase = ?
                ''', (row["Aircraft_Phase"]))   
        fase_id = cursor.fetchone()[0]
        
        cursor.execute('''
                INSERT OR IGNORE INTO Hechos_Incidentes (fecha_id, aeronave_id, aeropuerto_salida_id, 
                       aeropuerto_destino_id, ubicacion_incidente, categoria_id, causa_id, tipo_dano_id, 
                       fase_id, hora, tripulacion_total, tripulacion_fallecidos, pasajeros_total, pasajeros_fallecidos,
                       fatalidades_tierra, fatalidades_colision)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''', (fecha_id, aeronave_id, aeropuerto_salida_id, aeropuerto_destino_id, row["Incident_Location"],
                      categoria_id, causa_id, tipo_dano_id, fase_id, row["Time"], row["Occupants_Crew"],
                      row["Fatalities_Crew"], row["Occupants_Passengers"], row["Fatalities_Passengers"],
                      row["Ground_Casualties"], row["Collision_Casualties"]))
        
    conn.commit()
    cursor.close()
    conn.close()
            
            
def main():
    dataset = "../data/Aircraft_Incident_Dataset.csv"
    df = extract(dataset)
    transform(df)
    load(df)

if __name__ == "__main__":
    main()