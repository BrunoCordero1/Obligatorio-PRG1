class EntidadDuplicadaException(Exception):
    """Excepción cuando se intenta registrar una entidad duplicada"""
    pass

class EntidadNoEncontradaException(Exception):
    """Excepción cuando no se encuentra una entidad solicitada"""
    pass

class DatoInvalidoException(Exception):
    """Excepción cuando se ingresa un dato inválido"""
    pass

class VueloCompletoException(Exception):
    """Excepción cuando un vuelo no tiene asientos disponibles"""
    pass

class TripulacionIncompletaException(Exception):
    """Excepción cuando un vuelo no tiene tripulación completa"""
    pass

class EquipajeInvalidoException(Exception):
    """Excepción relacionada con validación de equipaje"""
    pass