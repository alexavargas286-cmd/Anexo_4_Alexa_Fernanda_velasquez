"""
gui/pestana_reservas.py
Pestaña para crear, procesar y cancelar reservas.
"""
import tkinter as tk
from tkinter import ttk
from reservas import Reserva
from excepciones import SoftwareFJError, ReservaInvalidaError
from registro_log import log
from gui.pestana_base import PestanaBase
from gui.componentes import TablaDatos, a_numero


class PestanaReservas(PestanaBase):

    @property
    def titulo(self):
        return "Reservas"

    def construir(self):
        form = self._formulario("Nueva reserva")
        self.__cliente = self._campo(form, 0, "Cliente", ttk.Combobox(form, state="readonly", width=28))
        self.__servicio = self._campo(form, 1, "Servicio", ttk.Combobox(form, state="readonly", width=28))
        self.__horas = self._campo(form, 2, "Horas")
        self.__descuento = self._campo(form, 3, "Descuento (%)")
        self.__descuento.insert(0, "0")
        self.__iva = tk.BooleanVar(value=True)
        ttk.Checkbutton(form, text="Incluir IVA (19 %)", variable=self.__iva).grid(row=4, column=1, sticky="w")
        ttk.Button(form, text="Crear y procesar reserva", command=self.crear).grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        ttk.Button(form, text="Cancelar reserva seleccionada", command=self.cancelar).grid(
            row=6, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        self.__ingresos = tk.StringVar(value="Ingresos: $0")
        ttk.Label(form, textvariable=self.__ingresos, font=("Segoe UI", 10, "bold")).grid(
            row=7, column=0, columnspan=2, sticky="w", pady=(16, 0))

        self.__tabla = TablaDatos(self, ("ID", "Cliente", "Servicio", "Horas", "Estado", "Total"),
                                  (45, 160, 160, 60, 100, 110))
        self.__tabla.pack(side="left", fill="both", expand=True)
        self.__tabla.color("PROCESADA", "#1a6e2e")
        self.__tabla.color("CANCELADA", "#a33")

    @staticmethod
    def __buscar(lista, texto):
        """Busca el objeto según la opción elegida en el combo ('id - nombre')."""
        if not texto:
            return None
        id_buscado = int(texto.split(" - ")[0])
        return next((x for x in lista if x.id == id_buscado), None)

    def crear(self):
        reserva = None
        try:
            cliente = self.__buscar(self._gestor.clientes, self.__cliente.get())
            servicio = self.__buscar(self._gestor.servicios, self.__servicio.get())
            if cliente is None or servicio is None:
                raise ReservaInvalidaError("Selecciona un cliente y un servicio.")
            horas = a_numero(self.__horas.get(), "horas")
            descuento = a_numero(self.__descuento.get() or "0", "descuento") / 100
            reserva = Reserva(cliente, servicio, horas)
            reserva.confirmar()
            reserva.procesar(impuesto=self.__iva.get(), descuento=descuento)
        except SoftwareFJError as error:
            causa = f" | Causa: {error.__cause__}" if error.__cause__ else ""
            log.error(f"[GUI] Reserva fallida: {error}{causa}")
            if reserva is not None and reserva.estado == "CONFIRMADA":
                reserva.cancelar()               # No se deja la reserva a medias
            self._error(error)
        else:
            self._exito(f"Reserva #{reserva.id} procesada por ${reserva.total:,.2f}")
        finally:
            if reserva is not None:
                self._gestor.reservas.append(reserva)   # Queda en el historial con su estado
            self._app.refrescar_todo()

    def cancelar(self):
        id_sel = self.__tabla.seleccionado()
        reserva = next((r for r in self._gestor.reservas if r.id == id_sel), None)
        if reserva is None:
            self._app.notificar("Selecciona una reserva de la tabla.", es_error=True)
            return
        try:
            reserva.cancelar()
        except SoftwareFJError as error:
            log.error(f"[GUI] Cancelación rechazada: {error}")
            self._error(error)
        else:
            self._exito(f"Reserva #{reserva.id} cancelada")
        finally:
            self._app.refrescar_todo()

    def refrescar(self):
        # Se actualizan las opciones de los combos con los clientes y servicios actuales
        self.__cliente["values"] = [f"{c.id} - {c.nombre}" for c in self._gestor.clientes]
        self.__servicio["values"] = [f"{s.id} - {s.nombre}" for s in self._gestor.servicios]
        self.__tabla.limpiar()
        for r in self._gestor.reservas:
            self.__tabla.agregar(r.id, (r.id, r.cliente.nombre, r.servicio.nombre, r.horas,
                                        r.estado, f"${r.total:,.2f}"), etiqueta=r.estado)
        ingresos = sum(r.total for r in self._gestor.reservas if r.estado == "PROCESADA")
        self.__ingresos.set(f"Ingresos: ${ingresos:,.2f}")