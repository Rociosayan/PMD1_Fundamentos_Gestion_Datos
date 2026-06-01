# Caso 12 - Gimnasio Socios

## Enfoque del caso

Este caso entrega una sola tabla desnormalizada para que el estudiante identifique datos repetidos y proponga el modelo normalizado.

La base no incluye tablas normalizadas, claves foraneas ni una solucion relacional ya construida.

## Archivo SQLite

- `gimnasio_socios.db`

## Tabla disponible

- `asistencias_pagos_original`: tabla de partida con 500 registros. Mezcla datos de la operacion principal con datos descriptivos de clientes, productos, sedes, categorias u otras entidades del caso.

## Reto PMD1

1. Explorar la tabla original.
2. Detectar patrones repetidos y dependencias entre columnas.
3. Proponer entidades, claves primarias y claves foraneas.
4. Crear las tablas normalizadas en SQLite.
5. Insertar los datos desde `asistencias_pagos_original` hacia las nuevas tablas.
6. Reconstruir un reporte con `JOIN` para validar que no se perdio informacion.
7. Limpiar datos con Pandas y preparar un dataset analitico.

Variable objetivo sugerida: `pago_mensual`.
Variable predictora basica sugerida: `asistencias_mes`.

## Archivo CSV

La carpeta `csv/` contiene solo la tabla original:

- `asistencias_pagos_original.csv`
