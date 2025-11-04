from Entidades.persona import Persona
from datetime import datetime

class Tripulante(Persona):
    """Clase que representa un tripulante (piloto, copiloto, azafata)"""
    
    ROLES_VALIDOS = ["piloto", "copiloto", "azafata", "azafato"]
    
    def __init__(self, documento, apellido, nombre, email, celular, rol, fecha_ingreso_compania, horas_vuelo):
        super().__init__(documento, apellido, nombre, email, celular)
        if rol.lower() not in self.ROLES_VALIDOS:
            raise ValueError(f"Rol inválido. Debe ser uno de: {', '.join(self.ROLES_VALIDOS)}")
        self.rol = rol.lower()
        self.fecha_ingreso_compania = fecha_ingreso_compania
        self.horas_vuelo = horas_vuelo
    
    def obtener_tipo(self):
        return "Tripulante"
    
    def __str__(self):
        return f"Tripulante ({self.rol}): {super().__str__()} - Horas vuelo: {self.horas_vuelo}"