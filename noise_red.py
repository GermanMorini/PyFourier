#!/bin/python3

from scipy.io import wavfile
from scipy.io.wavfile import write
from sys import argv
import numpy as np
import matplotlib.pyplot as plt

if len(argv) != 4:
    print(f"Uso: {argv[0]} ARCHIVO_ORIGINAL.wav PERFIL_RUIDO.wav ARCHIVO_LIMPIO.wav")
    exit(1)

frecuencia_muestreo, senal_original = wavfile.read(argv[1])
_, perfil_ruido = wavfile.read(argv[2])

# Si los archivos son estéreo, tomar el promedio de ambos canales
if len(senal_original.shape) > 1:
    senal_original = senal_original.mean(axis=1)
if len(perfil_ruido.shape) > 1:
    perfil_ruido = perfil_ruido.mean(axis=1)

# Asegurarse de que las señales tengan la misma longitud
min_length = min(len(senal_original), len(perfil_ruido))
senal_original = senal_original[:min_length]
perfil_ruido = perfil_ruido[:min_length]

X_k = np.fft.fft(perfil_ruido)
R_k = np.abs(X_k) ** 2

S_k = np.fft.fft(senal_original)

# Reducción de ruido en el dominio de frecuencias
threshold = np.sqrt(R_k)
Y_k = S_k.copy()
mask = np.abs(S_k) > threshold
Y_k[~mask] = 0
Y_k[mask] = S_k[mask] * (np.abs(S_k[mask]) - threshold[mask]) / np.abs(S_k[mask])

senal_limpia = np.fft.ifft(Y_k).real

# Normalizar la señal limpia
senal_limpia = senal_limpia / np.max(np.abs(senal_limpia))

# Guardar la señal limpia en un archivo WAV
nombre_archivo_salida = argv[3]
write(nombre_archivo_salida, frecuencia_muestreo, (senal_limpia * 32767).astype(np.int16))

# Visualización de los espectrogramas
plt.figure(figsize=(12, 12))

plt.subplot(3, 1, 1)
plt.plot(senal_original)
plt.title('Señal Original')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')

plt.subplot(3, 1, 2)
plt.plot(senal_limpia)
plt.title('Señal Limpia')
plt.xlabel('Muestras')
plt.ylabel('Amplitud')

plt.subplot(3, 1, 3)
plt.specgram(senal_limpia, Fs=frecuencia_muestreo, NFFT=1024, noverlap=512, cmap='viridis')
plt.title('Espectrograma de la Señal Limpia')
plt.xlabel('Tiempo (s)')
plt.ylabel('Frecuencia (Hz)')

plt.tight_layout()
plt.show()
