# Archivo __init__.py para el paquete entidades
# Este archivo permite importar las clases del paquete

from .persona import Persona
from .cliente import Cliente
from .tripulante import Tripulante
from .compania import Compania
from .vuelo import Vuelo
from .ticket import Ticket
from .equipaje import Equipaje

__all__ = ['Persona', 'Cliente', 'Tripulante', 'Compania', 'Vuelo', 'Ticket', 'Equipaje']