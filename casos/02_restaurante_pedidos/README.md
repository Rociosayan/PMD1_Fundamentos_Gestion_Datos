# Restaurante - Pedidos y consumo

## Contexto
Un restaurante de menu y platos a la carta analiza pedidos diarios.

## Tablas
- `clientes`: datos de clientes.
- `platos`: catalogo de platos.
- `locales`: sedes, zonas o puntos de operacion.
- `pedidos`: tabla principal con 500 registros y claves foraneas.

## Reto PMD1
Predecir el total del pedido usando el tiempo de preparacion o la cantidad de platos.

Variable objetivo sugerida: `total_pedido`.
Variable predictora basica sugerida: `tiempo_preparacion_min`.

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
    f.id_pedido,
    p.nombre AS cliente,
    p.distrito AS distrito_cliente,
    p.segmento,
    i.nombre AS plato,
    i.categoria,
    l.nombre AS local,
    l.zona,
    f.fecha_operacion,
    f.cantidad_platos,
    f.tiempo_preparacion_min,
    f.precio_plato,
    f.descuento_pct,
    f.canal,
    f.metodo_pago,
    f.calificacion,
    f.total_pedido
FROM pedidos f
LEFT JOIN clientes p ON f.id_cliente = p.id_cliente
LEFT JOIN platos i ON f.id_plato = i.id_plato
LEFT JOIN locales l ON f.id_local = l.id_local;
```
