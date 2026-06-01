# Panaderia - Normalizacion y SQL basico

## Contexto

La panaderia "Dulce Migaja" vende panes, pasteles, bebidas y productos salados en tres locales. La administracion necesita entender por que conviene separar clientes, productos, categorias, locales y ventas en tablas distintas.

Este caso fue preparado para:

- Semana 4: normalizacion relacional, claves primarias, claves foraneas y JOIN.
- Laboratorio Calificado 2: interpretacion de consultas SQL basicas de semanas 3 y 4.

## Base SQLite

Archivo principal:

- `panaderia_normalizacion.db`

URL raw para Google Colab:

```text
https://raw.githubusercontent.com/Rociosayan/PMD1_Fundamentos_Gestion_Datos/main/casos/17_panaderia_normalizacion/panaderia_normalizacion.db
```

## Tablas incluidas

### Tabla para explicar el problema

- `ventas_original`: tabla desnormalizada. Repite datos de cliente, producto, categoria y local en cada venta.

### Tablas normalizadas

- `categorias`: catalogo de categorias.
- `productos`: productos vendidos y su categoria.
- `clientes`: datos basicos de clientes.
- `locales`: locales de venta.
- `ventas`: tabla transaccional con IDs y cantidad vendida.

## Uso didactico sugerido

### Semana 4

1. Descargar la base desde GitHub.
2. Observar `ventas_original`.
3. Identificar datos repetidos.
4. Comparar con las tablas normalizadas.
5. Explicar por que `ventas` guarda `id_cliente`, `id_producto` e `id_local`.
6. Reconstruir la informacion con `INNER JOIN`.

### Laboratorio Calificado 2

Usar consultas cortas:

- `SELECT`
- `INNER JOIN`
- `LEFT JOIN`
- `GROUP BY`
- `ORDER BY`

No requiere subconsultas, vistas, indices ni temas avanzados.

## Consulta base para reconstruir ventas

```sql
SELECT
    v.id_venta,
    v.fecha,
    c.nombre AS cliente,
    c.distrito AS distrito_cliente,
    p.nombre AS producto,
    cat.nombre AS categoria,
    l.nombre AS local,
    l.distrito AS distrito_local,
    v.cantidad,
    p.precio_unitario,
    v.cantidad * p.precio_unitario AS total_venta,
    v.metodo_pago
FROM ventas v
INNER JOIN clientes c ON v.id_cliente = c.id_cliente
INNER JOIN productos p ON v.id_producto = p.id_producto
INNER JOIN categorias cat ON p.id_categoria = cat.id_categoria
INNER JOIN locales l ON v.id_local = l.id_local
ORDER BY v.id_venta;
```

## Ejemplo de descarga en Colab

```python
from pathlib import Path
import urllib.request
import sqlite3
import pandas as pd

url = "https://raw.githubusercontent.com/Rociosayan/PMD1_Fundamentos_Gestion_Datos/main/casos/17_panaderia_normalizacion/panaderia_normalizacion.db"
db_path = Path("panaderia_normalizacion.db")
urllib.request.urlretrieve(url, db_path)

conn = sqlite3.connect(db_path)

ventas_original = pd.read_sql_query("SELECT * FROM ventas_original;", conn)
ventas_original.head()
```

## Archivos CSV

La carpeta `csv/` contiene una copia de cada tabla para revision rapida:

- `ventas_original.csv`
- `categorias.csv`
- `productos.csv`
- `clientes.csv`
- `locales.csv`
- `ventas.csv`
