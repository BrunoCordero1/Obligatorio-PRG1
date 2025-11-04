from datetime import datetime

class Vuelo:
    """Clase que representa un vuelo turístico"""
    
    def __init__(self, codigo, origen, destino, duracion_horas, fecha, compania, capacidad_asientos, tipo_vuelo):
        self.codigo = codigo
        self.origen = origen
        self.destino = destino
        self.duracion_horas = duracion_horas
        self.fecha = fecha
        self.compania = compania  # Objeto Compania
        self.capacidad_asientos = capacidad_asientos
        self.tipo_vuelo = tipo_vuelo.lower()  # "nacional" o "internacional"
        self.estado = "activo"
        self.tickets = []  # Colección de tickets
        self.equipajes = []  # Colección de equipajes en bodega
        self.tripulacion = {
            "pilotos": [],
            "copilotos": [],
            "azafatas": []
        }
    
    def es_internacional(self):
        """Retorna True si el vuelo es internacional"""
        return self.tipo_vuelo == "internacional"
    
    def obtener_asientos_disponibles(self):
        """Retorna la cantidad de asientos disponibles"""
        return self.capacidad_asientos - len(self.tickets)
    
    def agregar_ticket(self, ticket):
        """Agrega un ticket al vuelo"""
        if len(self.tickets) >= self.capacidad_asientos:
            raise ValueError("No hay asientos disponibles en este vuelo")
        self.tickets.append(ticket)
    
    def agregar_tripulante(self, tripulante):
        """Agrega un tripulante a la tripulación del vuelo"""
        rol = tripulante.rol
        if rol == "piloto":
            self.tripulacion["pilotos"].append(tripulante)
        elif rol == "copiloto":
            self.tripulacion["copilotos"].append(tripulante)
        elif rol in ["azafata", "azafato"]:
            self.tripulacion["azafatas"].append(tripulante)
    
    def validar_tripulacion_completa(self):
        """Valida que el vuelo tenga al menos un piloto, un copiloto y una azafata"""
        return (len(self.tripulacion["pilotos"]) >= 1 and 
                len(self.tripulacion["copilotos"]) >= 1 and 
                len(self.tripulacion["azafatas"]) >= 1)
    
    def agregar_equipaje(self, equipaje):
        """Agrega equipaje al vuelo"""
        self.equipajes.append(equipaje)
    
    def quitar_equipaje(self, codigo_equipaje):
        """Elimina un equipaje del vuelo"""
        self.equipajes = [e for e in self.equipajes if e.codigo != codigo_equipaje]
    
    def quitar_ticket(self, numero_ticket):
        """Elimina un ticket del vuelo"""
        self.tickets = [t for t in self.tickets if t.numero != numero_ticket]
    
    def cancelar(self):
        """Cancela el vuelo"""
        self.estado = "cancelado"
    
    def __str__(self):
        return f"Vuelo {self.codigo} - {self.origen} → {self.destino} - {self.fecha.strftime('%d/%m/%Y %H:%M')} - Estado: {self.estado}"