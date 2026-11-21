"""
main.py
Clase principal del sistema Software FJ.
Uso:  python main.py             -> abre la interfaz gráfica
      python main.py --consola   -> simulación de las 20 operaciones en consola
"""
import sys
from sistema import GestorSoftwareFJ
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from registro_log import log, ARCHIVO_LOG


class Main:
    """Punto de entrada del sistema Software FJ."""

    def __init__(self):
        self.__gestor = GestorSoftwareFJ()     # Listas internas, sin base de datos

    @staticmethod
    def __titulo(numero, texto):
        print(f"\nOperación {numero}: {texto}")

    def simular(self):
        """Ejecuta las 20 operaciones válidas e inválidas."""
        g, t = self.__gestor, self.__titulo
        log.info("===== Inicio de la simulación Software FJ =====")

        # ---------- CLIENTES ----------
        t(1, "Registrar cliente válido")
        ana = g.registrar_cliente(nombre="ana lucía torres", documento="1121456789",
                                  correo="ana.torres@gmail.com", telefono="3104567890")
        t(2, "Registrar cliente válido")
        jorge = g.registrar_cliente(nombre="Jorge Rincón", documento="86012345",
                                    correo="jrincon@hotmail.com", telefono="3209876543")
        t(3, "Cliente con correo inválido")
        g.registrar_cliente(nombre="Pedro Gómez", documento="12345678",
                            correo="pedro.gomez.com", telefono="3001112233")
        t(4, "Cliente con nombre vacío")
        g.registrar_cliente(nombre="", documento="99887766", correo="x@y.com", telefono="3001112233")
        t(5, "Cliente sin teléfono (parámetro faltante)")
        g.registrar_cliente(nombre="Laura Díaz", documento="55443322", correo="laura@gmail.com")
        t(6, "Cliente con documento duplicado")
        g.registrar_cliente(nombre="Ana Torres", documento="1121456789",
                            correo="otra@gmail.com", telefono="3110000000")

        # ---------- SERVICIOS ----------
        t(7, "Crear sala válida")
        sala = g.crear_servicio(ReservaSala, "Sala Guaviare", 50000, capacidad=30)
        t(8, "Crear alquiler de equipo válido")
        portatiles = g.crear_servicio(AlquilerEquipo, "Portátil Lenovo", 8000, cantidad=5)
        t(9, "Crear asesoría válida")
        asesoria = g.crear_servicio(AsesoriaEspecializada, "Ciberseguridad", 90000, nivel="senior")
        t(10, "Servicio con tarifa negativa")
        g.crear_servicio(ReservaSala, "Sala Fantasma", -20000, capacidad=10)
        t(11, "Asesoría con nivel inexistente")
        g.crear_servicio(AsesoriaEspecializada, "Redes", 70000, nivel="master")
        t(12, "Servicio que se marca como no disponible")
        auditorio = g.crear_servicio(ReservaSala, "Auditorio", 120000, capacidad=80, disponible=False)

        # ---------- RESERVAS ----------
        t(13, "Reserva válida de sala con IVA")
        g.crear_reserva(ana, sala, 3)
        t(14, "Reserva válida de equipos con descuento del 10 %")
        g.crear_reserva(jorge, portatiles, 8, descuento=0.10)
        t(15, "Reserva de asesoría sin IVA")
        g.crear_reserva(ana, asesoria, 1.5, impuesto=False)
        t(16, "Reserva de un servicio no disponible")
        g.crear_reserva(jorge, auditorio, 2)
        t(17, "Reserva con horas fuera de rango")
        g.crear_reserva(ana, sala, 20)
        t(18, "Reserva con cliente inexistente")
        g.crear_reserva(None, sala, 2)
        t(19, "Reserva con descuento inválido (error encadenado)")
        g.crear_reserva(jorge, asesoria, 2, descuento=1.5)
        t(20, "Intentar cancelar una reserva ya procesada")
        try:
            g.reservas[0].cancelar()
        except Exception as error:
            log.error(f"Cancelación rechazada: {error}")
            print(f"  ✗ Error: {error}")

        g.resumen()
        log.info("===== Fin de la simulación =====")
        print(f"\nTodos los eventos quedaron registrados en '{ARCHIVO_LOG}'.")

    @staticmethod
    def abrir_interfaz():
        """Abre la ventana gráfica."""
        from gui.aplicacion import AppSoftwareFJ
        AppSoftwareFJ().mainloop()

    def ejecutar(self, argumentos):
        if "--consola" in argumentos:
            self.simular()
        else:
            self.abrir_interfaz()


if __name__ == "__main__":
    Main().ejecutar(sys.argv[1:])
