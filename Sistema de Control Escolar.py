def registrar_estudiante():                  # Registra datos y los guarda en estudiantes.txt
    matricula = input("Matrícula: ")
    nombre = input("Nombre completo: ")
    carrera = input("Carrera: ")
    semestre = input("Semestre: ")
    promedio = float(input("Promedio: "))
    estado = "Activo"

    archivo = open("estudiantes.txt", "a")
    archivo.write(matricula + "," + nombre + "," + carrera + "," + semestre + "," + str(promedio) + "," + estado + "\n")
    archivo.close()

    print("Estudiante registrado exitosamente.")

def consultar_estudiantes():                 # Lista todos los estudiantes con estado "Activo"
    archivo = open("estudiantes.txt", "r")
    
    print("\n--- LISTADO DE ESTUDIANTES ---")
    for linea in archivo:
        datos = linea.split(",")
        if datos[5].strip() == "Activo":
            print("Matrícula:", datos[0])
            print("Nombre:", datos[1])
            print("Carrera:", datos[2])
            print("Semestre:", datos[3])
            print("Promedio:", datos[4])
            print("------------------------------")
            
    archivo.close()

def buscar_estudiante():                     # Localiza y muestra un estudiante por su matrícula
    matricula_buscar = input("Matrícula a buscar: ")
    archivo = open("estudiantes.txt", "r")
    encontrado = False

    for linea in archivo:
        datos = linea.split(",")
        if datos[0] == matricula_buscar and datos[5].strip() == "Activo":
            print("Nombre:", datos[1])
            print("Carrera:", datos[2])
            print("Semestre:", datos[3])
            print("Promedio:", datos[4])
            encontrado = True

    archivo.close()

    if encontrado == False:
        print("No existe la matrícula o el estudiante fue dado de baja.")

def modificar_promedio():                    # Reescribe el archivo con el promedio actualizado
    matricula_buscar = input("Matrícula del estudiante a modificar: ")
    
    archivo = open("estudiantes.txt", "r")
    lineas = archivo.readlines()
    archivo.close()

    archivo = open("estudiantes.txt", "w")
    encontrado = False
    
    for linea in lineas:
        datos = linea.split(",")
        if datos[0] == matricula_buscar and datos[5].strip() == "Activo":
            nuevo_promedio = float(input("Ingrese el nuevo promedio: "))
            nueva_linea = datos[0] + "," + datos[1] + "," + datos[2] + "," + datos[3] + "," + str(nuevo_promedio) + "," + datos[5]
            archivo.write(nueva_linea)
            encontrado = True
            print("Promedio actualizado correctamente.")
        else:
            archivo.write(linea)
            
    archivo.close()
    
    if encontrado == False:
        print("Estudiante no encontrado.")

def eliminar_estudiante():                   # Cambia el estado a "Inactivo" (Borrado lógico)
    matricula_buscar = input("Matrícula del estudiante a eliminar: ")
    
    archivo = open("estudiantes.txt", "r")
    lineas = archivo.readlines()
    archivo.close()

    archivo = open("estudiantes.txt", "w")
    encontrado = False
    
    for linea in lineas:
        datos = linea.split(",")
        if datos[0] == matricula_buscar and datos[5].strip() == "Activo":
            nueva_linea = datos[0] + "," + datos[1] + "," + datos[2] + "," + datos[3] + "," + datos[4] + ",Inactivo\n"
            archivo.write(nueva_linea)
            encontrado = True
            print("Estudiante eliminado del sistema (Borrado lógico).")
        else:
            archivo.write(linea)
            
    archivo.close()
    
    if encontrado == False:
        print("Estudiante no encontrado.")

def mostrar_destacados():                    # Filtra y muestra estudiantes con promedio >= 90
    archivo = open("estudiantes.txt", "r")
    
    print("\n--- ESTUDIANTES DESTACADOS (Promedio >= 90) ---")
    for linea in archivo:
        datos = linea.split(",")
        if datos[5].strip() == "Activo":
            promedio = float(datos[4])
            if promedio >= 90.0:
                print("Matrícula:", datos[0], "- Nombre:", datos[1], "- Promedio:", promedio)
            
    archivo.close()

def menu():                                  # Controla la ejecución y las opciones del usuario
    opcion = 0
    while opcion != 7:
        print("\n=== SISTEMA DE CONTROL ESCOLAR ===")
        print("1. Registrar estudiante")
        print("2. Consultar todos los estudiantes")
        print("3. Buscar estudiante por matrícula")
        print("4. Modificar promedio")
        print("5. Eliminar estudiante")
        print("6. Mostrar estudiantes destacados")
        print("7. Salir")
        
        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            registrar_estudiante()
        elif opcion == 2:
            consultar_estudiantes()
        elif opcion == 3:
            buscar_estudiante()
        elif opcion == 4:
            modificar_promedio()
        elif opcion == 5:
            eliminar_estudiante()
        elif opcion == 6:
            mostrar_destacados()
        elif opcion == 7:
            print("Saliendo del sistema...")
        else:
            print("Opción Incorrecta")

menu()