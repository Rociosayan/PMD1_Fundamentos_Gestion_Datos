# PMD1 - Bases de datos sinteticas para Fundamentos de Gestion de Datos

Este paquete contiene 18 casos cotidianos para el PMD1. Cada caso incluye una base SQLite relacional, archivos CSV por tabla, un `schema.sql` y una guia breve.

La idea didactica es que el estudiante:

1. Descargue la base desde GitHub.
2. Se conecte a SQLite desde Colab.
3. Use SQL para unir tablas y construir un dataset analitico.
4. Limpie datos con Pandas.
5. Entrene una regresion lineal simple.
6. Guarde la tabla limpia y/o predicciones nuevamente en SQLite.

## Casos disponibles

| N | Caso | Base SQLite | Variable objetivo | Predictora sugerida |
|---|---|---|---|---|
| 01 | RetailMax - Ventas en tienda | `retailmax_ventas.db` | `monto_total` | `cantidad_productos` |
| 02 | Restaurante - Pedidos y consumo | `restaurante_pedidos.db` | `total_pedido` | `tiempo_preparacion_min` |
| 03 | Farmacia - Ventas de productos | `farmacia_ventas.db` | `monto_boleta` | `cantidad_medicamentos` |
| 04 | Ferreteria - Compras de articulos | `ferreteria_ventas.db` | `monto_compra` | `cantidad_articulos` |
| 05 | Clinica - Atenciones ambulatorias | `clinica_atenciones.db` | `costo_atencion` | `duracion_consulta_min` |
| 06 | Veterinaria - Servicios para mascotas | `veterinaria_atenciones.db` | `costo_servicio` | `peso_mascota_kg` |
| 07 | HotelSmart - Reservas hoteleras | `hotel_reservas.db` | `monto_reserva` | `noches_estadia` |
| 08 | FoodDelivery - Pedidos a domicilio | `food_delivery_entregas.db` | `tiempo_entrega_min` | `distancia_km` |
| 09 | LogiExpress - Envios urbanos | `logiexpress_envios.db` | `costo_envio` | `peso_paquete_kg` |
| 10 | AgroData - Produccion de cultivos | `agrodata_cultivos.db` | `rendimiento_kg` | `hectareas` |
| 11 | EnergyHome - Consumo electrico | `energyhome_consumo.db` | `consumo_kwh` | `numero_habitantes` |
| 12 | Gimnasio - Socios y asistencias | `gimnasio_socios.db` | `pago_mensual` | `asistencias_mes` |
| 13 | Panaderia - Ventas diarias | `panaderia_ventas.db` | `ingreso_venta` | `cantidad_unidades` |
| 14 | Taller mecanico - Ordenes de servicio | `taller_mecanico_ordenes.db` | `costo_reparacion` | `horas_trabajo` |
| 15 | Industria - Paradas de maquina y procesos | `industria_paradas_procesos.db` | `costo_parada_soles` | `duracion_parada_min` |
| 16 | Abarrotes - Ventas e inventario | `abarrotes_ventas_inventario.db` | `monto_venta_soles` | `cantidad_unidades` |
| 17 | Panaderia - Normalizacion y SQL basico | `panaderia_normalizacion.db` | `total_venta` | `cantidad` |
| 18 | MiniMarket C2 - Normalizacion y SQL basico | `minimarket_normalizacion.db` | `total_venta` | `cantidad` |

## Ejemplo para descargar desde GitHub en Colab

```python
import requests
import sqlite3
import pandas as pd

url = "https://raw.githubusercontent.com/USUARIO/REPO/main/casos/01_retailmax_ventas/retailmax_ventas.db"
r = requests.get(url)
open("retailmax_ventas.db", "wb").write(r.content)

conn = sqlite3.connect("retailmax_ventas.db")

df = pd.read_sql_query("SELECT * FROM ventas LIMIT 5", conn)
df
```

## Nota sobre claves primarias y foraneas

Cada base ya viene con claves primarias y foraneas. El estudiante no necesita inventarlas desde cero para iniciar el analisis, pero si debe entenderlas para hacer los `JOIN`.

Tambien puede revisar el archivo `schema.sql` de cada caso para ver como se crea la estructura.

## Modelos de mineria adicionales

Tambien se incluye una carpeta de modelos aplicados:

- `modelos_mineria/02_operaciones_paradas_maquina`: notebook y datos sinteticos para prediccion de paradas no programadas de maquina en operacion minera.
