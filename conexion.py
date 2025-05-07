from sqlalchemy import create_engine

def obtener_engine():
    server = 'NEURABYTE'
    database = 'TiendaVirtual'
    connection_string = (
        f"mssql+pyodbc://@{server}/{database}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )
    return create_engine(connection_string)