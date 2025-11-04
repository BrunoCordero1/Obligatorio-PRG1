from Sistema import Sistema
from Excepciones.excepciones import *
from datetime import datetime

def limpiar_pantalla():
    """Limpia la pantalla (funciona en Windows y Unix)"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input("\nPresione Enter para continuar...")

def solicitar_entero(mensaje):
    """Solicita un número entero validando la entrada"""
    while True:
        try:
            valor = input(mensaje).strip()
            if not valor:
                raise ValueError("El campo no puede estar vacío")
            return int(valor)
        except ValueError as e:
            print(f"Error: {e}. Ingrese un número entero válido.")

def solicitar_float(mensaje):
    """Solicita un número decimal validando la entrada"""
    while True:
        try:
            valor = input(mensaje).strip()
            if not valor:
                raise ValueError("El campo no puede estar vacío")
            return float(valor)
        except ValueError as e:
            print(f"Error: {e}. Ingrese un número válido.")

def solicitar_texto(mensaje):
    """Solicita un texto validando que no esté vacío"""
    while True:
        valor = input(mensaje).strip()
        if not valor:
            print("Error: El campo no puede estar vacío.")
        else:
            return valor

def solicitar_fecha(mensaje):
    """Solicita una fecha en formato DD/MM/YYYY HH:MM"""
    while True:
        try:
            fecha_str = input(mensaje).strip()
            if not fecha_str:
                raise ValueError("La fecha no puede estar vacía")
            return datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
        except ValueError:
            print("Error: Formato de fecha inválido. Use DD/MM/YYYY HH:MM (ej: 25/12/2025 14:30)")

def registrar_persona(sistema):
    """Opción 1: Registrar persona"""
    limpiar_pantalla()
    print("="*60)
    print("REGISTRAR PERSONA")
    print("="*60)
    
    print("\nTipo de persona:")
    print("1. Cliente")
    print("2. Tripulante")
    
    tipo_opcion = solicitar_entero("\nSeleccione opción: ")
    
    try:
        documento = solicitar_texto("Documento de identidad: ")
        apellido = solicitar_texto("Apellido: ")
        nombre = solicitar_texto("Nombre: ")
        email = solicitar_texto("Email: ")
        celular = solicitar_texto("Celular: ")
        
        if tipo_opcion == 1:
            nacionalidad = solicitar_texto("Nacionalidad: ")
            persona = sistema.registrar_persona("cliente", documento, apellido, nombre, 
                                               email, celular, nacionalidad=nacionalidad)
            print(f"\n✓ Cliente registrado exitosamente: {persona}")
        elif tipo_opcion == 2:
            print("\nRoles disponibles: piloto, copiloto, azafata, azafato")
            rol = solicitar_texto("Rol: ")
            fecha_ingreso = solicitar_fecha("Fecha de ingreso a la compañía (DD/MM/YYYY HH:MM): ")
            horas_vuelo = solicitar_float("Horas de vuelo acumuladas: ")
            
            persona = sistema.registrar_persona("tripulante", documento, apellido, nombre,
                                               email, celular, rol=rol, 
                                               fecha_ingreso_compania=fecha_ingreso,
                                               horas_vuelo=horas_vuelo)
            print(f"\n✓ Tripulante registrado exitosamente: {persona}")
        else:
            print("\n✗ Opción inválida")
    except (EntidadDuplicadaException, DatoInvalidoException) as e:
        print(f"\n✗ Error: {e}")
    
    pausar()

def registrar_compania(sistema):
    """Opción 2: Registrar compañía"""
    limpiar_pantalla()
    print("="*60)
    print("REGISTRAR COMPAÑÍA AÉREA")
    print("="*60)
    
    try:
        codigo = solicitar_texto("\nCódigo de la compañía (ej: GOL, AER): ").upper()
        nombre = solicitar_texto("Nombre de la compañía: ")
        pais_origen = solicitar_texto("País de origen: ")
        
        compania = sistema.registrar_compania(codigo, nombre, pais_origen)
        print(f"\n✓ Compañía registrada exitosamente: {compania}")
    except EntidadDuplicadaException as e:
        print(f"\n✗ Error: {e}")
    
    pausar()

def crear_vuelo(sistema):
    """Opción 3: Crear vuelo"""
    limpiar_pantalla()
    print("="*60)
    print("CREAR VUELO")
    print("="*60)
    
    # Mostrar compañías disponibles
    if not sistema.companias:
        print("\n✗ No hay compañías registradas. Registre una compañía primero.")
        pausar()
        return
    
    print("\nCompañías disponibles:")
    for comp in sistema.companias:
        print(f"  - {comp.codigo}: {comp.nombre}")
    
    try:
        origen = solicitar_texto("\nOrigen: ")
        destino = solicitar_texto("Destino: ")
        duracion_horas = solicitar_float("Duración en horas: ")
        fecha = solicitar_fecha("Fecha del vuelo (DD/MM/YYYY HH:MM): ")
        codigo_compania = solicitar_texto("Código de compañía: ").upper()
        capacidad_asientos = solicitar_entero("Capacidad de asientos: ")
        
        print("\nTipo de vuelo:")
        print("1. Nacional")
        print("2. Internacional")
        tipo_opcion = solicitar_entero("Seleccione opción: ")
        tipo_vuelo = "nacional" if tipo_opcion == 1 else "internacional"
        
        vuelo = sistema.crear_vuelo(origen, destino, duracion_horas, fecha, 
                                    codigo_compania, capacidad_asientos, tipo_vuelo)
        print(f"\n✓ Vuelo creado exitosamente:")
        print(f"  Código: {vuelo.codigo}")
        print(f"  Ruta: {vuelo.origen} → {vuelo.destino}")
        print(f"  Fecha: {vuelo.fecha.strftime('%d/%m/%Y %H:%M')}")
    except (EntidadNoEncontradaException, DatoInvalidoException) as e:
        print(f"\n✗ Error: {e}")
    
    pausar()

def crear_ticket(sistema):
    """Opción 4: Crear ticket"""
    limpiar_pantalla()
    print("="*60)
    print("CREAR TICKET")
    print("="*60)
    
    # Mostrar vuelos activos
    vuelos_activos = sistema.obtener_vuelos_activos()
    if not vuelos_activos:
        print("\n✗ No hay vuelos activos disponibles.")
        pausar()
        return
    
    print("\nVuelos activos:")
    for vuelo in vuelos_activos:
        disponibles = vuelo.obtener_asientos_disponibles()
        print(f"  - {vuelo.codigo}: {vuelo.origen} → {vuelo.destino} ({disponibles} asientos disponibles)")
    
    # Mostrar clientes
    clientes = sistema.obtener_clientes()
    if not clientes:
        print("\n✗ No hay clientes registrados.")
        pausar()
        return
    
    print("\nClientes registrados:")
    for cliente in clientes:
        print(f"  - {cliente.documento}: {cliente.nombre} {cliente.apellido}")
    
    try:
        codigo_vuelo = solicitar_texto("\nCódigo de vuelo: ").upper()
        documento_pasajero = solicitar_texto("Documento del pasajero: ")
        
        ticket = sistema.crear_ticket(codigo_vuelo, documento_pasajero)
        print(f"\n✓ Ticket creado exitosamente:")
        print(f"  {ticket}")
    except (EntidadNoEncontradaException, EntidadDuplicadaException, 
            VueloCompletoException, DatoInvalidoException) as e:
        print(f"\n✗ Error: {e}")
    
    pausar()

def asignar_personal(sistema):
    """Opción 5: Asignar personal a vuelo"""
    limpiar_pantalla()
    print("="*60)
    print("ASIGNAR PERSONAL A VUELO")
    print("="*60)
    
    # Mostrar vuelos activos
    vuelos_activos = sistema.obtener_vuelos_activos()
    if not vuelos_activos:
        print("\n✗ No hay vuelos activos disponibles.")
        pausar()
        return
    
    print("\nVuelos activos:")
    for vuelo in vuelos_activos:
        print(f"  - {vuelo.codigo}: {vuelo.origen} → {vuelo.destino}")
    
    # Mostrar tripulantes
    tripulantes = sistema.obtener_tripulantes()
    if not tripulantes:
        print("\n✗ No hay tripulantes registrados.")
        pausar()
        return
    
    print("\nTripulantes disponibles:")
    for tripulante in tripulantes:
        print(f"  - {tripulante.documento}: {tripulante.nombre} {tripulante.apellido} ({tripulante.rol})")
    
    try:
        codigo_vuelo = solicitar_texto("\nCódigo de vuelo: ").upper()
        documento_tripulante = solicitar_texto("Documento del tripulante: ")
        
        sistema.asignar_personal_vuelo(codigo_vuelo, documento_tripulante)
        print(f"\n✓ Tripulante asignado exitosamente al vuelo {codigo_vuelo}")
    except (EntidadNoEncontradaException, EntidadDuplicadaException, DatoInvalidoException) as e:
        print(f"\n✗ Error: {e}")
    
    pausar()

def registrar_equipaje(sistema):
    """Opción 6: Registrar equipaje"""
    limpiar_pantalla()
    print("="*60)
    print("REGISTRAR EQUIPAJE EN BODEGA")
    print("="*60)
    
    # Mostrar vuelos activos con tickets
    vuelos_con_tickets = [v for v in sistema.obtener_vuelos_activos() if v.tickets]
    if not vuelos_con_tickets:
        print("\n✗ No hay vuelos con tickets vendidos.")
        pausar()
        return
    
    print("\nVuelos con pasajeros:")
    for vuelo in vuelos_con_tickets:
        print(f"\n  Vuelo {vuelo.codigo}:")
        for ticket in vuelo.tickets:
            tiene_equipaje = any(e.pasajero.documento == ticket.pasajero.documento for e in vuelo.equipajes)
            estado = "✓ Con equipaje" if tiene_equipaje else "○ Sin equipaje"
            print(f"    Ticket #{ticket.numero}: {ticket.pasajero.nombre} {ticket.pasajero.apellido} {estado}")
    
    try:
        codigo_vuelo = solicitar_texto("\nCódigo de vuelo: ").upper()
        numero_ticket = solicitar_entero("Número de ticket: ")
        peso = solicitar_float("Peso del equipaje (kg): ")
        
        equipaje = sistema.registrar_equipaje(codigo_vuelo, numero_ticket, peso)
        print(f"\n✓ Equipaje registrado exitosamente:")
        print(f"  Código: {equipaje.codigo}")
        print(f"  Peso: {equipaje.peso} kg")
        print(f"  Costo adicional: USD {equipaje.costo}")
        
        if equipaje.costo > 0:
            print(f"  ⚠ Se aplicó cargo por sobrepeso")
    except (EntidadNoEncontradaException, EntidadDuplicadaException, 
            EquipajeInvalidoException, DatoInvalidoException) as e:
        print(f"\n✗ Error: {e}")
    
    pausar()

def visualizar_vuelos(sistema):
    """Opción 7: Visualizar vuelos"""
    limpiar_pantalla()
    print(sistema.visualizar_vuelos())
    pausar()

def cancelar_ticket(sistema):
    """Opción 8: Cancelar ticket"""
    limpiar_pantalla()
    print("="*60)
    print("CANCELAR TICKET")
    print("="*60)
    
    # Mostrar vuelos con tickets
    vuelos_con_tickets = [v for v in sistema.obtener_vuelos_activos() if v.tickets]
    if not vuelos_con_tickets:
        print("\n✗ No hay tickets para cancelar.")
        pausar()
        return
    
    print("\nVuelos con tickets:")
    for vuelo in vuelos_con_tickets:
        print(f"\n  Vuelo {vuelo.codigo}:")
        for ticket in vuelo.tickets:
            print(f"    Ticket #{ticket.numero}: {ticket.pasajero.nombre} {ticket.pasajero.apellido}")
    
    try:
        codigo_vuelo = solicitar_texto("\nCódigo de vuelo: ").upper()
        numero_ticket = solicitar_entero("Número de ticket a cancelar: ")
        
        sistema.cancelar_ticket(codigo_vuelo, numero_ticket)
        print(f"\n✓ Ticket cancelado exitosamente")
        print(f"  Se liberó el asiento y se eliminó el equipaje asociado (si existía)")
    except EntidadNoEncontradaException as e:
        print(f"\n✗ Error: {e}")
    
    pausar()

def cancelar_vuelo(sistema):
    """Opción 9: Cancelar vuelo"""
    limpiar_pantalla()
    print("="*60)
    print("CANCELAR VUELO")
    print("="*60)
    
    vuelos_activos = sistema.obtener_vuelos_activos()
    if len(vuelos_activos) < 2:
        print("\n✗ Se necesitan al menos 2 vuelos activos (uno para cancelar y otro para reasignar).")
        pausar()
        return
    
    print("\nVuelos activos:")
    for vuelo in vuelos_activos:
        cant_pasajeros = len(vuelo.tickets)
        print(f"  - {vuelo.codigo}: {vuelo.origen} → {vuelo.destino} ({cant_pasajeros} pasajeros)")
    
    try:
        codigo_vuelo = solicitar_texto("\nCódigo del vuelo a cancelar: ").upper()
        codigo_vuelo_destino = solicitar_texto("Código del vuelo para reasignar: ").upper()
        causa = solicitar_texto("Causa de la cancelación: ")
        
        sistema.cancelar_vuelo(codigo_vuelo, codigo_vuelo_destino, causa)
        print(f"\n✓ Vuelo cancelado exitosamente")
        print(f"  Pasajeros, personal y equipaje reasignados al vuelo {codigo_vuelo_destino}")
    except (EntidadNoEncontradaException, VueloCompletoException, DatoInvalidoException) as e:
        print(f"\n✗ Error: {e}")
    
    pausar()

def menu_informes(sistema):
    """Submenú de informes"""
    while True:
        limpiar_pantalla()
        print("="*60)
        print("MENÚ DE INFORMES")
        print("="*60)
        print("\n1. Informe de pasajeros por vuelo")
        print("2. Informe de personal asignado")
        print("3. Informe de vuelos por compañía")
        print("4. Informe de vuelos cancelados")
        print("0. Volver al menú principal")
        
        opcion = solicitar_entero("\nSeleccione opción: ")
        
        if opcion == 1:
            limpiar_pantalla()
            if not sistema.vuelos:
                print("\n✗ No hay vuelos registrados.")
                pausar()
                continue
            
            print("Vuelos disponibles:")
            for vuelo in sistema.vuelos:
                print(f"  - {vuelo.codigo}")
            
            try:
                codigo_vuelo = solicitar_texto("\nCódigo de vuelo: ").upper()
                print(sistema.informe_pasajeros_por_vuelo(codigo_vuelo))
            except EntidadNoEncontradaException as e:
                print(f"\n✗ Error: {e}")
            pausar()
            
        elif opcion == 2:
            limpiar_pantalla()
            if not sistema.vuelos:
                print("\n✗ No hay vuelos registrados.")
                pausar()
                continue
            
            print("Vuelos disponibles:")
            for vuelo in sistema.vuelos:
                print(f"  - {vuelo.codigo}")
            
            try:
                codigo_vuelo = solicitar_texto("\nCódigo de vuelo: ").upper()
                print(sistema.informe_personal_asignado(codigo_vuelo))
            except EntidadNoEncontradaException as e:
                print(f"\n✗ Error: {e}")
            pausar()
            
        elif opcion == 3:
            limpiar_pantalla()
            print(sistema.informe_vuelos_por_compania())
            pausar()
            
        elif opcion == 4:
            limpiar_pantalla()
            print(sistema.informe_vuelos_cancelados())
            pausar()
            
        elif opcion == 0:
            break
        else:
            print("\n✗ Opción inválida")
            pausar()

def menu_principal():
    """Menú principal del sistema"""
    sistema = Sistema()
    
    while True:
        limpiar_pantalla()
        print("="*60)
        print("SISTEMA DE GESTIÓN DE AEROPUERTO MERCOSUR")
        print("="*60)
        print("\n1. Registrar persona (cliente o tripulante)")
        print("2. Registrar compañía aérea")
        print("3. Crear vuelo")
        print("4. Crear ticket (asignar pasajero a vuelo)")
        print("5. Asignar personal a vuelo")
        print("6. Registrar equipaje en bodega")
        print("7. Visualizar vuelos")
        print("8. Cancelar ticket")
        print("9. Cancelar vuelo")
        print("10. Informes")
        print("0. Salir")
        
        opcion = solicitar_entero("\nSeleccione opción: ")
        
        if opcion == 1:
            registrar_persona(sistema)
        elif opcion == 2:
            registrar_compania(sistema)
        elif opcion == 3:
            crear_vuelo(sistema)
        elif opcion == 4:
            crear_ticket(sistema)
        elif opcion == 5:
            asignar_personal(sistema)
        elif opcion == 6:
            registrar_equipaje(sistema)
        elif opcion == 7:
            visualizar_vuelos(sistema)
        elif opcion == 8:
            cancelar_ticket(sistema)
        elif opcion == 9:
            cancelar_vuelo(sistema)
        elif opcion == 10:
            menu_informes(sistema)
        elif opcion == 0:
            limpiar_pantalla()
            print("\n¡Gracias por usar el sistema!")
            print("="*60)
            break
        else:
            print("\n✗ Opción inválida")
            pausar()

if __name__ == "__main__":
    menu_principal()