import random
import math
import numpy as np
import time
from scipy.io import wavfile

#Esquema de comunicación de Shannon: Fuente de informacion
def transmisor (mensaje):
  fuente_de_informacion = "/content/mensaje_morse.txt"
  with open(mensaje, 'r') as archivo:
    mensaje = archivo.read()
    print ("Mensaje original: ")
    print(mensaje)
  return mensaje

#Codificación del mensaje
def codificador (mensaje_original, diccionario): #recibimos el mensaje enviado desde nuestra fuente de informacion
  mensaje_codificado = []
  for letra in mensaje_original.upper():
    if letra in diccionario:
      mensaje_codificado.append(diccionario[letra])
    else:
       mensaje_codificado.append('?','=','!','¡')
  archivo = ' '.join(mensaje_codificado)
  return archivo

def canal(archivo):
  probabilidad = 0.2
  print("llego el archivo", type(archivo))
  mensaje_morse = []

  for pulsaciones in archivo:
    mensaje_morse.append(pulsaciones)
    if pulsaciones in mensaje_morse and random.random() < probabilidad:
            print("se agrego ruido aqui")
            ruido = random.choice(['.', '-'])
            mensaje_morse.append(ruido)
    print(pulsaciones)
    time.sleep(0.5)
  mensaje_distorsionado = ''.join(mensaje_morse)
  print(''.join(mensaje_morse))
  return mensaje_distorsionado

# Función para generar una onda sinusoidal de una frecuencia específica
def generate_sin_wave(frequency, duration, SAMPLE_RATE):
    time_points = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = np.sin(2 * np.pi * frequency * time_points)
    return wave

# Función para transformar un símbolo Morse en una onda
def morse_to_wave(symbol, DOT_DURATION, SAMPLE_RATE):
    if symbol == '.':
        return generate_sin_wave(500, DOT_DURATION, SAMPLE_RATE)
    elif symbol == '-':
        return generate_sin_wave(500, DOT_DURATION * 3, SAMPLE_RATE)
    elif symbol == '/':
        return np.zeros(int(SAMPLE_RATE * DOT_DURATION * 7))  # Espacio entre palabras

def receptor(morse_message):
  # Definir la duración de un punto en segundos y la frecuencia de muestreo
  DOT_DURATION = 1
  SAMPLE_RATE = 44100

  # Convertir el mensaje Morse en una serie de ondas
  morse_wave = np.concatenate([morse_to_wave(char, DOT_DURATION, SAMPLE_RATE) for char in morse_message.replace(' ', '/')])

  # Normalizar la onda entre -1 y 1
  morse_wave = morse_wave / np.max(np.abs(morse_wave))

  # Crear el archivo WAV
  wavfile.write("morse_audio.wav", SAMPLE_RATE, (morse_wave * 32767).astype(np.int16))

  print("Archivo 'morse_audio.wav' creado.")

#PROCESO DE COMUNICACIÓN
# Diccionario de caracteres Morse
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', ' ': '/'
}

mensaje = transmisor('/content/mensaje_morse.txt')
mensaje_codificado =codificador(mensaje,MORSE_CODE_DICT)
print("Mensaje codificado:", mensaje_codificado)
mensaje_distorsionado = canal(mensaje_codificado)
receptor(mensaje_distorsionado)