from Entidades.cliente import Cliente
from Entidades.tripulante import Tripulante
from Entidades.compania import Compania
from Entidades.vuelo import Vuelo
from Entidades.ticket import Ticket
from Entidades.equipaje import Equipaje
from Excepciones.excepciones import *
from datetime import datetime

class Sistema:
    """Clase que gestiona todo el sistema del aeropuerto"""
    
    def __init__(self):
        self.personas = []  # Clientes y tripulación
        self.companias = []
        self.vuelos = []
        self.tickets_vendidos = []
        self.tickets_cancelados = []
        self._contador_vuelos = 1
    
    # ========== REGISTROS ==========
    
    def registrar_persona(self, tipo, documento, apellido, nombre, email, celular, **kwargs):
        """Registra una persona (cliente o tripulante) en el sistema"""
        # Verificar si ya existe
        if self._buscar_persona_por_documento(documento):
            raise EntidadDuplicadaException(f"Ya existe una persona con documento {documento}")
        
        if tipo.lower() == "cliente":
            nacionalidad = kwargs.get('nacionalidad')
            if not nacionalidad:
                raise DatoInvalidoException("La nacionalidad es requerida para clientes")
            persona = Cliente(documento, apellido, nombre, email, celular, nacionalidad)
        elif tipo.lower() == "tripulante":
            rol = kwargs.get('rol')
            fecha_ingreso = kwargs.get('fecha_ingreso_compania')
            horas_vuelo = kwargs.get('horas_vuelo', 0)
            if not rol:
                raise DatoInvalidoException("El rol es requerido para tripulantes")
            persona = Tripulante(documento, apellido, nombre, email, celular, rol, fecha_ingreso, horas_vuelo)
        else:
            raise DatoInvalidoException("Tipo de persona inválido. Debe ser 'cliente' o 'tripulante'")
        
        self.personas.append(persona)
        return persona
    
    def registrar_compania(self, codigo, nombre, pais_origen):
        """Registra una compañía aérea en el sistema"""
        if self._buscar_compania_por_codigo(codigo):
            raise EntidadDuplicadaException(f"Ya existe una compañía con código {codigo}")
        
        compania = Compania(codigo, nombre, pais_origen)
        self.companias.append(compania)
        return compania
    
    def crear_vuelo(self, origen, destino, duracion_horas, fecha, codigo_compania, capacidad_asientos, tipo_vuelo):
        """Crea un nuevo vuelo en el sistema"""
        # Buscar la compañía
        compania = self._buscar_compania_por_codigo(codigo_compania)
        if not compania:
            raise EntidadNoEncontradaException(f"No existe una compañía con código {codigo_compania}")
        
        # Generar código único para el vuelo
        codigo_vuelo = f"{codigo_compania}{self._contador_vuelos:03d}"
        self._contador_vuelos += 1
        
        # Validar tipo de vuelo
        if tipo_vuelo.lower() not in ["nacional", "internacional"]:
            raise DatoInvalidoException("El tipo de vuelo debe ser 'nacional' o 'internacional'")
        
        vuelo = Vuelo(codigo_vuelo, origen, destino, duracion_horas, fecha, compania, capacidad_asientos, tipo_vuelo)
        self.vuelos.append(vuelo)
        return vuelo
    
    def crear_ticket(self, codigo_vuelo, documento_pasajero):
        """Crea un ticket asignando un pasajero a un vuelo"""
        # Buscar vuelo
        vuelo = self._buscar_vuelo_por_codigo(codigo_vuelo)
        if not vuelo:
            raise EntidadNoEncontradaException(f"No existe un vuelo con código {codigo_vuelo}")
        
        if vuelo.estado != "activo":
            raise DatoInvalidoException("No se pueden crear tickets para vuelos cancelados")
        
        # Buscar pasajero
        pasajero = self._buscar_persona_por_documento(documento_pasajero)
        if not pasajero or pasajero.obtener_tipo() != "Cliente":
            raise EntidadNoEncontradaException(f"No existe un cliente con documento {documento_pasajero}")
        
        # Verificar que el pasajero no tenga ya un ticket en este vuelo
        for ticket in vuelo.tickets:
            if ticket.pasajero.documento == documento_pasajero:
                raise EntidadDuplicadaException("El pasajero ya tiene un ticket en este vuelo")
        
        # Verificar disponibilidad
        if vuelo.obtener_asientos_disponibles() <= 0:
            raise VueloCompletoException("No hay asientos disponibles en este vuelo")
        
        # Crear ticket con número secuencial
        numero_ticket = len(vuelo.tickets) + 1
        ticket = Ticket(numero_ticket, pasajero, codigo_vuelo)
        
        vuelo.agregar_ticket(ticket)
        self.tickets_vendidos.append(ticket)
        pasajero.agregar_vuelo_historial(codigo_vuelo)
        
        return ticket
    
    def asignar_personal_vuelo(self, codigo_vuelo, documento_tripulante):
        """Asigna un tripulante a un vuelo"""
        # Buscar vuelo
        vuelo = self._buscar_vuelo_por_codigo(codigo_vuelo)
        if not vuelo:
            raise EntidadNoEncontradaException(f"No existe un vuelo con código {codigo_vuelo}")
        
        if vuelo.estado != "activo":
            raise DatoInvalidoException("No se puede asignar personal a vuelos cancelados")
        
        # Buscar tripulante
        tripulante = self._buscar_persona_por_documento(documento_tripulante)
        if not tripulante or tripulante.obtener_tipo() != "Tripulante":
            raise EntidadNoEncontradaException(f"No existe un tripulante con documento {documento_tripulante}")
        
        # Verificar que no esté ya asignado
        todas_tripulaciones = (vuelo.tripulacion["pilotos"] + 
                              vuelo.tripulacion["copilotos"] + 
                              vuelo.tripulacion["azafatas"])
        for t in todas_tripulaciones:
            if t.documento == documento_tripulante:
                raise EntidadDuplicadaException("Este tripulante ya está asignado a este vuelo")
        
        vuelo.agregar_tripulante(tripulante)
        return True
    
    def registrar_equipaje(self, codigo_vuelo, numero_ticket, peso):
        """Registra equipaje en bodega para un pasajero"""
        # Buscar vuelo
        vuelo = self._buscar_vuelo_por_codigo(codigo_vuelo)
        if not vuelo:
            raise EntidadNoEncontradaException(f"No existe un vuelo con código {codigo_vuelo}")
        
        if vuelo.estado != "activo":
            raise DatoInvalidoException("No se puede registrar equipaje en vuelos cancelados")
        
        # Buscar ticket en el vuelo
        ticket = None
        for t in vuelo.tickets:
            if t.numero == numero_ticket:
                ticket = t
                break
        
        if not ticket:
            raise EntidadNoEncontradaException(f"No existe el ticket #{numero_ticket} en el vuelo {codigo_vuelo}")
        
        # Verificar que el pasajero no tenga ya equipaje registrado
        for equipaje in vuelo.equipajes:
            if equipaje.pasajero.documento == ticket.pasajero.documento:
                raise EntidadDuplicadaException("Este pasajero ya tiene equipaje registrado en este vuelo")
        
        # Validar peso y calcular costo
        try:
            costo = Equipaje.calcular_costo(peso, vuelo.es_internacional())
        except ValueError as e:
            raise EquipajeInvalidoException(str(e))
        
        # Crear equipaje
        codigo_equipaje = f"{codigo_vuelo}-{numero_ticket}"
        equipaje = Equipaje(codigo_equipaje, ticket.pasajero, peso, costo, vuelo.es_internacional())
        vuelo.agregar_equipaje(equipaje)
        
        return equipaje
    
    def cancelar_ticket(self, codigo_vuelo, numero_ticket):
        """Cancela un ticket y libera el asiento"""
        # Buscar vuelo
        vuelo = self._buscar_vuelo_por_codigo(codigo_vuelo)
        if not vuelo:
            raise EntidadNoEncontradaException(f"No existe un vuelo con código {codigo_vuelo}")
        
        # Buscar ticket en el vuelo
        ticket = None
        for t in vuelo.tickets:
            if t.numero == numero_ticket:
                ticket = t
                break
        
        if not ticket:
            raise EntidadNoEncontradaException(f"No existe el ticket #{numero_ticket} en el vuelo {codigo_vuelo}")
        
        # Quitar equipaje si existe
        codigo_equipaje = f"{codigo_vuelo}-{numero_ticket}"
        vuelo.quitar_equipaje(codigo_equipaje)
        
        # Quitar ticket del vuelo
        vuelo.quitar_ticket(numero_ticket)
        
        # Mover a tickets cancelados
        self.tickets_cancelados.append(ticket)
        self.tickets_vendidos = [t for t in self.tickets_vendidos if not (t.numero == numero_ticket and t.codigo_vuelo == codigo_vuelo)]
        
        return True
    
    def cancelar_vuelo(self, codigo_vuelo, codigo_vuelo_destino, causa):
        """Cancela un vuelo y reasigna pasajeros, personal y equipaje a otro vuelo"""
        # Buscar vuelo a cancelar
        vuelo_origen = self._buscar_vuelo_por_codigo(codigo_vuelo)
        if not vuelo_origen:
            raise EntidadNoEncontradaException(f"No existe un vuelo con código {codigo_vuelo}")
        
        # Buscar vuelo destino
        vuelo_destino = self._buscar_vuelo_por_codigo(codigo_vuelo_destino)
        if not vuelo_destino:
            raise EntidadNoEncontradaException(f"No existe un vuelo con código {codigo_vuelo_destino}")
        
        if vuelo_destino.estado != "activo":
            raise DatoInvalidoException("El vuelo destino debe estar activo")
        
        # Verificar capacidad del vuelo destino
        if vuelo_destino.obtener_asientos_disponibles() < len(vuelo_origen.tickets):
            raise VueloCompletoException("El vuelo destino no tiene suficientes asientos disponibles")
        
        # Reasignar tickets
        for ticket_viejo in vuelo_origen.tickets:
            # Crear nuevo ticket en vuelo destino
            numero_nuevo = len(vuelo_destino.tickets) + 1
            ticket_nuevo = Ticket(numero_nuevo, ticket_viejo.pasajero, codigo_vuelo_destino)
            vuelo_destino.agregar_ticket(ticket_nuevo)
            
            # Actualizar en tickets vendidos
            for i, t in enumerate(self.tickets_vendidos):
                if t.numero == ticket_viejo.numero and t.codigo_vuelo == codigo_vuelo:
                    self.tickets_vendidos[i] = ticket_nuevo
                    break
        
        # Reasignar equipajes
        for equipaje_viejo in vuelo_origen.equipajes:
            # Buscar el número de ticket del pasajero en el vuelo destino
            numero_ticket_nuevo = None
            for ticket in vuelo_destino.tickets:
                if ticket.pasajero.documento == equipaje_viejo.pasajero.documento:
                    numero_ticket_nuevo = ticket.numero
                    break
            
            if numero_ticket_nuevo:
                codigo_nuevo = f"{codigo_vuelo_destino}-{numero_ticket_nuevo}"
                equipaje_nuevo = Equipaje(codigo_nuevo, equipaje_viejo.pasajero, 
                                         equipaje_viejo.peso, equipaje_viejo.costo, 
                                         vuelo_destino.es_internacional())
                vuelo_destino.agregar_equipaje(equipaje_nuevo)
        
        # Reasignar tripulación
        for piloto in vuelo_origen.tripulacion["pilotos"]:
            if piloto not in vuelo_destino.tripulacion["pilotos"]:
                vuelo_destino.agregar_tripulante(piloto)
        
        for copiloto in vuelo_origen.tripulacion["copilotos"]:
            if copiloto not in vuelo_destino.tripulacion["copilotos"]:
                vuelo_destino.agregar_tripulante(copiloto)
        
        for azafata in vuelo_origen.tripulacion["azafatas"]:
            if azafata not in vuelo_destino.tripulacion["azafatas"]:
                vuelo_destino.agregar_tripulante(azafata)
        
        # Cancelar vuelo origen
        vuelo_origen.cancelar()
        vuelo_origen.causa_cancelacion = causa
        vuelo_origen.fecha_cancelacion = datetime.now()
        
        return True
    
    # ========== INFORMES ==========
    
    def informe_pasajeros_por_vuelo(self, codigo_vuelo):
        """Genera informe de pasajeros de un vuelo específico"""
        vuelo = self._buscar_vuelo_por_codigo(codigo_vuelo)
        if not vuelo:
            raise EntidadNoEncontradaException(f"No existe un vuelo con código {codigo_vuelo}")
        
        informe = f"\n{'='*80}\n"
        informe += f"INFORME DE PASAJEROS - VUELO {codigo_vuelo}\n"
        informe += f"{vuelo.origen} → {vuelo.destino} | {vuelo.fecha.strftime('%d/%m/%Y %H:%M')}\n"
        informe += f"{'='*80}\n\n"
        
        if not vuelo.tickets:
            informe += "No hay pasajeros registrados en este vuelo.\n"
        else:
            for ticket in vuelo.tickets:
                pasajero = ticket.pasajero
                # Contar equipaje del pasajero
                cant_equipaje = sum(1 for e in vuelo.equipajes if e.pasajero.documento == pasajero.documento)
                
                informe += f"Ticket #{ticket.numero}\n"
                informe += f"  Nombre: {pasajero.nombre} {pasajero.apellido}\n"
                informe += f"  Cédula: {pasajero.documento}\n"
                informe += f"  Nacionalidad: {pasajero.nacionalidad}\n"
                informe += f"  Cantidad de equipaje: {cant_equipaje}\n"
                informe += f"{'-'*80}\n"
        
        informe += f"\nTotal pasajeros: {len(vuelo.tickets)}\n"
        informe += f"{'='*80}\n"
        return informe
    
    def informe_personal_asignado(self, codigo_vuelo):
        """Genera informe del personal asignado a un vuelo"""
        vuelo = self._buscar_vuelo_por_codigo(codigo_vuelo)
        if not vuelo:
            raise EntidadNoEncontradaException(f"No existe un vuelo con código {codigo_vuelo}")
        
        informe = f"\n{'='*80}\n"
        informe += f"INFORME DE PERSONAL - VUELO {codigo_vuelo}\n"
        informe += f"{vuelo.origen} → {vuelo.destino} | {vuelo.fecha.strftime('%d/%m/%Y %H:%M')}\n"
        informe += f"{'='*80}\n\n"
        
        informe += "PILOTOS:\n"
        if not vuelo.tripulacion["pilotos"]:
            informe += "  No hay pilotos asignados\n"
        else:
            for piloto in vuelo.tripulacion["pilotos"]:
                informe += f"  - {piloto.nombre} {piloto.apellido} (Doc: {piloto.documento}) - {piloto.horas_vuelo} hrs\n"
        
        informe += "\nCOPILOTOS:\n"
        if not vuelo.tripulacion["copilotos"]:
            informe += "  No hay copilotos asignados\n"
        else:
            for copiloto in vuelo.tripulacion["copilotos"]:
                informe += f"  - {copiloto.nombre} {copiloto.apellido} (Doc: {copiloto.documento}) - {copiloto.horas_vuelo} hrs\n"
        
        informe += "\nAZAFATAS/AZAFATOS:\n"
        if not vuelo.tripulacion["azafatas"]:
            informe += "  No hay azafatas/azafatos asignados\n"
        else:
            for azafata in vuelo.tripulacion["azafatas"]:
                informe += f"  - {azafata.nombre} {azafata.apellido} (Doc: {azafata.documento}) - {azafata.horas_vuelo} hrs\n"
        
        informe += f"\n{'='*80}\n"
        
        # Validar si está completa
        if vuelo.validar_tripulacion_completa():
            informe += "✓ Tripulación completa\n"
        else:
            informe += "✗ Tripulación incompleta (se requiere al menos 1 piloto, 1 copiloto y 1 azafata/o)\n"
        
        informe += f"{'='*80}\n"
        return informe
    
    def informe_vuelos_por_compania(self):
        """Genera tabla comparativa de vuelos por compañía"""
        informe = f"\n{'='*80}\n"
        informe += "INFORME DE VUELOS POR COMPAÑÍA\n"
        informe += f"{'='*80}\n\n"
        
        if not self.companias:
            informe += "No hay compañías registradas.\n"
        else:
            for compania in self.companias:
                vuelos_compania = [v for v in self.vuelos if v.compania.codigo == compania.codigo]
                vuelos_activos = [v for v in vuelos_compania if v.estado == "activo"]
                vuelos_cancelados = [v for v in vuelos_compania if v.estado == "cancelado"]
                
                informe += f"{compania.nombre} ({compania.codigo}) - {compania.pais_origen}\n"
                informe += f"  Total de vuelos: {len(vuelos_compania)}\n"
                informe += f"  Vuelos activos: {len(vuelos_activos)}\n"
                informe += f"  Vuelos cancelados: {len(vuelos_cancelados)}\n"
                
                if vuelos_compania:
                    informe += f"  Vuelos:\n"
                    for vuelo in vuelos_compania:
                        informe += f"    • {vuelo.codigo}: {vuelo.origen} → {vuelo.destino} ({vuelo.estado})\n"
                
                informe += f"{'-'*80}\n"
        
        informe += f"\n{'='*80}\n"
        return informe
    
    def informe_vuelos_cancelados(self):
        """Genera historial de vuelos cancelados"""
        vuelos_cancelados = [v for v in self.vuelos if v.estado == "cancelado"]
        
        informe = f"\n{'='*80}\n"
        informe += "INFORME DE VUELOS CANCELADOS\n"
        informe += f"{'='*80}\n\n"
        
        if not vuelos_cancelados:
            informe += "No hay vuelos cancelados.\n"
        else:
            for vuelo in vuelos_cancelados:
                causa = getattr(vuelo, 'causa_cancelacion', 'No especificada')
                fecha_cancel = getattr(vuelo, 'fecha_cancelacion', 'No registrada')
                if isinstance(fecha_cancel, datetime):
                    fecha_cancel = fecha_cancel.strftime('%d/%m/%Y %H:%M')
                
                # Contar pasajeros que tenía el vuelo (ya no están en tickets pero podemos ver tickets cancelados)
                pasajeros_afectados = len([t for t in self.tickets_cancelados if t.codigo_vuelo == vuelo.codigo])
                
                informe += f"Vuelo: {vuelo.codigo}\n"
                informe += f"  Ruta: {vuelo.origen} → {vuelo.destino}\n"
                informe += f"  Fecha programada: {vuelo.fecha.strftime('%d/%m/%Y %H:%M')}\n"
                informe += f"  Fecha de cancelación: {fecha_cancel}\n"
                informe += f"  Causa: {causa}\n"
                informe += f"  Pasajeros afectados: {pasajeros_afectados}\n"
                informe += f"  Compañía: {vuelo.compania.nombre}\n"
                informe += f"{'-'*80}\n"
        
        informe += f"\nTotal de vuelos cancelados: {len(vuelos_cancelados)}\n"
        informe += f"{'='*80}\n"
        return informe
    
    def visualizar_vuelos(self):
        """Muestra todos los vuelos programados"""
        informe = f"\n{'='*80}\n"
        informe += "VUELOS PROGRAMADOS\n"
        informe += f"{'='*80}\n\n"
        
        if not self.vuelos:
            informe += "No hay vuelos registrados.\n"
        else:
            vuelos_activos = [v for v in self.vuelos if v.estado == "activo"]
            
            if not vuelos_activos:
                informe += "No hay vuelos activos.\n"
            else:
                for vuelo in vuelos_activos:
                    informe += f"{vuelo.codigo} - {vuelo.origen} → {vuelo.destino}\n"
                    informe += f"  Fecha: {vuelo.fecha.strftime('%d/%m/%Y %H:%M')}\n"
                    informe += f"  Duración: {vuelo.duracion_horas} horas\n"
                    informe += f"  Compañía: {vuelo.compania.nombre}\n"
                    informe += f"  Tipo: {vuelo.tipo_vuelo.capitalize()}\n"
                    informe += f"  Asientos: {len(vuelo.tickets)}/{vuelo.capacidad_asientos}\n"
                    informe += f"  Tripulación completa: {'Sí' if vuelo.validar_tripulacion_completa() else 'No'}\n"
                    informe += f"{'-'*80}\n"
        
        informe += f"{'='*80}\n"
        return informe
    
    # ========== MÉTODOS AUXILIARES ==========
    
    def _buscar_persona_por_documento(self, documento):
        """Busca una persona por su documento"""
        for persona in self.personas:
            if persona.documento == documento:
                return persona
        return None
    
    def _buscar_compania_por_codigo(self, codigo):
        """Busca una compañía por su código"""
        for compania in self.companias:
            if compania.codigo == codigo:
                return compania
        return None
    
    def _buscar_vuelo_por_codigo(self, codigo):
        """Busca un vuelo por su código"""
        for vuelo in self.vuelos:
            if vuelo.codigo == codigo:
                return vuelo
        return None
    
    def obtener_clientes(self):
        """Retorna lista de clientes"""
        return [p for p in self.personas if isinstance(p, Cliente)]
    
    def obtener_tripulantes(self):
        """Retorna lista de tripulantes"""
        return [p for p in self.personas if isinstance(p, Tripulante)]
    
    def obtener_vuelos_activos(self):
        """Retorna lista de vuelos activos"""
        return [v for v in self.vuelos if v.estado == "activo"]