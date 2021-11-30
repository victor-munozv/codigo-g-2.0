#python process_weather_data.py -cs 320045 -in /mnt/c/Users/56995/Desktop/DOCUMENTOS/especial/climadata/320045/ -out /mnt/c/Users/56995/Desktop/DOCUMENTOS/especial/climadata/320045/ -bv 1 -bph 1 -br 1 -bt 1
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import glob
import pickle
import argparse

parser = argparse.ArgumentParser(description='script para descargar datos de meteochile')
parser.add_argument('-cs', action="store", dest = 'codigo_estacion', default=False, 
                    help = 'Código de la estacion meteorológica')
parser.add_argument('-in', action="store",dest = 'infol', default=False, 
                    help = 'carpeta de donde sacar los archivos')
parser.add_argument('-out',action="store",dest = 'outfol', default=None, 
                    help = 'carpeta donde guardar archivo destino')
parser.add_argument('-bv', action="store",dest='bv',default = False, 
                    help = 'valor booleano (1 o 0) para indicar si se procesan datos de viento')
parser.add_argument('-bph', action="store",dest='bph',default = False, 
                    help = 'valor booleano (1 o 0) para indicar si se procesan datos de presion y humedad')
parser.add_argument('-br', action="store",dest='br',default=False, 
                    help = 'valor booleano (1 o 0) para indicar si se procesan datos de radiacion')
parser.add_argument('-bt', action="store",dest='bt',default=False, 
                    help = 'valor booleano (1 o 0) para indicar si se procesan datos de temperatura')

args = parser.parse_args()

EST_ID = args.codigo_estacion
wat_to_process = [bool(int(args.bv)),bool(int(args.bph)),bool(int(args.br)),bool(int(args.bt))]
print('Procesando datos brutos descargados de meteochile...')
print('De la estacion meteorologica '+str(EST_ID)+'...')
if(wat_to_process[0]):
    print('incluyendo datos del viento...')
if(wat_to_process[1]):
    print('incluyendo datos de presión/humedad...')
if(wat_to_process[2]):
    print('incluyendo datos de radiación...')
if(wat_to_process[3]):
    print('incluyendo datos de temperatura...')


folder_input = args.infol
PATHS=[]
useful_cols = []
filenames = []
PATHZ = [folder_input+"/VIENTO",folder_input+"/PRESSHUM",folder_input+"/RAD",folder_input+"/TEMP"] 
useful_colz = [ ['momento','ddInst','ffInst'],
                ['momento','hr','p0'],
                ['momento','radiacionGlobalInst','radiacionGlobalAcumulada24Horas'],
                ['momento','ts','td']]

EXT = "*.csv"
print('Generando lista de archivos sobre la cual operar...')
print(PATHS)
print(PATHZ)
for ii in range(len(wat_to_process)):
    if wat_to_process[ii]:
        PATHS.append(PATHZ[ii])
        useful_cols.append(useful_colz[ii])
        filenames.append([file
                        for path, subdir, files in os.walk(PATHZ[ii])
                        for file in glob.glob(os.path.join(path, EXT))])
        filenames[ii].sort()
df_list = []
full_pd = pd.DataFrame([])
print('\n Generando dataframe con toda la data indicada... \n')
print(filenames)
for ii in range(len(filenames)):
    for jj in range(len(filenames[ii])):
        print('vamos en archivo'+filenames[ii][jj],end='\r')
        tmp_pd=pd.read_csv(filenames[ii][jj],sep=';')[useful_cols[ii]]
        tmp_pd['momento']=pd.to_datetime(tmp_pd['momento'])
        if jj == 0:
            full_pd=tmp_pd
        else:
            full_pd=full_pd.append(tmp_pd, ignore_index=True)
    df_list.append(full_pd)
del full_pd

for ii in range(len(df_list)):
    print(df_list[ii])
    df_list[ii].set_index('momento',inplace = True)

df2db = df_list[0]
for ii in range(1,len(df_list)):
    df2db = df2db.join(df_list[ii],how='outer')
del df_list

df2dbcolumns = []
for ii in range(len(wat_to_process)):
    if wat_to_process[ii]:
        df2dbcolumns.extend(useful_colz[ii][1:])
        
df2db.columns = df2dbcolumns
print('\n Columnas incluidas: '); print(['momento'],df2dbcolumns)

if args.outfol != None:
    csv_folder = args.outfol
else:
    csv_folser = str(EST_ID)
csv_name = 'proc_clima.csv'
print('Se guardan los datos la carpeta '+str(csv_folder)+' como '+csv_name)
try:
    os.mkdir(csv_folder)
except Exception as e:
    print(e)
    print('probablemente error por que la carpeta ya existe')
df2db.to_csv(csv_folder+csv_name,sep=';')