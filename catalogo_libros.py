import json
import os
from libro import Libro
from nodo_libro import NodoLibro
class CatalogoLibros:
    def __init__(self, archivo):
        self.raiz = None
        self.archivo = archivo
        self.cargar_datos()

    def cargar_datos(self):
        if not os.path.exists(self.archivo):
            # Si el archivo no existe, crea un árbol vacío y guarda los datos
            self.raiz = None
            self.guardar_datos()
            return

        try:
            with open(self.archivo, 'r') as file:
                data = json.load(file)
                self.raiz = self._cargar_datos(data)
        except FileNotFoundError:
            pass

    def _cargar_datos(self, data):
        if data is None:
            return None

        nodo = NodoLibro(Libro(data['isbn'], data['titulo'], data['autor']))
        nodo.izquierda = self._cargar_datos(data.get('izquierda'))
        nodo.derecha = self._cargar_datos(data.get('derecha'))

        return nodo

    def guardar_datos(self):
        data = self._obtener_datos(self.raiz)
        with open(self.archivo, 'w') as file:
            json.dump(data, file, indent=2)

    def _obtener_datos(self, nodo):
        if nodo is None:
            return None

        data = {
            'isbn': nodo.libro.isbn,
            'titulo': nodo.libro.titulo,
            'autor': nodo.libro.autor,
            'izquierda': self._obtener_datos(nodo.izquierda),
            'derecha': self._obtener_datos(nodo.derecha)
        }

        return data

    def insertar_libro(self, libro):
        self.raiz = self._insertar_libro(self.raiz, libro)

    def _insertar_libro(self, nodo, libro):
        if nodo is None:
            return NodoLibro(libro)
        
        if libro.isbn < nodo.libro.isbn:
            nodo.izquierda = self._insertar_libro(nodo.izquierda, libro)
        elif libro.isbn > nodo.libro.isbn:
            nodo.derecha = self._insertar_libro(nodo.derecha, libro)
        
        return nodo

    def buscar_libro(self, isbn):
        return self._buscar_libro(self.raiz, isbn)

    def _buscar_libro(self, nodo, isbn):
        if nodo is None or nodo.libro.isbn == isbn:
            return nodo.libro if nodo else None

        if isbn < nodo.libro.isbn:
            return self._buscar_libro(nodo.izquierda, isbn)
        else:
            return self._buscar_libro(nodo.derecha, isbn)

    def eliminar_libro(self, isbn):
        self.raiz = self._eliminar_libro(self.raiz, isbn)

    def _eliminar_libro(self, nodo, isbn):
        if nodo is None:
            return nodo

        if isbn < nodo.libro.isbn:
            nodo.izquierda = self._eliminar_libro(nodo.izquierda, isbn)
        elif isbn > nodo.libro.isbn:
            nodo.derecha = self._eliminar_libro(nodo.derecha, isbn)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda

            nodo.libro = self._min_valor(nodo.derecha)
            nodo.derecha = self._eliminar_libro(nodo.derecha, nodo.libro.isbn)

        return nodo

    def _min_valor(self, nodo):
        while nodo.izquierda is not None:
            nodo = nodo.izquierda
        return nodo.libro

    def mostrar_catalogo_ordenado(self):
        catalogo = []
        self._inorden(self.raiz, catalogo.append)
        return catalogo

    def _inorden(self, nodo, visitar):
        if nodo is not None:
            self._inorden(nodo.izquierda, visitar)
            visitar(nodo.libro)
            self._inorden(nodo.derecha, visitar)
