# Sistema de Control Escolar (Gestión Estudiantil)

Este repositorio contiene un sistema interactivo de consola programado en lenguaje Python, diseñado para permitir el registro, consulta y procesamiento de información académica de estudiantes.

El núcleo del programa opera sobre el manejo de persistencia de datos mediante archivos de texto (`estudiantes.txt`), manipulando la información a través de estructuras de datos para gestionar operaciones de altas, bajas y modificaciones bajo un enfoque de programación estructurada.

## Equipo de Desarrollo

Proyecto desarrollado en la **Universidad del Valle de México (UVM)**, para la carrera de Ingeniería en Sistemas Computacionales.

![Carlos](https://img.shields.io/badge/GitHub-Carlos-181717?logo=github) ![Santiago](https://img.shields.io/badge/GitHub-Santiago-181717?logo=github)

## Características Técnicas

* **Gestión Persistente de Archivos:** Lectura, escritura y anexado de datos en formato de texto plano (CSV-style) para almacenar matrícula, nombre, carrera, semestre, promedio y estado de cada estudiante.
* **Sistema CRUD con Borrado Lógico:** Capacidad para registrar nuevos estudiantes, buscar por matrícula, modificar promedios y eliminar registros mediante un cambio de estado a "Inactivo" para mantener la integridad histórica de la base de datos.
* **Filtros de Búsqueda:** Módulo de consulta condicional para iterar sobre los registros y extraer métricas específicas, como la generación de reportes de estudiantes destacados (Promedio >= 90).
* **Control de Flujo y Recursividad:** Estructuración del código en funciones y procedimientos independientes, integrando menús de decisión iterativos y confirmaciones recursivas para garantizar la seguridad en acciones críticas.
