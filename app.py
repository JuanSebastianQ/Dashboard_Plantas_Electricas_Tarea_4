# ===========================================================
# Dashboard en streamlit - Tarea 4
# Dashboard: Plantas de generación electrica en el mundo
# Dataset: Global Power Plant Database
# ===========================================================

# Se importa las librerias que se van a utilizar en el proyecto
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from scipy import stats

# Se configura la pagina (Tutulo de la pestaña y ancho completo)
st.set_page_config(page_title="Plantas de Generación Eléctrica", layout="wide")

# Se carga de datos de la base de datos de plantas
@st.cache_data
def cargar_datos():
    df = pd.read_csv("global_power_plant_database.csv",
                     encoding = "latin-1")
    # Limpieza de coordenadas geograficas: latitud fuera de 90 o
    # longitud fuera de 180 no existen.
    df.loc[df['latitude'].abs() > 90, 'latitude'] = np.nan
    df.loc[df['longitude'].abs() > 180, 'longitude'] = np.nan
    return df

df_data  = cargar_datos()     

# Titulo y descripcion del dashboard
st.title('¿Como es la distribución de las plantas de generación eléctrica en el mundo?')
st.caption('Este dashboard permite explorar la distribución de las plantas de generación eléctrica en el mundo,'
           'por lo que se puede analizar la cantidad de plantas por país, por tipo de planta y por capacidad instalada.'
           'ademas se puede analizar la relación entre la capacidad instalada y el tipo de planta, asi como la relación '
           'entre la capacidad instalada y el país donde se encuentra la planta.')

# seccion de filtros para el dashboard
with st.sidebar:
    st.header('Filtros')
    
    # Filtro categorico: el usuario elige uno o varios combustibles
    combustible = st.multiselect("Combustible principal de la planta",
                                 sorted(df_data["fuel1"].dropna().unique()),
                                 default = ["Hydro", "Solar", "Wind", "Gas",
                                            "Coal"],
                                 )
    
    # Filtro numerico: rango de año de puesta en marcha de la planta
    anio_min, anio_max = st.slider("Año de puesta en marcha de la planta",
                                   1950, 2018, (1950, 2018))
    
    # Todos los graficos y metricas de abajo usan df_filtrado
    df_filtrado = df_data[df_data["fuel1"].isin(combustible)
                          & df_data["commissioning_year"].between(anio_min, anio_max)
                          ]
    
    # Si no se queda ninguna planta, se muestra un mensaje de error
    if df_filtrado.empty:
        st.warning("No hay plantas que cumplan con los filtros seleccionados.")
        st.stop() # Detiene la ejecución del resto del código si no hay datos que mostrar

# Exploracion de los datos: se muestran las primeras filas del dataframe        
st.header('1. Exploración de los datos')

# se muestra una tabla con las primeras filas del dataframe filtrado
col1, col2, col3 = st.columns(3)
col1.metric("Plantas (conteo)", f"{len(df_filtrado):,}")
col2.metric("Capacidad promedio (MW)", f"{df_filtrado['capacity_mw'].mean():,.1f}")
col3.metric("Variacion entre plantas (MW)", f"{df_filtrado['capacity_mw'].std():,.1f}")

# Tabla que se actualiza con los filtros
st.dataframe( df_filtrado[["name", "country_long", "fuel1",
                           "capacity_mw", "commissioning_year"]],
             height = 300,      
)       

# Visualizacion de la distribucion de plantas por pais y por tipo de planta

st.header('2. Visualizaciones')
izq, der = st.columns(2) # Dos graficos por filas

# Grafico 1: Cuantas plantas hay de cada combustibles
with izq:
    fig, ax = plt.subplots()
    orden = df_filtrado["fuel1"].value_counts().index
    sns.countplot(data = df_filtrado, y = "fuel1", order = orden, color="steelblue", ax=ax)
    ax.set_title("Numero de plantas por tipo de combustible")
    ax.set_xlabel("Numero de plantas")
    ax.set_ylabel("Combustible principal")
    st.pyplot(fig)
    
# Grafico 2: Cuantos paises tienen plantas de generacion electrica
    fig, ax = plt.subplots()
    top_paises = df_filtrado["country_long"].value_counts().head(10)
    sns.barplot(x=top_paises.values, y=top_paises.index, color="darkorange", ax=ax)
    ax.set_title("Los 10 países con más plantas")
    ax.set_xlabel("Número de plantas")
    ax.set_ylabel("País")
    st.pyplot(fig)
    
# Grafico 2: Cuantas plantas empezaron a operar cada año
with der: 
    por_anio = df_filtrado.groupby("commissioning_year").size()
    fig, ax = plt.subplots()
    ax.plot(por_anio.index, por_anio.values, color="steelblue")
    ax.set_title("Plantas puestas en operación por año")
    ax.set_xlabel("Año")
    ax.set_ylabel("Número de plantas")
    st.pyplot(fig)

# Grafico 3: tamaño de la planta vs energia que genera
    fig, ax = plt.subplots()
    sns.scatterplot(data=df_filtrado, x="capacity_mw", y="estimated_generation_gwh",
                    hue="fuel1", alpha=0.4, s=15, ax=ax)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Capacidad de la planta vs. energía que genera")
    ax.set_xlabel("Capacidad instalada (MW, escala log)")
    ax.set_ylabel("Generación estimada (GWh/año, escala log)")
    st.pyplot(fig)
    
# validacion estadistica
st.header("3. Validación estadística")
st.write("**Pregunta:** ¿las plantas hidroeléctricas y las solares tienen distinto tamaño?")

# Misma prueba de la Tarea 3 (t de Student), con TODO el dataset (no depende de filtros)
hydro = df_filtrado[df_filtrado["fuel1"] == "Hydro"]["capacity_mw"].dropna()
solar = df_filtrado[df_filtrado["fuel1"] == "Solar"]["capacity_mw"].dropna()
t_stat, p_value = stats.ttest_ind(hydro, solar, equal_var=False)

c1, c2 = st.columns(2)
c1.metric("Tamaño promedio hidroeléctricas (MW)", f"{hydro.mean():,.1f}")
c2.metric("Tamaño promedio solares (MW)", f"{solar.mean():,.1f}")

# Interpretación en lenguaje claro (p < 0.05 = la diferencia no parece casualidad)
if p_value < 0.05:
    st.write("Las plantas hidroeléctricas son, en promedio, bastante más grandes que las "
             "solares. Es muy poco probable que esta diferencia sea casualidad.")
else:
    st.write("No se encontró una diferencia clara de tamaño entre ambos tipos de planta.")

## Hallazgos
st.header("4. Hallazgos")
st.subheader("¿Qué analicé?")
st.write("""Se analizó una base de datos de 10.338 plantas de generación eléctrica a nivel mundial, considerando su distribución por tipo de combustible, 
         ubicación geográfica, año de puesta en operación y la relación entre la capacidad instalada (MW) y la generación estimada de energía (GWh/año). 
         Además, evalué indicadores generales como el número de plantas, la capacidad promedio y la variación de capacidad entre instalaciones.""")

st.subheader("¿Qué encontré?")
st.write("""Se encontró que las plantas hidroeléctricas representan la mayor cantidad de instalaciones, seguidas por las eólicas, solares y de gas; 
         donde Estados Unidos concentra el mayor número de plantas, seguido de Brasil y China. También se observa un crecimiento significativo en la entrada 
         en operación de nuevas instalaciones desde los años 2000 y una relación positiva entre la capacidad instalada y la generación estimada de energía.
         """)

st.subheader("¿Qué significa?")
st.write("""Los resultados muestran que la infraestructura de generación eléctrica presenta una distribución desigual entre países y tecnologías; 
         Asimismo, evidencian una expansión de la capacidad de generación durante las últimas décadas y una relación entre el tamaño de las instalaciones y su potencial de producción energética, 
         aunque el combustible y las condiciones operativas también pueden influir en la generación.""")

st.subheader("¿Qué se recomendaría?")
st.write("""Se recomienda profundizar en la comparación del desempeño de las diferentes fuentes energéticas, evaluar el crecimiento de las tecnologías renovables y analizar las diferencias 
         entre países en términos de capacidad instalada. Además, sería conveniente incorporar datos de generación real y factores de capacidad para evaluar la eficiencia de las plantas y 
         obtener conclusiones más precisas sobre su desempeño energético.""")

st.subheader("Resultados Estadística - Ejercicio IA T4-C")
st.write("""Se observa que las plantas con mayor capacidad presentan mayores valores de generación eléctrica estimada, ya que la relación encontrada es muy alta; 
            Sin embargo, este resultado debe interpretarse con precaución, ya que la generación estimada fue calculada utilizando la capacidad instalada como uno de sus datos de entrada. 
            Por tanto, esta relación era esperable y no constituye una evidencia independiente de que una mayor capacidad instalada garantice una mayor producción real de electricidad, 
            por lo que para evaluar el desempeño de las plantas, se recomienda complementar este análisis con datos de generación real y disponibilidad operativa.""")
