# Copyright (c) 2025 César Rivera
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# Este script realiza la conexión a la base de datos, une las tablas 'orders' y 'customers'
# y ejecuta un análisis estadístico de los montos de compra por cliente y por ciudad.

from conexion import obtener_engine
import pandas as pd
from scipy import stats

# Conexión a la base de datos
engine = obtener_engine()

# Cargar datos desde la base
with engine.connect() as conn:
    customers = pd.read_sql("SELECT * FROM customers", conn)
    orders = pd.read_sql("SELECT * FROM orders", conn)

# Unir órdenes con clientes
orders_with_customers = orders.merge(customers, on='customer_id')

# Funciones de análisis
def analisis_montos(df):
    total_por_cliente = df.groupby('nombre')['monto'].sum()
    total_por_ciudad = df.groupby('ciudad')['monto'].sum()
    return total_por_cliente, total_por_ciudad

def estadisticas_basicas(df):
    return df['monto'].mean(), df['monto'].std()

def intervalo_confianza(df):
    media = df['monto'].mean()
    return stats.t.interval(
        confidence=0.90,
        df=len(df['monto']) - 1,
        loc=media,
        scale=stats.sem(df['monto'])
    )

# Ejecutar análisis
print("\n🔹 Análisis por cliente y ciudad:")
cliente_total, ciudad_total = analisis_montos(orders_with_customers)
print("Top 5 clientes con mayor monto total:")
print(cliente_total.sort_values(ascending=False).head())
print("\nTop 5 ciudades con mayor monto total:")
print(ciudad_total.sort_values(ascending=False).head())

print("\n🔹 Estadísticas básicas:")
media, desviacion = estadisticas_basicas(orders)
print(f"Media del monto: {media:.2f}")
print(f"Desviación estándar del monto: {desviacion:.2f}")

print("\n🔹 Intervalo de confianza del 90%:")
confianza = intervalo_confianza(orders)
print(f"Intervalo: ({confianza[0]:.2f}, {confianza[1]:.2f})")
