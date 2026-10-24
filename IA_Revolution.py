#Importacion de librerias
import tkinter as tk
import random

#########################
#Constantes
#########################

PATH_MAPA= "mapa.txt"
PATH_MISILES="misiles.txt"
PATH_BITACORA="bitacora.txt"

#########################
#Variables globales
#########################

mapa=[] #Aqui se cargan los puntos del mapa
misiles=[] #Aqui se cargan los misiles
bitacora=[] #Aqui se cargan los disparos realizados
misiles_con_x_clave=[] #Aqui se guardan los misiles con la clave dada
terrenos=[] #Aqui esta la ubicacion de los terrenos en la lista mapa y sus puntos
vida_paises=[]#Aqui va estar la vida y territorio de los paises[[pais1,terreno_total,terreno_restante,vida,[[provincia1,terreno_total,terreno_restante,vida,[[territorio1,terreno_total,terreno_restante,vida],[territorio1,terreno_total,terreno_restante,vida]],[provincia2...]],[pais2,[...]]
mapa_cargado=False
disparo_grafica=[] #Aqui se va a guarda el punto del canva para luego borrarlo
misiles_disparados=0
pais_misil=""
tipo_misil=""
botones=[] #Aqui se guardan los botones del menu
misil_danho=0 #Aqui se guarda el danho del misil
x=[] #Se guarda una longitud
y=[] #Se guuarda una latitud
clave=0 #Aqui se guarda la clave
territorio_seleccionado=[] #Aqui se guardan los datos para seleccionar un territorio
territorio_seleccionado2=[] #Aqui se va a guardar una copia de territorio_seleccionado
territorios_aniquilados=[]#Aqui van a ir los territorios con vida 0
mensaje_validar=False #Una validacion para saber si se puso el mensaje
entrada="" #Aqui se guarda lo que ingrese el usuario
cuenta=0 #Esta cuenta es la que maneja los menus
opicion=0 #Esto decide cual boton se apreto


#########################
#Funciones
#########################

#------------
#Commons
#------------

# is_lista
# retorn True si el valor puede ser una lista
#E: Sting
#S: Bool
def is_lista(str_value):
    try:
        eval_value=eval(str_value)
        if type(eval_value)==list:
            return True
        return False
    except:
        return False
    
# Es entero
'''retorna True si el valor se puede convertir a entero, False si no'''
#E: un valor cualquiera
#S: boolean
def es_entero(value):
        try:
                integer = int(value)
                return True
        except:
                return False
            

            
#------------
#Funciones para archivos
#------------

#Guardar un archivo
def guardar(ruta,elemento):
    with open(ruta,"w") as file:
        file.write(str(elemento))

#Cargar un archivo
def cargar(ruta):
    try:
        with open(ruta,"r") as file:
            lista_str=file.read()
            if is_lista(lista_str):
                return eval(lista_str)
            else:
                return []
    except:
        return []

#------------
#Algoritmos
#------------

"""
Convertir cordenadas (grados, minutos y segundos a decimales)
a decimales. la formula es grados + minutos/60 + segundos/3600 pero
en mi mapa cada grado son 2,6 pixels entonces la formula seria
(grados + minutos/60 + segundos/3600)*2.16
"""
#E: una lista con 3 numeros[grados,minutos y segundos] para las coordenadas
#S: las coordenadas en decimal
#R:
def convertir_coordenadas_a_decimales(coordenadas):
    grados= coordenadas[0]
    minutos= coordenadas[1]
    segundos= coordenadas[2]
    coordenada_decimal= (abs(grados) + minutos/60 + segundos/3600)*2.6
    if grados<0:
        return -1*coordenada_decimal
    return coordenada_decimal

"""
Conseguir territorios,
Guarda en la lista terrenos la ubicacion de los territorios en la lista mapa y sus dos puntos
"""

def conseguir_territorios():
    global mapa,terrenos
    terrenos=[]
    num_pais=0
    num_provincia=0
    num_territorio=0
    for pais in mapa:  #Aqui se saca el pais
        num_provincia=0
        for provincia in pais[1]: #aqui se saca la provincia pero primero
            if type(provincia)==str: #Se debe pasar el nombre
                pass
            else:
                for territorios in provincia: #Aqui es lo mismo que con la provincia
                    num_territorio=0
                    if type(territorios)== str:
                        pass
                    else:
                        for territorio in territorios:
                            x1= territorio[1][0][0]
                            y1= territorio[1][0][1]
                            x2= territorio[1][1][0]
                            y2= territorio[1][1][1]
                            
                            x1_decimal= convertir_coordenadas_a_decimales(x1)
                            y1_decimal= convertir_coordenadas_a_decimales(y1)
                            x2_decimal= convertir_coordenadas_a_decimales(x2)
                            y2_decimal= convertir_coordenadas_a_decimales(y2)
                            
                            terrenos.append([territorio[0],num_pais,num_provincia,num_territorio,[[x1,y1],[x2,y2],[[472 +x1_decimal,314 -y1_decimal],[472 +x2_decimal,314 -y2_decimal]]]])#Esta lista me guarda el ubicacion del territorio en la lista con sus dos puntos tanto en grados y decimales 
                            num_territorio+=1
            num_provincia+=1
        num_pais+=1

"""
Buscar coordenadas terreno,
dado un territorio de terrenos esta 
funcion me devuelve las coordenadas ya sea
en grados o decimales. decimale=True para devolver 
decimales y false para grados
"""
#E: Una lista que es un terreno de la lista terrenos y un bool para
# que si es True entonces devuelve decimales y false para grados
#S: una lista con las coordenadas [x1,y1,x2,y2] o [longitud1,latitud1,longitud2,latitud2]
def buscar_coordenadas_terreno(terreno,decimal):
    if decimal:
        return [terreno[4][2][0][0],terreno[4][2][0][1],terreno[4][2][1][0],terreno[4][2][1][1]]
    return [terreno[4][0][0],terreno[4][0][1],terreno[4][1][0],terreno[4][1][1]]

"""
Esta adentro,
Esta funcion dice si un punto esta dentro de un rectangulo
"""
#E: Un x,y como enteros en decimal y un rectangulo que es una lista
#S: Un bool True si esta adentro y false sino
def esta_adentro(x,y,rectangulo):
    x_min,x_max=sorted([rectangulo[0],rectangulo[2]])
    y_min,y_max=sorted([rectangulo[1],rectangulo[3]])
    return x_min<=x<=x_max and y_min<=y<=y_max

"""
Validar terrenos detro de mapa,
de la lista terrenos va a a decir 
si un terreno esta dentro o no de la grafica
"""
#S: una lista con el terreno afuera de la grafia o una lista vacia si todo esta bien
def terreno_dentro_grafica():
    global terrenos
    for terreno in terrenos:
        x1,y1,x2,y2=buscar_coordenadas_terreno(terreno,True)
        area_grafica=[4,80,940,548]
        if not esta_adentro(x1,y1,area_grafica) and not esta_adentro(x2,y2,area_grafica):
            return terreno
    return []

"""
Validar que no se tralapen,
Esta funcion valida que no se traslapen 2 territorios
Si se traslapa devuelve una lista con los 2 terrenos
sino una lista vacia
"""
#E: La lista con todos los terrenos
#S: Una lista con los 2 terrenos que se chocan o una lista vacia
def se_traslapan(terrenos):
    total= len(terrenos)-1
    i=0
    while i<total:
        j=i+1
        x1,y1,x2,y2= buscar_coordenadas_terreno(terrenos[i],True)
        while j <= total:
            rectangulo= buscar_coordenadas_terreno(terrenos[j],True)
            if esta_adentro(x1,y1,rectangulo) and esta_adentro(x2,y2,rectangulo) and esta_adentro(x1,y2,rectangulo) and esta_adentro(x2,y1,rectangulo):
                return [terrenos[i],terrenos[j]]
            j+=1
        i+=1
    return []
    



#-------------------------------------------------------------------------------------

"""
calcular terreno territorio, aqui se va a calcular 
el terreno de un territo dado con su lista
1 grado= 600 km lineales
1 min= 10 km lin
1 seg= 0.167 Km lin
Area= Base * Altura
"""
#E: una lista con la inforamacion del terreno
#S: Area del terreno
def calcular_terreno_territorio(terreno):    
    coordenadas= buscar_coordenadas_terreno(terreno,False)
    longitud1= abs(coordenadas[0][0]*600)+coordenadas[0][1]*10+coordenadas[0][2]*0.167
    latitud1= abs(coordenadas[1][0]*600)+coordenadas[1][1]*10+coordenadas[1][2]*0.167
    longitud2= abs(coordenadas[2][0]*600)+coordenadas[2][1]*10+coordenadas[2][2]*0.167
    latitud2= abs(coordenadas[3][0]*600)+coordenadas[3][1]*10+coordenadas[3][2]*0.167
    if coordenadas[0][0]<0:
        longitud1*=-1
    if coordenadas[1][0]<0:
        latitud1*=-1
    if coordenadas[2][0]<0:
        longitud2*=-1
    if coordenadas[3][0]<0:
        latitud2*=-1

    base= abs(longitud1-longitud2)
    altura= abs(latitud1-latitud2)
    return round(base * altura,2)
    
"""
crear vida territorio, esta funcion va a meter de forma ordenada
toda la informacion respectiva sobre el terreno
del territorio dado
"""
#E: La lista del territorio
#S: Una lis con el terreno y vida del territori
def crear_vida_territorio(territorio):
    area=calcular_terreno_territorio(territorio)
    return [territorio[0],area,area,100]

"""
crear vida provincia, esta funcion va a meter de forma ordenada
toda la informacion respectiva sobre el terreno
de cada provincia por pais
"""
#E: la lista del pais
#S: Una lista con las provicias con su terreno y vida
def crear_vida_provincias(pais,num_pais):
    global terrenos
    i=0
    provincia= pais[0][0]
    terrenos_provincias=[[provincia,0,0,100,[]]]
    for territorio in terrenos:
        if territorio[1]==num_pais:
            if pais[territorio[2]][0]!=provincia:
                i+=1
                provincia=pais[territorio[2]][0]
                terrenos_provincias.append([provincia,0,0,100,[]])
            terreno= crear_vida_territorio(territorio)
            terrenos_provincias[i][4].append(terreno)
            terrenos_provincias[i][1]+=terreno[1]
            terrenos_provincias[i][2]+=terreno[2]
    return terrenos_provincias
                   
    
"""
crear vida paises, esta funcion va a meter de forma ordenada
toda la informacion respectiva sobre el terreno 
de cada pais
"""
def crear_vida_paises():
    global vida_paises,mapa
    vida_paises=[]
    num_pais=0
    for pais in mapa:
        vida_paises.append([pais[0],0,0,100,[]])
        terrenos_provincias=crear_vida_provincias(pais[1],num_pais)
        for provincia in terrenos_provincias:
            vida_paises[num_pais][1]+= provincia[1]
            vida_paises[num_pais][2]+= provincia[2]
        vida_paises[num_pais][4].append(terrenos_provincias)
        num_pais+=1
#---------------------------------------------------------------------------------------

"""
Buscar misil, esta funcion con un número que le den
debera buscar cuales misiles comparten esa clave
"""
def buscar_misiles():
    global misiles,clave,misiles_con_x_clave
    misiles_con_x_clave=[]
    for pais in misiles:
        for misil in pais[3]:
            clave_misli= misil[4]
            if es_entero(clave_misli):
                clave_misli=int(clave_misli)
                if clave_misli==clave:
                    misiles_con_x_clave.append([pais[0],misil[0],misil[3],clave_misli,misil[1]])

#Crear mensaje para los misiles encontrados
def crea_mensaje_misiles():
    global misiles_con_x_clave
    mensaje= f"Paises con misiles con esa clave: "
    for pais in misiles_con_x_clave:
        mensaje+= str(pais[0])+", "+str(pais[1])+", "+str(pais[2])+" | "
    mensaje= mensaje[0:-3] +"."
    return mensaje


#Bajar vida
#Esta funcion baja la vida de los territorios
#E: El territorio golpeado(lista) y el daño(entero)
def bajar_vida(territorio_golpe,danho):
    global vida_paises
    pais=vida_paises[territorio_golpe[1]]
    provincia=pais[4][0][territorio_golpe[2]]
    territorio=provincia[4][territorio_golpe[3]]

    if territorio[2]<danho:
        danho=territorio[2]
        territorio[2]=0
    else:
        territorio[2]-=danho     
    territorio[3]=round(territorio[2]/territorio[1]*100,2)
    if provincia[2]<danho:
        danho=provincia[2]
        provincia[2]=0
    else:
        provincia[2]-=danho
    provincia[3]=round(provincia[2]/provincia[1]*100,2)
    pais[2]-=danho
    if pais[2]<0:
        pais[2]=0
    pais[3]=round(pais[2]/pais[1]*100,2)
    
#---------------------------------------------------------------------------------------

"""
Cargar partida,
Hace que si hay una partida guardada, se cargue y se actualice la vida de los paises
"""
def cargar_partida():
    global bitacora,misiles,vida_paises
    if bitacora==[]:
        return
    for registro in bitacora:
        if registro[5]!=[]:   
            pais_misil=registro[2]
            tipo_misil=registro[3]
            cantidad=registro[1]
            coordenadas_disparo=registro[4]
            x_mapa=472 + convertir_coordenadas_a_decimales(coordenadas_disparo[0])
            y_mapa=314 - convertir_coordenadas_a_decimales(coordenadas_disparo[1])

            danho_por_misil=0
            for pais in misiles:
                if pais[0]==pais_misil:
                    for misil in pais[3]:
                        if misil[0]==tipo_misil:
                            danho_por_misil=misil[1]
                            break

            if danho_por_misil != 0:
                for territorio in terrenos:
                    coordenadas=buscar_coordenadas_terreno(territorio,True)
                    if esta_adentro(x_mapa,y_mapa,coordenadas):
                        bajar_vida(territorio,cantidad*danho_por_misil)
                        break

#---------------------------------------------------------------------------------------
        
"""
Atino el disparo, esta funcion dice si 
el disparo realizado quedo dentro de un 
territorio o no
"""
#S: Retorna la lista del territorio que pego o una lista vacia 
def atino_el_disparo():
    global x,y,terrenos,misil_danho
    x_mapa=472 + convertir_coordenadas_a_decimales(x)
    y_mapa=314 - convertir_coordenadas_a_decimales(y)
    for territorio in terrenos:
        coordenadas= buscar_coordenadas_terreno(territorio,True)
        if esta_adentro(x_mapa,y_mapa,coordenadas):
            bajar_vida(territorio,misil_danho)
            return territorio
    return []

#Actualizar misiles
#E: Un entero que es la cantidad de esos misiles gastados

def actualizar_cantidad_misiles(gastados):
    global misiles_con_x_clave,misiles
    for pais in misiles:
        if pais[0]==misiles_con_x_clave[0][0]:
            for misil in pais[3]:
                if misiles_con_x_clave[0][3]==int(misil[4]):
                    misil[3]-=gastados
                    pais[2]-=gastados
    guardar(PATH_MISILES,misiles)
    
#--------------------------------------------------------------------------
#Obtener la informacion 
#E: Una lista con el territorio
#S: Una lista con el pais, provincia y territorio
def obtener_informacion_acierto(territorio):
    if territorio==[]:
        return []
    pais=mapa[territorio[1]][0]
    provincia=mapa[territorio[1]][1][territorio[2]][0]
    territorio_actual=mapa[territorio[1]][1][territorio[2]][1][territorio[3]][0]
    return [pais,provincia,territorio_actual]

#Actualizar bitacora
#E: Una lista con el territorio
def actualizar_bitacora(territorio):
    global bitacora,opicion,misiles_disparados,pais_misil,tipo_misil,x,y
    if opicion==1:
        modo="Aleatorio"
    elif opicion==2:
        modo="Manual"
    # Registro: modo, cantidad, pais, misil, coordenadas, acierto, informacion del acierto.
    bitacora.append([
            modo,
            misiles_disparados,
            pais_misil,
            tipo_misil,
            [x,y]])
    i=len(bitacora)-1
    if territorio!=[]:
        bitacora[i].append(obtener_informacion_acierto(territorio))
    else:
        bitacora[i].append([])
    guardar(PATH_BITACORA,bitacora)
    
#Buscar territorio
#E: Una lista con la ubicacion del territorio en la lista terrenos
#S: El territorio encontrado(lista)
def buscar_territorio(territorio_escogido):
    global terrenos
    for territorio in terrenos:
        if territorio_escogido[0]==territorio[1] and territorio_escogido[1]==territorio[2] and territorio_escogido[2]==territorio[3]:
            return territorio    
     
#disparos recibidos en territorio
#E: Un territorio lista
#S: La cantidad de disparos recibidos
def disparos_recibidos_en_territorio(territorio):
    global bitacora
    coordenadas=buscar_coordenadas_terreno(territorio,True)
    i=0
    for registro in bitacora:
        coordenadas_disparo=registro[4]
        x=472 + convertir_coordenadas_a_decimales(coordenadas_disparo[0])
        y=314 - convertir_coordenadas_a_decimales(coordenadas_disparo[1])
        if esta_adentro(x,y,coordenadas):
            i+=1
    return i

#Disparos recibidos por provincia de x pais
#E: Un numero que es la ubicacion del pais en la lista vida_paises
#S: Una lista con la cantidad de disparos recibidos por provincia y territorio
def disparos_por_provincia(num_pais):
    pais=vida_paises[num_pais]
    disparos_territorios=[]
    disparos_provincia=[]
    num_provincia=0
    suma_disparos=0
    i=0
    for provincia in pais[4][0]:
        disparos_territorios=[]
        suma_disparos=0
        disparos_provincia.append([provincia[0],0,disparos_territorios])
        for terreno in terrenos:
            if terreno[1]==num_pais and num_provincia== terreno[2]:
                disparos=disparos_recibidos_en_territorio(terreno)
                disparos_territorios.append([terreno[0],disparos])
                suma_disparos+=disparos
        disparos_provincia[i][1]=suma_disparos
        num_provincia+=1
        i+=1
    return disparos_provincia

"""
Mover territorio,
esta funcion mueve un territorio a otro pais y 
provincia o solamente a otra provincia del mismo pais.
"""
#E: Una lista con la informacion del territorio y otra lista con el destino
#S: Un bool True si se pudo mover y False sino

def mover_territorio(territorio,destino):
    global mapa
    if territorio[1]==destino[0] and territorio[2]==destino[1]:
        return False
    provincia=mapa[territorio[1]][1][territorio[2]]
    terreno=provincia[1][territorio[3]]
    mapa[territorio[1]][1][territorio[2]][1].pop(territorio[3])
    mapa[destino[0]][1][destino[1]][1].append(terreno)
    if provincia[1]==[]:
        mapa[territorio[1]][1].pop(territorio[2])
        
    guardar(PATH_MAPA,mapa)
    conseguir_territorios()
    crear_vida_paises()
    cargar_partida()
    return True
 
"""
aniquilar territorios,
Todos los territorios con vida 0 los copia a una lista
donde todos los territorios tienen vida 0
"""
#S: Devuelve una lista con los territorios aniquilados esa ronda 
 
def aniquilar_territorios():
    global vida_paises,territorios_aniquilados
    aniquilados_actual=[]
    for pais in vida_paises:
        for provincia in pais[4][0]:
            for territorio in provincia[4]:
                nombre_territorio= territorio[0]
                if territorio[2]==0 and nombre_territorio not in territorios_aniquilados:
                    territorios_aniquilados.append(nombre_territorio)
                    aniquilados_actual.append(nombre_territorio)
    return aniquilados_actual     

"""
territorios muertos,
Esta funcion va a devolver el % de territorios
muertos
"""
#S: un real positivo que es el % de territorios muertos
def territorios_muertos():
    global territorios_aniquilados,terrenos
    aniquilar_territorios()
    porcentaje_de_muertos= round(len(territorios_aniquilados)/len(terrenos)*100,2)
    return porcentaje_de_muertos
          
    
#------------
#Funciones para entradas
#------------

#Pedir una cantidad de misiles
def pedir_misiles():
    global misiles_con_x_clave,entrada,cuenta,misil_danho,misiles_disparados,pais_misil,tipo_misil
    pais=misiles_con_x_clave[0]
    var_mensaje.set(f"Del pais {pais[0]}, de los misiles {pais[1]}\nCuantos desea disparar")
    if not es_entero(entrada):
        if entrada!="":
            var_error.set("Error! solo se aceptan números enteros positivos")
    else:
        entrada=int(entrada)
        if entrada>pais[2] or entrada<0:
         var_error.set(f"Error! solo puedes lanzar de 0 a {pais[2]} misiles")
        elif entrada==0:
            var_mensaje.set(f"No se lanzo ningun misil {pais[1]} de {pais[0]}")
            cuenta=0
            var_entrada.set("")
            boton_continuar.grid()
            ocultar_introducir()
            misiles_con_x_clave=misiles_con_x_clave[1:]
        else:
            cuenta+=0.5
            actualizar_cantidad_misiles(entrada)
            misil_danho=pais[-1]*entrada
            misiles_disparados=entrada
            pais_misil=pais[0]
            tipo_misil=pais[1]
            var_error.set("")
            misiles_con_x_clave=misiles_con_x_clave[1:]
            submenu_IA()
           
#-------------------------------------------------------------------
#Pedir un grado
#E: Pide el rango
#S: True si se introduce correctamente y False sino
def pedir_grados(rango):
    global entrada
    if es_entero(entrada):
        entrada=int(entrada)
        if abs(entrada)>rango:
            var_error.set(f"Solo se permiten grados de -{rango} a {rango}")
            return False
        var_error.set("")
        var_entrada.set("")
        return True
    if entrada!="":
        var_error.set("Error! eso no es un grado valido")
    return False

#Pedir minuto o segundo
#E: Pide el rango por si es latitud o lungitud,
#S: True si se introduce correctamente y False sino
def pedir_min_o_sec(rango):
    global entrada
    if es_entero(entrada):
        entrada=int(entrada) #Aqui convierto la entrada a entero
        if 0>entrada or entrada>rango:
            var_error.set(f"Solo se permiten numeros de 0 a {rango}")
            return False
        var_error.set("")
        var_entrada.set("")
        return True
    if entrada!="":
        var_error.set("Error! eso no es valido")
    return False

#Pedir un punto    
def pedir_un_punto():
    global cuenta
    if cuenta<4:
        rango=[180]
    else:
        rango=[90]
    rango+=[60,3600]
    if cuenta==2 or cuenta==5:
        return pedir_grados(rango[0])
    elif 3<=cuenta<=4 or 6<=cuenta<=7:
        return pedir_min_o_sec(rango[1])

#Indicar las entradas para un punto
#Estos van a ser los los mensajes del label 
def indicar_entradas_punto():
    global cuenta
    palabra="latitud"
    palabra2="minutos"
    if cuenta<5:
        palabra="longitud"
    if cuenta==2 or cuenta==5:
        var_mensaje.set(f"Introduce los grados para la {palabra}")
        return #esto es para que no sigua
    elif cuenta==4 or cuenta==7:
        palabra2= "segundos"
    var_mensaje.set(f"Introduce los {palabra2} para la {palabra}")

#armar coordenadas         
def armar_punto():   
    global punto,cuenta,x,y,entrada
    if pedir_un_punto() and cuenta<5:
        x.append(entrada)
        cuenta+=1
    elif pedir_un_punto() and cuenta<8:
        y.append(entrada)
        cuenta+=1
    indicar_entradas_punto()
    if cuenta==8:
        submenu_IA()
#-------------------------------------------------------------------   
#Pedir una clave
def pedir_clave():
    global cuenta,clave,entrada
    label_mensaje.grid(row=0,column=0,padx=10,pady=10)
    if es_entero(entrada):
        entrada=int(entrada)
        if 0>entrada or entrada>99:
            var_error.set("Solo se permiten numeros de 0 a 99")
        else:
            var_error.set("")
            var_entrada.set("")
            clave=entrada
            cuenta+=1.5
            ocultar_introducir()
            submenu_IA()
    elif entrada!="":
        var_error.set("Error! eso no es valido")
        
#----------------------------------------------------------------

#Pedir pais, provincia o territorio
#E: tipo es un string que indica si es pais, provincia o territorio lo que se pide y elementos es la lista de los elementos
def pedir_pais_provincia_territorio(tipo,elementos):
    global territorio_seleccionado,entrada,cuenta,mensaje_validar
    if not mensaje_validar:
        preposicion="de la" 
        if tipo!="provincia" :
            preposicion="del"
        mensaje=f"Introduce el número {preposicion} {tipo} para seleccionarlo:\n"
        i=1
        for elemento in elementos:
            mensaje+=F"{i}. {elemento[0]}\n"
            i+=1
        mensaje=mensaje[:-1]
        var_mensaje.set(mensaje)
        label_mensaje.grid()
        mostrar_introducir()
        mensaje_validar=True
    if es_entero(entrada):
        entrada=int(entrada)
        if 1 <= entrada <= len(elementos):
            territorio_seleccionado.append(entrada-1)
            ocultar_introducir()
            mensaje_validar=False
            cuenta+=1
            var_error.set("")
            var_entrada.set("")
            menu_principal()
        else:
            var_error.set(f"Solo se pueden números desde 1 asta {len(elementos)}")
    elif entrada!="":
        var_error.set("Error! eso no es valido")
        
"""
Escoger pais, provincia o territorio
Si el caso de que solo haya un pais, provincia o territorio y no se pueda escoger lo pone automaticamente sino va a pedir el dato como se debe
"""
def escoger_pais_provincia_territorio(tipo,elementos):
    global territorio_seleccionado,cuenta
    if len(elementos)==1:
        territorio_seleccionado.append(0)
        preposicion="un"
        if tipo=="provincia":
            preposicion="una"
        var_mensaje.set(f"Solo hay {preposicion} {tipo} por lo que se selecciono automaticamente {elementos[0][0]}")
        cuenta+=0.5
        boton_continuar.grid()
        menu_principal()
    else :
        pedir_pais_provincia_territorio(tipo,elementos)

    

#------------
#Funciones para la interfaz grafica
#------------

#Escribir los grados verticales
def escribir_grados_verticales():
    y=68
    x=32
    cuenta= 170
    canvas.create_text(10,y,text="180",font=("Arial",10)) #Esto es para que no se corte el 180
    while x<=950:
        canvas.create_text(x,y,text=str(abs(cuenta)),font=("Arial",10))
        x+=26
        cuenta-=10
        
#Escribir los grados horizontales
def escribir_grados_horizontales():
    y=80
    x=960
    cuenta= 90
    while y<530:
        if cuenta<0:
            canvas.create_text(x,y,text=f"{str(abs(cuenta))} S",font=("Arial",10))
        elif cuenta==0:
            canvas.create_text(x,y,text=str(cuenta),font=("Arial",10))
        else:
            canvas.create_text(x,y,text=f"{str(cuenta)} N",font=("Arial",10))
        y+=26
        cuenta-=10
    canvas.create_text(x,545,text=f"{str(abs(cuenta))} S",font=("Arial",10)) #Esto es para que no se corte el ultimo 90
    canvas.create_text(162,40,text="Longitud Oeste",font=("Arial",15))
    canvas.create_text(788,40,text="Longitud Este",font=("Arial",15))


#Hacer lineas verticales de la grafica
def crea_lineas_verticales():
    intervaloX=4
    intervaloY=80
    linea=0
    pintar=True
    while linea<37:
        intervaloY=80
        pintar=True
        while intervaloY<550:
            if pintar:
                canvas.create_line(intervaloX,intervaloY,intervaloX,intervaloY+3,fill="black")
                pintar=False
            else:
                pintar=True
            intervaloY+=4
        intervaloX+=26
        linea+=1

#Hacer lineas horizontales de la grafica
def crear_lineas_horizontales():
    intervaloX=4
    intervaloY=80
    linea=0
    pintar=True
    while linea<19:
        intervaloX=4
        pintar=True
        while intervaloX<940:
            if pintar:
                canvas.create_line(intervaloX,intervaloY,intervaloX+3,intervaloY,fill="black")
                pintar=False
            else:
                pintar=True
            intervaloX+=4
        intervaloY+=26
        linea+=1

#Crear la grafica
def crear_grafica():
    crea_lineas_verticales()
    crear_lineas_horizontales()
    escribir_grados_verticales()
    escribir_grados_horizontales()
    
#Ocultar botones
def ocultar_botones():
    global botones
    for boton in botones:
        boton.grid_forget()
        
def mostrar_botones():
    global botones
    num_boton=0
    arriba=True
    for boton in botones:
        if arriba:
            boton.grid(row=1,column=num_boton,padx=20,pady=20)
            arriba=False
        else:
            boton.grid(row=2,column=num_boton,padx=9,pady=20)
            num_boton+=1
            arriba=True
    

#Cargar mapa (graficar los territorios)
def cargar_mapa():
    global terrenos
    for terreno in terrenos:
        coordenadas= buscar_coordenadas_terreno(terreno,True)
        canvas.create_rectangle(coordenadas[0],coordenadas[1],coordenadas[2],coordenadas[3],outline="red")

#Mostrar menu para introducir
def mostrar_introducir():
    campo_entrada.grid(row=1,column=0,padx=10,pady=10)
    boton_menu_principal.grid(row=2,column=0,padx=10,pady=10)
    label_error.grid(row=3,column=0,padx=10,pady=10)
    
def ocultar_introducir():
    campo_entrada.grid_forget()
    boton_menu_principal.grid_forget()
    label_error.grid_forget()
    
#Mostra los misiles con clave
def mostrar_misiles_clave():
    global misiles_con_x_clave
    buscar_misiles()
    label_mensaje.grid(row=0,column=0,padx=10,pady=10)
    if misiles_con_x_clave==[]:
        var_mensaje.set(f"La clave es {clave}\nNo se encontranron misiles con la clave {clave}")
    else:
        var_mensaje.set(f"La clave es {clave}\n{crea_mensaje_misiles()}")
     
#Mostrar disparo en en el mapa
def mostrar_disparo():
    global x,y,disparo_grafica
    x_mapa= 472 + convertir_coordenadas_a_decimales(x)
    y_mapa= 314 - convertir_coordenadas_a_decimales(y)
    tiro=canvas.create_oval(x_mapa-7,y_mapa-7,x_mapa+7,y_mapa+7,fill="Black")
    disparo_grafica.append(tiro)
    
#Borrar disparo en el mapa    
def borrar_disparo():
    global disparo_grafica
    if disparo_grafica!=[]:
        canvas.delete(disparo_grafica[0])
        disparo_grafica=[]
    
    
#Indicar si el disparo conecto con un territos
def pego_el_disparo():
    global misil_danho
    territorio= atino_el_disparo()
    if territorio==[]:
        var_mensaje.set("La IA fallo el disparo")
    else:
        pais=mapa[territorio[1]][0]
        provincia= mapa[territorio[1]][1][territorio[2]][0]
        nombre_territorio= territorio[0]
        porcentaje_vida= vida_paises[territorio[1]][4][0][territorio[2]][4][territorio[3]][3]
        var_mensaje.set(f"La IA acerto el disparo en {nombre_territorio} de la provincia {provincia} del pais {pais}\nHizo un daño total de {misil_danho} en Km cuadrados y al territorio le queda un {porcentaje_vida}% de vida")
    actualizar_bitacora(territorio)
    
#mostrar mensaje
def mostrar_mensaje(mensaje):  
    var_mensaje.set(mensaje)
    label_mensaje.config(font=("consolas",12),justify="left")
    label_mensaje.grid()  
    
#Mostrar botones y ocultar mensaje
def mostrar_botones_ocultar_mensaje():
    label_mensaje.grid_forget()
    label_mensaje.config(font=("Arial",10),justify="center")
    frame_labels_botones.pack_forget()
    canvas.pack()
    frame_labels_botones.pack()
    mostrar_botones()  
    
def cambiar_tamanho_introducir(tamanho):
    fuente=("Arial",tamanho)
    campo_entrada.configure(font=fuente)
    boton_menu_principal.configure(font=fuente)
    label_error.configure(font=fuente)

"""
Mostrar Territorios,
Esta funcion muestra el pais % de vida Km2 y Km2 muertos
luego va con las provincias y por ultimo los territorios
"""
def mostrar_territorios():
    global vida_paises
    mensaje=""
    for pais in vida_paises:
        mensaje+= F"{pais[0]:<20} \t{pais[3]:<5} % de vida\t\t{pais[1]:<15} Km2\t{pais[1]-pais[2]:<15} Km2 muertos\n"
        for provincia in pais[4][0]:
            mensaje+= F"\t{provincia[0]:<20} \t{provincia[3]:<5} % de vida\t\t{provincia[1]:<13} Km2\t{provincia[1]-provincia[2]:<13} Km2 muertos\n"
            for territorio in provincia[4]:
                mensaje+= F"\t\t{territorio[0]:<20} \t{territorio[3]:<5} % de vida\t\t{territorio[1]:<13} Km2\t{territorio[1]-territorio[2]:<13} Km2 muertos\n"
        mensaje+="\n"
    mensaje=mensaje[:-2]
    mostrar_mensaje(mensaje)
    
    
"""
Mostrar ranking de paises por extension,
Esta funcion muestra el ranking de paises por extension de mayor a menor
"""
def mostrar_ranking_pais_extension():
    global vida_paises

    # Ordena los países de mayor a menor según su extensión total
    ranking = sorted(vida_paises, key=lambda pais: pais[1], reverse=True)

    mensaje = "Ranking de países por extensión:\n"
    i=1
    for pais in ranking:
        mensaje += f"{i}. {pais[0]:<20}  {pais[1]:>15} Km2\n"
        i+=1
        
    mostrar_mensaje(mensaje)
    
"""
Mostrar ranking de paises por extension viva,
Esta funcion muestra el ranking de paises por extension de mayor a menor viva
"""
def mostrar_ranking_pais_extension_viva():
    global vida_paises

    # Ordena los países de mayor a menor según su extensión total
    ranking = sorted(vida_paises, key=lambda pais: pais[2], reverse=True)

    mensaje = "Ranking de países por extensión viva:\n"
    i=1
    for pais in ranking:
        mensaje += f"{i}. {pais[0]:<20}  {pais[2]:>15} Km2 vivos\n"
        i+=1
        
    mostrar_mensaje(mensaje)
    
#Mostrar pais seleccionado
def mostrar_pais_seleccionado():
    global mapa,territorio_seleccionado
    var_mensaje.set(f"Se selecciono correctamente el pais {mapa[territorio_seleccionado[0]][0]}")
    
#Mostrar provincia seleccionada
def mostrar_provincia_seleccionado():
    global mapa,territorio_seleccionado
    var_mensaje.set(f"Se selecciono correctamente la provincia {mapa[territorio_seleccionado[0]][1][territorio_seleccionado[1]][0]}")
    
def mostrar_status_territorio():
    global  territorio_seleccionado,vida_paises
    disparos_recibidos=disparos_recibidos_en_territorio(territorio_seleccionado)
    porcentaje_vida= vida_paises[territorio_seleccionado[1]][4][0][territorio_seleccionado[2]][4][territorio_seleccionado[3]][3]
    extension= vida_paises[territorio_seleccionado[1]][4][0][territorio_seleccionado[2]][4][territorio_seleccionado[3]][1]
    var_mensaje.set(f"El territorio {territorio_seleccionado[0]} de la provincia {mapa[territorio_seleccionado[1]][1][territorio_seleccionado[2]][0]} del pais {mapa[territorio_seleccionado[1]][0]} tiene un {porcentaje_vida}% de vida, una extension de {extension} Km2 y ha recibido {disparos_recibidos} disparos")
 
 
    
#Mostrar consult historica del pais
def mostrar_consulta_historica_pais():
    global territorio_seleccionado,vida_paises,terrenos
    num_pais=territorio_seleccionado[0]
    pais=vida_paises[num_pais]
    mensaje=f"{pais[0]:<20} \t{pais[1]:<15} Km2\t{pais[3]:<5} % de vida\n" 
    disparos_provincia= disparos_por_provincia(num_pais)
    for provincia in disparos_provincia:
        mensaje+=f"\t{provincia[0]:<20} {provincia[1]} disparos recibidos\n"
        for territorio in provincia[2]:
            mensaje+=f"\t\t{territorio[0]:<20} {territorio[1]} disparos recibidos\n"
    mostrar_mensaje(mensaje[:-1])
    
# Indicar los territorios aniquilados
def indicar_territorios_aniquilados():
    territorios= aniquilar_territorios()
    if territorios==[]:
        var_mensaje.set("No se aniquiló ningun territorio")
    else:
        mensaje= f"Se aniquiló a {territorios[0]}"
        num_territorios= len(territorios)
        if num_territorios>1:
            if num_territorios>2:
                i=1
                while i<num_territorios-1:
                    mensaje+= f", {territorios[i]} "
                    i+=1
            mensaje+= f" y {territorios[-1]}"
        var_mensaje.set(mensaje)
 
#Mostrar quien fue el ganador        
def mostrar_ganador():
    porcentaje_muertos= territorios_muertos()
    if porcentaje_muertos>50:
        var_mensaje.set(f"La IA ganó aniquilando al {porcentaje_muertos}% de los territorios")
    else:
        var_mensaje.set(f"La humanidad gano ya que solo se murio el {porcentaje_muertos}% de los territorios")
        
        
    

#########################
#Funciones de submenus
#########################

# submenu_cargar_mapa():
def submenu_cargar_mapa():
    global mapa_cargado,cuenta,terrenos,opicion
    if mapa_cargado and cuenta==0:
        var_mensaje.set("El mapa ya esta cargado")
        boton_continuar.grid()
    elif cuenta==0:
        mensaje="No se puede cargar el mapa"
        terreno= terreno_dentro_grafica()
        terrenos_traslapados= se_traslapan(terrenos)
        if terreno!=[]:
            var_mensaje.set(f"El territorio {terreno[0]} esta afuera de la grafica\n{mensaje}")
        elif terrenos_traslapados!=[]:
            var_mensaje.set(f"Los territorios {terrenos_traslapados[0][0]} y {terrenos_traslapados[1][0]} estan traslapados\n{mensaje}")
        else:
            cargar_mapa()
            var_mensaje.set("El mapa se cargo correctamente")
            mapa_cargado=True
        boton_continuar.grid()
    if cuenta==1:
        label_mensaje.grid_forget()
        mostrar_botones()
        
# submenu mapa no cargado
def submenu_mapa_no_cargado():
    global cuenta,opicion
    if opicion==2:
        opicion=1
        cuenta=0
    if cuenta==0:
        mostrar_botones_ocultar_mensaje()
        ocultar_botones()
        label_mensaje.grid()
        var_mensaje.set("El mapa aun no esta cargado")
        boton_continuar.grid()
    if cuenta ==1:
        label_mensaje.grid_forget()
        mostrar_botones()     
        cambiar_tamanho_introducir(10)          
#Submenu IA 
def submenu_IA():
    global cuenta,misiles_con_x_clave,x,y,entrada
    entrada= var_entrada.get()
    if cuenta==-1.5:
        mostrar_introducir()
        var_mensaje.set("Introduce la clave de los misiles que desea disparar")
        pedir_clave()
    elif cuenta==0:
        mostrar_misiles_clave()
        if misiles_con_x_clave==[]:
            cuenta=9
        boton_continuar.grid()  
    elif 1==cuenta:
        borrar_disparo()
        if misiles_con_x_clave==[]:
            cuenta=0
            label_mensaje.grid_forget()
            ocultar_introducir()
            mostrar_botones()
        elif misiles_con_x_clave[0][2]==0:
            cuenta=0
            var_mensaje.set(f"El pais {misiles_con_x_clave[0][0]} ya no tiene mas misiles {misiles_con_x_clave[0][1]}")
            ocultar_introducir()
            boton_continuar.grid()
            misiles_con_x_clave=misiles_con_x_clave[1:]
        else:
            mostrar_introducir()
            pedir_misiles()
        
    elif 1.5==cuenta:
        ocultar_introducir()
        var_entrada.set("")
        var_mensaje.set("Ahora vamos a introducir un punto del mapa")
        cuenta-=0.5
        boton_continuar.grid()
    elif 2<=cuenta<=7:
        mostrar_introducir()
        armar_punto()
    elif cuenta==8:
        ocultar_introducir()
        mostrar_disparo()
        pego_el_disparo()
        x=[]
        y=[]
        cuenta=0  
        boton_continuar.grid() 
    elif cuenta==10:
        cuenta=0
        label_mensaje.grid_forget()
        mostrar_botones()  
        
#submenu mostrar territorios   
def submenu_mostrar_territorios():
    global cuenta
    if cuenta==0:
        mostrar_territorios()
        boton_continuar.grid()
        canvas.pack_forget()
    elif cuenta==1:
        cuenta=0
        frame_labels_botones.pack_configure(expand=False)
        mostrar_botones_ocultar_mensaje() 
         
        
#Sub menu mostrar ranking pais extension  
def submenu_mostrar_ranking_pais_extension():
    global cuenta
    if cuenta==0:
        mostrar_ranking_pais_extension()
        boton_continuar.grid()
        canvas.pack_forget()
    elif cuenta==1:
        cuenta=0
        mostrar_botones_ocultar_mensaje()
        frame_labels_botones.pack_configure(expand=False)
        
def submenu_mostrar_ranking_pais_extension_viva():
    global cuenta
    if cuenta==0:
        mostrar_ranking_pais_extension_viva()
        boton_continuar.grid()
        canvas.pack_forget()
    elif cuenta==1:
        cuenta=0
        mostrar_botones_ocultar_mensaje()
        frame_labels_botones.pack_configure(expand=False)

def submenu_status_territorio():
    global cuenta,entrada,territorio_seleccionado,mapa
    entrada= var_entrada.get()
    if cuenta==0:
        canvas.pack_forget()
        escoger_pais_provincia_territorio("país",mapa)
    elif cuenta==0.5:
        cuenta+=0.5
    elif cuenta==1:
        boton_continuar.grid()
        boton_continuar.configure(font=("Arial",15))
        mostrar_pais_seleccionado()
    elif cuenta==1.5:
        cuenta+=0.5
    elif cuenta==2:
        escoger_pais_provincia_territorio("provincia",mapa[territorio_seleccionado[0]][1])
    elif cuenta==2.5:
        cuenta+=0.5
    elif cuenta==3:
        boton_continuar.grid()
        boton_continuar.configure(font=("Arial",15))
        mostrar_provincia_seleccionado()
    elif cuenta==4:
        provincia=mapa[territorio_seleccionado[0]][1][territorio_seleccionado[1]]
        escoger_pais_provincia_territorio("territorio",provincia[1])
    elif cuenta==4.5:
        cuenta-=0.5
    elif cuenta==5:
        boton_continuar.grid()
        boton_continuar.configure(font=("Arial",15))
        territorio_seleccionado=buscar_territorio(territorio_seleccionado)
        mostrar_status_territorio()
    elif cuenta==6:
        cambiar_tamanho_introducir(10)
        boton_continuar.configure(font=("Arial",10))
        frame_labels_botones.pack_configure(expand=False)
        mostrar_botones_ocultar_mensaje()

def submenu_consultar_historico_pais():
    global cuenta,entrada
    if cuenta==0:
        canvas.pack_forget()
        entrada= var_entrada.get()
        escoger_pais_provincia_territorio("país",mapa)
    elif cuenta==0.5:
        cuenta+=0.5 
    elif cuenta==1:
        mostrar_consulta_historica_pais()
        boton_continuar.grid()
    elif cuenta==2:
        frame_labels_botones.pack_configure(expand=False)
        cambiar_tamanho_introducir(10)
        mostrar_botones_ocultar_mensaje()
        
def submenu_Mover_territorio_a_otro_pais():
    global cuenta,entrada,territorio_seleccionado,mapa,territorio_seleccionado2
    entrada= var_entrada.get()
    if cuenta==0:
        canvas.pack_forget()
        escoger_pais_provincia_territorio("país",mapa)
    elif cuenta==0.5:
        cuenta+=0.5
    elif cuenta==1:
        boton_continuar.grid()
        boton_continuar.configure(font=("Arial",15))
        mostrar_pais_seleccionado()
    elif cuenta==1.5:
        cuenta+=0.5
    elif cuenta==2:
        escoger_pais_provincia_territorio("provincia",mapa[territorio_seleccionado[0]][1])
    elif cuenta==2.5:
        cuenta+=0.5
    elif cuenta==3:
        boton_continuar.grid()
        boton_continuar.configure(font=("Arial",15))
        mostrar_provincia_seleccionado()
    elif cuenta==4:
        provincia=mapa[territorio_seleccionado[0]][1][territorio_seleccionado[1]]
        escoger_pais_provincia_territorio("territorio",provincia[1])
    elif cuenta==4.5:
        cuenta-=0.5
    elif cuenta==5:
        boton_continuar.grid()
        boton_continuar.configure(font=("Arial",15))
        territorio_seleccionado=buscar_territorio(territorio_seleccionado)
        var_mensaje.set(f"Ahora introduce el pais y provincia de destino")
        territorio_seleccionado2=territorio_seleccionado
        territorio_seleccionado=[]
    elif cuenta==6:
        escoger_pais_provincia_territorio("país",mapa)
    elif cuenta==6.5:
        cuenta+=0.5
    elif cuenta==7:
        boton_continuar.grid()
        boton_continuar.configure(font=("Arial",15))
        mostrar_pais_seleccionado()
    elif cuenta==7.5:
        cuenta+=0.5
    elif cuenta==8:
        escoger_pais_provincia_territorio("provincia",mapa[territorio_seleccionado[0]][1])
    elif cuenta==9 or cuenta==8.5:
        boton_continuar.grid()
        boton_continuar.configure(font=("Arial",15))
        if mover_territorio(territorio_seleccionado2,territorio_seleccionado):
            var_mensaje.set(f"Se movio correctamente el territorio {territorio_seleccionado2[0]} a la provincia {mapa[territorio_seleccionado[0]][1][territorio_seleccionado[1]][0]} del pais {mapa[territorio_seleccionado[0]][0]}")
        else:
            var_mensaje.set(f"No se pudo mover el territorio {territorio_seleccionado2[0]} por que lo quisiste mover a la misma provincia y pais donde estaba")
    elif cuenta==10 or cuenta==9.5:
        cambiar_tamanho_introducir(10)
        boton_continuar.configure(font=("Arial",10))
        frame_labels_botones.pack_configure(expand=False)
        mostrar_botones_ocultar_mensaje()  
        
#Submenu aniquilar Territorios     

def submenu_aniquilar_territorios():
    global cuenta
    if cuenta==0:
        canvas.pack_forget()
        boton_continuar.configure(font=("Arial",15))
        label_mensaje.grid()
        boton_continuar.grid()
        indicar_territorios_aniquilados()
    elif cuenta==1:
        boton_continuar.configure(font=("Arial",10))
        frame_labels_botones.pack_configure(expand=False)
        mostrar_botones_ocultar_mensaje()  
        
#Submenu ganador
def submenu_ganador():
    global cuenta,mapa,misiles,bitacora
    if cuenta==0:
        canvas.pack_forget()
        boton_continuar.configure(font=("Arial",15))
        label_mensaje.grid()
        boton_continuar.grid()
        mostrar_ganador()
    elif cuenta==1:
        var_mensaje.set("Muchas gracias")
        boton_continuar.grid()
    elif cuenta==2:
        guardar(PATH_BITACORA,"")
        root.destroy()    
        

#########################
#Funciones de menus
#########################

def menu_cargar_mapa():
    global opicion,label_mensaje,cuenta
    label_mensaje.grid()
    cuenta=0
    opicion=0
    ocultar_botones()
    menu_principal()

def IA_aleatoria():
    global opicion,punto,cuenta,x,y,entrada,clave
    clave=0
    punto=[]
    x=[]
    y=[]
    cuenta=0
    entrada=""
    opicion=1
    var_entrada.set("")
    var_error.set("")
    ocultar_botones()
    clave= random.randint(1,99)
    menu_principal()
    
def IA_Manual():
    global opicion,punto,cuenta,x,y,entrada,clave
    clave=0
    punto=[]
    x=[]
    y=[]
    cuenta=-1.5
    entrada=""
    opicion=2
    var_entrada.set("")
    var_error.set("")
    ocultar_botones()
    menu_principal()
    
def menu_mostrar_territorios():
    global opicion,cuenta
    cuenta=0
    opicion=3
    ocultar_botones()
    frame_labels_botones.pack_configure(expand=True)
    menu_principal()
    
def menu_mostrar_ranking_pais_extension():
    global opicion,cuenta
    cuenta=0
    opicion=4
    ocultar_botones()
    frame_labels_botones.pack_configure(expand=True)
    menu_principal()
    
def menu_mostrar_ranking_pais_extension_viva():
    global opicion,cuenta
    cuenta=0
    opicion=5
    ocultar_botones()
    frame_labels_botones.pack_configure(expand=True)
    menu_principal()
    
def menu_status_territo():
    global cuenta, opicion, territorio_seleccionado
    cuenta=0
    opicion=6
    territorio_seleccionado=[]
    var_entrada.set("")
    ocultar_botones()
    cambiar_tamanho_introducir(15)
    label_mensaje.configure(font=("Arial",15))
    frame_labels_botones.pack_configure(expand=True)
    menu_principal()
    
def menu_consultar_historico_pais():
    global opicion,cuenta,territorio_seleccionado
    cuenta=0
    opicion=7
    territorio_seleccionado=[] 
    ocultar_botones()
    cambiar_tamanho_introducir(15)
    label_mensaje.configure(font=("Arial",15))
    frame_labels_botones.pack_configure(expand=True)
    menu_principal()
    
def menu_mover_territorio_a_otro_pais():
    global cuenta, opicion, territorio_seleccionado
    cuenta=0
    opicion=8
    territorio_seleccionado=[]
    var_entrada.set("")
    ocultar_botones()
    cambiar_tamanho_introducir(15)
    label_mensaje.configure(font=("Arial",15))
    frame_labels_botones.pack_configure(expand=True)
    menu_principal()
    
def menu_aniquilar_territorios():
    global cuenta, opicion
    cuenta=0
    opicion=9
    var_entrada.set("")
    ocultar_botones()
    label_mensaje.configure(font=("Arial",15))
    frame_labels_botones.pack_configure(expand=True)
    menu_principal()
    
def menu_ganador():
    global cuenta, opicion
    cuenta=0
    opicion=10
    var_entrada.set("")
    ocultar_botones()
    label_mensaje.configure(font=("Arial",15))
    frame_labels_botones.pack_configure(expand=True)
    menu_principal()
    
   
def menu_principal():
    global opicion,mapa_cargado
    if opicion==0:
        submenu_cargar_mapa()
    elif not mapa_cargado:
        submenu_mapa_no_cargado()
    elif opicion==1 or opicion==2:
        submenu_IA()  
    elif opicion==3:
        submenu_mostrar_territorios() 
    elif opicion==4:
        submenu_mostrar_ranking_pais_extension()
    elif opicion==5:
        submenu_mostrar_ranking_pais_extension_viva()
    elif opicion == 6:
        submenu_status_territorio()
    elif opicion==7:
        submenu_consultar_historico_pais()
    elif opicion==8:
        submenu_Mover_territorio_a_otro_pais()
    elif opicion==9:
        submenu_aniquilar_territorios()
    elif opicion==10:
        submenu_ganador()
    
#Boton de continuar
#Siempre le suma uno a la cuenta y llama
#al menu principal para que se muestre lo 
#que sea
def continuar():
    global cuenta
    cuenta+=1
    boton_continuar.grid_forget()
    menu_principal()
    

    
#########################
#Cargar archivos y otros
#########################    
    
mapa= cargar(PATH_MAPA)
misiles= cargar(PATH_MISILES)
bitacora= cargar(PATH_BITACORA)
conseguir_territorios()
crear_vida_paises()
cargar_partida()
aniquilar_territorios()

#########################
#Ventana
#########################

#Se crea la ventana
root= tk.Tk()                
root.title("AI Revolution")
root.config(bg="#3CF1E8")


#Variables Tk

var_entrada= tk.StringVar()
var_mensaje= tk.StringVar()
var_error= tk.StringVar()

#Se crea el canva
canvas= tk.Canvas(root,width=1000,height=550,bg="#77B5FE")
canvas.pack() 

mapa_mundi= tk.PhotoImage(file="mapa22.png")
canvas.create_image(475,305, image=mapa_mundi)
    
canvas.create_text(475,20,text="Mapa mundial",font=("Arial",20))
crear_grafica()
#Frame
frame_labels_botones= tk.Frame(root,width=1000,height=200,bg="#3CF1E8") 
frame_labels_botones.pack() #Esto es para poder poner los botones en abajo del canva

#Labels

label_mensaje=tk.Label(frame_labels_botones,textvariable=var_mensaje,bg="#3CF1E8",font=("arial",10))
label_error=tk.Label(frame_labels_botones,textvariable=var_error,bg="#3CF1E8",font=("arial",10))

#Botones

boton_cargar_mapa=tk.Button(frame_labels_botones,text="Cargar mapa",font=("Arial",10),command=menu_cargar_mapa)

boton_IA_auto= tk.Button(frame_labels_botones,text="IA Aleatoria",command=IA_aleatoria,font=("Arial",10))

boton_IA_manual= tk.Button(frame_labels_botones,text="IA Manual",command=IA_Manual,font=("Arial",10))

boton_lista_de_territorios=tk.Button(frame_labels_botones,text="Lista de territorios",command=menu_mostrar_territorios,font=("Arial",10))

boton_ranking_de_paises_extensión=tk.Button(frame_labels_botones,text="Ranking de países por extensión",command=menu_mostrar_ranking_pais_extension,font=("Arial",10))

boton_ranking_de_paises_vida=tk.Button(frame_labels_botones,text="Ranking de países por porcentaje de vida",command=menu_mostrar_ranking_pais_extension_viva,font=("Arial",10))

boton_status_del_territorio=tk.Button(frame_labels_botones,text="Status del territorio",command=menu_status_territo,font=("Arial",10))

boton_consultar_historico_pais=tk.Button(frame_labels_botones,text="Consultar histórico de país",command=menu_consultar_historico_pais,font=("Arial",10))


boton_mover_territorio_a_otro_pais=tk.Button(frame_labels_botones,text="Mover territorio a otro país",command=menu_mover_territorio_a_otro_pais,font=("Arial",10))

boton_aniquilar_territorios=tk.Button(frame_labels_botones,text="Aniquilar territorios",command=menu_aniquilar_territorios,font=("Arial",10))

boton_ganador=tk.Button(frame_labels_botones,text="Ganador",font=("Arial",10),command=menu_ganador)

boton_salir=tk.Button(frame_labels_botones,text="Salir",font=("Arial",10),command=root.destroy)

botones=[boton_cargar_mapa,boton_IA_auto,boton_IA_manual,boton_lista_de_territorios,boton_ranking_de_paises_extensión,boton_ranking_de_paises_vida,boton_status_del_territorio,boton_consultar_historico_pais,boton_mover_territorio_a_otro_pais,boton_aniquilar_territorios,boton_ganador,boton_salir]
mostrar_botones()

boton_continuar=tk.Button(frame_labels_botones,text="Continuar",command=continuar)
    
boton_menu_principal= tk.Button(frame_labels_botones,text="introducir",command=menu_principal) 
#Entrada
campo_entrada=tk.Entry(frame_labels_botones,textvariable=var_entrada,font=("Arial",10))

root.mainloop()