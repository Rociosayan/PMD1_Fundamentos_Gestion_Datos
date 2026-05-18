# LogiExpress - Envios urbanos

## Contexto
Una empresa de mensajeria analiza costos y tiempos de envio.

## Tablas
- `clientes`: datos de clientes.
- `tipos_envio`: catalogo de tipo_envios.
- `sedes`: sedes, zonas o puntos de operacion.
- `envios`: tabla principal con 500 registros y claves foraneas.

## Reto PMD1
Predecir el costo de envio segun el peso del paquete.

Variable objetivo sugerida: `costo_envio`.
Variable predictora basica sugerida: `peso_paquete_kg`.

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
    f.id_envio,
    p.nombre AS cliente,
    p.distrito AS distrito_cliente,
    p.segmento,
    i.nombre AS tipo_envio,
    i.categoria,
    l.nombre AS sede,
    l.zona,
    f.fecha_operacion,
    f.cantidad_paquetes,
    f.peso_paquete_kg,
    f.tarifa_base,
    f.descuento_pct,
    f.canal,
    f.metodo_pago,
    f.calificacion,
    f.costo_envio
FROM envios f
LEFT JOIN clientes p ON f.id_cliente = p.id_cliente
LEFT JOIN tipos_envio i ON f.id_tipo_envio = i.id_tipo_envio
LEFT JOIN sedes l ON f.id_sede = l.id_sede;
```
