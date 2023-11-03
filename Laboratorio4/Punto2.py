import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import control as ct

# Streamlit app title
st.title('Punto 2-Laboratorio 4')

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
        
        
        

        A = None
        ancho_de_banda = None
        margen_de_fase = None
        margen_de_ganancia = None
        pico = None
        frecuencia_de_resonancia = None
        
        
        max_magnitude = max(magnitud_dB) 
        resonance_frequency = frecuencia[magnitud_dB.tolist().index(max_magnitude)]
        
        
        # Calcular el valor de -3 dB por debajo del máximo
        cutoff_magnitude = max_magnitude - 3.0 #! Calculo de los 3 decibeles

        # Buscar la frecuencia de corte (frecuencia donde la magnitud cae a -3 dB por debajo del máximo)
        for i in range(len(magnitud_dB)):
            if magnitud_dB[i] <= cutoff_magnitude:
                cutoff_frequency = frecuencia[i]
            break
    
            
        resonance_phase = fase_grados[magnitud_dB.tolist().index(max_magnitude)]

        phase_margin = 180 - resonance_phase
        
        index_minus_180_deg = None
        for i, phase in enumerate(fase_grados):
            if phase <= -180:
                index_minus_180_deg = i
            break



        if index_minus_180_deg is not None:
            gain_at_minus_180_deg = 10 ** (magnitud_dB[index_minus_180_deg] / 20)  # Convertir de dB a ganancia lineal
            st.write("Margen de ganancia: {} dB".format(gain_at_minus_180_deg))
        else:
            st.write("No se encontró un margen de ganancia de -180 grados en el rango de frecuencias proporcionado.")
            
            
            
        lower_frequency = None
        upper_frequency = None

        # Buscar la frecuencia donde la magnitud cruza -3 dB por debajo del máximo
        for i in range(len(magnitud_dB)):
            if magnitud_dB[i] >= cutoff_magnitude:
                if lower_frequency is None:
                    lower_frequency = frecuencia[i]
            elif lower_frequency is not None:
                upper_frequency = frecuencia[i]
                break
            
        if lower_frequency is not None and upper_frequency is not None:
            bandwidth = upper_frequency - lower_frequency
            st.write("Ancho de banda: {} Hz".format(bandwidth))
        else:
            st.write("No se encontró un ancho de banda de -3 dB por debajo del máximo en el rango de frecuencias proporcionado.")
    
        st.write("Margen de fase: {} grados".format(phase_margin))

        st.write("Frecuencia de resonancia: {} Hz".format(resonance_frequency))

        st.write("Frecuencia de corte (-3 dB por debajo del máximo): {} Hz".format(cutoff_frequency))
        
        
        st.pyplot(fig)




