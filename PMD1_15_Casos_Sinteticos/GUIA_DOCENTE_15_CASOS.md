# Guía docente PMD1 2026-II — quince casos sintéticos

Los quince archivos contienen datos inventados (soles peruanos). Cada caso tiene cuatro tablas separadas —Operaciones, Clientes, Catalogo y Sedes— más una hoja LEEME. Todos conservan los mismos problemas didácticos: nulos (4 en la predictora, 5 en la segunda variable y 3 en el objetivo), seis filas duplicadas exactas en Operaciones, fechas en formatos distintos (unas 20 por caso con formato d/m/aaaa) y espacios sobrantes en seis nombres de cliente. No hay tabla analítica ni resultados resueltos.

## Casos

| Archivo | Predictora simple sugerida | Objetivo | Variables candidatas para K-Means | R² orientativo |
|---|---|---|---|---:|
| 01_Delivery_PMD1.xlsx | distancia_km | tiempo_entrega_min | distancia_km, items_pedido, carga_operativa_pct | 0.54 |
| 02_Restaurante_PMD1.xlsx | comensales | tiempo_servicio_min | comensales, platos_pedidos, ocupacion_local_pct | 0.39 |
| 03_Farmacia_PMD1.xlsx | cantidad_productos | tiempo_atencion_min | cantidad_productos, productos_con_receta, afluencia_local | 0.41 |
| 04_Hotel_PMD1.xlsx | noches_estadia | gasto_estadia_soles | noches_estadia, huespedes, tarifa_noche_soles | 0.61 |
| 05_Agro_PMD1.xlsx | hectareas | cosecha_kg | hectareas, riego_horas_semana, fertilizante_kg | 0.59 |
| 06_Energia_PMD1.xlsx | area_m2 | consumo_kwh_mes | area_m2, habitantes, electrodomesticos | 0.52 |
| 07_Taller_PMD1.xlsx | antiguedad_auto_anios | horas_reparacion | antiguedad_auto_anios, kilometraje_miles_km, piezas_revisadas | 0.50 |
| 08_Ferreteria_PMD1.xlsx | peso_carga_kg | costo_transporte_soles | peso_carga_kg, bultos, distancia_km | 0.48 |
| 09_Clinica_PMD1.xlsx | procedimientos | duracion_atencion_min | procedimientos, edad_paciente, espera_previa_min | 0.54 |
| 10_Logistica_PMD1.xlsx | volumen_m3 | costo_envio_soles | volumen_m3, peso_kg, distancia_km | 0.59 |
| 11_Retail_PMD1.xlsx | articulos_boleta | monto_venta_soles | articulos_boleta, minutos_en_tienda, descuento_pct | 0.43 |
| 12_Veterinaria_PMD1.xlsx | peso_mascota_kg | costo_servicio_soles | peso_mascota_kg, duracion_consulta_min, edad_mascota_anios | 0.56 |
| 13_Industria_PMD1.xlsx | duracion_parada_min | costo_parada_soles | duracion_parada_min, operarios_afectados, antiguedad_maquina_anios | 0.45 |
| 14_Educacion_PMD1.xlsx | horas_estudio_semana | nota_examen | horas_estudio_semana, asistencia_pct, tareas_entregadas | 0.62 (*) |
| 15_Soporte_TI_PMD1.xlsx | usuarios_afectados | horas_resolucion | usuarios_afectados, antiguedad_equipo_anios, tickets_previos_mes | 0.43 |

Los R² salen de una separación de prueba del 25 % con `random_state=42`, sobre las filas con predictora y objetivo completos, tal como se entregan el archivo (sin quitar duplicados ni valores extremos). Son orientativos: no son un umbral de evaluación y cambian según la limpieza que decida el equipo.

(*) En Educación hay dos notas fuera de la escala 0-20 (error de digitación de decimal, por ejemplo 8,1 escrito como 81). El R² de la tabla es el obtenido después de excluirlas; sin excluirlas el valor es inestable y depende de en qué partición caigan.

## Unidad de análisis y K-Means

La unidad sugerida es una operación (una fila de Operaciones). El equipo debe limpiar, escalar, elegir k e interpretar los grupos. En los casos 11 a 15 los datos se generaron a partir de tres perfiles latentes (operaciones pequeñas, medianas y grandes), por lo que k = 3 suele ser una elección defendible; el equipo debe sustentarla con inercia y silueta, no asumirla. Una silueta modesta (0,3 a 0,5) es normal y no se penaliza automáticamente.

## Problemas de calidad presentes en todos los casos

- Seis filas de Operaciones duplicadas exactamente (mismo id_operacion).
- Nulos en la predictora, en la segunda variable y en el objetivo.
- Fechas en texto: la mayoría en formato aaaa-mm-dd y unas 20 en d/m/aaaa sin ceros. Con día ≤ 12 el orden día/mes es ambiguo y el equipo debe decidir y justificar.
- Seis nombres de cliente con espacios al final.
- Entre 1 y 4 valores extremos en el objetivo (y en Energía, también en electrodomésticos).

## Revisión del 18-oct-2026

- **09_Clinica**: `edad_paciente` tomaba valores de 1 a 8 que no eran edades. Ahora son edades en años (15 a 77) con la misma relación con las demás variables.
- **10_Logistica**: `peso_kg` tomaba valores de 1 a 8 para cargas de hasta 8 m³. Ahora está en kilogramos plausibles (30 a 364).
- Agregados los casos 11 a 15 con el mismo formato y los mismos problemas didácticos. En Retail el precio del catálogo interviene en el monto de la venta, de modo que la integración con Catalogo aporta información real al análisis.
- Se verificó en los quince casos: 0 claves huérfanas entre Operaciones y las otras tres tablas, id_operacion repetido solo en las 6 filas duplicadas.
