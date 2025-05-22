import json
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:angeles47@127.0.0.1/prueba_tecnica")

# Abrir y leer el archivo JSON
with open('data_prueba_tecnica.json', 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)

df = pd.DataFrame(datos)

df = df.rename(columns={'name': 'company_name', 'paid_at': 'updated_at', 'status': 'status_'})

#Modificacion de tipo de datos
df['id'] = df['id'].astype(str)
df['company_name'] = df['company_name'].astype(str)
df['company_id'] = df['company_id'].astype(str)
df['amount'] = df['amount'].astype(float)
df['status_'] = df['status_'].astype(str)
df['created_at'] = pd.to_datetime(df['created_at'], format='mixed')
df['updated_at'] = pd.to_datetime(df['updated_at'], format='mixed')

# Validacion y filtro de columnas
df = df[df['amount'] < 1e14] 

id_companies_repited = df.groupby('company_id')['company_name'].value_counts()

print("Id's y nombre de compañias a las que pertenecen, y el número de veces que se repite")
print(id_companies_repited)

#Identificar el id que se asocia a más de una compañia (debería ser unico por compañia)
id_companies = df.groupby('company_id')['company_name'].nunique().reset_index(name='asociated_companies').query('asociated_companies>1')

#Guardar id identificado
company_ids_problem = id_companies['company_id'].tolist()

id_to_name = {}
name_to_id = {}

#Buscar el par (id-compañia) que más se repite para asumir un valor correcto
for company_id in company_ids_problem:
    filtered_df = df[df['company_id'] == company_id]
    #Nombre que más se repite asociado al ID que más se repite
    most_common_name = filtered_df['company_name'].value_counts().idxmax()
    #Diccionarios con los valores de id y nombres que hay que modificar
    id_to_name.update({company_id: most_common_name})
    name_to_id.update({most_common_name: company_id})

df['company_name'] = df['company_id'].map(id_to_name).fillna(df['company_name'])
df['company_id'] = df['company_name'].map(name_to_id).fillna(df['company_id'])

#Se verifica que ahora cada company_id pertenezca a un solo company_name
id_companies_updated = df.groupby('company_id')['company_name'].value_counts()

print("Id's y nombre de compañias a las que pertenecen corregido")
print(id_companies_updated)

#Carga de datos a base de datos
df.to_sql("data_transformed", con=engine, if_exists="replace", index=False)
print("Datos cargados en base de datos correctamente.")