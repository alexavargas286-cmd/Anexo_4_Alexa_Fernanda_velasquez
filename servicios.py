"""
servicios.py
Clase abstracta Servicio y tres servicios especializados.
Aquí está el polimorfismo (cada servicio calcula el costo a su manera)
y la sobrecarga del método calcular_costo.
"""
from abc import abstractmethod
from entidades import Entidad
from excepciones import DatoInvalidoError, CalculoInconsistenteError, ParametroFaltanteError

IVA = 0.19   # Impuesto que se aplica cuando se pide el costo con impuestos


class Servicio(Entidad):
    """Servicio genérico. No se puede instanciar directamente."""

    def __init__(self, nombre, tarifa_base, disponible=True):
        super().__init__()
        if not nombre:
            raise ParametroFaltanteError("nombre del servicio")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatoInvalidoError("tarifa_base", tarifa_base, "Debe ser un número mayor que cero.")
        self._nombre = nombre
        self._tarifa_base = float(tarifa_base)
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        self._disponible = bool(estado)

    @abstractmethod
    def costo_por_hora(self):
        """Cada servicio define su propio valor por hora (polimorfismo)."""
        pass

    @abstractmethod
    def validar_parametros(self, horas):
        """Cada servicio tiene sus propias reglas sobre la duración."""
        pass

    def calcular_costo(self, horas, *, impuesto=False, descuento=0.0):
        """
        Método "sobrecargado". Python no permite varias firmas con el mismo nombre,
        así que la sobrecarga se simula con parámetros opcionales:
          calcular_costo(h)                      -> costo simple
          calcular_costo(h, impuesto=True)       -> costo + IVA
          calcular_costo(h, descuento=0.1)       -> costo con descuento
          calcular_costo(h, impuesto=True, descuento=0.1) -> ambas cosas
        """
        self.validar_parametros(horas)                 # Primero se validan las horas
        if not 0 <= descuento < 1:
            raise DatoInvalidoError("descuento", descuento, "Debe estar entre 0 y 0.99.")
        total = self.costo_por_hora() * horas          # Costo según el tipo de servicio
        total -= total * descuento                     # Se resta el descuento
        if impuesto:
            total += total * IVA                       # Se suma el IVA si se pidió
        if total <= 0:
            raise CalculoInconsistenteError(f"El costo calculado para '{self.nombre}' no es válido: {total}")
        return round(total, 2)

    def validar(self):
        return self._tarifa_base > 0

    def __str__(self):
        return self.describir()


class ReservaSala(Servicio):
    """Reserva de salas de reuniones. El costo depende de la capacidad."""

    def __init__(self, nombre, tarifa_base, capacidad, disponible=True):
        super().__init__(nombre, tarifa_base, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("capacidad", capacidad, "Debe ser un entero positivo.")
        self.capacidad = capacidad

    def costo_por_hora(self):
        # Salas de más de 20 personas tienen un recargo del 25 %
        return self._tarifa_base * (1.25 if self.capacidad > 20 else 1)

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 12:
            raise DatoInvalidoError("horas", horas, "Una sala se reserva entre 1 y 12 horas.")

    def describir(self):
        return f"Sala '{self.nombre}' (capacidad {self.capacidad}) - ${self.costo_por_hora():,.0f}/h"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos (portátiles, video beam, etc.). Se cobra por unidad."""

    def __init__(self, nombre, tarifa_base, cantidad, disponible=True):
        super().__init__(nombre, tarifa_base, disponible)
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise DatoInvalidoError("cantidad", cantidad, "Debe ser un entero positivo.")
        self.cantidad = cantidad

    def costo_por_hora(self):
        return self._tarifa_base * self.cantidad

    def validar_parametros(self, horas):
        # Los equipos se alquilan mínimo 2 horas y máximo 72 (tres días)
        if not isinstance(horas, (int, float)) or not 2 <= horas <= 72:
            raise DatoInvalidoError("horas", horas, "Los equipos se alquilan entre 2 y 72 horas.")

    def describir(self):
        return f"Alquiler de {self.cantidad} x '{self.nombre}' - ${self.costo_por_hora():,.0f}/h"


class AsesoriaEspecializada(Servicio):
    """Asesoría con un especialista. El nivel del asesor cambia el valor."""

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre, tarifa_base, nivel, disponible=True):
        super().__init__(nombre, tarifa_base, disponible)
        if nivel not in self.NIVELES:
            raise DatoInvalidoError("nivel", nivel, f"Opciones: {', '.join(self.NIVELES)}.")
        self.nivel = nivel

    def costo_por_hora(self):
        return self._tarifa_base * self.NIVELES[self.nivel]

    def validar_parametros(self, horas):
        # Las asesorías van de media hora en media hora, hasta 8 horas
        if not isinstance(horas, (int, float)) or horas <= 0 or horas > 8 or (horas * 2) % 1 != 0:
            raise DatoInvalidoError("horas", horas, "Asesorías de 0.5 a 8 horas, en bloques de media hora.")

    def describir(self):
        return f"Asesoría '{self.nombre}' nivel {self.nivel} - ${self.costo_por_hora():,.0f}/h"
