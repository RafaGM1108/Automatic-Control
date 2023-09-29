import streamlit as st
import math

epsilon = 1e-9  # Valor epsilon muy pequeño

def fill(n):
    matrix = []
    for i in range(n):
        tmp = []
        for j in range(int(math.ceil(n / 2.0))):
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
                    matrix[j][i] = epsilon  # Coloca epsilon en lugar de 0.0
                else:
                    matrix[j][i] = coeff[curr]
                curr += 1
    for i in range(2, n):
        pivote = matrix[i - 1][0]
        for j in range(m):
            if j < m - 1:
                if pivote == 0:
                    matrix[i][j] = 'E'  # Coloca epsilon en lugar de 0.0
                else:
                    matrix[i][j] = ((matrix[i - 1][0] * matrix[i - 2][j + 1]) - (matrix[i - 2][0] * matrix[i - 1][j + 1])) / pivote
    
    cambio = 0
    ant = matrix[0][0]
    for i in range(n):
        if cambio_signo(ant, matrix[i][0]):
            cambio += 1
        ant = matrix[i][0]
    
    return matrix, cambio


st.title("Criterio de Routh-Hurwitz")

coeff_str = st.text_input("Ingresa los coeficientes del polinomio separados por comas:")

if coeff_str:
    coeff = [float(x) for x in coeff_str.split(",")]
    matrix, cambio = routh_criterion(coeff)
    
    st.write("Matriz de Routh-Hurwitz:")
    st.table(matrix)
    
    st.write(f"Cambios de signo: {cambio}")
    if cambio > 0:
        st.write("El sistema es inestable")
    else:
        st.write("El sistema es estable")
