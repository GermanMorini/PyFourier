#!/bin/python3

from scipy.io import wavfile
from sys import argv
import numpy as np
import matplotlib.pyplot as plt

if len(argv) != 2:
    print(f"Uso: {argv[0]} ARCHIVO.wav")
    exit(1)

frecuencia_muestreo, senal = wavfile.read(argv[1])

if len(senal.shape) > 1:
    senal = senal.mean(axis=1)

n = len(senal)
fft = np.fft.fft(senal)
magnitud = np.abs(fft)
frecuencias = np.fft.fftfreq(n, d=1/frecuencia_muestreo)
mitad = n // 2
magnitud = magnitud[:mitad]
frecuencias = frecuencias[:mitad]

plt.figure(figsize=(12, 12))

plt.subplot(2, 1, 1)
plt.plot(frecuencias, magnitud)
plt.title('Espectro de Frecuencia')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.xlim(0, frecuencia_muestreo/2)

magnitud_normalizada = magnitud / n
magnitud_normalizada[magnitud_normalizada == 0] = 1e-10
db = 20 * np.log10(magnitud_normalizada)

plt.subplot(2, 1, 2)
plt.plot(frecuencias, db)
plt.title('Espectro de Frecuencia en Decibelios')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud (dB)')
plt.grid(True)
plt.xlim(0, frecuencia_muestreo/2)
plt.ylim(-120, 0)

plt.tight_layout()
plt.show()
