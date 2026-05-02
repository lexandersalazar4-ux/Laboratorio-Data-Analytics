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

        #Filtro por año anterior al ingresado
        anio = st.number_input("Filtar por año amximo", min_value=2000,max_value=2025)

        filtro_anio = Carroselectricos[Carroselectricos["Model Year"] < anio]
        st.subheader("Vehículos filtrados por año")
        st.dataframe(filtro_anio)

        #Filtro por precio menor al ingresado
        precio = st.number_input("Filtrar por precio máximo", min_value=0.0, max_value=845000.0)

        filtro_precio = Carroselectricos[Carroselectricos["Base_MSRP"] < precio]
        st.subheader("Vehículos filtrados por precio")
        st.dataframe(filtro_precio)

elif opcion == "Gimnasio" and Gimnasio is not None:
    st.header("Datos de Gimnasio")
    st.dataframe(Gimnasio)
    st.subheader("Estadisticas genereales")
    st.write(Gimnasio.describe())

    #Filtro de calorias minimas
    cal = st.number_input("Calorias minimas",min_value=0.0)

    filtro_cal = Gimnasio[Gimnasio["Calories_Burned"]>= cal]
    st.subheader("Calorias filtradas por calorias minimas")
    st.dataframe(filtro_cal)

    #Filtro por grasa maxima
    porcen_grasa = st.number_input("Filtro por porcentaje de grasa maximo",min_value=0.0,max_value=100.0)

    filtro_grasa = Gimnasio[Gimnasio["Fat_Percentage"]<= porcen_grasa]
    st.header("Porcentaje de grasa filtrado por porcentaje maximo")
    st.dataframe(filtro_grasa)

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

    #Filtro de precios por precios mayores
    precio = st.number_input("Filtro por precio mayor",min_value=0)

    videojuegos["price"] = pd.to_numeric(videojuegos["price"], errors="coerce")
    filtro_price = videojuegos[videojuegos["price"]>precio]
    st.header("Filtro de precio por precios mayores")
    st.dataframe(filtro_price)

    #Filtro por porcentaje de descuento
    desc = st.number_input("Filtro por porcentaje de descuento",min_value=0.0, max_value=100.0)

    videojuegos["salePercentage"] = pd.to_numeric(videojuegos["salePercentage"], errors="coerce")
    filtro_desc = videojuegos[videojuegos["salePercentage"]<desc]
    st.header("Filtro por porcentaje de descuento")
    st.dataframe(filtro_desc)

elif opcion == "Netflix" and netflix is not None:
    st.header("Datos de Netflix")
    st.dataframe(netflix)
    st.subheader("Estadisticas genereales")
    st.write(netflix.describe())

    #Filtro por año de estreno
    anio_e = st.number_input("Filtro por año de estreno",min_value=1990, max_value=2025)

    filtro_anio_e = netflix[netflix["release_year"]<anio_e]
    st.header("Filtro por año de estreno")
    st.dataframe(filtro_anio_e)

    #Filtro duracion en minutos
    peliculas = netflix[netflix["type"] == "Movie"]
    peliculas["duration_int"] = peliculas["duration"].str.extract(r'(\d+)').astype(float)

    duracion = st.number_input("Filtro por duracion en minutos",min_value=0.0)

    filtro_duracion = peliculas[peliculas["duration_int"]>duracion]
    st.header("Filtro de duracion en minutos")
    st.dataframe(filtro_duracion)