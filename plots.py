# Copyright (c) 2025 César Rivera
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
#Este script se encarga de crear un gráfico de dispersión y calcular el intervalo de confianza
    
from conexion import obtener_engine  # Conexión a la base de datos
import pandas as pd
from scipy import stats  # Para estadísticas y el intervalo de confianza
import matplotlib.pyplot as plt

#Paso 1: Obtener la conexión
engine = obtener_engine()

#Paso 2: Leer las tablas desde la base de datos
with engine.connect() as conn:
    customers = pd.read_sql("SELECT * FROM customers", conn)
    orders = pd.read_sql("SELECT * FROM orders", conn)

#Paso 3: Unir ambas tablas usando customer_id
orders_with_customers = orders.merge(customers, on='customer_id')

#Paso 4: Calcular el total de ventas por ciudad
total_por_ciudad = orders_with_customers.groupby('ciudad')['monto'].sum()

#Guardar los datos en un archivo CSV
total_por_ciudad.to_csv('total_por_ciudad.csv', header=True)

#Paso 5: Función para graficar el total por ciudad
def graficar_total_por_ciudad(total_por_ciudad):
    total_por_ciudad.plot(kind='bar', title='Total de Ventas por Ciudad', color='skyblue')
    plt.ylabel('Monto Total')
    plt.xlabel('Ciudad')
    plt.grid(True)
    plt.show()

#Llamar a la función para graficar
graficar_total_por_ciudad(total_por_ciudad)
