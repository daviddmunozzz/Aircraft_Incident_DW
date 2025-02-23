import os
import pandas as pd
import re
import time

def clean_location(text):
    if pd.isna(text):
        return text
    text = re.sub(r"\.{3}$", "", text) # Elimina los puntos suspensivos al final del texto
    text = re.sub(r"^\s*(near|whitin)\s+", "", text) # Elimina "near" y "whitin" al principio del texto
    return text.strip() # Elimina los espacios en blanco al principio y al final del texto

def extract_airport_info(airport_str):
    if pd.isna(airport_str):
        return pd.Series([None, None, None, None])
    
    # Caso 1: Con código IATA y ICAO
    match = re.match(r"^(.*) \((\w{3})/(\w{4})\) , (.*)$", airport_str)
    if match:
        return pd.Series([
            match.group(1).strip(),  # Nombre del aeropuerto
            match.group(2).strip(),  # Código IATA
            match.group(3).strip(),  # Código ICAO
            match.group(4).strip()   # País
        ])
    
    # Caso 2: Solo código ICAO (4 letras)
    match = re.match(r"^(.*) \((\w{4})\) , (.*)$", airport_str)
    if match:
        return pd.Series([
            match.group(1).strip(),  # Nombre del aeropuerto
            None,                    # No hay código IATA
            match.group(2).strip(),  # Código ICAO
            match.group(3).strip()   # País
        ])
    
    # Si no coincide con ninguno de los formatos, devolver None
    return pd.Series([None, None, None, None])

def extract_values(text):
    match = re.search(r"Fatalities:\s*(\d+)\s*/\s*Occupants:\s*(\d*)", text)
    if match:
        fatalities = int(match.group(1))  # Siempre habrá un número en Fatalities
        occupants = int(match.group(2)) if match.group(2) else pd.NA  # Si falta el número, asigna pd.NA
        return fatalities, occupants
    else:
        return pd.NA, pd.NA  # Si la estructura es inválida, devuelve NA en ambas columnas
    