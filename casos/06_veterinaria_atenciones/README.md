# Veterinaria - Servicios para mascotas

## Contexto
Una veterinaria revisa atenciones, servicios y costos por mascota.

## Tablas
- `mascotas`: datos de mascotas.
- `servicios`: catalogo de servicios.
- `sedes`: sedes, zonas o puntos de operacion.
- `atenciones`: tabla principal con 500 registros y claves foraneas.

## Reto PMD1
Predecir el costo del servicio usando el peso de la mascota.

Variable objetivo sugerida: `costo_servicio`.
Variable predictora basica sugerida: `peso_mascota_kg`.

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
    p.nombre AS mascota,
    p.distrito AS distrito_mascota,
    p.segmento,
    i.nombre AS servicio,
    i.categoria,
    l.nombre AS sede,
    l.zona,
    f.fecha_operacion,
    f.cantidad_servicios,
    f.peso_mascota_kg,
    f.tarifa_base,
    f.descuento_pct,
    f.canal,
    f.metodo_pago,
    f.calificacion,
    f.costo_servicio
FROM atenciones f
LEFT JOIN mascotas p ON f.id_mascota = p.id_mascota
LEFT JOIN servicios i ON f.id_servicio = i.id_servicio
LEFT JOIN sedes l ON f.id_sede = l.id_sede;
```
