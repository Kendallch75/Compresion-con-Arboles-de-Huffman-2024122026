from bitarray import bitarray
from collections import defaultdict
import heapq
import sys


class NodoHuffman:
    def __init__(self, frecuencia, byte=None, izquierda=None, derecha=None):
        self.frecuencia = frecuencia
        self.byte = byte
        self.izquierda = izquierda
        self.derecha = derecha

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia


def contar_frecuencia_bytes(ruta_archivo):
    frecuencia = defaultdict(int)
    with open(ruta_archivo, 'rb') as archivo:
        datos = bitarray()
        datos.fromfile(archivo)
    bytes_datos = datos.tobytes()
    for byte in bytes_datos:
        frecuencia[byte] += 1
    return frecuencia


def construir_arbol_huffman(frecuencias):
    cola_prioridad = [NodoHuffman(frecuencia=freq, byte=byte)
                      for byte, freq in frecuencias.items()]
    heapq.heapify(cola_prioridad)
    while len(cola_prioridad) > 1:
        izquierda = heapq.heappop(cola_prioridad)
        derecha = heapq.heappop(cola_prioridad)
        combinado = NodoHuffman(frecuencia=izquierda.frecuencia +
                                derecha.frecuencia, izquierda=izquierda, derecha=derecha)
        heapq.heappush(cola_prioridad, combinado)
    return cola_prioridad[0]


def generar_codigos_huffman(nodo, prefijo='', libro_codigos={}):
    if nodo.byte is not None:
        libro_codigos[nodo.byte] = prefijo
    else:
        generar_codigos_huffman(nodo.izquierda, prefijo + '0', libro_codigos)
        generar_codigos_huffman(nodo.derecha, prefijo + '1', libro_codigos)
    return libro_codigos


def comprimir_archivo(ruta_archivo, codigos):
    datos_comprimidos = bitarray()
    with open(ruta_archivo, 'rb') as archivo:
        datos = bitarray()
        datos.fromfile(archivo)
    bytes_datos = datos.tobytes()
    for byte in bytes_datos:
        datos_comprimidos.extend(codigos[byte])
    return datos_comprimidos


def guardar_archivo_comprimido(ruta_original, datos_comprimidos):
    nueva_ruta = ruta_original + '.huff'
    with open(nueva_ruta, 'wb') as archivo:
        datos_comprimidos.tofile(archivo)


def guardar_tabla_huffman(ruta_archivo, codigos):
    ruta_tabla = ruta_archivo + '.table'
    with open(ruta_tabla, 'w') as archivo:
        for byte, codigo in codigos.items():
            archivo.write(f"{byte}:{codigo}\n")


def altura_arbol(nodo):
    if nodo is None:
        return 0
    altura_izquierda = altura_arbol(nodo.izquierda)
    altura_derecha = altura_arbol(nodo.derecha)
    return max(altura_izquierda, altura_derecha) + 1


def anchura_arbol(nodo):
    if nodo is None:
        return 0
    anchura_izquierda = anchura_arbol(nodo.izquierda)
    anchura_derecha = anchura_arbol(nodo.derecha)
    return anchura_izquierda + anchura_derecha + 1


def contar_nodos_arbol(nodo):
    if nodo is None:
        return 0
    contar_izquierda = contar_nodos_arbol(nodo.izquierda)
    contar_derecha = contar_nodos_arbol(nodo.derecha)
    return contar_izquierda + contar_derecha + 1


def guardar_estadisticas_huffman(ruta_archivo, frecuencias, arbol_huffman):
    ruta_estadisticas = ruta_archivo + '.stats'
    altura = altura_arbol(arbol_huffman)
    anchura = anchura_arbol(arbol_huffman)
    cantidad_nodos = contar_nodos_arbol(arbol_huffman)

    with open(ruta_estadisticas, 'w') as archivo:
        archivo.write(f"Altura del árbol: {altura}\n")
        archivo.write(f"Anchura del árbol: {anchura}\n")
        archivo.write(f"Cantidad de nodos en el árbol: {cantidad_nodos}\n\n")
        archivo.write("Tabla de frecuencias original:\n")
        for byte, frecuencia in frecuencias.items():
            archivo.write(f"Byte: {byte}, Frecuencia: {frecuencia}\n")


def main(nombre_archivo):
    frecuencias = contar_frecuencia_bytes(nombre_archivo)
    arbol_huffman = construir_arbol_huffman(frecuencias)
    codigos_huffman = generar_codigos_huffman(arbol_huffman)
    datos_comprimidos = comprimir_archivo(nombre_archivo, codigos_huffman)
    guardar_archivo_comprimido(nombre_archivo, datos_comprimidos)
    guardar_tabla_huffman(nombre_archivo, codigos_huffman)
    guardar_estadisticas_huffman(nombre_archivo, frecuencias, arbol_huffman)


nombre_archivo = sys.argv[1]
main(nombre_archivo)
# Argentian se va a llevar la copa america y Francia la Euro
