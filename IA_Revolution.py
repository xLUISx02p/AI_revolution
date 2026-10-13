#Importacion de librerias
import tkinter as tk
import random as rnd

#########################
#Constantes
#########################

PATH_MAPA= "mapa.txt"
PATH_MISILES="misiles.txt"

#########################
#Variables globales
#########################

mapa=[] #Aqui se cargan los puntos del mapa
misiles=[] #Aqui se cargan los misiles
misiles_con_x_clave=[['Costa Rica', 'Balistico', 40,23], ['Panama', 'Ojiva', 23]] #Aqui se guardan los misiles con la clave dada
terrenos=[] #Aqui esta la ubicacion de los terrenos en la lista mapa y sus puntos
vida_paises=[]#Aqui va estar la vida y territorio de los paises[[pais1,terreno_total,terreno_restante,vida,[[provincia1,terreno_total,terreno_restante,vida,[[territorio1,terreno_total,terreno_restante,vida],[territorio1,terreno_total,terreno_restante,vida]],[provincia2...]],[pais2,[...]]
botones=[] #Aqui se guardan los botones del menu
misiles_danho=[] #Estos son los misiles lanzados y el daño ahco a un punto [cantidad de misiles,daño en Km2]
x=[] #Se guarda una longitud
y=[] #Se guuarda una latitud
clave=0 #Aqui se guarda la clave
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
    with open(ruta,"r") as file:
        lista_str=file.read()
        if is_lista(lista_str):
            return eval(lista_str)
        else:
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

def conseguir_territorios():
    global mapa,terrenos
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
                            terrenos.append([territorio[0],num_pais,num_provincia,num_territorio,[[x1,y1],[x2,y2],[[472 +convertir_coordenadas_a_decimales(x1),314 -convertir_coordenadas_a_decimales(y1)],[472 +convertir_coordenadas_a_decimales(x2),314 -convertir_coordenadas_a_decimales(y2)]]]])#Esta lista me guarda el ubicacion del territorio en la lista con sus dos puntos tanto en grados y decimales 
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
    return base * altura
    
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
            terrenos_provincias[i][4].append([terreno])
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
    num_pais=0
    for pais in mapa:
        vida_paises.append([pais[0],0,0,100,[]])
        terrenos_provincias=crear_vida_provincias(pais[1],num_pais)
        for provincia in terrenos_provincias:
            vida_paises[num_pais][1]+= provincia[1]
            vida_paises[num_pais][2]+= provincia[2]
        vida_paises[num_pais][4].append(terrenos_provincias)
        num_pais+=1


"""
Buscar misil, esta funcion con un número que le den
debera buscar cuales misiles comparten esa clave
"""
def buscar_misiles():
    global misiles,clave,misiles_con_x_clave
    misiles_con_x_clave=[]
    for pais in misiles:
        for misil in pais[3]:
            if misil[4]==clave:
                misiles_con_x_clave.append([pais[0],misil[0],misil[3],misil[4]])

#Crear mensaje para los misiles encontrados
def crea_mensaje_misiles():
    global misiles_con_x_clave
    mensaje= f"Paises con misiles con esa clave: "
    for pais in misiles_con_x_clave:
        mensaje+= str(pais[0])+", "+str(pais[1])+", "+str(pais[2])+" | "
    mensaje= mensaje[0:-3] +"."
    return mensaje

"""
Atino el disparo, esta funcion dice si 
el disparo realizado quedo dentro de un 
territorio o no
"""
#S: Retorna la lista del territorio que pego o una lista vacia 
def atino_el_disparo():
    global x,y,terrenos
    print(x,y)
    for territorio in terrenos:
        coordenadas= buscar_coordenadas_terreno(territorio,True)
        print(coordenadas)
        if ((coordenadas[0]<= x <=coordenadas[2])and (coordenadas[3]<= y <=coordenadas[1])) :
            return territorio
    return []

#Actualizar misiles
#E: Un entero que es la cantidad de esos misiles gastados

def actualizar_cantidad_misiles(gastados):
    global misiles_con_x_clave,misiles
    for pais in misiles:
        if pais[0]==misiles_con_x_clave[0][0]:
            for misil in pais[3]:
                if misiles_con_x_clave[0][3]==misil[4]:
                    misil[3]-=gastados
    guardar(PATH_MISILES,misiles)

#------------
#Funciones para entradas
#------------

#Pedir una cantidad de misiles
def pedir_misiles():
    global misiles_con_x_clave,entrada,cuenta
    if misiles_con_x_clave==[]:
        cuenta==9
    else:
        pais=misiles_con_x_clave[0]
        var_mensaje.set(f"Del pais {pais[0]}, de los misiles {pais[1]}\nCuantos desea disparar")
        if not es_entero(entrada):
            if entrada=="":
                pass
            else:
                var_error.set("Error! solo se aceptan números enteros positivos")
        else:
            entrada=int(entrada)
            if entrada>pais[2]:
             var_error.set(f"Error! solo puedes lanzar de 0 a {pais[2]} misiles")
            else:
                cuenta+=0.5
                actualizar_cantidad_misiles(entrada)
                misiles_con_x_clave=misiles_con_x_clave[1:]
                var_error.set("")
                submenu_IA_aleatoria()
        

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

#Indicar las entradas
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
    if cuenta==4 or cuenta==7:
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
        submenu_IA_aleatoria()
    

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
        boton.pack_forget()
        
def mostrar_botones():
    global botones
    for boton in botones:
        boton.pack()
    

#Cargar mapa (graficar los territorios)
def cargar_mapa():
    global terrenos
    for terreno in terrenos:
        coordenadas= buscar_coordenadas_terreno(terreno,True)
        canvas.create_rectangle(coordenadas[0],coordenadas[1],coordenadas[2],coordenadas[3],outline="red")

#Mostrar menu para introducir
def mostrar_introducir():
    campo_entrada.pack()
    boton_menu_principal.pack()
    label_error.pack()
    
def ocultar_introducir():
    campo_entrada.pack_forget()
    boton_menu_principal.pack_forget()
    label_error.pack_forget()
    
#Mostra los misiles con clave
def mostrar_misiles_clave():
    global misiles_con_x_clave
    buscar_misiles()
    label_mensaje.pack()
    if len(misiles_con_x_clave)==0:
        var_mensaje.set(f"La clave es {clave}\nNo se encontranron misiles con la clave {clave}")
    else:
        var_mensaje.set(f"La clave es {clave}\n{crea_mensaje_misiles()}")
     
#Mostrar disparo en en el mapa
def mostrar_disparo():
    global x,y
    x= 472 + convertir_coordenadas_a_decimales(x) #Aqui de una vez se pasan los valores a decimales
    y= 314 - convertir_coordenadas_a_decimales(y)
    canvas.create_oval(x-7,y-7,x+7,y+7,fill="black")
    
#Indicar si el disparo conecto con un territos
def pego_el_disparo():
    territorio= atino_el_disparo()
    if territorio==[]:
        var_mensaje.set("La IA fallo el disparo")
    else:
        pais=mapa[territorio[1]][0]
        provincia= mapa[territorio[1]][1][territorio[2]][0]
        nombre_territorio= territorio[0]
        var_mensaje.set(f"La IA acerto el disparo en {nombre_territorio} de la provincia {provincia} del pais {pais}")


#########################
#Funciones de submenus
#########################
               
#Submenu IA Aleatoria
def submenu_IA_aleatoria():
    global cuenta,misiles_con_x_clave,x,y
    if cuenta==0:
        mostrar_misiles_clave()
        boton_continuar.pack()
        if len(misiles_con_x_clave)==0:
            label_mensaje.pack_forget()
            mostrar_botones()
    elif 1==cuenta:
        mostrar_introducir()
        pedir_misiles()
    elif 1.5==cuenta:
        ocultar_introducir()
        var_entrada.set("")
        var_mensaje.set("Ahora vamos a introducir un punto del mapa")
        cuenta-=0.5
        boton_continuar.pack()
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
        boton_continuar.pack() 
            
        
            
        
    


#########################
#Funciones de menus
#########################

#IA aleatoria
"""
Aqui se va abrir el menu donde
la IA debe adivinar un codigo y 
lanzar un misil
"""
def IA_aleatoria():
    global opicion,punto,cuenta,x,y,entrada,clave
    clave=0
    punto=[]
    x=[]
    y=[]
    cuenta=0
    entrada=""
    opicion=2
    var_entrada.set("")
    var_error.set("")
    ocultar_botones()
    clave=23
    menu_principal()
    
    
def menu_principal():
    global entrada,opicion
    entrada= var_entrada.get()
    if opicion==2:
        submenu_IA_aleatoria()    
    
#Boton de continuar
#Siempre le suma uno a la cuenta y llama
#al menu principal para que se muestre lo 
#que sea
def continuar():
    global cuenta
    cuenta+=1
    boton_continuar.pack_forget()
    menu_principal()
    

    
#########################
#Cargar archivos y otros
#########################    
    
mapa= cargar(PATH_MAPA)
misiles= cargar(PATH_MISILES)
conseguir_territorios()
crear_vida_paises()

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
    
crear_grafica()
canvas.create_text(475,20,text="Mapa mundial",font=("Arial",20))
cargar_mapa()

#Labels

label_mensaje=tk.Label(root,textvariable=var_mensaje,bg="#3CF1E8")
label_error=tk.Label(root,textvariable=var_error,bg="#3CF1E8")

#Botones

boton_IA_auto= tk.Button(root,text="IA Aleatoria",command=IA_aleatoria,)
boton_IA_auto.pack()
botones.append(boton_IA_auto)

boton_continuar=tk.Button(root,text="Continuar",command=continuar)
    
boton_menu_principal= tk.Button(root,text="introducir",command=menu_principal)

#Entrada
campo_entrada=tk.Entry(root,textvariable=var_entrada)

root.mainloop()