# -*- coding: utf-8 -*-
"""Shannon-fano_y_Huffman_Telegrafo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ygzm9tQxtdXnFGjetXeYOnLs-IoxXFLr
"""

import random
import math
import numpy as np
import time
import collections
import heapq
from scipy.io import wavfile
from collections import Counter, defaultdict
from heapq import heappush, heappop, heapify

"""##HUFFMAN"""

class NodoHuffman:
    def __init__(self, simbolo, frecuencia):
        self.simbolo = simbolo
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

def contar_frecuencias(mensaje_binario):
    return Counter(mensaje_binario)

def construir_arbol_huffman(frecuencias):
    nodos = [NodoHuffman(simbolo, frecuencia) for simbolo, frecuencia in frecuencias.items()]

    while len(nodos) > 1:
        nodos.sort(key=lambda nodo: nodo.frecuencia)
        izquierda = nodos.pop(0)
        derecha = nodos.pop(0)
        nuevo_nodo = NodoHuffman(None, izquierda.frecuencia + derecha.frecuencia)
        nuevo_nodo.izquierda = izquierda
        nuevo_nodo.derecha = derecha
        nodos.append(nuevo_nodo)

    return nodos[0]

def generar_diccionario_huffman(arbol, codigo_actual='', diccionario={}):
    if arbol.simbolo is not None:
        diccionario[arbol.simbolo] = codigo_actual
    if arbol.izquierda is not None:
        generar_diccionario_huffman(arbol.izquierda, codigo_actual + '0', diccionario)
    if arbol.derecha is not None:
        generar_diccionario_huffman(arbol.derecha, codigo_actual + '1', diccionario)
    return diccionario

def codificar_huffman(mensaje_binario):
    frecuencias = contar_frecuencias(mensaje_binario)
    arbol = construir_arbol_huffman(frecuencias)
    diccionario = generar_diccionario_huffman(arbol)
    mensaje_codificado = ''.join(diccionario[byte] for byte in mensaje_binario)
    return mensaje_codificado, diccionario

def decodificar_huffman(mensaje_codificado, diccionario):
    diccionario_inverso = {codigo: simbolo for simbolo, codigo in diccionario.items()}
    mensaje_decodificado = ''
    codigo_actual = ''
    for bit in mensaje_codificado:
        codigo_actual += bit
        if codigo_actual in diccionario_inverso:
            simbolo = diccionario_inverso[codigo_actual]
            mensaje_decodificado += simbolo
            codigo_actual = ''
    return mensaje_decodificado

def mostrar_tabla_huffman(diccionario):
    print("Tabla Huffman:")
    print("Símbolo\tCódigo Huffman")
    for simbolo, codigo in diccionario.items():
        print(f"{simbolo}\t{codigo}")

    # Agregar la creación del archivo .txt
    with open("tabla_huffman.txt", "w") as tabla_file:
        tabla_file.write("Símbolo\tCódigo Huffman\n")
        for simbolo, codigo in diccionario.items():
            tabla_file.write(f"{simbolo}\t{codigo}\n")

"""##SHANON-FANO"""

def contar_frecuencias(datos):
    # Esta función cuenta las frecuencias de cada byte en los datos y devuelve un diccionario
    frecuencias = collections.Counter(datos)

    # Ordenar el diccionario de frecuencias de mayor a menor
    frecuencias_ordenadas = dict(sorted(frecuencias.items(), key=lambda x: x[1], reverse=True))

    return frecuencias_ordenadas

def construir_arbol_shannon_fano(frecuencias):
    # Esta función construye un árbol Shannon-Fano a partir de las frecuencias

    if len(frecuencias) == 0:
        return []

    # Ordenar símbolos por frecuencia descendente
    simbolos_ordenados = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)

    # Caso base: si solo hay un símbolo, devolver el árbol con ese símbolo
    if len(simbolos_ordenados) == 1:
        return [(simbolos_ordenados[0][0], '')]

    # Dividir símbolos en dos grupos aproximadamente iguales
    mitad = len(simbolos_ordenados) // 2
    grupo1 = simbolos_ordenados[:mitad]
    grupo2 = simbolos_ordenados[mitad:]

    # Construir el árbol de forma recursiva
    arbol_grupo1 = construir_arbol_shannon_fano(dict(grupo1))
    arbol_grupo2 = construir_arbol_shannon_fano(dict(grupo2))

    # Asignar '0' a los símbolos en el grupo 1 y '1' al grupo 2
    arbol = [(simbolo, codigo + '0') for simbolo, codigo in arbol_grupo1] + [(simbolo, codigo + '1') for simbolo, codigo in arbol_grupo2]

    return arbol

def comprimir_shannon_fano(datos):
    # Esta función comprime los datos utilizando el algoritmo Shannon-Fano

    frecuencias = contar_frecuencias(datos)
    arbol = construir_arbol_shannon_fano(frecuencias)

    # Construir un diccionario para buscar rápidamente los códigos
    diccionario_codigo = {simbolo: codigo for simbolo, codigo in arbol}

    # Calcular las probabilidades de los símbolos
    total_simbolos = sum(frecuencias.values())
    probabilidades = {simbolo: frecuencia / total_simbolos for simbolo, frecuencia in frecuencias.items()}

    datos_encriptados = []
    codigo_actual = ''

    for byte in datos:
        codigo_actual += diccionario_codigo[byte]

        while len(codigo_actual) >= 8:

            # Dividir y agregar bytes completos al resultado
            byte_cortado = codigo_actual[:8]
            datos_encriptados.append(int(byte_cortado, 2))
            codigo_actual = codigo_actual[8:]

    if codigo_actual:

        # Agregar el último byte (si es que hay alguno)
        datos_encriptados.append(int(codigo_actual, 2))

    # Generar y guardar la tabla de símbolos y probabilidades en un archivo de texto
    with open("tabla_shannon_fano.txt", "w") as tabla_file:
        tabla_file.write("Símbolo\tProbabilidad\n")

        for simbolo, probabilidad in probabilidades.items():
            tabla_file.write(f"{simbolo}\t{probabilidad:.6f}\n")

    return bytes(datos_encriptados), arbol

def descomprimir_shannon_fano(datos, arbol):
    diccionario_simbolo = {codigo: simbolo for simbolo, codigo in arbol}
    datos_binarios = ''.join(format(byte, '08b') for byte in datos)
    datos_desencriptados = []

    codigo_actual = ''

    for bit in datos_binarios:
        codigo_actual += bit

        if codigo_actual in diccionario_simbolo:
            # Se encontró una coincidencia completa, agregar el símbolo al resultado
            simbolo = diccionario_simbolo[codigo_actual]
            datos_desencriptados.append(simbolo)
            codigo_actual = ''  # Reiniciar el código actual

    return datos_desencriptados

"""##ESQUEMA DE COMUNICACIÓN"""

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
  contador_ruido = []
  for pulsaciones in archivo:
    #mensaje_morse.append(pulsaciones)
    if pulsaciones in mensaje_morse and random.random() < probabilidad:
            ruido = random.choice(['.', '-'])
            mensaje_morse.append(ruido)
            contador_ruido.append("Si")
    else:
         mensaje_morse.append(pulsaciones)
         contador_ruido.append("No")
    print(pulsaciones)
    time.sleep(0.5)
  entropiatotal = calculo_entropia(contador_ruido)
  mensaje_distorsionado = ''.join(mensaje_morse)
  print(''.join(mensaje_morse))
  return mensaje_distorsionado,entropiatotal

def calculo_entropia (contador_ruido):
  contador = np.unique(contador_ruido, return_counts=True)
  lista_valores = []
  print (contador)
  tamaño = len(contador_ruido)
  for i in range (len(contador[0])):
    n=contador[1][i]
    probabilidad = n/tamaño
    lista_valores.append(probabilidad)
  entropia = -sum(probabilidad * math.log2(probabilidad) for probabilidad in lista_valores)
  return entropia

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
#print("Entropía de la fuente de información:",calculo_entropia)
mensaje_codificado =codificador(mensaje,MORSE_CODE_DICT)
print("Mensaje codificado:", mensaje_codificado)
mensaje_distorsionado, entropia = canal(mensaje_codificado)
print("Entropía de la fuente de información:",entropia)
receptor(mensaje_distorsionado)

#ALGORITMO HUFFMAN
mensaje_binario,entropia = canal (mensaje)
mensaje_codificado, diccionario = codificar_huffman(mensaje_binario)
mensaje_decodificado = decodificar_huffman(mensaje_codificado, diccionario)

print("Mensaje original:", mensaje_binario)
print("Mensaje codificado:", mensaje_codificado)
print("Mensaje decodificado:", mensaje_decodificado)

mostrar_tabla_huffman(diccionario)

#ALGORITMO SHANON-FANO

datos_originales = canal (mensaje)
datos_comprimidos, arbol_shannon_fano = comprimir_shannon_fano(datos_originales)
datos_descomprimidos = descomprimir_shannon_fano(datos_comprimidos, arbol_shannon_fano)

# Mostrar los resultados
print("Datos originales:", datos_originales)
print("Datos comprimidos:", datos_comprimidos)
print("Datos descomprimidos:", ''.join(str(d) for d in datos_descomprimidos))