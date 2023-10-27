import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st 


archivo_csv = 'example_P2.csv'

dataframe = pd.read_csv(archivo_csv)

magnitud = dataframe['Mag'].values
fase = dataframe['Phase'].values
frecuencia = dataframe['W'].values

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.semilogx(frecuencia, magnitud)
plt.title('Diagrama de Bode - Magnitud')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Magnitud [dB]')

plt.subplot(2, 1, 2)
plt.semilogx(frecuencia, fase)
plt.title('Diagrama de Bode - Fase')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Fase [grados]')

plt.tight_layout()
plt.show()
