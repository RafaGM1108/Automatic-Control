import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

epsilon_symbol = "ε"  # Usar el símbolo epsilon (ε) en la interfaz

# Valor epsilon muy pequeño para cálculos internos
epsilon_value = 1e-9  

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
    for i in range(m):
        for j in range(2):
            if curr < n:
                if curr == 0 and coeff[curr] == 0:
                    matrix[j][i] = epsilon_symbol  # Mostrar ε en la interfaz
                else:
                    matrix[j][i] = coeff[curr]
                curr += 1
    for i in range(2, n):
        pivote = matrix[i - 1][0]
        for j in range(m):
            if j < m - 1:
                if pivote == 0:
                    # Reemplazar solo el elemento en la matriz con ε en lugar de toda la fila
                    matrix[i][j] = epsilon_symbol  # Mostrar ε en la interfaz
                else:
                    matrix[i][j] = ((matrix[i - 1][0] * matrix[i - 2][j + 1]) - (matrix[i - 2][0] * matrix[i - 1][j + 1])) / pivote
        # Asignar epsilon_value a pivote para cálculos internos
        if pivote == epsilon_symbol:
            pivote = epsilon_value
    
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

st.title("Criterio de Routh-Hurwitz y Gráfico de Raíces")

coeff_str = st.text_input("Ingresa los coeficientes del polinomio separados por coma:")

if coeff_str:
    try:
        coeff = [float(x) for x in coeff_str.split(",")]
        n = len(coeff)
        s = sp.symbols('s')
        equation = sum(coeff[i] * s**(n - i - 1) for i in range(n))
        
        matrix, cambio, unstable_roots = routh_criterion(coeff)
        
        st.write("Matriz de Routh-Hurwitz:")

        st.table(matrix)
        
        st.write(f"Cambios de signo: {cambio}")
        
        if cambio == 0 and len(unstable_roots) == 0:
            st.write("El sistema es críticamente estable.")
        elif cambio > 0:
            st.write(f"El sistema es inestable y tiene {cambio} raíces inestables.")
        elif len(unstable_roots) > 0:
            st.write(f"El sistema es estable con {len(unstable_roots)} raíces en el eje imaginario.")
        
        # Calcular y graficar las raíces
        roots = sp.solve(equation, s)
        
        if roots:
            roots = [complex(root.evalf()) for root in roots]
            real_part = [root.real for root in roots]
            imag_part = [root.imag for root in roots]
            
            plt.figure(figsize=(8, 6))
            plt.scatter(real_part, imag_part, marker='x', color='red', label='Raíces')
            plt.axhline(y=0, color='k', linestyle='--', linewidth=0.7)
            plt.axvline(x=0, color='k', linestyle='--', linewidth=0.7)
            plt.xlabel('Parte Real')
            plt.ylabel('Parte Imaginaria')
            plt.title('Gráfico de Raíces en el Plano Complejo')
            plt.legend()
            
            st.pyplot(plt)
            
            if unstable_roots:
                st.write("Las raíces inestables son:")
                for root in unstable_roots:
                    st.write(root)
        else:
            st.write("La ecuación no tiene raíces reales en el plano complejo.")
    except Exception as e:
        st.write("Ocurrió un error al procesar los coeficientes. Asegúrate de que estén en el formato correcto separados por coma.")