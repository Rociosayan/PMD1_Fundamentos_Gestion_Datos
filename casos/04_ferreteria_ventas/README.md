# Ferreteria - Compras de articulos

## Contexto
Una ferreteria analiza compras de materiales, herramientas e insumos.

## Tablas
- `clientes`: datos de clientes.
- `articulos`: catalogo de articulos.
- `tiendas`: sedes, zonas o puntos de operacion.
- `ventas`: tabla principal con 500 registros y claves foraneas.

## Reto PMD1
Predecir el monto de compra a partir de la cantidad de articulos.

Variable objetivo sugerida: `monto_compra`.
Variable predictora basica sugerida: `cantidad_articulos`.

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
    i.nombre AS articulo,
    i.categoria,
    l.nombre AS tienda,
    l.zona,
    f.fecha_operacion,
    f.cantidad,
    f.cantidad_articulos,
    f.precio_unitario,
    f.descuento_pct,
    f.canal,
    f.metodo_pago,
    f.calificacion,
    f.monto_compra
FROM ventas f
LEFT JOIN clientes p ON f.id_cliente = p.id_cliente
LEFT JOIN articulos i ON f.id_articulo = i.id_articulo
LEFT JOIN tiendas l ON f.id_tienda = l.id_tienda;
```
