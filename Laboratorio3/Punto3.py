import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from tbcontrol.symbolic import routh

def fill(n):
    matrix = []
    for i in range(n):
        tmp = []
        for j in range(int(sp.ceiling(n / 2))):
            tmp.append(0)
        matrix.append(tmp)
    return matrix

def cambio_signo(n1, n2):
    if (n1 < 0) and (n2 > 0):
        return True
    elif (n1 > 0) and (n2 < 0):
        return True
    else:
        return False

def routh_criterion(coeff):
    n = len(coeff)
    matrix = fill(n)
    m = len(matrix[0])
    curr = 0
    epsilon_symbol = sp.symbols('ε')  # Símbolo epsilon
    
    for i in range(m):
        for j in range(2):
            if curr < n:
                matrix[j][i] = coeff[curr]
                curr += 1
                
    for i in range(2, n):
        pivote = matrix[i - 1][0]
        for j in range(m):
            if j < m - 1:
                if pivote == 0:
                    matrix[i][0] = epsilon_symbol  # Usar símbolo epsilon en lugar de cadena "E"
                else:
                    matrix[i][j] = ((matrix[i - 1][0] * matrix[i - 2][j + 1]) - (matrix[i - 2][0] * matrix[i - 1][j + 1])) / pivote

    cambio = 0
    ant = matrix[0][0]
    unstable_roots = []  # Almacenar raíces inestables
    for i in range(n):
        if cambio_signo(ant, matrix[i][0]):
            cambio += 1
            # Verificar si la raíz es inestable (parte real positiva)
            if i < n - 1:
                s = sp.symbols('s')
                poly = sp.Poly(coeff, s)
                roots = sp.solve(poly, s)
                for root in roots:
                    if root.is_real and root.evalf() > 0:
                        unstable_roots.append(root)
        ant = matrix[i][0]
    
    return matrix, cambio, unstable_roots

st.title("Calculadora de Routh-Hurwitz y Gráfico de Raíces")

# Ingreso de coeficientes del polinomio
coeff_str = st.text_input("Ingresa los coeficientes del polinomio separados por coma:")

# Ingreso de valor de 'k'
k_input = st.text_input("Ingresa el valor de 'k' (si es necesario):")

s = sp.Symbol('s')

if coeff_str:
    try:
        # Parsear los coeficientes ingresados por el usuario
        coeff = [sp.S(x.strip()) if x != 'k' else 'k' for x in coeff_str.split(",")]

        # Calcular la matriz de Routh-Hurwitz
        routh_matrix, cambios, unstable_roots = routh_criterion(coeff)

        # Mostrar la matriz de Routh-Hurwitz como una tabla
        st.write("Matriz de Routh-Hurwitz:")

        st.table(routh_matrix)
        
        st.write(f"Cambios de signo en la primera columna: {cambios}")

        if k_input:
            try:
                k_value = float(k_input)
                coeff_with_k = [k_value if coeff == 'k' else coeff for coeff in coeff]
                equation = sp.Poly(coeff_with_k, s)
                roots = sp.solve(equation, s)

                if roots:
                    roots = [complex(root.evalf()) for root in roots]
                    real_part = [root.real for root in roots]
                    imag_part = [root.imag for root in roots]

                    # Mostrar las raíces en la interfaz
                    st.write("Raíces calculadas:")
                    for root in roots:
                        st.write(root)

                    # Graficar raíces
                    plt.figure(figsize=(8, 6))
                    plt.scatter(real_part, imag_part, marker='x', color='red', label='Raíces')
                    plt.axhline(y=0, color='k', linestyle='--', linewidth=0.7)
                    plt.axvline(x=0, color='k', linestyle='--', linewidth=0.7)
                    plt.xlabel('σ')
                    plt.ylabel('jω')
                    plt.title('Gráfico de Raíces en el Plano Complejo')
                    plt.legend()

                    st.pyplot(plt)

                    if cambios == 0 and len(unstable_roots) == 0:
                        st.write("El sistema es críticamente estable y no hay raíces con parte real positiva.")
                    elif cambios > 0:
                        st.write(f"El sistema es inestable y tiene {cambios} raíces inestables con parte real positiva.")
                    elif len(unstable_roots) > 0:
                        st.write(f"El sistema es estable con {len(unstable_roots)} raíces en el eje imaginario.")

                else:
                    st.write("La ecuación no tiene raíces reales en el plano complejo.")
            except ValueError:
                st.write("El valor ingresado para 'k' no es válido.")
        else:
            st.write("Ingresa un valor para 'k' si es necesario.")
    except Exception as e:
        st.write("Ocurrió un error al procesar los coeficientes. Asegúrate de que estén en el formato correcto separados por coma.")

