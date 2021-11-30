* Si se está en Windows (10 en adelante proceder como sigue en letra cursiva) *

- * Descargar e Instalar subsistema de Ubuntu para windows (en la microsoft Store) *

![ubun3](./image_readme/download_ubun2.png)

- * Abrir la aplicación ubuntu (ahora comenzará a crear el subsistema de archivos que contendrá a Ubuntu) *

- * Instalar anaconda (python con todo lo que necesitas preinstalado) *
```bash
mkdir tmp
cd /tmp
curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
bash Anaconda3-2019.03-Linux-x86_64.sh
```

- * Copiar el archivo "download_meteochile.py" a la carpeta donde está contenido Ubuntu*

* Usualmente es una ruta como: C:\Users\USUARIO\AppData\Local\Packages\CanonicalGroupLimited.UbuntuonWindows_XXXXXXXXXXXXX\LocalState\rootfs\home (donde XXXXXXXXXXXX puede cambiar para el equipo donde se instale Ubuntu y USUARIO es el nombre de usuario de Windows)*
** Esto debe hacerse con la aplicación de Ubuntu CERRADA **

- Ejecutar la rutina que descarga los datos meteorológicos de meteochile (Dentro de Ubuntu)
```bash
python /ruta/del/programa/download_meteochile.py -cs CCCCCC -init YYYYMM -end YYYYMM -bv 1 -bph 1 -br 1 -bt 1
```
** detalle de los parámetros **
-- ** -cs : Código de la estación meteorológica (ej 300041) **
-- ** -init : fecha inicial de cuando descargar datos en formato YYYYMM (ej: para agosto 2018, usar 201808)
-- ** -end : fecha final hasta donde llegará la descarga de datos en formato YYYYMM, considerar un mes más al que se quiere descargar (ej: para agosto 2019 -> colocar septiembre 2019 y en formato YYYYMM 201909)
-- ** -bv : valor booleano (1 o 0) para indicar si se descargan o no los datos de viento **
-- ** -bph : valor booleano (1 o 0) para indicar si se descargan datos de presion y humedad **
-- ** -br : valor booleano (1 o 0) para indicar si se descargan datos de radiacion ** 
-- ** -bt : valor booleano (1 o 0) para indicar si se descargan datos de temperatura **
* esto descargara los datos brutos de meteochile en la misma carpeta donde se ejecutó este script. *

- Se ejecuta el script "process_weather_data.py":
```
python /ruta/del/programa/process_weather_data.py -cs CCCCCC -in /ruta/carpeta/de/data/bruta/ -out /ruta/carpeta/de/destino/ -bv 1 -bph 1 -br 1 -bt 1
```
** detalle de los parámetros **
-- ** -cs Código de la estacion meteorológica. **
-- ** -in Carpeta de donde sacar los archivos. **
-- ** -out Carpeta donde guardar archivo destino. **
-- ** -bv Valor booleano (1 o 0) para indicar si se procesan datos de viento. **
-- ** -bph Valor booleano (1 o 0) para indicar si se procesan datos de presion y humedad. **
-- ** -br Valor booleano (1 o 0) para indicar si se procesan datos de radiacion. **
-- ** -bt Valor booleano (1 o 0) para indicar si se procesan datos de temperatura. **

- Se descargan los datos del explorador solar [http://ernc.dgf.uchile.cl:48080/fotovoltaico]
- - Se rellena el formulario y se genera la simulación del sistema fotovoltáico
![formulario](./image_readme/formulario_explorador.png)
- - Se descarga la data de la simulación (click en 1 y luego en 2)
![formulario](./image_readme/descarga_shitto.png)

- Se entrena el modelo predictor de potencia ejecutando el script "get_model.py"
```bash
python /ruta/del/programa/get_model.py -tdata ruta/de/data/del/explorador/CCCCCC-PPPPkw/CCCCCC-PPPPkw.csv -tokwhd 0 -split_r 0.85 -n_est 100 -m_loc ruta/de/destino/mdl_pred.pckl -scf_loc ruta/de/destino/scf.pckl -sct_loc ruta/de/destino/sct.pckl
```
** CCCCCC: Codigo de la estacion meteorologica **
** PPPP: potencia instalada de la planta PV** 

-- ** -tdata La ubicación archivo de origen con la data del explorador solar para entrenar
-- ** tokwhd variable binaria para indicar si se pasara el modelo a kilowatthora/dia (1) o no (0)
-- ** split_r (valor numerico flotante en el rango [0.0,1.0] que indica la porcion de la data que se usara para entrenar)
-- ** n_est valor numerico entero que indica la cantidad de estimadores que tendra el modelo regresor RandomForest (ponle 100 nomas)
-- ** m_loc ubicacion donde se guardara el .pckl del modelo (ponerlo con extension .pckl porfavor)
-- ** scf_loc ubicacion donde se guardara el escalador de los features de la data (ponerlo con extension .pckl porfavor)
-- ** sct_loc ubicacion donde se guardara el escalador de los targets de la data (ponerlo con extension .pckl porfavor)

- Ejecuta jupyter notebook
```
jupyter notebook
```

- Abre el archivo plot_pmgd.ipynb

- cambia los valores como se indica:
- - stationcode = 'codigo de est. meteorologica entre comillas simples'
- - pot_instalada = 'potencia instalada entre comillas simples'
- - nombre_key_pmgd = 'nombre de la KEY de la pmgd entre comillas simples (se los posibles nombres en el output del cuadro anterior)'
- - ruta_base_estmm = '/carpeta/de/la/data/meteorologica/'
- - ruta_base_exp = './carpeta/de/data/del/explorador_solar/'