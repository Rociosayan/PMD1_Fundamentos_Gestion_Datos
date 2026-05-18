# HotelSmart - Reservas hoteleras

## Contexto
Un hotel analiza reservas, tipo de habitacion y monto facturado.

## Tablas
- `huespedes`: datos de huespeds.
- `habitaciones`: catalogo de habitacions.
- `hoteles`: sedes, zonas o puntos de operacion.
- `reservas`: tabla principal con 500 registros y claves foraneas.

## Reto PMD1
Predecir el monto de reserva a partir de las noches de estadia.

Variable objetivo sugerida: `monto_reserva`.
Variable predictora basica sugerida: `noches_estadia`.

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
    f.id_reserva,
    p.nombre AS huesped,
    p.distrito AS distrito_huesped,
    p.segmento,
    i.nombre AS habitacion,
    i.categoria,
    l.nombre AS hotel,
    l.zona,
    f.fecha_operacion,
    f.cantidad_habitaciones,
    f.noches_estadia,
    f.tarifa_noche,
    f.descuento_pct,
    f.canal,
    f.metodo_pago,
    f.calificacion,
    f.monto_reserva
FROM reservas f
LEFT JOIN huespedes p ON f.id_huesped = p.id_huesped
LEFT JOIN habitaciones i ON f.id_habitacion = i.id_habitacion
LEFT JOIN hoteles l ON f.id_hotel = l.id_hotel;
```
