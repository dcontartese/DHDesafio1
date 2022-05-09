import numpy as np
import re


####################################################################
## Parametros: dataset - Set de datos a analizar.
##             valor - columna por el cual agrupar.
## Retorna: Lista de diccionarios con clave valor y una serie con las cantidades de null por columna
##
###################################################################
def nulosPorAgrupacion(data, agrupador):
    listaCantidad = []
    for n in data[agrupador].unique():
        mask = data[agrupador] == n
        dataParcial = data[mask]                
        serieNulos = dataParcial.isnull().sum() / dataParcial.shape[0]
        listaCantidad.append([n, serieNulos])
    return listaCantidad

####################################################################
## Parametros: geometry - Punto.
##             geo_data - dataFrame con los poligonos.
##             valor - Nombre de la columna de geo_data a retornar.
## Retorna: Valor de la columna geo_data a la cual pertenece el punto
###################################################################

def obtenerValorPorPunto(geometry, geo_data, valor):
    strValor = ''
    for i in range(geo_data.shape[0]):
        if geo_data.loc[i, 'geometry'].contains(geometry):
            strValor = geo_data.loc[i, valor]
            break
    return strValor

####################################################################
## Parametros: valor - string a analizar.
## Retorna: string con datos concatenados.
###################################################################

def obtenerCaracteristicas(valor):
    valor = valor.lower()
    caracteristica = '|'
    if valor.find('piscina')>-1 or valor.find('pileta')>-1:
        caracteristica = caracteristica  + 'Piscina|'
    
    if valor.find('estrenar')>-1:
        caracteristica = caracteristica + 'Estrenar|'
    
    if valor.find('parrilla')>-1:
        caracteristica = caracteristica + 'Parrilla|'
        
    if valor.find('solarium')>-1:
        caracteristica = caracteristica + 'Solarium|'
        
    if valor.find('garage')>-1 | valor.find('cochera')>-1:
        caracteristica = caracteristica + 'Cochera|'
        
    return caracteristica

####################################################################
## Parametros: valor - string a analizar.
##             regex - regex a analizar
## Retorna: cantidad de ambientes
###################################################################

def ObtieneAmbientes(valor, regex):
    resultado = None
    roomsM = regex.match(valor.lower())
    #del objeto match recupero el grupo  
    if roomsM != None:
        resultado=roomsM.group('rooms')
        #print("resultado", resultado)
#room_match = data_room.apply(lambda x: x if x is None else x.group('rooms'))
    if resultado == "un": 
        resultado=1
    elif resultado == "dos":
        resultado=2
    elif resultado=="tres":
        resultado=3
    elif resultado=="cuatro":
        resultado=4
    elif resultado =="cinco":
        resultado=5
    elif resultado=="seis":
        resultado=6
    else:
        resultado=resultado
        
    return resultado 


####################################################################
## Parametros: valor - string a analizar.
##             regex - regex a analizar
## Retorna: valor de las expensas
###################################################################

def limpia_expensas(valor, regex):
    valor_clean = valor.lower().replace('.',"")
    #print(valor_clean)
    salida=regex.search(valor_clean)
    if salida != None:
        #print('salida antes',salida.group('expensas'))
        salida= salida.group('expensas')
    return salida

####################################################################
## Parametros: valor - string a analizar.
## Retorna: valor de las expensas
###################################################################

def obtenerExpensas(valor):
        
    if valor.find('casi sin expensas')>-1:
        Vexpensas = 8
    elif valor.find('sin expensas')>-1:
        Vexpensas = 0
    else:
        Vexpensas = np.NaN
    return Vexpensas

####################################################################
## Parametros: clave - string a encontrar en la serie.
##             serie - serie en la que quiero encontrar el valor.
## Retorna: valor de las expensas
###################################################################

def obtenerInformacion(clave, serie):        
    if clave in serie.index:
        cantidad = serie[clave]
    else:
        cantidad = np.NaN
    return cantidad

####################################################################
## Parametros: punto - punto del dataset que quiero evaluar
##             datoPoligono - dataframe con los poligonos y el valor a obtener
##             campo - nombre de la columna a obtener.
##             f - dato para la barra de avance.
## Retorna: valor del campo solicitado
###################################################################

def obtenerValorPorCercania(punto, datoPoligono, campo, f):
    ref = 100
    valor = np.NaN
    f.value += 1
    for i in range(datoPoligono.shape[0]):        
        dist = datoPoligono.geometry.iloc[i].distance(punto)        
        if dist < ref:
            ref = dist
            valor = datoPoligono.loc[i, campo]
    return valor

####################################################################
## Parametros: valor - texto a revisar
## Retorna: la cantidad de antigüedad
###################################################################

def ObtieneAntiguedad(valor):
    patron_anti = ".*ANTIGEDAD\s(?P<ant>\d+)\sAOS"
    regex = re.compile (patron_anti)
    resultado = np.NaN
    valor1 = valor.upper()#.replace("Ã‘","N").replace("ÃŒ","U")
    valor1 = re.sub("[^a-zA-Z0-9\s]","",valor1)
    #print("v",valor1 )
    #antiM = regex.match(valor1)
    antiM = re.match(patron_anti, valor1)
    #print(antiM)
    #del objeto match recupero el grupo
    if antiM != None:
        resultado=float(antiM.group('ant'))        
        #print ("r", resultado)
    return resultado

##################################
## Busca edificios Luxury
## Parametros: valor - string a analizar.
## Retorna: SI en caso de verificar la validación
#################################

def obtenerLuxury(valor):
    valor = valor.lower()
    vLuxury = None
    if valor.find('le parc')>-1 or valor.find('leparc')>-1 or valor.find('chateau')>-1:
        vLuxury = 'SI'
    return vLuxury