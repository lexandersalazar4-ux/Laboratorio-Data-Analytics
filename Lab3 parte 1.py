import pandas as pd
import streamlit as st

st.title("Análisis de datos estadísticos laboratorio 3")

# Función para cargar datos de forma segura
def cargar_datos(archivo):
    try:
        return pd.read_csv(archivo)
    except FileNotFoundError:
        st.error(f"No se encontró el archivo: {archivo}")
        return None

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
    st.subheader("Datos generales")
    st.dataframe(Carroselectricos)
    st.subheader("Estadisticas generales")
    st.write(Carroselectricos.describe())
    st.subheader("Añadir carros extras")

    with st.form("form_vehiculos"):
        nuevo_VIN = st.text_input("VIN (1-10)")
        nueva_ciudad = st.text_input("Ciudad")
        Modelo_de_año = st.number_input("Modelo de año", min_value=0)
        Make = st.text_input("Marca")
        Model = st.text_input("Model")
        tipo_de_carro_electrico = st.text_input("Tipo de carro electrico")
        CAVF_ELigibility = st.text_input("CAFV_Eligibility")
        Electric_Range = st.number_input("Rango electrico", min_value=0)
        Base_MSRP = st.number_input("Base_MSRP", min_value=0)
        Electric_Utility = st.text_input("Electric Utility")

        submitted = st.form_submit_button("Agregar vehículo")
        
        if submitted:
            nuevo_registro = pd.DataFrame({
                "VIN (1-10)": [nuevo_VIN],
                "City": [nueva_ciudad],
                "Model Year": [Modelo_de_año],
                "Make": [Make],
                "Model": [Model],
                "Electric_Vehicle_Type": [tipo_de_carro_electrico],
                "CAFV_Eligibility": [CAVF_ELigibility],
                "Electric_Range": [Electric_Range],
                "Base_MSRP": [Base_MSRP],
                "Electric Utility": [Electric_Utility]
            })

            Carroselectricos = pd.concat([Carroselectricos, nuevo_registro], ignore_index=True)

            st.success("Vehículo agregado correctamente ✅")
            st.dataframe(Carroselectricos)
elif opcion == "Gimnasio" and Gimnasio is not None:
    st.header("Datos de Gimnasio")
    st.dataframe(Gimnasio)
    st.subheader("Estadisticas genereales")
    st.write(Gimnasio.describe())
elif opcion == "Videojuegos" and videojuegos is not None:
    st.header("Datos de Steam 2024")
    st.dataframe(videojuegos)
    st.subheader("Estadisticas genereales")
    st.write(videojuegos.describe())

    st.subheader("Añadir nuevo videojuego")

    with st.form("form_videojuegos"):
        titulo = st.text_input("Título")
        descripcion = st.text_area("Descripción")
        precio = st.number_input("Precio", min_value=0.0)
        descuento = st.number_input("Porcentaje de descuento", min_value=0.0, max_value=100.0)
        reseñas_recientes = st.text_input("Reseñas recientes")
        reseñas_totales = st.text_input("Reseñas totales")

        submitted = st.form_submit_button("Agregar videojuego")

        if submitted:
            # Validación básica
            if titulo == "":
                st.warning("El título es obligatorio")
            else:
                nuevo_registro = pd.DataFrame({
                    "title": [titulo],
                    "description": [descripcion],
                    "price": [precio],
                    "salePercentage": [descuento],
                    "recentReviews": [reseñas_recientes],
                    "allReviews": [reseñas_totales]
                })

                videojuegos = pd.concat([videojuegos, nuevo_registro], ignore_index=True)

                st.success("Videojuego agregado correctamente 🎮")
                st.dataframe(videojuegos)
elif opcion == "Netflix" and netflix is not None:
    st.header("Datos de Netflix")
    st.dataframe(netflix)
    st.subheader("Estadisticas genereales")
    st.write(netflix.describe())