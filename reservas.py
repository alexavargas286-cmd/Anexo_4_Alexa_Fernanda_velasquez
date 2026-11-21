"""
reservas.py
Clase Reserva: une cliente, servicio y duración, y maneja sus estados.
"""
from entidades import Entidad, Cliente
from servicios import Servicio
from excepciones import (ReservaInvalidaError, OperacionNoPermitidaError,
                         ServicioNoDisponibleError, SoftwareFJError, CalculoInconsistenteError)
from registro_log import log


class Reserva(Entidad):
    """Una reserva pasa por los estados: PENDIENTE -> CONFIRMADA -> PROCESADA, o CANCELADA."""

    def __init__(self, cliente, servicio, horas):
        super().__init__()
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un servicio válido.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(servicio.nombre)
        servicio.validar_parametros(horas)       # Puede lanzar DatoInvalidoError
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "PENDIENTE"
        self.total = 0.0

    def confirmar(self):
        if self.estado != "PENDIENTE":
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva en estado {self.estado}.")
        self.estado = "CONFIRMADA"
        log.info(f"Reserva #{self.id} confirmada para {self.cliente.nombre}")

    def cancelar(self):
        if self.estado in ("CANCELADA", "PROCESADA"):
            raise OperacionNoPermitidaError(f"La reserva #{self.id} ya está {self.estado} y no se puede cancelar.")
        self.estado = "CANCELADA"
        log.info(f"Reserva #{self.id} cancelada")

    def procesar(self, impuesto=True, descuento=0.0):
        """
        Calcula el total y deja la reserva como PROCESADA.
        Usa try/except/else/finally y encadena la excepción si el cálculo falla.
        """
        if self.estado != "CONFIRMADA":
            raise OperacionNoPermitidaError("Solo se procesan reservas confirmadas.")
        try:
            total = self.servicio.calcular_costo(self.horas, impuesto=impuesto, descuento=descuento)
        except SoftwareFJError as error:
            # Encadenamiento: se lanza un error nuevo pero se conserva la causa original
            raise CalculoInconsistenteError(f"No se pudo procesar la reserva #{self.id}") from error
        else:
            # Solo entra aquí si el cálculo salió bien
            self.total = total
            self.estado = "PROCESADA"
            log.info(f"Reserva #{self.id} procesada. Total: ${total:,.2f}")
        finally:
            # Siempre se deja constancia del intento, haya funcionado o no
            log.info(f"Intento de procesamiento de la reserva #{self.id} finalizado (estado: {self.estado})")
        return self.total

    def validar(self):
        return self.estado in ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")

    def describir(self):
        return (f"Reserva #{self.id} | {self.cliente.nombre} | {self.servicio.nombre} | "
                f"{self.horas} h | {self.estado} | ${self.total:,.2f}")

    def __str__(self):
        return self.describir()
