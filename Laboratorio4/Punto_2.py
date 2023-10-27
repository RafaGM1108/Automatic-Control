import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


try:
    df = pd.read_csv('example_P2.csv')
except FileNotFoundError:
    print("Error: El archivo CSV no se encontró.")
    exit(1)

frecuencia = df['W'].values
magnitud_dB = df['Mag'].values
fase_grados = df['Phase'].values

ganancia = 10**(magnitud_dB / 20)
fase_radianes = np.deg2rad(fase_grados)


if len(np.where(ganancia < -3)[0]) == 1:
    orden_estimado = 1
else:
    orden_estimado = 2

def transfer_function(freq, *params):
    if orden_estimado == 1:
        K, tau = params
        return K / (1 + 1j * 2 * np.pi * freq * tau)
    elif orden_estimado == 2:
        K, omega_n, zeta = params
        return K / (1 - (1j * 2 * np.pi * freq / omega_n) + (1j * 2 * np.pi * freq / omega_n)**2 + 2 * zeta * 1j * 2 * np.pi * freq / omega_n)


if orden_estimado == 1:
    popt, _ = curve_fit(transfer_function, frecuencia, ganancia, p0=(1, 1))
    K_estimado, tau_estimado = popt
elif orden_estimado == 2:
    popt, _ = curve_fit(transfer_function, frecuencia, ganancia, p0=(1, 1, 1))
    K_estimado, omega_n_estimado, zeta_estimado = popt

plt.figure()
plt.subplot(2, 1, 1)
plt.semilogx(frecuencia, magnitud_dB)
plt.ylabel('Amplitud (dB)')
plt.grid()
plt.title('Diagrama de Bode')
plt.subplot(2, 1, 2)
plt.semilogx(frecuencia, fase_grados)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Fase (grados)')
plt.grid()
plt.show()


if orden_estimado == 1:
    print("Función de Transferencia Estimada (Orden 1):")
    print(f"H(s) = {K_estimado} / (1 + s{tau_estimado})")
elif orden_estimado == 2:
    print("Función de Transferencia Estimada (Orden 2):")
    print(f"H(s) = {K_estimado} / (1 - s^2/{omega_n_estimado}^2 + s/{zeta_estimado}/{omega_n_estimado})")
