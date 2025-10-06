import pandas as pd
import numpy as np
import openpyxl

ventas=pd.read_excel("Ventas.xlsx")
clientes=pd.read_excel('Clientes.xlsx')
detalle=pd.read_excel('Detalle_ventas.xlsx')
productos=pd.read_excel('Productos.xlsx')

ventas_detalle=pd.merge(ventas,detalle,on='id_venta')
datos=pd.merge(ventas_detalle,productos,on='id_producto')
datos=pd.merge(datos,clientes,on='id_cliente')

medios,conteo=np.unique(datos['medio_pago'],return_counts=True)
frecuencia_medios=dict(zip(medios,conteo))

print("Frecuencia de métodos de pago")
for medio, total in frecuencia_medios.items():
    print(f"{medio}:{total}")

productos_por_medio =(
    datos.groupby(['medio_pago','id_producto'])['cantidad']
    .sum()
    .reset_index()
)

top_productos=productos_por_medio.sort_values(
    ['medio_pago','cantidad'],ascending=[True,False]
).groupby('medio_pago').head(3)

print('Productos más vendidos por medio de pago')
print(top_productos)

ciudades=(
    datos.groupby(['medio_pago','ciudad'])['id_cliente']
    .nunique()
    .reset_index()
    .rename(columns={'id_cliente':'num_clientes'})
)
top_ciudades=ciudades.sort_values(['medio_pago','num_clientes'],ascending=[True,False]).groupby('medio_pago').head(3)
print('Ciudades con mayor indicencia por medio de pago')
print(top_ciudades)

datos['fecha']=pd.to_datetime(datos['fecha'])
datos['dia_semana']=datos['fecha'].dt.day_name()

dias=(
    datos.groupby(['medio_pago','dia_semana'])['id_venta']
    .nunique()
    .reset_index()
    .rename(columns={'id_venta':'ventas_dia'})
)

print('Ventas por día de la semana y medio de pago')
print(dias)
