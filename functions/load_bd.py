import psycopg2
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

con = psycopg2.connect(
    host=os.getenv("HOST"),
    database=os.getenv("DATABASE"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    port=os.getenv("PORT")
)

df = pd.read_csv(r'C:\Users\lopez\Desktop\proyecto-agente\data\datos_turismo.csv',sep=',', encoding='utf-8', dtype=str)


data = []
#descuento, descuento_valor, descuento_descripcion, url_establecimiento, nombre, facebook, categoria, descripcion, direccion, horario, vigencia, condicion, telefono, correo, web, terminos
for index, row in df.iterrows():
    tupla = (
        row['descuento'],
        row['descuento_valor'],
        row['descuento_descripcion'],
        row['url_establecimiento'],
        row['nombre'],
        row['facebook'],
        row['categoria'],
        row['descripcion'],
        row['direccion'],
        row['horario'],
        row['vigencia'],
        row['condicion'],
        row['telefono'],
        row['correo'],
        row['web'],
        row['terminos']
    )

    data.append(tupla)

cur = con.cursor()
SQL_TRUNCATE = 'TRUNCATE TABLE public.promociones RESTART IDENTITY CASCADE;'

SQL_INSERT = 'INSERT INTO public.promociones(descuento, descuento_valor, descuento_descripcion, url_establecimiento, nombre, facebook, categoria, descripcion, direccion, horario, vigencia, condicion, telefono, correo, web, terminos)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'

print('Insertando datos a la base de datos...')
print('----->',data)


#cur.execute(SQL_TRUNCATE)
cur.executemany(SQL_INSERT, data)   
con.commit()
cur.close()
con.close()
print('Datos insertados correctamente!')