import pandas as pd
from conexion import obtener_engine  # Asegúrate de tener tu función de conexión aquí
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Función para obtener los datos desde la base de datos
def obtener_datos():
    # Crear el engine de conexión
    engine = obtener_engine()

    # Consulta SQL para obtener los datos
    sql_query = """
    SELECT c.ciudad, 
           COUNT(*) AS numero_clientes, 
           COALESCE(SUM(o.monto), 0) AS total_compra
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.customer_id
    GROUP BY c.ciudad
    ORDER BY c.ciudad ASC;
    """

    # Obtener los datos en un DataFrame
    df = pd.read_sql(sql_query, engine)

    return df

# Obtener los datos
df = obtener_datos()

# Convertir la columna 'ciudad' en variables binarias utilizando OneHotEncoder
encoder = OneHotEncoder(sparse_output=False, drop='first')  # drop='first' para evitar multicolinealidad
ciudades_encoded = encoder.fit_transform(df[['ciudad']])

# Convertimos el array de codificación a un DataFrame
ciudades_df = pd.DataFrame(ciudades_encoded, columns=encoder.get_feature_names_out(['ciudad']))

# Unimos las columnas de las ciudades codificadas al DataFrame original
df = pd.concat([df, ciudades_df], axis=1).drop(columns=['ciudad'])

# Dividir los datos en conjunto de entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(df.drop(columns=['total_compra']), df['total_compra'], test_size=0.2, random_state=42)

# Crear y entrenar el modelo RandomForestRegressor
modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_rf.fit(X_train, y_train)

# Realizar la predicción y evaluación
y_pred_rf = modelo_rf.predict(X_test)

# Calcular el error absoluto medio y el R²
mae_rf = mean_absolute_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

# Guardar las predicciones en un archivo CSV
df['predicciones'] = modelo_rf.predict(df.drop(columns=['total_compra']))  # Predicciones para todo el conjunto
df.to_csv("predicciones_compras.csv", index=False)

# Imprimir los resultados
print(f"MAE con Random Forest: {mae_rf:.2f}")
print(f"R² con Random Forest: {r2_rf:.2f}")
