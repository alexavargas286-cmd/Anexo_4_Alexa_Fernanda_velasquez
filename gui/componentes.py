"""
gui/componentes.py
Componentes reutilizables de la interfaz: la tabla de datos y la conversión de números.
"""
import tkinter as tk
from tkinter import ttk
from excepciones import DatoInvalidoError, ParametroFaltanteError


def a_numero(texto, campo, tipo=float):
    """Convierte el texto de un campo a número. Si falla, encadena el error original."""
    if texto.strip() == "":
        raise ParametroFaltanteError(campo)
    try:
        return tipo(texto.replace(",", "."))
    except ValueError as error:
        # Encadenamiento: el ValueError queda guardado como causa del DatoInvalidoError
        raise DatoInvalidoError(campo, texto, "Debe ser un número.") from error


class TablaDatos(ttk.Frame):
    """Tabla con barra de desplazamiento. Encapsula el Treeview para no repetir código."""

    def __init__(self, padre, columnas, anchos):
        super().__init__(padre)
        self.__arbol = ttk.Treeview(self, columns=columnas, show="headings", selectmode="browse")
        for columna, ancho in zip(columnas, anchos):
            self.__arbol.heading(columna, text=columna)
            self.__arbol.column(columna, width=ancho, anchor="w")
        barra = ttk.Scrollbar(self, orient="vertical", command=self.__arbol.yview)
        self.__arbol.configure(yscrollcommand=barra.set)
        self.__arbol.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

    def limpiar(self):
        """Borra todas las filas."""
        self.__arbol.delete(*self.__arbol.get_children())

    def agregar(self, identificador, valores, etiqueta=""):
        """Agrega una fila. El identificador permite saber qué objeto representa."""
        self.__arbol.insert("", "end", iid=str(identificador), values=valores, tags=(etiqueta,))

    def seleccionado(self):
        """Devuelve el id de la fila seleccionada o None si no hay ninguna."""
        seleccion = self.__arbol.selection()
        return int(seleccion[0]) if seleccion else None

    def color(self, etiqueta, color):
        """Asigna un color de texto a las filas con cierta etiqueta."""
        self.__arbol.tag_configure(etiqueta, foreground=color)