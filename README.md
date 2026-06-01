# PMD1 - Bases desnormalizadas para Fundamentos de Gestion de Datos

Este paquete contiene casos cotidianos para el PMD1. En general, cada caso incluye una base SQLite con una tabla grande desnormalizada, un CSV equivalente, un `schema.sql` minimo y una guia breve.

Excepcion: el caso 17 de panaderia se mantiene con `ventas_original` y tablas normalizadas porque ya fue usado en clase con esa estructura.

La idea didactica es que el estudiante:

1. Descargue la base desde GitHub.
2. Se conecte a SQLite desde Colab.
3. Observe una tabla con informacion repetida.
4. Identifique entidades, dependencias y posibles claves.
5. Normalice creando sus propias tablas con PK y FK.
6. Use `JOIN` para reconstruir la informacion despues de normalizar.
7. Limpie datos con Pandas y, si corresponde, entrene una regresion lineal simple.

## Casos disponibles

| N | Caso | Base SQLite | Tabla original | Variable objetivo | Predictora sugerida |
|---|---|---|---|---|---|
| 01 | Retailmax Ventas | `retailmax_ventas.db` | `ventas_original` | `monto_total` | `cantidad_productos` |
| 02 | Restaurante Pedidos | `restaurante_pedidos.db` | `pedidos_original` | `total_pedido` | `tiempo_preparacion_min` |
| 03 | Farmacia Ventas | `farmacia_ventas.db` | `ventas_original` | `monto_boleta` | `cantidad_medicamentos` |
| 04 | Ferreteria Ventas | `ferreteria_ventas.db` | `ventas_original` | `monto_compra` | `cantidad_articulos` |
| 05 | Clinica Atenciones | `clinica_atenciones.db` | `atenciones_original` | `costo_atencion` | `duracion_consulta_min` |
| 06 | Veterinaria Atenciones | `veterinaria_atenciones.db` | `atenciones_original` | `costo_servicio` | `peso_mascota_kg` |
| 07 | Hotel Reservas | `hotel_reservas.db` | `reservas_original` | `monto_reserva` | `noches_estadia` |
| 08 | Food Delivery Entregas | `food_delivery_entregas.db` | `entregas_original` | `tiempo_entrega_min` | `distancia_km` |
| 09 | Logiexpress Envios | `logiexpress_envios.db` | `envios_original` | `costo_envio` | `peso_paquete_kg` |
| 10 | Agrodata Cultivos | `agrodata_cultivos.db` | `produccion_original` | `rendimiento_kg` | `hectareas` |
| 11 | Energyhome Consumo | `energyhome_consumo.db` | `consumos_original` | `consumo_kwh` | `numero_habitantes` |
| 12 | Gimnasio Socios | `gimnasio_socios.db` | `asistencias_pagos_original` | `pago_mensual` | `asistencias_mes` |
| 13 | Panaderia Ventas | `panaderia_ventas.db` | `ventas_original` | `ingreso_venta` | `cantidad_unidades` |
| 14 | Taller Mecanico Ordenes | `taller_mecanico_ordenes.db` | `ordenes_original` | `costo_reparacion` | `horas_trabajo` |
| 15 | Industria Paradas Procesos | `industria_paradas_procesos.db` | `paradas_original` | `costo_parada_soles` | `duracion_parada_min` |
| 16 | Abarrotes Ventas Inventario | `abarrotes_ventas_inventario.db` | `ventas_original` | `monto_venta_soles` | `cantidad_unidades` |
| 17 | Panaderia Normalizacion | `panaderia_normalizacion.db` | `ventas_original` + tablas normalizadas | `total_venta` | `cantidad` |
| 18 | Minimarket Normalizacion | `minimarket_normalizacion.db` | `ventas_original` | `total_venta` | `cantidad` |

## Ejemplo para descargar desde GitHub en Colab

```python
import requests
import sqlite3
import pandas as pd

url = "https://raw.githubusercontent.com/USUARIO/REPO/main/casos/01_retailmax_ventas/retailmax_ventas.db"
r = requests.get(url)
open("retailmax_ventas.db", "wb").write(r.content)

conn = sqlite3.connect("retailmax_ventas.db")

df = pd.read_sql_query("SELECT * FROM ventas_original LIMIT 5", conn)
df
```

## Nota sobre normalizacion

Las bases de estudiantes no traen el modelo normalizado resuelto, excepto el caso 17 de panaderia que se conserva como material ya trabajado en clase. En los demas casos, el trabajo consiste en partir de la tabla original, reconocer repeticion de datos y construir las tablas normalizadas.

El `schema.sql` de cada caso muestra solamente la estructura de la tabla original. Las claves primarias, claves foraneas y tablas finales deben ser propuestas por el estudiante.

## Modelos de mineria adicionales

Tambien se incluye una carpeta de modelos aplicados:

- `modelos_mineria/02_operaciones_paradas_maquina`: notebook y datos sinteticos para prediccion de paradas no programadas de maquina en operacion minera.
