"""
entidades.py
Clase abstracta Entidad y clase Cliente con validaciones y encapsulación.
"""
import re                                   # Expresiones regulares para validar correo y teléfono
from abc import ABC, abstractmethod         # Herramientas para clases abstractas
from excepciones import DatoInvalidoError, ParametroFaltanteError


class Entidad(ABC):
    """Representa cualquier elemento general del sistema (clientes, servicios, reservas)."""

    _contador = 0   # Contador compartido para generar identificadores

    def __init__(self):
        Entidad._contador += 1              # Cada entidad nueva aumenta el contador
        self._id = Entidad._contador        # Identificador único (protegido)

    @property
    def id(self):
        """Solo lectura: el id no se puede cambiar desde afuera."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada entidad debe explicar qué es. Se obliga a implementarlo en las hijas."""
        pass

    @abstractmethod
    def validar(self):
        """Cada entidad debe validar sus propios datos."""
        pass


class Cliente(Entidad):
    """Cliente de Software FJ. Sus datos personales son privados y se validan al asignarlos."""

    PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")   # formato básico de correo
    PATRON_TELEFONO = re.compile(r"^3\d{9}$")                   # celular colombiano de 10 dígitos

    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()                  # Se asigna el id desde Entidad
        self.nombre = nombre                # Estas asignaciones pasan por los setters
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self.validar()                      # Validación final del objeto completo

    # ---------- nombre ----------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("nombre")
        if not all(parte.isalpha() for parte in str(valor).split()):
            raise DatoInvalidoError("nombre", valor, "Solo se permiten letras y espacios.")
        self.__nombre = str(valor).strip().title()   # Se guarda con mayúscula inicial

    # ---------- documento ----------
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("documento")
        valor = str(valor).strip()
        if not valor.isdigit() or not 6 <= len(valor) <= 10:
            raise DatoInvalidoError("documento", valor, "Debe tener entre 6 y 10 dígitos.")
        self.__documento = valor

    # ---------- correo ----------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not valor:
            raise ParametroFaltanteError("correo")
        if not self.PATRON_CORREO.match(valor):
            raise DatoInvalidoError("correo", valor, "Formato de correo no válido.")
        self.__correo = valor.lower()

    # ---------- teléfono ----------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = str(valor or "").strip()
        if not self.PATRON_TELEFONO.match(valor):
            raise DatoInvalidoError("telefono", valor, "Debe ser un celular de 10 dígitos que empiece por 3.")
        self.__telefono = valor

    def validar(self):
        """Revisión general: todos los atributos deben existir después de los setters."""
        for campo in ("nombre", "documento", "correo", "telefono"):
            if not getattr(self, campo, None):
                raise ParametroFaltanteError(campo)
        return True

    def describir(self):
        # Se oculta parte del documento para proteger el dato personal
        doc_oculto = "*" * (len(self.documento) - 4) + self.documento[-4:]
        return f"Cliente #{self.id}: {self.nombre} | Doc: {doc_oculto} | {self.correo}"

    def __str__(self):
        return self.describir()
