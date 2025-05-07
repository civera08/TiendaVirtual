from conexion import obtener_engine  # Importas la función de conexión a la base de datos
import pandas as pd

# Paso 1: Obtener la conexión
engine = obtener_engine()  # Esto te dará la conexión a la base de datos

# Paso 2: Leer los datos desde la base de datos usando la conexión activa
# Necesitamos usar `with engine.connect()` para asegurar que la conexión se maneje correctamente
with engine.connect() as conn:
    # Leer la tabla 'customers' desde la base de datos
    customers = pd.read_sql("SELECT * FROM customers", conn)

    # Leer la tabla 'orders' desde la base de datos
    orders = pd.read_sql("SELECT * FROM orders", conn)

    # Paso 3: Mostrar las primeras filas de cada tabla
    # `display()` solo funciona en entornos como Jupyter Notebook. Si estás usando otro editor, usa `print()`.
    # En este caso, usaremos print para hacerlo más general
    print("Datos de customers:")
    print(customers.head())  #Muestra las primeras 5 filas de la tabla 'customers'
    print("\n" + "-"*40 + "\n")  #Separador visual para claridad

    print("Datos de orders:")
    print(orders.head())  #Muestra las primeras 5 filas de la tabla 'orders'