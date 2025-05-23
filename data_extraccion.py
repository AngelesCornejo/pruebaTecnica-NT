import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:angeles47@127.0.0.1/prueba_tecnica")

query = "SELECT * FROM data_prueba_tecnica"
conexion = engine
df = pd.read_sql(query, conexion)
# Exportar a archivo JSON (formato de lista de diccionarios)
df.to_json("data_prueba_tecnica.json", orient="records", indent=4, force_ascii=False)
print("Datos exportados a data_prueba_tecnica.json con pandas correctamente.")
