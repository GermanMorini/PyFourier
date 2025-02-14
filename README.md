# Transformada de Fourier en python

## Explicación

Este es un ejemplo de uso de la transformada de Fourier en python

El objetivo es encontrar las frecuencias que componen un archivo de sonido (en este caso [bell.wav](bell.wav) usando
la transformada de Fourier, luego graficar las frecuencias principales usando [geogebra](bell.ggb) y compararlas
con un [espectrograma](bell.png) sacado de otro software

Adicionalmente se puede calcular las notas que componen el archivo de ejemplo usando [este script](midi_func.py),
que utiliza la función MIDI para calcular las notas en función de las frecuencias

Por ejemplo, si tomamos las frecuencias mas dominantes que son son `2645`, `7043` y  `13228` vemos que son
las notas `E, A, G#` (**Mi**, **La** y **Sol** sostenido)

---

## Como usarlo

~~~bash
source activate										# activa el entorno virtual

python3 TRF.py bell.wav								# aplica la transformada de Fourier al archivo de audio

python3 midi_func.py 2645 7043 13228 [...]  		# calcula las notas en función de las frecuencias ingresadas
~~~
