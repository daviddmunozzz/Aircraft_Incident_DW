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
            naturaleza_operacion TEXT,
            primer_vuelo DATE                  
        );

        CREATE TABLE Dim_Aeropuerto (
            aeropuerto_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT, 
            codigo_iata TEXT UNIQUE,
            codigo_icao TEXT UNIQUE,
            pais TEXT 
        );

        CREATE TABLE IF NOT EXISTS Dim_Incidente (  
            incidente_id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT,
            causa TEXT,
            tipo_dano TEXT
        );

        CREATE TABLE IF NOT EXISTS Dim_Fase_Vuelo (
            fase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            fase TEXT
        );
                         
        CREATE TABLE IF NOT EXISTS Dim_Fase_Vuelo (
            fase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            fase TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS Hechos_Incidentes (
            id_incidente INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_id INTEGER,
            aeronave_id INTEGER,
            operador_id INTEGER,
            ubicacion_id INTEGER,
            incidente_id INTEGER,
            fase_id INTEGER,
            hora TIME,
            fatalidades_total INTEGER,
            fatalidades_tierra INTEGER,
            fecha_primer_vuelo YEAR,
            FOREIGN KEY (fecha_id) REFERENCES Dim_Fecha(fecha_id),
            FOREIGN KEY (aeronave_id) REFERENCES Dim_Aeronave(aeronave_id),
            FOREIGN KEY (operador_id) REFERENCES Dim_Operador(operador_id),
            FOREIGN KEY (ubicacion_id) REFERENCES Dim_Ubicacion(ubicacion_id),
            FOREIGN KEY (incidente_id) REFERENCES Dim_Incidente(incidente_id),
            FOREIGN KEY (fase_id) REFERENCES Dim_Fase_Vuelo(fase_id)
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Base de datos SQLite creada exitosamente.")

if __name__ == "__main__":
    create_database()
