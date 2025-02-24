import sqlite3
from config import DATABASE_PATH

def create_database():
    """ Crea la base de datos SQLite con todas las tablas necesarias. """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Dim_Fecha (
            fecha_id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE,
            dia_semana TEXT,
            dia INTEGER,
            mes INTEGER,
            anio INTEGER
        );

        CREATE TABLE IF NOT EXISTS Dim_Aeronave (
            aeronave_id INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT,
            registro TEXT,
            motores TEXT,
            primer_vuelo YEAR                  
        );

        CREATE TABLE IF NOT EXISTS Dim_Aeropuerto (
            aeropuerto_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT, 
            codigo_iata TEXT UNIQUE,
            codigo_icao TEXT UNIQUE,
            pais TEXT 
        );

        CREATE TABLE IF NOT EXISTS Dim_Categoria_Incidente (  
            categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS Dim_Causa_Incidente (  
            causa_id INTEGER PRIMARY KEY AUTOINCREMENT,
            causa TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS Dim_Tipo_Dano (  
            tipo_dano_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_dano TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS Dim_Fase_Vuelo (
            fase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            fase TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS Hechos_Incidentes (
            id_incidente INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_id INTEGER,
            aeronave_id INTEGER,
            aeropuerto_salida_id INTEGER,
            aeropuerto_destino_id INTEGER,
            ubicacion_incidente TEXT,
            categoria_id INTEGER,
            causa_id INTEGER,
            tipo_dano_id INTEGER,
            fase_id INTEGER,
            hora TIME,
            
            tripulacion_total INTEGER DEFAULT 0,
            tripulacion_fallecidos INTEGER DEFAULT 0,
            pasajeros_total INTEGER DEFAULT 0,
            pasajeros_fallecidos INTEGER DEFAULT 0,
            fatalidades_tierra INTEGER DEFAULT 0,
            fatalidades_colision INTEGER DEFAULT 0,

            FOREIGN KEY (fecha_id) REFERENCES Dim_Fecha(fecha_id),
            FOREIGN KEY (aeronave_id) REFERENCES Dim_Aeronave(aeronave_id),
            FOREIGN KEY (aeropuerto_salida_id) REFERENCES Dim_Aeropuerto(aeropuerto_id),
            FOREIGN KEY (aeropuerto_destino_id) REFERENCES Dim_Aeropuerto(aeropuerto_id),
            FOREIGN KEY (categoria_id) REFERENCES Dim_Categoria_Incidente(categoria_id),
            FOREIGN KEY (causa_id) REFERENCES Dim_Causa_Incidente(causa_id),
            FOREIGN KEY (tipo_dano_id) REFERENCES Dim_Tipo_Dano(tipo_dano_id),
            FOREIGN KEY (fase_id) REFERENCES Dim_Fase_Vuelo(fase_id)
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Base de datos SQLite creada exitosamente.")

if __name__ == "__main__":
    create_database()
