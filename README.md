# Dashboard de la Plantas Electricas para la Tarea 4

## Descripción del proyecto

Este proyecto consiste en realizar un análisis exploratorio de datos (EDA) sobre la infraestructura de generación eléctrica a nivel mundial, con el propósito de identificar patrones, tendencias y diferencias en la producción de energía según el tipo de combustible, la ubicación geográfica y la capacidad de las plantas; por lo que se busca comprender cómo está distribuida la infraestructura energética, cómo ha evolucionado a través del tiempo y qué relación existe entre la capacidad instalada y la generación estimada de electricidad.

Para desarrollar el análisis se utilizó un dataset de plantas de generación eléctrica a nivel mundial, compuesto por 10.338 registros y variables como nombre de la planta, país, tipo de combustible, capacidad instalada en MW y año de puesta en operación, donde se seleccionó este conjunto de datos porque reúne información de diferentes tecnologías y países, lo que permite realizar comparaciones, identificar tendencias históricas y explorar las características de la infraestructura energética desde una perspectiva global.

Por lo que a través de la exploración, limpieza, análisis estadístico y visualización de los datos, se busca transformar la información en hallazgos relevantes que permitan comprender la composición del sector eléctrico, reconocer el crecimiento de las diferentes fuentes de energía y aportar información útil para el análisis y la toma de decisiones en el ámbito energético.

## Captura de pantalla

<img width="1917" height="1025" alt="image" src="https://github.com/user-attachments/assets/8fe8834c-b348-4f73-8e28-df62604575dd" />

<img width="1917" height="1027" alt="image" src="https://github.com/user-attachments/assets/01cd7651-af4d-471d-8614-80cb61a585bf" />

## Link directo al dashboard publicado en Streamlit

El link donde se puede encontrar el Dashboard: https://dashboardplantaselectricastarea4-9ywfgzyftyqpeuy6ewcbfl.streamlit.app/

## Hallazgos principales del EDA

Dentro del EDA del Datasets fueron los siguentes:

**1. Predominio de la energía hidroeléctrica:** Se observa que la hidroeléctrica es la fuente con mayor número de plantas, seguida por la eólica, solar y gas; siendo el carbón quien presenta una menor cantidad dentro de las cinco categorías analizadas.

**2. Concentración geográfica:** Se encuentra que Estados Unidos presenta el mayor número de plantas, seguido por Brasil, China e India, lo que evidencia una distribución desigual de la infraestructura energética entre países.

**3. Crecimiento de las instalaciones:** Se observa que hay mayores entrada en operación de plantas a partir de los años 2000, con un crecimiento especialmente pronunciado durante la década de 2010.

**4. Relación entre capacidad y generación:** Las plantas con mayor capacidad tienden a presentar una mayor generación de energía, aunque existen diferencias según el tipo de combustible.

## Instrucciones de instalación y ejecución local

**1.** Descargar el proyecto desde GitHub.
**2.** Abrir una terminal dentro de la carpeta del proyecto.
**3.** Instalar las librerías que se encuentran en el archivo requirements.txt de la siguiente manera: pip install -r requirements.txt. o descárgalas individualmente como: streamlit, pandas, numpy, matplotlib, seaborn, y scipy.
**4.** Ejecutar el dashboard mediante el comando 'python -m streamlit run app.py' en el terminal.
**5.** Se abre en el navegador en http://localhost:8501.

**Requisito:** 
- Se requiere que se ejecute en Python 3.13 o 3.14.
- Es importante que el archivo `global_power_plant_database.csv` esté en la misma carpeta que `app.py`.

## Sobre el autor:

**Nombre:** Juan Sebastian Quiroga Alarcon
**Curso:** Programación para el Análisis de Datos
**Grupo:** 26
**Universidad:** Universidad Nacional Abierta y a Distancia (UNAD)
**Fecha:** 25 de Noviembre de 2026
