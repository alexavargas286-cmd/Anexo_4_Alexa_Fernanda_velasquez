"""
gui/pestana_base.py
Clase abstracta de la que heredan todas las pestañas de la interfaz.
"""
from abc import ABC, abstractmethod
from tkinter import ttk


class PestanaBase(ttk.Frame, ABC):
    """
    Define lo que toda pestaña debe tener:
      - un título para mostrar en el Notebook
      - construir()  -> arma sus controles
      - refrescar()  -> vuelve a pintar sus datos (polimorfismo)
    """

    def __init__(self, app):
        super().__init__(app.pestanas, padding=10)
        self._app = app                      # Referencia a la ventana principal
        self._gestor = app.gestor            # Acceso a las listas internas del sistema
        self.construir()

    @property
    @abstractmethod
    def titulo(self):
        """Texto que aparece en la pestaña."""
        pass

    @abstractmethod
    def construir(self):
        """Cada pestaña arma sus propios controles."""
        pass

    @abstractmethod
    def refrescar(self):
        """Cada pestaña sabe cómo actualizar lo que muestra."""
        pass

    # ---- métodos comunes heredados por todas las pestañas ----
    def _campo(self, padre, fila, texto, widget=None):
        """Crea una etiqueta y un control en la fila indicada del formulario."""
        ttk.Label(padre, text=texto).grid(row=fila, column=0, sticky="w", pady=4)
        widget = widget or ttk.Entry(padre, width=30)
        widget.grid(row=fila, column=1, sticky="ew", pady=4)
        return widget

    def _formulario(self, titulo):
        """Marco de la izquierda donde van los campos."""
        marco = ttk.LabelFrame(self, text=titulo, padding=10)
        marco.pack(side="left", fill="y", padx=(0, 10))
        return marco

    def _exito(self, texto):
        self._app.notificar(texto)

    def _error(self, error):
        """Muestra el error con su causa (si viene encadenado)."""
        causa = f"\nCausa: {error.__cause__}" if getattr(error, "__cause__", None) else ""
        self._app.notificar(f"{error}{causa}", es_error=True)