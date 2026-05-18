# Taller mecanico - Ordenes de servicio

## Contexto
Un taller mecanico analiza costos de reparacion por servicio y sede.

## Tablas
- `clientes`: datos de clientes.
- `servicios`: catalogo de servicios.
- `sedes`: sedes, zonas o puntos de operacion.
- `ordenes`: tabla principal con 500 registros y claves foraneas.

## Reto PMD1
Predecir el costo de reparacion segun las horas de trabajo.

Variable objetivo sugerida: `costo_reparacion`.
Variable predictora basica sugerida: `horas_trabajo`.

## Suciedad incluida
- Espacios en blanco al inicio/final.
- Mayusculas y minusculas inconsistentes.
- Valores nulos.
- Fechas con formatos mezclados.
- Numeros guardados como texto, con coma decimal o simbolo `S/`.
- Duplicados parciales en la tabla principal.
- Algunos valores extremos.

## Consulta base para Pandas

```sql
SELECT
    f.id_orden,
    p.nombre AS cliente,
    p.distrito AS distrito_cliente,
    p.segmento,
    i.nombre AS servicio,
    i.categoria,
    l.nombre AS sede,
    l.zona,
    f.fecha_operacion,
    f.cantidad_repuestos,
    f.horas_trabajo,
    f.tarifa_base,
    f.descuento_pct,
    f.canal,
    f.metodo_pago,
    f.calificacion,
    f.costo_reparacion
FROM ordenes f
LEFT JOIN clientes p ON f.id_cliente = p.id_cliente
LEFT JOIN servicios i ON f.id_servicio = i.id_servicio
LEFT JOIN sedes l ON f.id_sede = l.id_sede;
```
