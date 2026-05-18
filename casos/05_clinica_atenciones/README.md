# Clinica - Atenciones ambulatorias

## Contexto
Una clinica pequena analiza costos de atencion por servicio y sede.

## Tablas
- `pacientes`: datos de pacientes.
- `servicios`: catalogo de servicios.
- `sedes`: sedes, zonas o puntos de operacion.
- `atenciones`: tabla principal con 500 registros y claves foraneas.

## Reto PMD1
Predecir el costo de atencion segun la duracion de la consulta.

Variable objetivo sugerida: `costo_atencion`.
Variable predictora basica sugerida: `duracion_consulta_min`.

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
    f.id_atencion,
    p.nombre AS paciente,
    p.distrito AS distrito_paciente,
    p.segmento,
    i.nombre AS servicio,
    i.categoria,
    l.nombre AS sede,
    l.zona,
    f.fecha_operacion,
    f.cantidad_servicios,
    f.duracion_consulta_min,
    f.tarifa_base,
    f.descuento_pct,
    f.canal,
    f.metodo_pago,
    f.calificacion,
    f.costo_atencion
FROM atenciones f
LEFT JOIN pacientes p ON f.id_paciente = p.id_paciente
LEFT JOIN servicios i ON f.id_servicio = i.id_servicio
LEFT JOIN sedes l ON f.id_sede = l.id_sede;
```
