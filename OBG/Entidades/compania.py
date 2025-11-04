class Compania:
    """Clase que representa una compañía aérea"""
    
    def __init__(self, codigo, nombre, pais_origen):
        self.codigo = codigo
        self.nombre = nombre
        self.pais_origen = pais_origen
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo}) - {self.pais_origen}"