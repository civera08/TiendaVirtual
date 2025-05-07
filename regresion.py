import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder

# Cargar tus datos en un DataFrame
df = pd.DataFrame({
    'ciudad': ['Acapulco', 'Aguascalientes', 'Buenavista', 'Cabo San Lucas', 'Campeche', 'Cancún', 'Celaya', 'Chalco', 'Chetumal', 'Chicoloapan', 'Chihuahua', 'Chilpancingo', 'Chimalhuacán', 'Ciudad Acuña', 'Ciudad Apodaca', 'Ciudad Benito Juárez', 'Ciudad del Carmen', 'Ciudad Juárez', 'Ciudad López Mateos', 'Ciudad Madero', 'Ciudad Nicolás Romero', 'Ciudad Obregón', 'Ciudad Victoria', 'Coatzacoalcos', 'Colima', 'Cuautitlán Izcalli', 'Cuautla', 'Cuernavaca', 'Culiacán', 'Durango', 'Ecatepec', 'Ensenada', 'García', 'General Escobedo', 'Gómez Palacio', 'Guadalajara', 'Guadalupe', 'Hermosillo', 'Irapuato', 'Ixtapaluca', 'Jiutepec', 'La Paz', 'León', 'Los Mochis', 'Manzanillo', 'Matamoros', 'Mazatlán', 'Mérida', 'Mexicali', 'Mexico City', 'Minatitlán', 'Miramar', 'Monclova', 'Monterrey', 'Morelia', 'Naucalpan', 'Nezahualcóyotl', 'Nogales', 'Nuevo Laredo', 'Oaxaca', 'Ojo de Agua', 'Pachuca', 'Piedras Negras', 'Playa del Carmen', 'Poza Rica', 'Puebla', 'Puerto Vallarta', 'Querétaro', 'Reynosa', 'Salamanca', 'Saltillo', 'San Cristóbal', 'San Francisco Coacalco', 'San Juan del Río', 'San Luis Potosí', 'San Luis Río Colorado', 'San Nicolás', 'San Pablo de las Salinas', 'Santa Catarina', 'Soledad', 'Tampico', 'Tapachula', 'Tehuacán', 'Tepic', 'Tijuana', 'Tlalnepantla', 'Tlaquepaque', 'Toluca', 'Tonalá', 'Torreón', 'Tuxtla Gutiérrez', 'Uruapan', 'Veracruz', 'Villa de Álvarez', 'Villahermosa', 'Xalapa', 'Xico', 'Zamora', 'Zapopan'], 
    'monto': [108071, 84010, 92868, 92048, 65527, 79102, 105792, 69308, 54159, 130048, 101490, 108145, 82405, 98300, 78678, 74941, 94760, 50083, 60911, 152785, 78548, 75797, 91398, 75226, 131058, 60473, 91442, 60377, 91147, 41757, 44714, 77362, 94251, 90207, 48832, 105115.43, 185615, 71573, 70855, 87490, 28022, 94129, 33204, 36575, 45856, 7611, 83728, 88552, 82575, 61878.19, 69386, 102987, 94106, 101777.22, 81383, 94699, 69361, 73668, 100641, 98001, 76944, 133927, 82240, 68124, 74908, 103513, 45774, 64947, 41979, 85152, 101144, 101643, 48934, 62307, 150585, 65051, 138121, 62733, 62773, 132534, 73475, 40625, 73376, 62853, 92485, 61747, 102780, 101332, 61060, 66659, 68059, 104307, 19103, 72823, 73251, 125887, 72101, 72322, 33541],
    'customers': [130, 101, 121, 121, 87, 105, 126, 89, 70, 157, 132, 132, 104, 124, 96, 92, 117, 61, 76, 191, 97, 95, 119, 85, 161, 83, 118, 80, 119, 47, 60, 89, 126, 127, 63, 121, 231, 90, 88, 107, 38, 118, 38, 47, 58, 12, 102, 111, 101, 72, 85, 131, 115, 137, 106, 114, 85, 102, 125, 118, 100, 169, 117, 87, 89, 131, 56, 88, 48, 109, 123, 131, 70, 75, 181, 80, 169, 80, 73, 165, 96, 53, 90, 71, 117, 74, 120, 119, 80, 88, 88, 130, 25, 93, 88, 154, 101, 90, 38]
  # Aquí pondrías todos tus datos
}
)

# Convertimos la ciudad en variables binarias
encoder = OneHotEncoder(sparse_output=False)
ciudades_encoded = encoder.fit_transform(df[['ciudad']])

# Convertimos el array a un DataFrame
ciudades_df = pd.DataFrame(ciudades_encoded, columns=encoder.get_feature_names_out(['ciudad']))

# Unimos las variables de ciudad al DataFrame original y eliminamos la columna original
df = pd.concat([df, ciudades_df], axis=1).drop(columns=['ciudad'])

# Dividir datos en entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(df.drop(columns=['monto']), df['monto'], test_size=0.2, random_state=42)

# Entrenar modelo Random Forest
modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_rf.fit(X_train, y_train)

# Predicción y evaluación
y_pred_rf = modelo_rf.predict(X_test)

mae_rf = mean_absolute_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

df.to_csv("predicciones_compras.csv", index=False)

print(f"MAE con Random Forest: {mae_rf:.2f}")
print(f"R² con Random Forest: {r2_rf:.2f}")