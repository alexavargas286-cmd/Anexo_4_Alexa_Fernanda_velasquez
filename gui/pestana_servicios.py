"""
gui/pestana_servicios.py
Pestaña para crear servicios de los tres tipos y cambiar su disponibilidad.
"""
import tkinter as tk
from tkinter import ttk
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import SoftwareFJError
from registro_log import log
from gui.pestana_base import PestanaBase
from gui.componentes import TablaDatos, a_numero

# Nombre visible -> (clase, campo extra, etiqueta del campo)
TIPOS_SERVICIO = {
    "Reserva de sala": (ReservaSala, "capacidad", "Capacidad (personas)"),
    "Alquiler de equipo": (AlquilerEquipo, "cantidad", "Cantidad de equipos"),
    "Asesoría especializada": (AsesoriaEspecializada, "nivel", "Nivel"),
}


class PestanaServicios(PestanaBase):

    @property
    def titulo(self):
        return "Servicios"

    def construir(self):
        form = self._formulario("Crear servicio")
        self.__tipo = self._campo(form, 0, "Tipo", ttk.Combobox(form, values=list(TIPOS_SERVICIO),
                                                               state="readonly", width=28))
        self.__tipo.current(0)
        self.__tipo.bind("<<ComboboxSelected>>", lambda evento: self.__cambiar_tipo())
        self.__nombre = self._campo(form, 1, "Nombre")
        self.__tarifa = self._campo(form, 2, "Tarifa base por hora")
        self.__lbl_extra = ttk.Label(form)
        self.__lbl_extra.grid(row=3, column=0, sticky="w", pady=4)
        self.__extra = ttk.Entry(form, width=30)
        self.__nivel = ttk.Combobox(form, values=list(AsesoriaEspecializada.NIVELES),
                                    state="readonly", width=28)
        self.__nivel.current(0)
        self.__disponible = tk.BooleanVar(value=True)
        ttk.Checkbutton(form, text="Disponible", variable=self.__disponible).grid(row=4, column=1, sticky="w")
        ttk.Button(form, text="Crear servicio", command=self.crear).grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        ttk.Button(form, text="Cambiar disponibilidad del seleccionado",
                   command=self.alternar_disponibilidad).grid(row=6, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        self.__cambiar_tipo()

        self.__tabla = TablaDatos(self, ("ID", "Tipo", "Nombre", "Detalle", "Valor/hora", "Disponible"),
                                  (45, 150, 150, 120, 100, 80))
        self.__tabla.pack(side="left", fill="both", expand=True)

    def __cambiar_tipo(self):
        """Muestra el campo extra que corresponde al tipo elegido."""
        _, campo, etiqueta = TIPOS_SERVICIO[self.__tipo.get()]
        self.__lbl_extra.config(text=etiqueta)
        self.__extra.grid_forget()
        self.__nivel.grid_forget()
        (self.__nivel if campo == "nivel" else self.__extra).grid(row=3, column=1, sticky="ew", pady=4)

    def crear(self):
        clase, campo, _ = TIPOS_SERVICIO[self.__tipo.get()]
        try:
            tarifa = a_numero(self.__tarifa.get(), "tarifa_base")
            extra = self.__nivel.get() if campo == "nivel" else a_numero(self.__extra.get(), campo, int)
            # Polimorfismo: la misma línea crea cualquiera de los tres servicios
            servicio = clase(self.__nombre.get().strip(), tarifa, extra, disponible=self.__disponible.get())
        except SoftwareFJError as error:
            log.error(f"[GUI] No se pudo crear el servicio: {error}")
            self._error(error)
        else:
            self._gestor.servicios.append(servicio)
            log.info(f"[GUI] Servicio creado: {servicio.describir()}")
            self._exito(f"Servicio creado: {servicio.nombre}")
        finally:
            self._app.refrescar_todo()

    def alternar_disponibilidad(self):
        id_sel = self.__tabla.seleccionado()
        servicio = next((s for s in self._gestor.servicios if s.id == id_sel), None)
        if servicio is None:
            self._app.notificar("Selecciona un servicio de la tabla.", es_error=True)
            return
        servicio.cambiar_disponibilidad(not servicio.disponible)
        estado = "disponible" if servicio.disponible else "no disponible"
        log.info(f"[GUI] Servicio '{servicio.nombre}' ahora {estado}")
        self._exito(f"'{servicio.nombre}' quedó {estado}")
        self._app.refrescar_todo()

    @staticmethod
    def __detalle(servicio):
        if isinstance(servicio, ReservaSala):
            return f"{servicio.capacidad} personas"
        if isinstance(servicio, AlquilerEquipo):
            return f"{servicio.cantidad} unidades"
        return f"nivel {servicio.nivel}"

    def refrescar(self):
        nombres = {datos[0]: nombre for nombre, datos in TIPOS_SERVICIO.items()}
        self.__tabla.limpiar()
        for s in self._gestor.servicios:
            self.__tabla.agregar(s.id, (s.id, nombres[type(s)], s.nombre, self.__detalle(s),
                                        f"${s.costo_por_hora():,.0f}", "Sí" if s.disponible else "No"))