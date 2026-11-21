"""
sistema.py
Clase GestorSoftwareFJ: guarda clientes, servicios y reservas en listas internas
(sin base de datos) y centraliza el manejo de errores.
"""
from entidades import Cliente
from reservas import Reserva
from excepciones import SoftwareFJError, ReservaInvalidaError
from registro_log import log


class GestorSoftwareFJ:
    def __init__(self):
        self.clientes = []     # Lista interna de clientes
        self.servicios = []    # Lista interna de servicios
        self.reservas = []     # Lista interna de reservas

    def registrar_cliente(self, **datos):
        """Intenta crear un cliente. Si falla, se registra el error y se devuelve None."""
        try:
            cliente = Cliente(**datos)
        except TypeError as error:
            # Ocurre si faltan argumentos al llamar el constructor
            log.error(f"Registro de cliente con parámetros incompletos: {error}")
            print(f"  ✗ Error: parámetros incompletos ({error})")
            return None
        except SoftwareFJError as error:
            log.error(f"Registro de cliente rechazado: {error}")
            print(f"  ✗ Error: {error}")
            return None
        else:
            if any(c.documento == cliente.documento for c in self.clientes):
                log.warning(f"Documento duplicado: {cliente.documento}")
                print("  ✗ Error: ya existe un cliente con ese documento")
                return None
            self.clientes.append(cliente)
            log.info(f"Cliente registrado: {cliente.nombre}")
            print(f"  ✓ {cliente}")
            return cliente

    def crear_servicio(self, clase_servicio, *args, **kwargs):
        """Crea cualquier tipo de servicio (polimorfismo: recibe la clase como parámetro)."""
        try:
            servicio = clase_servicio(*args, **kwargs)
        except (SoftwareFJError, TypeError) as error:
            log.error(f"No se pudo crear el servicio {clase_servicio.__name__}: {error}")
            print(f"  ✗ Error: {error}")
            return None
        self.servicios.append(servicio)
        log.info(f"Servicio creado: {servicio.describir()}")
        print(f"  ✓ {servicio}")
        return servicio

    def crear_reserva(self, cliente, servicio, horas, impuesto=True, descuento=0.0):
        """Crea, confirma y procesa una reserva completa. Ningún error detiene el programa."""
        reserva = None
        try:
            if cliente is None or servicio is None:
                raise ReservaInvalidaError("No se puede reservar con un cliente o servicio inexistente.")
            reserva = Reserva(cliente, servicio, horas)
            reserva.confirmar()
            reserva.procesar(impuesto=impuesto, descuento=descuento)
        except SoftwareFJError as error:
            # Si hay una causa original (encadenamiento), también se registra
            causa = f" | Causa: {error.__cause__}" if error.__cause__ else ""
            log.error(f"Reserva fallida: {error}{causa}")
            print(f"  ✗ Error: {error}{causa}")
            if reserva and reserva.estado == "CONFIRMADA":
                reserva.cancelar()      # Se cancela para no dejarla a medias
        except Exception as error:
            # Red de seguridad para cualquier error no previsto
            log.critical(f"Error inesperado al reservar: {error!r}")
            print(f"  ✗ Error inesperado: {error!r}")
        else:
            print(f"  ✓ {reserva}")
        finally:
            if reserva is not None:
                self.reservas.append(reserva)   # Se guarda para el historial, sea cual sea su estado
        return reserva

    def resumen(self):
        print("\n========== RESUMEN ==========")
        print(f"Clientes registrados: {len(self.clientes)}")
        print(f"Servicios creados:    {len(self.servicios)}")
        print(f"Reservas totales:     {len(self.reservas)}")
        procesadas = [r for r in self.reservas if r.estado == "PROCESADA"]
        print(f"Reservas procesadas:  {len(procesadas)}")
        print(f"Ingresos:             ${sum(r.total for r in procesadas):,.2f}")
