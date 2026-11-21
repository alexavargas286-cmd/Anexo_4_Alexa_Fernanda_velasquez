"""
gui/pestana_clientes.py
Pestaña para registrar clientes y verlos en una tabla.
"""
from tkinter import ttk
from entidades import Cliente
from excepciones import SoftwareFJError, DatoInvalidoError
from registro_log import log
from gui.pestana_base import PestanaBase
from gui.componentes import TablaDatos


class PestanaClientes(PestanaBase):

    @property
    def titulo(self):
        return "Clientes"

    def construir(self):
        form = self._formulario("Registrar cliente")
        self.__nombre = self._campo(form, 0, "Nombre completo")
        self.__documento = self._campo(form, 1, "Documento")
        self.__correo = self._campo(form, 2, "Correo")
        self.__telefono = self._campo(form, 3, "Celular")
        ttk.Button(form, text="Registrar", command=self.registrar).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        self.__tabla = TablaDatos(self, ("ID", "Nombre", "Documento", "Correo", "Celular"),
                                  (50, 180, 110, 200, 110))
        self.__tabla.pack(side="left", fill="both", expand=True)

    def registrar(self):
        try:
            cliente = Cliente(nombre=self.__nombre.get(), documento=self.__documento.get(),
                              correo=self.__correo.get().strip(), telefono=self.__telefono.get())
            if any(c.documento == cliente.documento for c in self._gestor.clientes):
                raise DatoInvalidoError("documento", cliente.documento, "Ya existe un cliente con ese documento.")
        except SoftwareFJError as error:
            log.error(f"[GUI] Registro de cliente rechazado: {error}")
            self._error(error)
        else:
            self._gestor.clientes.append(cliente)
            log.info(f"[GUI] Cliente registrado: {cliente.nombre}")
            for campo in (self.__nombre, self.__documento, self.__correo, self.__telefono):
                campo.delete(0, "end")
            self._exito(f"Cliente registrado: {cliente.nombre}")
        finally:
            self._app.refrescar_todo()          # Todas las pestañas se actualizan

    def refrescar(self):
        self.__tabla.limpiar()
        for c in self._gestor.clientes:
            doc_oculto = "*" * (len(c.documento) - 4) + c.documento[-4:]
            self.__tabla.agregar(c.id, (c.id, c.nombre, doc_oculto, c.correo, c.telefono))