import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("Visualizador de Diagrama de Bode")

# Widget para cargar un archivo CSV
uploaded_file = st.file_uploader("Cargar un archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        dataframe = pd.read_csv(uploaded_file)

        magnitud = dataframe['Mag'].values
        fase = dataframe['Phase'].values
        frecuencia = dataframe['W'].values

        st.subheader("Diagrama de Bode - Magnitud")
        plt.figure(figsize=(12, 6))
        plt.semilogx(frecuencia, magnitud)
        plt.title('Diagrama de Bode - Magnitud')
        plt.xlabel('Frecuencia [Hz]')
        plt.ylabel('Magnitud [dB]')
        st.pyplot(plt)

        st.subheader("Diagrama de Bode - Fase")
        plt.figure(figsize=(12, 6))
        plt.semilogx(frecuencia, fase)
        plt.title('Diagrama de Bode - Fase')
        plt.xlabel('Frecuencia [Hz]')
        plt.ylabel('Fase [grados]')
        st.pyplot(plt)

    except Exception as e:
        st.error("Ocurrió un error al cargar y procesar el archivo CSV. Asegúrate de que el archivo sea válido.")
