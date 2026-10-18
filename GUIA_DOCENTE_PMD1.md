# Guia PMD1

> **Actualización 2026-II (18-oct-2026).** El PMD1 vigente usa los quince casos de `PMD1_15_Casos_Sinteticos/` (Excel con cuatro tablas separadas), los Word de `PMD1_Casos_Word_2026II/` y la rúbrica `Rubrica_PMD1_2026II_10_Casos.docx`. Exige integración SQL, limpieza, regresión lineal simple y K-Means, informe técnico sin código y sustentación individual. Lo que sigue de esta guía corresponde a las 18 bases SQLite de `casos/` (material de apoyo anterior).


## Enfoque recomendado

Cada grupo elige un caso distinto. En general, los casos comparten la misma logica didactica:

1. Base SQLite con una tabla desnormalizada.
2. Datos repetidos de varias entidades en la misma tabla.
3. Analisis de redundancia y dependencias.
4. Diseno de tablas normalizadas por parte del estudiante.
5. Creacion de claves primarias y foraneas.
6. Carga de datos desde la tabla original hacia el modelo normalizado.
7. Validacion con consultas `JOIN`.
8. Limpieza en Pandas y analisis simple.

Nota: los casos 17 de panaderia y 18 de minimarket se conservan con `ventas_original` y tablas normalizadas porque ya fueron usados en clase/laboratorio con esa estructura. Los demas casos quedan como tablas desnormalizadas para que el estudiante normalice.

## Como explicar PK y FK

La base de estudiantes debe iniciar como una sola tabla plana. Esa tabla mezcla datos de personas, productos, sedes, operaciones y otras entidades del caso.

El estudiante debe decidir que informacion se separa. Por ejemplo:

- Datos de personas o clientes en una tabla propia.
- Datos de productos, servicios o items en una tabla propia.
- Datos de sedes, zonas o locales en una tabla propia.
- Datos de operaciones en una tabla principal que guarde claves foraneas.

Despues de normalizar, el estudiante reconstruye un reporte con SQL:

```sql
SELECT *
FROM ventas v
JOIN clientes c ON v.id_cliente = c.id_cliente
JOIN productos p ON v.id_producto = p.id_producto
JOIN sucursales s ON v.id_sucursal = s.id_sucursal;
```

## Limpieza esperada

Los estudiantes deben resolver al menos:

- Espacios en blanco con `.str.strip()`.
- Mayusculas/minusculas con `.str.title()` o `.str.upper()`.
- Valores nulos con imputacion o eliminacion justificada.
- Duplicados con `.drop_duplicates()`.
- Numeros en texto, por ejemplo `S/ 45.90` o `45,90`.
- Fechas con formatos distintos usando `pd.to_datetime()`.
- Valores extremos revisados con graficos o reglas simples.

## Regresion lineal simple

Para PMD1 se recomienda una sola variable predictora numerica.

El objetivo no es hacer el mejor modelo del mundo, sino demostrar el flujo completo:

tabla original -> normalizacion -> SQL/JOIN -> Pandas -> limpieza -> interpretacion.

## Entregables sugeridos

- Notebook Colab reproducible.
- Base SQLite descargada desde GitHub.
- Diagrama o explicacion del modelo normalizado propuesto.
- Script SQL que crea tablas normalizadas e inserta datos.
- Consultas `JOIN` de validacion.
- Tabla limpia guardada en SQLite.
- Informe breve con interpretacion de resultados.

## Evaluacion sugerida

| Criterio | Peso |
|---|---:|
| Identificacion de redundancia y entidades | 20% |
| Diseno de PK/FK y estructura normalizada | 25% |
| Creacion y carga de tablas normalizadas | 20% |
| Consultas SQL con `JOIN` para validar | 15% |
| Limpieza de datos con Pandas | 10% |
| Interpretacion del caso y conclusiones | 10% |
