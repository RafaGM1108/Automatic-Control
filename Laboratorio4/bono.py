import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

# Streamlit app title
st.title('Bode Diagram Plotter')

# File upload section
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error: {e}")
    else:
        # Extract data from the CSV
        frecuencia = df['W'].values
        magnitud_dB = df['Mag'].values
        fase_grados = df['Phase'].values

        # Create the Bode plot
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        ax1.semilogx(frecuencia, magnitud_dB)
        ax1.set_ylabel('Amplitud (dB)')
        ax1.grid()
        ax1.set_title('Bode Diagram')

        ax2.semilogx(frecuencia, fase_grados)
        ax2.set_xlabel('Frecuencia (Hz)')
        ax2.set_ylabel('Fase (grados)')
        ax2.grid()


        # Calculate and display cutoff frequency and bandwidth
        
        
        A = None
        ancho_de_banda = None
        margen_de_fase = None
        margen_de_ganancia = None
        pico = None
        frecuencia_de_resonancia = None

        # Encuentra el índice del pico (máxima magnitud)
        
        
        cutoff_indices = np.where(magnitud_dB <= 0.707)[0]
        if len(cutoff_indices) > 0:
            first_index = cutoff_indices[0]
            A = frecuencia[first_index]

            # Encuentra el último índice que cumple la condición
            last_index = cutoff_indices[-1]

            # Calcula el ancho de banda
            ancho_de_banda = frecuencia[last_index] - frecuencia[first_index]

        st.write("Frecuencia de corte:", A)
        st.write("Ancho de Banda:", ancho_de_banda)


        # Encuentra el índice de la frecuencia de cruce donde la magnitud es 0 dB
        crossing_indices = np.where(np.diff(np.signbit(magnitud_dB)))[0]
        if len(crossing_indices) > 0:
            # Calcula el margen de ganancia
            gain_margin_index = crossing_indices[0]
            margen_de_ganancia = -magnitud_dB[gain_margin_index]

        # Encuentra el índice de la frecuencia de cruce donde la fase es -180 grados
        phase_crossing_indices = np.where(np.diff(np.signbit(fase_grados + 180)))[0]
        if len(phase_crossing_indices) > 0:
            # Calcula el margen de fase
            phase_margin_index = phase_crossing_indices[0]
            margen_de_fase = -180 - fase_grados[phase_margin_index]

        st.write("Margen de Fase:", margen_de_fase)
        st.write("Margen de Ganancia:", margen_de_ganancia)
        
        peak_magnitude_index = np.argmax(magnitud_dB)
        if peak_magnitude_index is not None:
            # Calcula el pico y la frecuencia de resonancia
            pico = magnitud_dB[peak_magnitude_index]
            frecuencia_de_resonancia = frecuencia[peak_magnitude_index]

        st.write("Pico:", pico)
        st.write("Frecuencia de Resonancia:", frecuencia_de_resonancia)
        
        st.pyplot(fig)
