from Entidades.persona import Persona
from datetime import datetime

class Cliente(Persona):
    """Clase que representa un cliente/pasajero del sistema"""
    
    def __init__(self, documento, apellido, nombre, email, celular, nacionalidad):
        super().__init__(documento, apellido, nombre, email, celular)
        self.nacionalidad = nacionalidad
        self.fecha_ingreso = datetime.now()
        self.historial_vuelos = []
    
    def obtener_tipo(self):
        return "Cliente"
    
    def agregar_vuelo_historial(self, codigo_vuelo):
        """Agrega un vuelo al historial del cliente"""
        if codigo_vuelo not in self.historial_vuelos:
            self.historial_vuelos.append(codigo_vuelo)
    
    def __str__(self):
        return f"Cliente: {super().__str__()} - Nacionalidad: {self.nacionalidad}"