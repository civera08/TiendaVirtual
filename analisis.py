# analisis_tienda.py

from conexion import obtener_engine  # Conexión a la base de datos
import pandas as pd
from scipy import stats  # Para estadísticas y el intervalo de confianza

# Paso 1: Obtener la conexión
engine = obtener_engine()

# Paso 2: Leer las tablas desde la base de datos
with engine.connect() as conn:
    customers = pd.read_sql("SELECT * FROM customers", conn)
    orders = pd.read_sql("SELECT * FROM orders", conn)

# Paso 3: Unir ambas tablas usando customer_id
orders_with_customers = orders.merge(customers, on='customer_id')

# Paso 4: Funciones de análisis

def analisis_montos(df):
    total_por_cliente = df.groupby('nombre')['monto'].sum()
    total_por_ciudad = df.groupby('ciudad')['monto'].sum()
    return total_por_cliente, total_por_ciudad

def estadisticas_basicas(df):
    media = df['monto'].mean()
    std = df['monto'].std()
    return media, std

def intervalo_confianza(df):
    media = df['monto'].mean()
    intervalo = stats.t.interval(
        confidence=0.90,
        df=len(df['monto']) - 1,
        loc=media,
        scale=stats.sem(df['monto'])
    )
    return intervalo

# Paso 5: Llamar funciones y mostrar resultados

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
