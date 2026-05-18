# Guia docente PMD1

## Enfoque recomendado

Cada grupo elige un caso distinto. Todos los casos tienen la misma dificultad tecnica:

1. Base SQLite con 4 tablas relacionadas.
2. Tabla principal con 500 registros.
3. Datos sucios controlados.
4. Consulta SQL con `JOIN`.
5. Limpieza en Pandas.
6. Regresion lineal simple.
7. Guardado de resultados limpios en SQLite.

## Como explicar PK y FK

La base no debe ser una sola tabla plana. La estructura ideal es:

- Tabla de personas o clientes: tiene una clave primaria, por ejemplo `id_cliente`.
- Tabla de productos, servicios o items: tiene una clave primaria, por ejemplo `id_producto`.
- Tabla de sedes, zonas o locales: tiene una clave primaria, por ejemplo `id_sucursal`.
- Tabla principal: contiene las operaciones y guarda claves foraneas como `id_cliente`, `id_producto` e `id_sucursal`.

El estudiante arma su dataset final con SQL:

```sql
SELECT *
FROM ventas v
JOIN clientes c ON v.id_cliente = c.id_cliente
JOIN productos p ON v.id_producto = p.id_producto
JOIN sucursales s ON v.id_sucursal = s.id_sucursal;
```

## Limpieza esperada

Los estudiantes deben resolver al menos:

- Espacios en blanco con `.str.strip()`.
- Mayusculas/minusculas con `.str.title()` o `.str.upper()`.
- Valores nulos con imputacion o eliminacion justificada.
- Duplicados con `.drop_duplicates()`.
- Numeros en texto, por ejemplo `S/ 45.90` o `45,90`.
- Fechas con formatos distintos usando `pd.to_datetime()`.
- Valores extremos revisados con graficos o reglas simples.

## Regresion lineal simple

Para PMD1 se recomienda una sola variable predictora numerica.

Ejemplos:

- Retail: `cantidad_productos` -> `monto_total`.
- Restaurante: `tiempo_preparacion_min` -> `total_pedido`.
- Delivery: `distancia_km` -> `tiempo_entrega_min`.
- Hotel: `noches_estadia` -> `monto_reserva`.
- Cultivos: `hectareas` -> `rendimiento_kg`.

El objetivo no es hacer el mejor modelo del mundo, sino demostrar el flujo completo:

SQL -> Pandas -> Limpieza -> Regresion -> Interpretacion -> SQLite.

## Entregables sugeridos

- Notebook Colab reproducible.
- Base SQLite descargada desde GitHub o generada desde el caso.
- Tabla limpia guardada en SQLite.
- Tabla de predicciones guardada en SQLite.
- Informe breve con interpretacion de resultados.

## Evaluacion sugerida

| Criterio | Peso |
|---|---:|
| Conexion y consultas SQL con `JOIN` | 20% |
| Comprension de PK/FK y estructura relacional | 15% |
| Limpieza de datos con Pandas | 25% |
| Regresion lineal simple y metricas | 20% |
| Guardado de tabla limpia/predicciones en SQLite | 10% |
| Interpretacion del caso y conclusiones | 10% |

