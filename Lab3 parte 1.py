import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Análisis de datos estadísticos lab 3")

# Función para cargar datos de forma segura
def cargar_datos(archivo):
    try:
        return pd.read_csv(archivo)
    except FileNotFoundError:
        st.error(f"No se encontró el archivo: {archivo}")
        return None

# Usa nombres de archivo directos si están en la misma carpeta
Carroselectricos = cargar_datos("carroselectricosdatos.csv")
videojuegos = cargar_datos("steam_store_data_2024.csv")
netflix = cargar_datos("netflix_titles.csv")
Gimnasio = cargar_datos("GymExerciseTracking.csv")

opcion = st.sidebar.selectbox(
    "Selecciona una opción",
    ["Vehículos", "Gimnasio", "Videojuegos", "Netflix"]
)

# Mostrar datos según la opción
if opcion == "Vehículos" and Carroselectricos is not None:
    st.header("Datos de Vehículos Eléctricos")
    st.dataframe(Carroselectricos)

elif opcion == "Gimnasio" and Gimnasio is not None:
    st.header("Datos de Gimnasio")
    st.dataframe(Gimnasio)

elif opcion == "Videojuegos" and videojuegos is not None:
    st.header("Datos de Steam 2024")
    st.dataframe(videojuegos)

elif opcion == "Netflix" and netflix is not None:
    st.header("Datos de Netflix")
    st.dataframe(netflix)