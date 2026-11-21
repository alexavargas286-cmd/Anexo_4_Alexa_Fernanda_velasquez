"""
gui/aplicacion.py
Ventana principal. Crea las pestañas y las coordina.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from sistema import GestorSoftwareFJ
from registro_log import log
from gui.pestana_clientes import PestanaClientes
from gui.pestana_servicios import PestanaServicios
from gui.pestana_reservas import PestanaReservas
from gui.pestana_log import PestanaLog


class AppSoftwareFJ(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Software FJ - Gestión de clientes, servicios y reservas")
        self.geometry("980x620")
        self.minsize(860, 540)
        self.__configurar_estilo()
        self.gestor = GestorSoftwareFJ()          # Listas internas, sin base de datos

        ttk.Label(self, text="Software FJ", style="Titulo.TLabel").pack(anchor="w", padx=12, pady=(10, 0))
        self.pestanas = ttk.Notebook(self)
        self.pestanas.pack(fill="both", expand=True, padx=10, pady=8)

        # Todas son PestanaBase: se crean y se agregan de la misma forma
        self.__lista_pestanas = [clase(self) for clase in
                                 (PestanaClientes, PestanaServicios, PestanaReservas, PestanaLog)]
        for pestana in self.__lista_pestanas:
            self.pestanas.add(pestana, text=pestana.titulo)

        self.__estado = tk.StringVar(value="Listo.")
        ttk.Label(self, textvariable=self.__estado, anchor="w", relief="sunken",
                  padding=(8, 3)).pack(fill="x", side="bottom")

        log.info("Interfaz gráfica iniciada")
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.refrescar_todo()

    def __configurar_estilo(self):
        estilo = ttk.Style(self)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("Treeview", rowheight=24)
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 14, "bold"))

    def refrescar_todo(self):
        """Polimorfismo: cada pestaña sabe refrescarse a su manera."""
        for pestana in self.__lista_pestanas:
            pestana.refrescar()

    def notificar(self, texto, es_error=False):
        """Muestra el mensaje en la barra de estado; si es error, también en una ventana."""
        self.__estado.set(("✗ " if es_error else "✓ ") + texto.replace("\n", " "))
        if es_error:
            messagebox.showerror("Error", texto)

    def cerrar(self):
        log.info("Interfaz gráfica cerrada")
        self.destroy()