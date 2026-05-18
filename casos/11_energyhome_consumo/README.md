# EnergyHome - Consumo electrico

## Contexto
Una empresa local analiza consumo electrico mensual de hogares.

## Tablas
- `hogares`: datos de hogars.
- `tarifas`: catalogo de tarifas.
- `distritos`: sedes, zonas o puntos de operacion.
- `consumos`: tabla principal con 500 registros y claves foraneas.

## Reto PMD1
Predecir el consumo electrico segun el numero de habitantes.

Variable objetivo sugerida: `consumo_kwh`.
Variable predictora basica sugerida: `numero_habitantes`.

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
    f.id_consumo,
    p.nombre AS hogar,
    p.distrito AS distrito_hogar,
    p.segmento,
    i.nombre AS tarifa,
    i.categoria,
    l.nombre AS distrito,
    l.zona,
    f.fecha_operacion,
    f.electrodomesticos,
    f.numero_habitantes,
    f.tarifa_base,
    f.descuento_pct,
    f.canal,
    f.metodo_pago,
    f.calificacion,
    f.consumo_kwh
FROM consumos f
LEFT JOIN hogares p ON f.id_hogar = p.id_hogar
LEFT JOIN tarifas i ON f.id_tarifa = i.id_tarifa
LEFT JOIN distritos l ON f.id_distrito = l.id_distrito;
```
