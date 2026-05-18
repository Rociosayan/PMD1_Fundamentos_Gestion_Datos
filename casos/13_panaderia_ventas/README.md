# Panaderia - Ventas diarias

## Contexto
Una panaderia analiza ventas de productos por local y turno.

## Tablas
- `clientes`: datos de clientes.
- `productos`: catalogo de productos.
- `locales`: sedes, zonas o puntos de operacion.
- `ventas`: tabla principal con 500 registros y claves foraneas.

## Reto PMD1
Predecir el ingreso de venta segun la cantidad de unidades vendidas.

Variable objetivo sugerida: `ingreso_venta`.
Variable predictora basica sugerida: `cantidad_unidades`.

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
    f.id_venta,
    p.nombre AS cliente,
    p.distrito AS distrito_cliente,
    p.segmento,
    i.nombre AS producto,
    i.categoria,
    l.nombre AS local,
    l.zona,
    f.fecha_operacion,
    f.cantidad,
    f.cantidad_unidades,
    f.precio_unitario,
    f.descuento_pct,
    f.canal,
    f.metodo_pago,
    f.calificacion,
    f.ingreso_venta
FROM ventas f
LEFT JOIN clientes p ON f.id_cliente = p.id_cliente
LEFT JOIN productos i ON f.id_producto = i.id_producto
LEFT JOIN locales l ON f.id_local = l.id_local;
```
