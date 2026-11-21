"""
gui/pestana_log.py
Pestaña que muestra el contenido del archivo de log.
"""
import tkinter as tk
from tkinter import ttk
from registro_log import ARCHIVO_LOG
from gui.pestana_base import PestanaBase


class PestanaLog(PestanaBase):

    MAX_LINEAS = 500   # Solo se muestran las últimas líneas para no saturar la vista

    @property
    def titulo(self):
        return "Registro (log)"

    def construir(self):
        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(0, 6))
        ttk.Label(barra, text=f"Archivo: {ARCHIVO_LOG}").pack(side="left")
        ttk.Button(barra, text="Actualizar", command=self.refrescar).pack(side="right")
        self.__texto = tk.Text(self, wrap="none", font=("Consolas", 9), state="disabled")
        desplazar = ttk.Scrollbar(self, orient="vertical", command=self.__texto.yview)
        self.__texto.configure(yscrollcommand=desplazar.set)
        desplazar.pack(side="right", fill="y")
        self.__texto.pack(fill="both", expand=True)
        self.__texto.tag_configure("ERROR", foreground="#b00020")
        self.__texto.tag_configure("WARNING", foreground="#9a6700")

    @staticmethod
    def __leer_archivo():
        """Lee el log. Si todavía no existe, devuelve una lista vacía."""
        try:
            with open(ARCHIVO_LOG, encoding="utf-8") as archivo:
                return archivo.readlines()
        except FileNotFoundError:
            return []

    def refrescar(self):
        self.__texto.configure(state="normal")
        self.__texto.delete("1.0", "end")
        for linea in self.__leer_archivo()[-self.MAX_LINEAS:]:
            if "| ERROR" in linea or "| CRITICAL" in linea:
                etiqueta = "ERROR"
            elif "| WARNING" in linea:
                etiqueta = "WARNING"
            else:
                etiqueta = ""
            self.__texto.insert("end", linea, etiqueta)
        self.__texto.configure(state="disabled")
        self.__texto.see("end")