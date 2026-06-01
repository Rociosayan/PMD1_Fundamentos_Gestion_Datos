# Caso 18 - MiniMarket C2: normalizacion y SQL basico

Este caso fue preparado para el Laboratorio Calificado 2 del curso Fundamentos de Gestion de Datos.

La empresa ficticia MiniMarket C2 registra ventas de productos de abarrotes, bebidas, limpieza y cuidado personal. La base permite comparar una tabla desnormalizada con un modelo organizado en tablas relacionadas.

## Base de datos

- Archivo SQLite: `minimarket_normalizacion.db`
- Enlace directo para Colab:

```text
https://raw.githubusercontent.com/Rociosayan/PMD1_Fundamentos_Gestion_Datos/main/casos/18_minimarket_normalizacion/minimarket_normalizacion.db
```

## Tablas

- `ventas_original`: tabla desnormalizada con datos repetidos de clientes, productos, categorias y locales.
- `categorias`: categorias de producto.
- `productos`: productos con precio unitario y relacion hacia categoria.
- `clientes`: clientes del minimarket.
- `locales`: locales de venta.
- `ventas`: transacciones normalizadas con claves hacia clientes, productos y locales.

## Uso didactico

La base esta pensada para actividades de:

- Reconocimiento de tablas y campos.
- Identificacion de datos repetidos en `ventas_original`.
- Interpretacion de claves primarias y claves foraneas.
- Consultas con `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY`, `COUNT`, `SUM`, `AVG`.
- Consultas con `INNER JOIN` y `LEFT JOIN`.
- Interpretacion de resultados de ventas por producto, categoria, cliente y local.

## Nota para el laboratorio

El estudiante no debe crear la base desde cero. El notebook debe descargar el archivo `.db` desde GitHub y conectarse con SQLite para interpretar consultas.
