# Copyright (c) 2025 César Rivera
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

from sqlalchemy import create_engine

# Conexión con credenciales de Windows
def obtener_engine():
    server = 'TuServidor'
    database = 'TuDB'
    connection_string = (
        f"mssql+pyodbc://@{server}/{database}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )
# Para autenticación SQL Server (usuario y contraseña)
#connection_string = (
#   f"mssql+pyodbc://{usuario}:{contraseña}@{server}/{database}"
#    "?driver=ODBC+Driver+17+for+SQL+Server"
    
    return create_engine(connection_string)
