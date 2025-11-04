class Ticket:
    """Clase que representa un ticket de vuelo"""
    
    def __init__(self, numero, pasajero, codigo_vuelo):
        self.numero = numero  # Número único dentro del vuelo (1..capacidad)
        self.pasajero = pasajero  # Objeto Cliente
        self.codigo_vuelo = codigo_vuelo
    
    def __str__(self):
        return f"Ticket #{self.numero} - Vuelo: {self.codigo_vuelo} - Pasajero: {self.pasajero.nombre} {self.pasajero.apellido}"