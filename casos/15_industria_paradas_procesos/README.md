# Caso 15 - Industria Paradas Procesos

## Enfoque del caso

Este caso entrega una sola tabla desnormalizada para que el estudiante identifique datos repetidos y proponga el modelo normalizado.

La base no incluye tablas normalizadas, claves foraneas ni una solucion relacional ya construida.

## Archivo SQLite

- `industria_paradas_procesos.db`

## Tabla disponible

- `paradas_original`: tabla de partida con 500 registros. Mezcla datos de la operacion principal con datos descriptivos de clientes, productos, sedes, categorias u otras entidades del caso.

## Reto PMD1

1. Explorar la tabla original.
2. Detectar patrones repetidos y dependencias entre columnas.
3. Proponer entidades, claves primarias y claves foraneas.
4. Crear las tablas normalizadas en SQLite.
5. Insertar los datos desde `paradas_original` hacia las nuevas tablas.
6. Reconstruir un reporte con `JOIN` para validar que no se perdio informacion.
7. Limpiar datos con Pandas y preparar un dataset analitico.

Variable objetivo sugerida: `costo_parada_soles`.
Variable predictora basica sugerida: `duracion_parada_min`.

## Archivo CSV

La carpeta `csv/` contiene solo la tabla original:

- `paradas_original.csv`
