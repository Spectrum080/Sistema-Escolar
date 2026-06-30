import os                                      # Lib nativa para el SO

ARCHIVO = "estudiantes.txt"                    # Nombre de la BD

# ==========================================
# FUNCIONES AUXILIARES Y DE MEMORIA
# ==========================================

def confirmar_accion(mensaje):                 # RECURSIVIDAD: Valida S/N
    respuesta = input(mensaje + " (SI/NO): ").strip().upper()
    if respuesta == 'SI':
        return True                            # Continúa la acción
    elif respuesta == 'NO':
        return False                           # Aborta la acción
    else:
        print("Entrada no válida. Ingresa 'SI' o 'NO'.")
        return confirmar_accion(mensaje)       # Llamada recursiva si se equivoca

def Registro_estudiantes():                    # Vuelca el txt a RAM
    estudiantes = []                           # Lista vacía inicial
    if not os.path.exists(ARCHIVO):
        return estudiantes                     # Regresa vacío para no crashear
        
    with open(ARCHIVO, "r", encoding="utf-8") as f: # Abre modo lectura ("r")
        for dato in f:                         # Itera línea x línea
            dato = dato.strip()                # Limpia saltos de línea (\n)
            if not dato: continue              # Ignora líneas vacías
            
            campos = dato.split("|")           # Separa campos por "|"
            if len(campos) == 6:               # Valida 6 campos exactos
                estudiante = {                 # Arma DICCIONARIO
                    "matricula": campos[0],
                    "nombre": campos[1],
                    "carrera": campos[2],
                    "semestre": int(campos[3]),    # Casteo a int
                    "promedio": float(campos[4]),  # Casteo a float
                    "activo": campos[5] == "True"  # String a booleano
                }
                estudiantes.append(estudiante) # Inyecta a matriz principal
    return estudiantes                         # Retorna datos listos

def guardar_datos(estudiantes):                # Vuelca RAM al disco
    with open(ARCHIVO, "w", encoding="utf-8") as f: # Abre modo escritura ("w")
        for est in estudiantes:
            # Arma string interpolando las keys
            campos = f"{est['matricula']}|{est['nombre']}|{est['carrera']}|{est['semestre']}|{est['promedio']}|{est['activo']}\n"
            f.write(campos)                    # Sobrescribe en el txt

def buscar_por_matricula(estudiantes, matricula): # Función Helper (DRY)
    for i in range(len(estudiantes)):          # Busca por índice
        if estudiantes[i]["matricula"] == matricula and estudiantes[i]["activo"] == True:
            return i                           # Regresa posición de match
    return -1                                  # -1 si no existe (código error)

# ==========================================
# FUNCIONES PRINCIPALES (CRUD)
# ==========================================

def registrar_estudiante():                    # CRUD: Create
    print("\n [ Registro de nuevo ingreso ] -------------- \n")
    estudiantes = Registro_estudiantes()       # Carga BD
    
    matricula = input("Matrícula: ").strip()   # Input y limpia espacios
    if buscar_por_matricula(estudiantes, matricula) != -1:
        print("Ya existe un estudiante activo con esa matrícula.") 
        return                                 # Corta ejecución si hay duplicado
        
    nombre = input("Nombre completo: ").strip()
    carrera = input("Carrera: ").strip()
    
    try:                                       # Control de inputs numéricos
        semestre = int(input("Semestre: "))
        promedio = float(input("Promedio (0-10): "))
    except ValueError:
        print("Error: Semestre y promedio deben ser numéricos.") # Msj error
        return                                 # Aborta registro
        
    nuevo_estudiante = {                       # Dict del nuevo ingreso
        "matricula": matricula,
        "nombre": nombre,
        "carrera": carrera,
        "semestre": semestre,
        "promedio": promedio,
        "activo": True                         # Activo x defecto
    }
    
    estudiantes.append(nuevo_estudiante)       # Mete a lista
    guardar_datos(estudiantes)                 # Vuelca al txt
    print("\n [ Estudiante registrado exitosamente en la BD ] -------------- \n") # Msj info

def consultar_todos():                         # CRUD: Read All
    print("\n [ Lista de todos los Estudiantes ] -------------- \n")
    estudiantes = Registro_estudiantes()       # Carga BD
    hay_estudiantes = False                    # Bandera
    
    for est in estudiantes:                    # Itera matriz
        if est["activo"]:                      # Filtra activos (bool)
            hay_estudiantes = True             # Prende bandera
            print(f"Matrícula: {est['matricula']} | Nombre: {est['nombre']} | Carrera: {est['carrera']} | Semestre: {est['semestre']} | Promedio: {est['promedio']}")
            
    if not hay_estudiantes:
        print("No hay estudiantes registrados o activos en el sistema aun.") # Msj vacío
    print("\n")

def buscar_estudiante():                       # CRUD: Read One
    print("\n [ Buscar Estudiante ] -------------- \n")
    matricula = input("Introduce la matrícula en especifico: ").strip()
    estudiantes = Registro_estudiantes()       # Carga BD
    indice = buscar_por_matricula(estudiantes, matricula) # Usa helper
    
    if indice != -1:                           # Si hay match
        est = estudiantes[indice]              # Aisla dict
        print("\nEstudiante encontrado: \n")
        print(f"Matrícula: {est['matricula']}")
        print(f"Nombre: {est['nombre']}")
        print(f"Carrera: {est['carrera']}")
        print(f"Semestre: {est['semestre']}")
        print(f"Promedio: {est['promedio']}")
    else:
        print("\n Estudiante no encontrado o borrado de la BD. \n") # Msj error

def modificar_promedio():                      # CRUD: Update
    print("\n [ Modificar Promedio ] -------------- \n")
    matricula = input("Introduce la matrícula del estudiante: ").strip()
    estudiantes = Registro_estudiantes()       # Carga BD
    indice = buscar_por_matricula(estudiantes, matricula) # Busca pos
    
    if indice != -1:                           # Si existe
        if confirmar_accion(f"¿Seguro de alterar promedio a {estudiantes[indice]['nombre']}?"): # Msj recursivo
            try:
                nuevo_promedio = float(input(f"Promedio actual ({estudiantes[indice]['promedio']}) - Nuevo: "))
                estudiantes[indice]["promedio"] = nuevo_promedio # Machaca valor
                guardar_datos(estudiantes)     # Vuelca a txt
                print("\n-Promedio actualizado correctamente en la BD.\n") # Msj info
            except ValueError:
                print("Error: El promedio debe ser numérico.") # Msj error
        else:
            print("Operación cancelada por el usuario.") # Msj aborto
    else:
        print("Estudiante no encontrado.")     # Msj error

def eliminar_estudiante():                     # CRUD: Delete (Lógico)
    print("\n [ Eliminar Estudiante ] -------------- \n")
    matricula = input("Introduce la matrícula a eliminar: ").strip()
    estudiantes = Registro_estudiantes()       # Carga BD
    indice = buscar_por_matricula(estudiantes, matricula) # Busca pos
    
    if indice != -1:                           # Si existe
        if confirmar_accion(f"¿ABSOLUTAMENTE seguro de ELIMINAR a {estudiantes[indice]['nombre']}?"): # Msj crítico
            estudiantes[indice]["activo"] = False # Borrado lógico (bool a False)
            guardar_datos(estudiantes)         # Vuelca txt
            print("\n-Estudiante eliminado exitosamente (Borrado Lógico).\n") # Msj info
        else:
            print("Operación de borrado cancelada.") # Msj aborto
    else:
        print("\n-Estudiante no encontrado.\n") # Msj error

def mostrar_excelencia():                      # Filtro Especial
    print("\n [ Estudiantes con Promedio >= 9.0 ] -------------- \n")
    estudiantes = Registro_estudiantes()       # Carga BD
    hay_excelencia = False                     # Bandera
    
    for est in estudiantes:
        if est["activo"] and est["promedio"] >= 9.0: # Doble filtro
            hay_excelencia = True              # Prende bandera
            print(f"Matrícula: {est['matricula']} | Nombre: {est['nombre']} | Promedio: {est['promedio']} | Carrera: {est['carrera']}")
            
    if not hay_excelencia:
        print("\n-Nadie con promedio >= 9.0.\n") # Msj promedio -9

def menu():                                    # Controlador Principal
    while True:                                # Ciclo infinito
        print("-" * 45)
        print(" Sistema de control escolar | Menú Principal ")
        print("-" * 45)
        print("1.Registrar estudiante")
        print("2.Consultar todos los estudiantes")
        print("3.Buscar estudiante por matrícula")
        print("4.Modificar promedio")
        print("5.Eliminar estudiante")
        print("6.Mostrar estudiantes con promedio mayor o igual a 9.0")
        print("7. Salir")
        print("-" * 45)
        
        opcion = input("Selecciona una opción ¡VALIDA!(1-7): ").strip()
        
        if opcion == "1": registrar_estudiante()
        elif opcion == "2": consultar_todos()
        elif opcion == "3": buscar_estudiante()
        elif opcion == "4": modificar_promedio()
        elif opcion == "5": eliminar_estudiante()
        elif opcion == "6": mostrar_excelencia()
        elif opcion == "7":
            print("Saliendo del Menu...")      # Despedida
            break                              # Rompe While True
        else:
            print("Opción no encontrada. Intenta de nuevo.") # Msj error

if __name__ == "__main__":                     # Buena práctica de módulo
    menu()                                     # Inicia app
