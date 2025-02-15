import numpy as np
import sounddevice as sd
import pandas as pd
from scipy.io.wavfile import write
from sys import argv

if len(argv) != 5:
    print(f"Uso: {argv[0]} ARCHIVO.csv DEC_TYPE DURACION DEC_TIME")
    exit(1)

dec_type = {
    0: "none",
    1: "exponential",
    2: "linear"
}

archivo_csv = argv[1]
duracion = float(argv[3])
tasa_muestreo = 44100
decay_type = dec_type[int(argv[2])]
decay_time = float(argv[4])
nombre_archivo_salida = f"{archivo_csv}-reconstruido.wav"

try:
    datos = pd.read_csv(archivo_csv)
    if not all(col in datos.columns for col in ['frecuencia', 'amplitud']):
        raise ValueError("El CSV debe contener columnas 'frecuencia' y 'amplitud'")
except FileNotFoundError:
    print(f"Error: No se encontró el archivo {archivo_csv}")
    exit()

t = np.linspace(0, duracion, int(tasa_muestreo * duracion), endpoint=False)
onda = np.zeros_like(t)

for _, fila in datos.iterrows():
    frecuencia = fila['frecuencia']
    amplitud = fila['amplitud']
    onda += amplitud * np.cos(2 * np.pi * frecuencia * t)

onda_normalizada = onda / np.max(np.abs(onda))

if decay_type == "exponential":
    envelope = np.exp(-t / decay_time)
elif decay_type == "linear":
    envelope = np.clip(1 - (t / decay_time), 0, None)
elif decay_type == "none":
    envelope = 1
else:
    raise ValueError("Tipo de decaimiento no válido. Usar 'exponential' o 'linear'")

onda_con_decaimiento = onda_normalizada * envelope

onda_final = onda_con_decaimiento / np.max(np.abs(onda_con_decaimiento))

write(nombre_archivo_salida, tasa_muestreo, (onda_final * 32767).astype(np.int16))
