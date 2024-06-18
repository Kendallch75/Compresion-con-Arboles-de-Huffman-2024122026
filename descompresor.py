from bitarray import bitarray
from collections import defaultdict
import sys


class NodoHuffman:
    def __init__(self, frecuencia, byte=None, izquierda=None, derecha=None):
        self.frecuencia = frecuencia
        self.byte = byte
        self.izquierda = izquierda
        self.derecha = derecha

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia


def leer_tabla_huffman(ruta_tabla):
    tabla_codigos = {}
    with open(ruta_tabla, 'r') as archivo:
        for linea in archivo:
            byte, codigo = linea.strip().split(':')
            tabla_codigos[int(byte)] = codigo
    return tabla_codigos


def reconstruir_arbol_huffman(tabla_codigos):
    raiz = NodoHuffman(0)
    for byte, codigo in tabla_codigos.items():
        nodo_actual = raiz
        for bit in codigo:
            if bit == '0':
                if nodo_actual.izquierda is None:
                    nodo_actual.izquierda = NodoHuffman(0)
                nodo_actual = nodo_actual.izquierda
            else:
                if nodo_actual.derecha is None:
                    nodo_actual.derecha = NodoHuffman(0)
                nodo_actual = nodo_actual.derecha
        nodo_actual.byte = byte
    return raiz


def descomprimir_archivo(ruta_comprimida, arbol_huffman, ruta_salida):
    with open(ruta_comprimida, 'rb') as archivo_comprimido:
        datos_comprimidos = bitarray()
        datos_comprimidos.fromfile(archivo_comprimido)
    datos_descomprimidos = bytearray()
    nodo_actual = arbol_huffman
    for bit in datos_comprimidos:
        if bit == 0:
            nodo_actual = nodo_actual.izquierda
        else:
            nodo_actual = nodo_actual.derecha
        if nodo_actual.byte is not None:
            datos_descomprimidos.append(nodo_actual.byte)
            nodo_actual = arbol_huffman
    with open(ruta_salida, 'wb') as archivo_salida:
        archivo_salida.write(datos_descomprimidos)


ruta_archivo_comprimido = sys.argv[1]
ruta_tabla_huffman = sys.argv[2]
ruta_archivo_salida = sys.argv[3]

tabla_codigos = leer_tabla_huffman(ruta_tabla_huffman)
arbol_huffman = reconstruir_arbol_huffman(tabla_codigos)
descomprimir_archivo(ruta_archivo_comprimido,
                     arbol_huffman, ruta_archivo_salida)

print("Archivo descomprimido con éxito.")
