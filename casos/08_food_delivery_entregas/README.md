# FoodDelivery - Pedidos a domicilio

## Contexto
Una plataforma local mide tiempos de entrega de pedidos.

## Tablas
- `clientes`: datos de clientes.
- `restaurantes`: catalogo de restaurantes.
- `zonas`: sedes, zonas o puntos de operacion.
- `entregas`: tabla principal con 500 registros y claves foraneas.

## Reto PMD1
Predecir el tiempo de entrega segun la distancia en kilometros.

Variable objetivo sugerida: `tiempo_entrega_min`.
Variable predictora basica sugerida: `distancia_km`.

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
    f.id_entrega,
    p.nombre AS cliente,
    p.distrito AS distrito_cliente,
    p.segmento,
    i.nombre AS restaurante,
    i.categoria,
    l.nombre AS zona,
    l.zona,
    f.fecha_operacion,
    f.cantidad_items,
    f.distancia_km,
    f.costo_pedido,
    f.descuento_pct,
    f.canal,
    f.metodo_pago,
    f.calificacion,
    f.tiempo_entrega_min
FROM entregas f
LEFT JOIN clientes p ON f.id_cliente = p.id_cliente
LEFT JOIN restaurantes i ON f.id_restaurante = i.id_restaurante
LEFT JOIN zonas l ON f.id_zona = l.id_zona;
```
