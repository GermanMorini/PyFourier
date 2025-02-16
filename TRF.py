#!/bin/python3

from scipy.io import wavfile
from sys import argv
import numpy as np
import matplotlib.pyplot as plt
import logging as log

log.basicConfig(
    level=log.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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

log.info(f"Frecuencia de muestreo: {frecuencia_muestreo}")
log.info(f"Cantidad de muestras de la señal: {n}")

plt.figure(figsize=(10, 8))

plt.subplot(2, 1, 1)
plt.plot(frecuencias, magnitud)
plt.title('Espectro de Frecuencias (escala lineal)')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.xlim(0, frecuencia_muestreo/2)

plt.subplot(2, 1, 2)
plt.specgram(senal, Fs=frecuencia_muestreo, NFFT=1024*4)
plt.title('Espectrograma')
plt.xlabel('Timepo (s)')
plt.ylabel('Frecuencia (Hz)')

plt.tight_layout()
plt.show()
