# LavaYa · Panel de Análisis de Pedidos (Streamlit)

Panel web del caso 16 Lavandería.
Módulos (pantalla de inicio con tarjetas): Resumen ejecutivo · Base de datos · Análisis exploratorio · Calidad de datos ·
Modelo de tarifa · Simulador de costo · Segmentación de pedidos (K-Means).

Datos: `casos_PMD1/16_Lavanderia/16_Lavanderia_PMD1.xlsx` (ruta relativa del repo); si no existe, se descarga de la URL raw de GitHub.

## Ejecutar en local
```
pip install -r app_lavanderia/requirements.txt
streamlit run app_lavanderia/app.py
```

## Publicar en Streamlit Community Cloud
1. Verifica que el repositorio `Rociosayan/PMD1_Fundamentos_Gestion_Datos` sea **público** y tenga esta carpeta en la rama `main`.
2. Entra a https://share.streamlit.io e inicia sesión con tu cuenta de GitHub (autoriza el acceso si lo pide).
3. Clic en **Create app** → **Deploy a public app from GitHub**.
4. Repository: `Rociosayan/PMD1_Fundamentos_Gestion_Datos` · Branch: `main` · Main file path: `app_lavanderia/app.py`.
5. (Opcional) En **App URL** elige un nombre, por ejemplo `pmd1-lavanderia`.
6. En **Advanced settings** elige Python 3.11 o 3.12 y clic en **Deploy**. Streamlit instala `app_lavanderia/requirements.txt` (archivo junto a app.py).
7. Comparte la URL `https://<nombre>.streamlit.app` con los estudiantes. Cada `git push` a `main` actualiza la app automáticamente.
