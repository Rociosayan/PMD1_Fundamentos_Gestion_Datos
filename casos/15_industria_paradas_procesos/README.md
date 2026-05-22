# Industria - Paradas de maquina y procesos

## Contexto
Una planta de produccion registra paradas de maquina, condiciones del proceso, unidades producidas, defectos y costo estimado de cada parada.

## Tablas
- `maquinas`: catalogo de equipos por linea, tipo y antiguedad.
- `procesos`: procesos productivos con parametros objetivo.
- `turnos`: turnos y supervisores.
- `paradas`: tabla principal con 500 registros, claves foraneas y datos operativos.

## Reto PMD1
Predecir el costo de una parada de maquina a partir de su duracion en minutos.

Variable objetivo sugerida: `costo_parada_soles`.
Variable predictora basica sugerida: `duracion_parada_min`.

## Mineria de datos incluida
El archivo `modelo_mineria_paradas_procesos.py` descarga/lee la base local, arma el dataset analitico con SQL, limpia numeros guardados como texto, entrena una regresion lineal simple y guarda estos resultados en la misma base SQLite:

- `dataset_paradas_limpio`
- `predicciones_costo_parada`
- `metricas_modelo_paradas`

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
    f.id_parada,
    m.nombre AS maquina,
    m.linea,
    m.tipo_maquina,
    m.antiguedad_anios,
    p.nombre AS proceso,
    p.familia,
    p.temperatura_objetivo_c,
    p.velocidad_objetivo_u_h,
    t.nombre AS turno,
    t.supervisor,
    f.fecha_operacion,
    f.tiempo_operacion_h,
    f.unidades_producidas,
    f.defectos_unidades,
    f.temperatura_promedio_c,
    f.velocidad_real_u_h,
    f.causa_parada,
    f.criticidad,
    f.duracion_parada_min,
    f.costo_parada_soles
FROM paradas f
LEFT JOIN maquinas m ON f.id_maquina = m.id_maquina
LEFT JOIN procesos p ON f.id_proceso = p.id_proceso
LEFT JOIN turnos t ON f.id_turno = t.id_turno;
```
