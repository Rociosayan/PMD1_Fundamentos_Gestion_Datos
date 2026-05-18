# Gimnasio - Socios y asistencias

## Contexto
Un gimnasio analiza pagos, asistencias y planes contratados.

## Tablas
- `socios`: datos de socios.
- `planes`: catalogo de plans.
- `sedes`: sedes, zonas o puntos de operacion.
- `asistencias_pagos`: tabla principal con 500 registros y claves foraneas.

## Reto PMD1
Predecir el pago mensual usando las asistencias del mes.

Variable objetivo sugerida: `pago_mensual`.
Variable predictora basica sugerida: `asistencias_mes`.

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
    f.id_registro,
    p.nombre AS socio,
    p.distrito AS distrito_socio,
    p.segmento,
    i.nombre AS plan,
    i.categoria,
    l.nombre AS sede,
    l.zona,
    f.fecha_operacion,
    f.clases_tomadas,
    f.asistencias_mes,
    f.tarifa_plan,
    f.descuento_pct,
    f.canal,
    f.metodo_pago,
    f.calificacion,
    f.pago_mensual
FROM asistencias_pagos f
LEFT JOIN socios p ON f.id_socio = p.id_socio
LEFT JOIN planes i ON f.id_plan = i.id_plan
LEFT JOIN sedes l ON f.id_sede = l.id_sede;
```
