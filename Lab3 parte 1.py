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


#----------------------------------------VEHICULOS---------------------------------------------------------------------
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
            Carroselectricos.to_csv("carroselectricosdatos.csv", index=False)

            st.success("Vehículo agregado correctamente ✅")
            st.dataframe(Carroselectricos)

#-------------------------Seccion de filtros de la data de vehiculos----------------------------------
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

#------------------------------------Seccion de Exploracion avanzada_Ve--------------------------------

        st.divider()
        st.subheader("Exploración Avanzada - Vehículos")
        
        # Crear variable categórica
        bins_ve = [-1, 99, 250, float('inf')]
        labels_ve = ['Bajo', 'Medio', 'Alto']
        Carroselectricos['RangoCategoria'] = pd.cut(Carroselectricos['Electric_Range'], bins=bins_ve, labels=labels_ve)

        st.divider()
        st.header("Análisis Avanzado: Vehículos")

        #Conteo por categoria
        conteo_ve = Carroselectricos['RangoCategoria'].value_counts()
        st.write("Cantidad de registros por categoría:", conteo_ve)

        #Grafico de barras
        st.subheader("Gráfico: Distribución de Vehículos por Rango")
        st.bar_chart(conteo_ve)
        
        # Analisis agrupado 
        st.subheader("Analisis Agrupado: Base MSPR, Año de modelo, Rango Electrico")
        analisis_ve = Carroselectricos.groupby('RangoCategoria', observed=False).agg({
            'Base_MSRP': 'mean',
            'Model Year': 'mean',
            'Electric_Range': 'std'
        }).rename(columns={
            'Base_MSRP': 'Media Precio',
            'Model Year': 'Media Año',
            'Electric_Range': 'Desv. Estándar Rango'
        })
        st.dataframe(analisis_ve)


#----------------------------------------GIMNASIO---------------------------------------------------------------------

elif opcion == "Gimnasio" and Gimnasio is not None:
    st.header("Datos de Gimnasio")
    st.dataframe(Gimnasio)
    st.subheader("Estadisticas genereales")
    st.write(Gimnasio.describe())

#-------------------------Seccion de filtros de la data de gimnasio----------------------------------
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

#------------------------------------Seccion de Exploracion avanzada_Gim--------------------------------

    st.divider()
    st.subheader("Exploración Avanzada - Gimnasio")
        
     # Crear variable categórica
    bins_gim = [-1,2,5,7]
    labels_gim = ['Baja', 'Moderada', 'Alta']
    Gimnasio['NivelFrecuencia'] = pd.cut(Gimnasio['Workout_Frequency (days/week)'], bins=bins_gim, labels=labels_gim)
        
    st.write("Datos de NivelFrecuencia:")
    st.dataframe(Gimnasio[['Age', 'Gender', 'Workout_Frequency (days/week)', 'NivelFrecuencia']].head())

    st.divider()
    st.header("Análisis Avanzado: Gimnasio")

    #Conteo por categoria
    conteo_gi = Gimnasio['NivelFrecuencia'].value_counts()
    st.write("Cantidad de registros por categoría:", conteo_gi)

    #Grafico de barras
    st.subheader("Gráfico: Distribución de nivel de frecuencia por Rango")
    st.bar_chart(conteo_gi)
        
    # Analisis agrupado 
    st.subheader("AnalsiS agrupado:Duracion, Experiencia, BMI")
    analisis_gi = Gimnasio.groupby('NivelFrecuencia', observed=False).agg({
        'Session_Duration (hours)': 'mean',
        'Experience_Level': 'mean',
        'BMI': 'std'
    }).rename(columns={
        'Session_Duration (hours)': 'Media de duracion de sesiones',
        'Experience_Level': 'Media de nivel de experiencia',
        'BMI': 'Desv. Estándar BMI'
    })
    st.dataframe(analisis_gi)


#----------------------------------------VIDEOJUEGOS---------------------------------------------------------------------
elif opcion == "Videojuegos" and videojuegos is not None:
    st.header("Datos de Steam 2024")
    videojuegos['price_clean'] = (
        videojuegos['price']
        .astype(str)
        .str.replace('$', '', regex=False)
        .str.replace(',', '', regex=False)
        .str.strip()
    )
    videojuegos['price_clean'] = pd.to_numeric(videojuegos['price_clean'], errors='coerce')

    videojuegos['salePercentage_clean'] = (
        videojuegos['salePercentage']
        .astype(str)
        .str.replace('%', '', regex=False)
        .str.replace('-', '', regex=False)
        .str.replace(r'[^0-9.]', '', regex=True)
        .str.strip()
    )

    videojuegos['salePercentage_clean'] = pd.to_numeric(videojuegos['salePercentage_clean'], errors="coerce")

    st.dataframe(videojuegos)
    st.subheader("Estadisticas genereales")
    st.write(videojuegos.describe())

    st.subheader("Añadir nuevo videojuego")

    with st.form("form_videojuegos"):
        titulo = st.text_input("Título")
        descripcion = st.text_area("Descripción")
        precio = st.number_input("Precio", min_value=0)
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
                videojuegos.to_csv("steam_store_data_2024.csv", index=False)

                st.success("Videojuego agregado correctamente 🎮")
                st.dataframe(videojuegos)

#-------------------------Seccion de filtros de la data de videojuegos----------------------------------
    #Filtro de precios por precios mayores
    precio = st.number_input("Filtro por precio mayor",min_value=0)

    filtro_price = videojuegos[videojuegos["price_clean"]>precio]
    st.header("Filtro de precio por precios mayores")
    st.dataframe(filtro_price)

    #Filtro por porcentaje de descuento
    desc = st.number_input("Filtro por porcentaje de descuento",min_value=0.0, max_value=100.0)

    filtro_desc = videojuegos[videojuegos["salePercentage_clean"]<desc]
    st.header("Filtro por porcentaje de descuento")
    st.dataframe(filtro_desc)


#------------------------------------Seccion de Exploracion avanzada_vid--------------------------------

    st.divider()
    st.subheader("Exploración Avanzada - Videojuegos")

     # Crear variable categórica
    bins_vid = [-1,9.99,24,float('inf')]
    labels_vid = ['Baja', 'Media', 'Alta']
    videojuegos['GamaJuego'] = pd.cut(videojuegos['price_clean'], bins=bins_vid, labels=labels_vid)

    st.divider()
    st.header("Análisis Avanzado: Videojuegos")

    #Conteo por categoria
    conteo_vid = videojuegos['GamaJuego'].value_counts()
    st.write("Cantidad de registros por categoría:", conteo_vid)

    #Grafico de barras
    st.subheader("Gráfico: Distribución de gama de juegos por Rango")
    st.bar_chart(conteo_vid)
        
    # Analisis agrupado 
    st.subheader("Analisis Agrupado: Precio, Descuento")
    analisis_vid = videojuegos.groupby('GamaJuego', observed=False).agg({
    'price_clean': ['mean', 'std'],
    'salePercentage_clean': 'mean',
    })
    analisis_vid.columns = [' '.join(col).strip() for col in analisis_vid.columns]
    analisis_vid = analisis_vid.rename(columns={
    'price_clean mean': 'Media del precio',
    'price_clean std': 'Desv. Estandar del precio',
    'salePercentage_clean mean': 'Media del porcentaje de descuento',
    })

    st.dataframe(analisis_vid)

#----------------------------------------NETFLIX---------------------------------------------------------------------
elif opcion == "Netflix" and netflix is not None:
    st.header("Datos de Netflix")
    st.dataframe(netflix)
    st.subheader("Estadisticas genereales")
    st.write(netflix.describe())

#-------------------------Seccion de filtros de la data de netflix----------------------------------
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


#------------------------------------Seccion de Exploracion avanzada_net--------------------------------
    st.divider()
    st.header("Exploración Avanzada - Netflix")

    #Limpieza de duracion
   
    netflix['duration_clean'] = (
        netflix['duration']
        .astype(str)
        .str.extract('(\d+)') 
    )
    netflix['duration_clean'] = pd.to_numeric(netflix['duration_clean'], errors='coerce').fillna(0)

    #Variable Categorica:TipoAudiencia
    def categorizar_audiencia(rating):
        ninos = ['G', 'TV-Y', 'TV-G', 'TV-Y7', 'TV-Y7-FV']
        adolescentes = ['PG', 'TV-PG']
        adultos_jovenes = ['PG-13', 'TV-14']
        adultos = ['R', 'TV-MA', 'NC-17']
        
        if rating in ninos: return 'Niños'
        if rating in adolescentes: return 'Adolescentes'
        if rating in adultos_jovenes: return 'Adultos Jóvenes'
        if rating in adultos: return 'Adultos'
        return 'Sin Clasificar'

    netflix['TipoAudiencia'] = netflix['rating'].apply(categorizar_audiencia)

    st.divider()
    st.subheader("Analisis Avanzado: Netflix")

    #Conteo de por categoria
    conteo_aud = netflix['TipoAudiencia'].value_counts()
    st.write("Cantidad de registros por categoría:",conteo_aud)

    #Grafico de barras
    st.subheader("Gráfico: Distribución de audiencia por Rango")
    st.bar_chart(conteo_aud)

    #Analisis agrupado
    st.divider()
    st.subheader("Análisis Agrupado: Audiencia, Contenido y Duración")

    def el_mas_comun(series):
    
        return series.mode()[0]

    analisis_netflix = netflix.groupby('TipoAudiencia').agg({
        'type': el_mas_comun,
        'duration_clean': 'mean' 
    }).rename(columns={
        'type': 'Contenido más común',
        'duration_clean': 'Duración promedio'
    })

    st.dataframe(analisis_netflix)
