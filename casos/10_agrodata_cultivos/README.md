# AgroData - Produccion de cultivos

## Contexto
Una asociacion agricola analiza rendimiento de cultivos por parcela.

## Tablas
- `parcelas`: datos de parcelas.
- `cultivos`: catalogo de cultivos.
- `zonas`: sedes, zonas o puntos de operacion.
- `produccion`: tabla principal con 500 registros y claves foraneas.

## Reto PMD1
Predecir el rendimiento en kilogramos segun las hectareas sembradas.

Variable objetivo sugerida: `rendimiento_kg`.
Variable predictora basica sugerida: `hectareas`.

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
    f.id_produccion,
    p.nombre AS parcela,
    p.distrito AS distrito_parcela,
    p.segmento,
    i.nombre AS cultivo,
    i.categoria,
    l.nombre AS zona,
    l.zona,
    f.fecha_operacion,
    f.cantidad_jornales,
    f.hectareas,
    f.costo_insumo,
    f.descuento_pct,
    f.canal,
    f.metodo_pago,
    f.calificacion,
    f.rendimiento_kg
FROM produccion f
LEFT JOIN parcelas p ON f.id_parcela = p.id_parcela
LEFT JOIN cultivos i ON f.id_cultivo = i.id_cultivo
LEFT JOIN zonas l ON f.id_zona = l.id_zona;
```
