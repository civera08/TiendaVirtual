from conexion import obtener_engine
import pandas as pd

engine = obtener_engine() #Esto te dará la conexión a la base de datos

#Paso 2: Leer los datos de ambas tablas usando la conexión
with engine.connect() as conn:
    customers = pd.read_sql("SELECT * FROM customers", conn)
    orders = pd.read_sql("SELECT * FROM orders", conn)

#Paso 3: Unir las órdenes con los clientes (merge por 'customer_id')
orders_with_customers = orders.merge(customers, on='customer_id')

#Paso 4: Mostrar los resultados
print(orders_with_customers)