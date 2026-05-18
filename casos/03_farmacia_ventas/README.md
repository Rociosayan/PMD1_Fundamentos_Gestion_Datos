# Farmacia - Ventas de productos

## Contexto
Una farmacia de barrio revisa ventas de medicamentos y cuidado personal.

## Tablas
- `clientes`: datos de clientes.
- `medicamentos`: catalogo de medicamentos.
- `sucursales`: sedes, zonas o puntos de operacion.
- `ventas`: tabla principal con 500 registros y claves foraneas.

## Reto PMD1
Predecir el monto de la boleta segun la cantidad de medicamentos.

Variable objetivo sugerida: `monto_boleta`.
Variable predictora basica sugerida: `cantidad_medicamentos`.

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
    i.nombre AS medicamento,
    i.categoria,
    l.nombre AS sucursal,
    l.zona,
    f.fecha_operacion,
    f.cantidad,
    f.cantidad_medicamentos,
    f.precio_unitario,
    f.descuento_pct,
    f.canal,
    f.metodo_pago,
    f.calificacion,
    f.monto_boleta
FROM ventas f
LEFT JOIN clientes p ON f.id_cliente = p.id_cliente
LEFT JOIN medicamentos i ON f.id_medicamento = i.id_medicamento
LEFT JOIN sucursales l ON f.id_sucursal = l.id_sucursal;
```
