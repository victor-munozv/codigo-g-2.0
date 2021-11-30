#python download_meteochile.py -cs 320019 -init 202001 -end 202002 -bv 1 -bph 1 -br 1 -bt 1
import argparse
import subprocess
import zipfile
from pandas import date_range

parser = argparse.ArgumentParser(description='script para descargar datos de meteochile')
parser.add_argument('-cs', action="store", dest = 'codigo_estacion', default=False, help = 'Código de la estacion meteorológica')
parser.add_argument('-init', action="store", dest = 'inito', default=False, help = 'fecha inicial a descargar (formato YYYYMM)')
parser.add_argument('-end', action="store",dest = 'endo', default=False, help = 'carpeta destino donde guardar los archivos')
parser.add_argument('-bv', action="store",dest='bv',default = False, help = 'valor booleano (1 o 0) para indicar si se descargan datos de viento')
parser.add_argument('-bph', action="store",dest='bph',default = False, help = 'valor booleano (1 o 0) para indicar si se descargan datos de presion y humedad')
parser.add_argument('-br', action="store",dest='br',default=False, help = 'valor booleano (1 o 0) para indicar si se descargan datos de radiacion')
parser.add_argument('-bt', action="store",dest='bt',default=False, help = 'valor booleano (1 o 0) para indicar si se descargan datos de temperatura')

args = parser.parse_args()

codigo_estacion = args.codigo_estacion
inito = args.inito
endo = args.endo

VIENTO_url = ['https://climatologia.meteochile.gob.cl/application/datos/getDatosEma/'+codigo_estacion+'/'+codigo_estacion+'_','_Viento.csv.zip']
PH_url = ['https://climatologia.meteochile.gob.cl/application/datos/getDatosEma/'+codigo_estacion+'/'+codigo_estacion+'_','_PresionHumedad.csv.zip']
RAD_url = ['https://climatologia.meteochile.gob.cl/application/datos/getDatosEma/'+codigo_estacion+'/'+codigo_estacion+'_','_RadiacionGlobal.csv.zip']
T_url = ['https://climatologia.meteochile.gob.cl/application/datos/getDatosEma/'+codigo_estacion+'/'+codigo_estacion+'_','_Temperatura.csv.zip']

fechas=date_range(inito[0:4]+'-'+inito[4:6],endo[0:4]+'-'+endo[4:6],freq='1M')
print(fechas)
relleno = []
for el in fechas:
    relleno.append(str(el.year)+str(el.month).zfill(2))
print(relleno)

carpetanames = ['./climadata/'+str(codigo_estacion),
                './climadata/'+str(codigo_estacion)+'/VIENTO/',
                './climadata/'+str(codigo_estacion)+'/PRESSHUM/',
                './climadata/'+str(codigo_estacion)+'/RAD/',
                './climadata/'+str(codigo_estacion)+'/TEMP/']

for ccnn in carpetanames:
	try:
		print('mkdir '+ccnn)
		subprocess.call(['mkdir',ccnn])
	except Exception as e:
		print(e)

zipnam = ['v.zip','ph.zip','r.zip','t.zip'] 
for rr in relleno:
    if bool(int(args.bv)) == True:
        subprocess.call(['wget',VIENTO_url[0]+rr+VIENTO_url[1],'-O',zipnam[0]])
    if bool(int(args.bph)) == True:
        subprocess.call(['wget',PH_url[0]+rr+PH_url[1],'-O',zipnam[1]])
    if bool(int(args.br)) == True:
        subprocess.call(['wget',RAD_url[0]+rr+RAD_url[1],'-O',zipnam[2]])
    if bool(int(args.bt)) == True:
        subprocess.call(['wget',T_url[0]+rr+T_url[1],'-O',zipnam[3]])
    for zz in range(len(zipnam)):
        try:
            with zipfile.ZipFile(zipnam[zz],"r") as zip_ref:
                zip_ref.extractall(carpetanames[zz+1])
                subprocess.call(['rm',zipnam[zz]])
        except:
            pass
