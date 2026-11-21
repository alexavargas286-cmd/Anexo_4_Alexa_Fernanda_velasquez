"""
excepciones.py
Excepciones personalizadas del sistema Software FJ.
Todas heredan de SoftwareFJError para poder capturarlas en un solo bloque si hace falta.
"""


class SoftwareFJError(Exception):
    """Excepción base del sistema. Guarda un código para identificar el tipo de error en el log."""

    def __init__(self, mensaje, codigo="FJ-000"):
        super().__init__(mensaje)          # Se pasa el mensaje a la clase Exception
        self.codigo = codigo               # Código interno del error

    def __str__(self):
        # Se muestra el código junto al mensaje para que el log sea más fácil de leer
        return f"[{self.codigo}] {super().__str__()}"


class DatoInvalidoError(SoftwareFJError):
    """Se lanza cuando un dato no cumple el formato o las reglas esperadas."""

    def __init__(self, campo, valor, detalle=""):
        mensaje = f"Dato inválido en '{campo}': {valor!r}. {detalle}".strip()
        super().__init__(mensaje, "FJ-100")
        self.campo = campo


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio."""

    def __init__(self, parametro):
        super().__init__(f"Falta el parámetro obligatorio '{parametro}'", "FJ-110")


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio que no está disponible."""

    def __init__(self, nombre_servicio):
        super().__init__(f"El servicio '{nombre_servicio}' no está disponible", "FJ-200")


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no se puede crear por datos incorrectos."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-300")


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una acción que el estado actual no permite."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-310")


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando el cálculo de un costo da un resultado sin sentido (negativo, etc.)."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-400")
