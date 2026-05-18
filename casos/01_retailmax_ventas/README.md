# RetailMax - Ventas en tienda

## Contexto
Una cadena pequena de tiendas analiza ventas por cliente, producto y sede.

## Tablas
- `clientes`: datos de clientes.
- `productos`: catalogo de productos.
- `sucursales`: sedes, zonas o puntos de operacion.
- `ventas`: tabla principal con 500 registros y claves foraneas.

## Reto PMD1
Predecir el monto total de venta a partir de la cantidad de productos.

Variable objetivo sugerida: `monto_total`.
Variable predictora basica sugerida: `cantidad_productos`.

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
    l.nombre AS sucursal,
    l.zona,
    f.fecha_operacion,
    f.cantidad,
    f.cantidad_productos,
    f.precio_unitario,
    f.descuento_pct,
    f.canal,
    f.metodo_pago,
    f.calificacion,
    f.monto_total
FROM ventas f
LEFT JOIN clientes p ON f.id_cliente = p.id_cliente
LEFT JOIN productos i ON f.id_producto = i.id_producto
LEFT JOIN sucursales l ON f.id_sucursal = l.id_sucursal;
```
