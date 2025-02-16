#!/bin/python3

import numpy as np
import pandas as pd
from scipy.io.wavfile import write
from sys import argv

if len(argv) != 3:
    print(f"Uso: {argv[0]} ARCHIVO.csv DURACION")
    exit(1)

archivo_csv = argv[1]
tasa_muestreo = 44100
duracion = float(argv[2])
nombre_archivo_salida = f"{archivo_csv}.wav"

try:
    datos = pd.read_csv(archivo_csv)

    # frecuencia, amplitud, tipo de decaimiento, tiempo del decaimiento
    if not all(col in datos.columns for col in ['frec', 'amp', 'dec', 'dec_time']):
        raise ValueError("El CSV debe contener columnas 'frec', 'amp', 'dec' y 'dec_time'")
except FileNotFoundError:
    print(f"Error: No se encontró el archivo {archivo_csv}")
    exit()

t = np.linspace(0, duracion, int(tasa_muestreo * duracion), endpoint=False)
onda = np.zeros_like(t)

# Normalizar los valores de amplitud (si NO estan en decibeles)
# datos['amp'] = datos['amp'] / np.abs(datos['amp'].max())

for _, fila in datos.iterrows():
    decay_type = fila['dec']
    decay_time = fila['dec_time']
    
    if decay_type == 1:
        envelope = np.exp(-t / decay_time)
    elif decay_type == 2:
        envelope = np.clip(1 - (t / decay_time), 0, None)
    elif decay_type == 0:
        envelope = 1
    else:
        raise ValueError("Tipo de decaimiento no válido")
    
    frecuencia = fila['frec']
    # amplitud = 20 * np.log10(fila['amp'])
    amplitud = 10 ** (fila['amp'] * 0.05) # si tenemos los valores en decibeles
    onda += envelope * amplitud * np.cos(2 * np.pi * frecuencia * t)

onda = onda / np.max(np.abs(onda))

write(nombre_archivo_salida, tasa_muestreo, (onda * 32767).astype(np.int16))
