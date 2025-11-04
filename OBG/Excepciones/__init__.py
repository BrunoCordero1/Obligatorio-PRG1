# Archivo __init__.py para el paquete excepciones
# Este archivo permite importar las excepciones del paquete

from .excepciones import (
    EntidadDuplicadaException,
    EntidadNoEncontradaException,
    DatoInvalidoException,
    VueloCompletoException,
    TripulacionIncompletaException,
    EquipajeInvalidoException
)

__all__ = [
    'EntidadDuplicadaException',
    'EntidadNoEncontradaException',
    'DatoInvalidoException',
    'VueloCompletoException',
    'TripulacionIncompletaException',
    'EquipajeInvalidoException'
]