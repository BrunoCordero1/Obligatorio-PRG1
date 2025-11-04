from abc import ABC, abstractmethod
from datetime import datetime

class Persona(ABC):
    """Clase abstracta que representa una persona en el sistema"""
    
    def __init__(self, documento, apellido, nombre, email, celular):
        self.documento = documento
        self.apellido = apellido
        self.nombre = nombre
        self.email = email
        self.celular = celular
    
    @abstractmethod
    def obtener_tipo(self):
        """Método abstracto para obtener el tipo de persona"""
        pass
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - Doc: {self.documento}"