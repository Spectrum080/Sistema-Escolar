import os                                                                                        # Importa módulo nativo para interactuar con el sistema operativo

ARCHIVO = "estudiantes.txt"                                                                      # Define la constante con el nombre del archivo de base de datos

# ==========================================
# FUNCIONES AUXILIARES Y DE MEMORIA
# ==========================================

def confirmar_accion(mensaje):
    """Función recursiva que exige validación estricta de SI/NO para acciones críticas."""
    respuesta = input(mensaje + " (SI/NO): ").strip().upper()                                    # Captura entrada, elimina espacios y convierte a mayúsculas
    if respuesta == 'SI':
        return True                                                                              # Retorna verdadero para confirmar la operación afirmativa
    elif respuesta == 'NO':
        return False                                                                             # Retorna falso para abortar la operación actual
    else:
        print("Entrada no válida. Ingresa 'SI' o 'NO'.")                                         # Notifica al usuario sobre una entrada fuera de formato
        return confirmar_accion(mensaje)                                                         # Ejecuta llamada recursiva hasta obtener una respuesta válida

def Registro_estudiantes():
    """Lee el archivo .txt y carga los registros activos en una lista de diccionarios en RAM."""
    estudiantes = []                                                                             # Inicializa la estructura de datos principal en memoria
    if not os.path.exists(ARCHIVO):
        return estudiantes                                                                       # Retorna la lista vacía si el archivo físico aún no existe
        
    with open(ARCHIVO, "r", encoding="utf-8") as f:                                              # Abre el archivo en modo lectura gestionando recursos seguramente
        for dato in f:                                                                           # Itera secuencialmente cada línea del documento
            dato = dato.strip()                                                                  # Elimina saltos de línea y espacios en blanco extremos
            if not dato: continue                                                                # Omite la iteración si la línea evaluada se encuentra vacía
            
            campos = dato.split("|")                                                             # Divide la cadena de texto utilizando el delimitador "|"
            if len(campos) == 6:                                                                 # Valida que la estructura del registro contenga 6 campos exactos
                estudiante = {                                                                   # Estructura los datos extraídos en un diccionario
                    "matricula": campos[0],
                    "nombre": campos[1],
                    "carrera": campos[2],
                    "semestre": int(campos[3]),                                                  # Convierte el tipo de dato de cadena a número entero
                    "promedio": float(campos[4]),                                                # Convierte el tipo de dato de cadena a decimal flotante
                    "activo": campos[5] == "True"                                                # Evalúa la cadena para asignar un valor booleano real
                }
                estudiantes.append(estudiante)                                                   # Añade el diccionario del estudiante a la lista principal
    return estudiantes                                                                           # Devuelve la lista estructurada con los registros procesados

def guardar_datos(estudiantes):
    """Sobrescribe el archivo .txt volcando la información actual de la memoria RAM."""
    with open(ARCHIVO, "w", encoding="utf-8") as f:                                              # Abre el archivo en modo escritura para sobrescritura total
        for est in estudiantes:                                                                  # Itera sobre la lista de diccionarios en memoria
            # Formatea los datos en una sola cadena de texto delimitada por caracteres "|"
            campos = f"{est['matricula']}|{est['nombre']}|{est['carrera']}|{est['semestre']}|{est['promedio']}|{est['activo']}\n"
            f.write(campos)                                                                      # Ejecuta la escritura de la cadena formateada en el almacenamiento físico

def buscar_por_nombre(nombre, estudiantes):
    """Itera sobre la lista buscando un match exacto por nombre."""
    for i in range(len(estudiantes)):                                                            # Itera utilizando los índices numéricos de la lista
        # Compara nombres en minúsculas para ignorar capitalización y valida estado activo del registro
        if estudiantes[i]["nombre"].lower() == nombre.lower() and estudiantes[i]["activo"] == True:
            return i                                                                             # Retorna el índice exacto donde se encontró el registro
    return -1                                                                                    # Retorna código -1 indicando que la búsqueda no obtuvo resultados

def buscar_por_matricula(estudiantes, matricula):
    """Itera sobre la lista buscando un match exacto por matrícula (DRY)."""
    for i in range(len(estudiantes)):                                                            # Itera utilizando los índices numéricos de la lista
        # Compara la matrícula exacta y verifica que el registro no esté dado de baja lógicamente
        if estudiantes[i]["matricula"] == matricula and estudiantes[i]["activo"] == True:
            return i                                                                             # Retorna el índice numérico correspondiente al registro
    return -1                                                                                    # Retorna código -1 indicando ausencia de coincidencias

# ==========================================
# FUNCIONES PRINCIPALES (CRUD)
# ==========================================

def registrar_estudiante():
    """Captura los datos de un nuevo estudiante, valida duplicados y guarda en la BD."""
    os.system('cls' if os.name == 'nt' else 'clear')                                             # Limpia la consola para renderizar la vista específica
    print("\n [ Registro de nuevo ingreso ] -------------- \n")
    estudiantes = Registro_estudiantes()                                                         # Carga el estado actual de la base de datos a memoria
    
    matricula = input("Matrícula: ").strip()                                                     # Solicita la captura de datos y limpia espacios residuales
    if buscar_por_matricula(estudiantes, matricula) != -1:
        print("Ya existe un estudiante activo con esa matrícula.") 
        return                                                                                   # Interrumpe la ejecución del módulo para prevenir duplicidad
        
    nombre = input("Nombre completo: ").strip()
    carrera = input("Carrera: ").strip()
    
    try:                                                                                         # Implementa bloque de manejo de excepciones para inputs numéricos
        semestre = int(input("Semestre: "))
        promedio = float(input("Promedio (0-10): "))
    except ValueError:
        print("Error: El semestre y el promedio deben contener valores estrictamente numéricos.")# Muestra mensaje de error
        return                                                                                   # Aborta el proceso de registro por inconsistencia de tipos de datos
        
    nuevo_estudiante = {                                                                         # Instancia el diccionario para el nuevo registro
        "matricula": matricula,
        "nombre": nombre,
        "carrera": carrera,
        "semestre": semestre,
        "promedio": promedio,
        "activo": True                                                                           # Asigna el estado activo por defecto a las nuevas inserciones
    }
    
    estudiantes.append(nuevo_estudiante)                                                         # Incorpora el nuevo registro a la matriz principal
    guardar_datos(estudiantes)                                                                   # Sincroniza la estructura de datos en memoria con el archivo de texto
    print("\n [ Estudiante registrado exitosamente en la BD ] -------------- \n")                # Emite confirmación de operación

def consultar_todos():
    """Imprime en consola todos los registros que se encuentren con estado activo."""
    os.system('cls' if os.name == 'nt' else 'clear')                                             # Limpia la consola para renderizar la vista específica
    print("\n [ Lista de todos los Estudiantes ] -------------- \n")
    estudiantes = Registro_estudiantes()                                                         # Recupera la información persistida
    hay_estudiantes = False                                                                      # Inicializa variable de control de estado
    
    for est in estudiantes:                                                                      # Inicia iteración sobre la estructura de datos
        if est["activo"]:                                                                        # Aplica filtro para omitir registros con borrado lógico
            hay_estudiantes = True                                                               # Cambia el estado de la bandera indicando presencia de registros
            print(f"Matrícula: {est['matricula']} | Nombre: {est['nombre']} | Carrera: {est['carrera']} | Semestre: {est['semestre']} | Promedio: {est['promedio']}")
            
    if not hay_estudiantes:
        print("No hay estudiantes registrados o activos en el sistema actualmente.")             # Maneja el escenario de base vacía
    print("\n")

def buscar_estudiante():
    """Permite buscar a un estudiante activo ya sea por matrícula o por nombre completo."""
    os.system('cls' if os.name == 'nt' else 'clear')                                             # Limpia la consola para renderizar la vista específica
    print("\n[ Buscar Estudiante ]--------------\n")
    estudiantes = Registro_estudiantes()                                                         # Recupera la base de datos a la memoria principal

    try:                                                                                         # Implementa manejo de errores preventivo en el submenú
        search = int(input("\nIntroduce 1 para buscar por nombre o 2 para buscar por matrícula: ").strip())
    except ValueError:
        print("Entrada no válida. Se requiere ingresar un valor numérico (1 o 2).")
        return                                                                                   # Interrumpe la operación ante entradas no soportadas

    if search == 1:
        nombre = input("\nIntroduce el nombre del estudiante: ").strip()
        indice = buscar_por_nombre(nombre, estudiantes)                                          # Delega la búsqueda a la función auxiliar de nombre
    elif search == 2:
        matricula = input("Introduce la matrícula del estudiante: ").strip()
        indice = buscar_por_matricula(estudiantes, matricula)                                    # Delega la búsqueda a la función auxiliar de matrícula
    else:
        print("Opción fuera de rango.")
        return                                                                                   # Detiene la ejecución si el selector no coincide

    if indice != -1:                                                                             # Evalúa si la búsqueda arrojó un índice válido
        est = estudiantes[indice]                                                                # Aísla el registro específico localizado
        print("\nEstudiante encontrado:\n")
        print(f"Matrícula: {est['matricula']}")
        print(f"Nombre: {est['nombre']}")
        print(f"Carrera: {est['carrera']}")
        print(f"Semestre: {est['semestre']}")
        print(f"Promedio: {est['promedio']}")
    else:
        print("\nEstudiante no encontrado o dado de baja del sistema.\n")                        # Reporta resultados infructuosos

def modificar_promedio():
    """Localiza un estudiante por matrícula y permite actualizar su promedio previa confirmación."""
    os.system('cls' if os.name == 'nt' else 'clear')                                             # Limpia la consola para renderizar la vista específica
    print("\n [ Modificar Promedio ] -------------- \n")
    matricula = input("Introduce la matrícula del estudiante: ").strip()
    estudiantes = Registro_estudiantes()                                                         # Inicializa la carga de datos
    indice = buscar_por_matricula(estudiantes, matricula)                                        # Determina la posición exacta del registro
    
    if indice != -1:                                                                             # Procede solo si el estudiante fue localizado exitosamente
        if confirmar_accion(f"¿Seguro de alterar promedio a {estudiantes[indice]['nombre']}?"):  # Lanza validación recursiva
            try:
                nuevo_promedio = float(input(f"Promedio actual ({estudiantes[indice]['promedio']}) - Nuevo: "))
                estudiantes[indice]["promedio"] = nuevo_promedio                                 # Modifica el valor en la estructura de memoria
                guardar_datos(estudiantes)                                                       # Ejecuta la sincronización en el almacenamiento físico
                print("\n-Promedio actualizado correctamente en la BD.\n")                       # Confirma el éxito de la transacción
            except ValueError:
                print("Error de tipo: El promedio introducido debe ser un número válido.")       # Control de formato
        else:
            print("Operación cancelada de forma manual por el usuario.")                         # Confirma cancelación voluntaria
    else:
        print("Identificador no encontrado en los registros activos.")                           # Notifica inexistencia

def eliminar_estudiante():
    """Realiza un borrado lógico de un estudiante, cambiando su estado a inactivo en la BD."""
    os.system('cls' if os.name == 'nt' else 'clear')                                             # Limpia la consola para renderizar la vista específica
    print("\n [ Eliminar Estudiante ] -------------- \n")
    matricula = input("Introduce la matrícula a eliminar: ").strip()
    estudiantes = Registro_estudiantes()                                                         # Sincroniza memoria con el archivo
    indice = buscar_por_matricula(estudiantes, matricula)                                        # Rastrea el índice del estudiante
    
    if indice != -1:                                                                             # Valida la existencia previa del registro
        if confirmar_accion(f"¿Estas seguro de ELIMINAR a {estudiantes[indice]['nombre']}?"):    # Confirmación crítica
            estudiantes[indice]["activo"] = False                                                # Ejecuta borrado lógico alterando la bandera booleana
            guardar_datos(estudiantes)                                                           # Persiste el cambio de estado en el archivo físico
            print("\n-Registro dado de baja exitosamente.\n")                                    # Confirma actualización
        else:
            print("Procedimiento de eliminación revocado.")                                      # Reporta la conservación del registro
    else:
        print("\n-No es posible localizar la matrícula solicitada.\n")                           # Error de búsqueda

def mostrar_excelencia():
    """Filtra y muestra únicamente a los estudiantes activos con promedio igual o superior a 9.0."""
    os.system('cls' if os.name == 'nt' else 'clear')                                             # Limpia la consola para renderizar la vista específica
    print("\n [ Estudiantes con Promedio >= 9.0 ] -------------- \n")
    estudiantes = Registro_estudiantes()                                                         # Inicia volcado de datos
    hay_excelencia = False                                                                       # Bandera de control para la presencia de resultados
    
    for est in estudiantes:
        if est["activo"] and est["promedio"] >= 9.0:                                             # Aplica validación condicional múltiple
            hay_excelencia = True                                                                # Registra el hallazgo de elementos que cumplen la condición
            print(f"Matrícula: {est['matricula']} | Nombre: {est['nombre']} | Promedio: {est['promedio']} | Carrera: {est['carrera']}")
            
    if not hay_excelencia:
        print("\n-No hay alumnos con promedio >= 9.0.\n")                                        # Informa ausencia de coincidencias

def menu():
    """Controlador principal del sistema: despliega el menú iterativo y gestiona el flujo de ejecución."""
    while True:                                                                                  # Establece el ciclo infinito del entorno de trabajo
        os.system('cls' if os.name == 'nt' else 'clear')                                         # Limpia el entorno antes de presentar la interfaz principal
        
        print("-" * 45)
        print(" Sistema de control escolar | Menú Principal ")
        print("-" * 45)
        print("1.Registrar estudiante")
        print("2.Consultar todos los estudiantes")
        print("3.Buscar estudiante")
        print("4.Modificar promedio")
        print("5.Eliminar estudiante")
        print("6.Mostrar estudiantes con promedio mayor o igual a 9.0")
        print("7. Salir")
        print("-" * 45)
        
        opcion = input("Selecciona una opción valida: ").strip()
        
        # Ejecución según el módulo seleccionado
        if opcion == "1": registrar_estudiante()
        elif opcion == "2": consultar_todos()
        elif opcion == "3": buscar_estudiante()
        elif opcion == "4": modificar_promedio()
        elif opcion == "5": eliminar_estudiante()
        elif opcion == "6": mostrar_excelencia()
        elif opcion == "7":
            print("Finalizando ejecución del sistema...")                                       # Emite mensaje de despedida
            break                                                                               # Interrumpe el ciclo principal liberando el proceso de la terminal
        else:
            print("Comando no reconocido. Verifique su selección.")                             # Gestiona errores de captura

        # Pausa añadida para permitir al usuario revisar la salida antes de limpiar la pantalla
        input("\nPresiona ENTER para continuar...") 

if __name__ == "__main__":                                                                      # Estándar de protección para la ejecución directa del script
    menu()                                                                                      # Llama a la función orquestadora
