#!/bin/python3

import sys
import math

notas = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def calcular_nota(frecuencia):
    if frecuencia <= 0:
        return "Silencio"
    
    midi = 12 * math.log2(frecuencia/440) + 69
    octava = (midi // 12) - 1
    nota = notas[int(midi % 12)]
    cents = int(100 * (midi % 1))  # Cents de desviación
    
    if cents >= 50:
        nota = notas[(int(midi % 12) + 1) % 12]
        cents -= 100
    
    return f"{nota}{int(octava)} {'+' if cents >=0 else ''}{cents} cents"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} frecuencia1 [frecuencia2 ...]")
        sys.exit(1)
    
    for arg in sys.argv[1:]:
        try:
            f = float(arg)
            print(f"{f:.2f} Hz: {calcular_nota(f)}")
        except ValueError:
            print(f"Error: '{arg}' no es un número válido")
