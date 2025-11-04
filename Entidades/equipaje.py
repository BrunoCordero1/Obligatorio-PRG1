class Equipaje:
    """Clase que representa equipaje en bodega"""
    
    def __init__(self, codigo, pasajero, peso, costo, es_internacional):
        self.codigo = codigo  # Formato: CODIGOVUELO-NROTICKET
        self.pasajero = pasajero
        self.peso = peso
        self.costo = costo
        self.es_internacional = es_internacional
    
    @staticmethod
    def calcular_costo(peso, es_internacional):
        """Calcula el costo del equipaje según el peso y tipo de vuelo"""
        if peso <= 23:
            return 0
        elif 24 <= peso <= 32:
            return 100 if es_internacional else 30
        elif 33 <= peso <= 45:
            return 200 if es_internacional else 60
        else:
            raise ValueError("El equipaje no puede superar los 45 kg")
    
    def __str__(self):
        return f"Equipaje {self.codigo} - Pasajero: {self.pasajero.nombre} {self.pasajero.apellido} - Peso: {self.peso}kg - Costo: USD {self.costo}"