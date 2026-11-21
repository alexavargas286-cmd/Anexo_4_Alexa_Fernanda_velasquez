"""
registro_log.py
Configuración del archivo de logs. Aquí se guardan los eventos y errores del sistema.
"""
import logging   # Módulo estándar de Python para registrar eventos

ARCHIVO_LOG = "software_fj.log"   # Nombre del archivo donde se guarda todo


def obtener_logger():
    """Crea (una sola vez) y devuelve el logger del sistema."""
    logger = logging.getLogger("SoftwareFJ")      # Logger con nombre propio
    if not logger.handlers:                       # Evita agregar handlers repetidos
        logger.setLevel(logging.INFO)             # Se registran INFO, WARNING y ERROR
        manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
        formato = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s",
                                    datefmt="%Y-%m-%d %H:%M:%S")
        manejador.setFormatter(formato)           # Se aplica el formato a cada línea
        logger.addHandler(manejador)              # Se conecta el archivo al logger
    return logger


log = obtener_logger()   # Instancia que importan los demás módulos
