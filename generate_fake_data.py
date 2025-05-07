import pandas as pd
from sqlalchemy import create_engine, text
from faker import Faker
import random

# Configura tu servidor y base de datos
server = 'NEURABYTE'  # Cambia si usas un nombre de instancia o IP
database = 'TiendaVirtual'  # Reemplaza por tu base de datos

# Cadena de conexión con autenticación de Windows
connection_string = (
    f"mssql+pyodbc://@{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)
engine = create_engine(connection_string)

# Generador de datos falsos
fake = Faker('es_MX')

# Leer el archivo CSV con las ciudades
ciudades_df = pd.read_csv(r'C:\Users\César\Documents\DS_Books\TiendaVirtual\ciudades_mexico.csv')  # Asegúrate de que el archivo esté en el directorio correcto

# Extraer las ciudades (columna 'ciudad_nombre')
ciudades_mexico = ciudades_df['ciudad_nombre'].tolist()

# Conexión activa con la base de datos
with engine.connect() as conn:
    # Obtener el último `customer_id` registrado
    result = conn.execute(text("SELECT COALESCE(MAX(customer_id), 0) FROM customers"))
    max_customer_id = result.scalar()  # Si la tabla está vacía, usa 0 como valor inicial

    # Insertar clientes
    for i in range(1, 1001):
        customer_id = max_customer_id + i
        nombre = fake.name().replace("'", "''")
        
        # Asignar una ciudad aleatoria de la lista
        ciudad = random.choice(ciudades_mexico)

        conn.execute(
            text("INSERT INTO customers (nombre, ciudad) VALUES (:nombre, :ciudad)"),
            {"nombre": nombre, "ciudad": ciudad}
        )

    conn.commit()  # Confirmar la inserción antes de cerrar el bloque

    # Obtener todos los `customer_id` válidos después de insertar clientes
    customer_ids = [row[0] for row in conn.execute(text("SELECT customer_id FROM customers")).fetchall()]

    if not customer_ids:
        print("Error: No hay clientes registrados.")
    else:
        # Obtener el último `order_id` registrado
        result = conn.execute(text("SELECT COALESCE(MAX(order_id), 0) FROM orders"))
        max_order_id = result.scalar()  # Si la tabla está vacía, usa 0 como valor inicial

        # Insertar órdenes
        for j in range(1, 10001):
            customer_id = random.choice(customer_ids)  # Seleccionar un `customer_id` existente
            fecha = fake.date_between(start_date='-4M', end_date='today')
            monto = random.randint(100, 1500)

            conn.execute(
                text("""
                    INSERT INTO orders (customer_id, fecha, monto)
                    VALUES (:customer_id, :fecha, :monto)
                """),
                {
                    "customer_id": customer_id,
                    "fecha": fecha,
                    "monto": monto
                }
            )

        conn.commit()  # Confirmar inserciones de órdenes

print("¡Datos insertados correctamente!")