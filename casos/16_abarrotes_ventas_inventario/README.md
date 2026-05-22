# Abarrotes - Ventas e inventario

## Contexto
Una cadena pequena de bodegas y tiendas de abarrotes analiza ventas diarias, inventario, mermas y margen por producto.

## Tablas
- `clientes`: datos de clientes frecuentes y ocasionales.
- `productos`: catalogo de abarrotes con proveedor, costo y precio de lista.
- `tiendas`: bodegas o puntos de venta por distrito y zona.
- `ventas`: tabla principal con 500 registros, claves foraneas y variables comerciales.

## Reto PMD1
Predecir el monto de venta de abarrotes a partir de la cantidad de unidades vendidas.

Variable objetivo sugerida: `monto_venta_soles`.
Variable predictora basica sugerida: `cantidad_unidades`.

## Mineria de datos incluida
El archivo `modelo_mineria_abarrotes.py` arma el dataset analitico con SQL, limpia numeros guardados como texto, entrena una regresion lineal simple y guarda estos resultados en la misma base SQLite:

- `dataset_abarrotes_limpio`
- `predicciones_monto_venta`
- `metricas_modelo_abarrotes`

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
    c.nombre AS cliente,
    c.distrito AS distrito_cliente,
    c.segmento,
    p.nombre AS producto,
    p.categoria,
    p.proveedor,
    t.nombre AS tienda,
    t.distrito AS distrito_tienda,
    t.zona,
    t.tipo_local,
    f.fecha_operacion,
    f.cantidad_unidades,
    f.precio_venta_unitario,
    f.costo_unitario,
    f.descuento_pct,
    f.stock_inicial,
    f.stock_final,
    f.merma_unidades,
    f.canal,
    f.metodo_pago,
    f.monto_venta_soles,
    f.margen_venta_soles
FROM ventas f
LEFT JOIN clientes c ON f.id_cliente = c.id_cliente
LEFT JOIN productos p ON f.id_producto = p.id_producto
LEFT JOIN tiendas t ON f.id_tienda = t.id_tienda;
```
