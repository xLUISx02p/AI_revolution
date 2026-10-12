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
misiles_con_x_clave=[] #Aqui se guardan los misiles con la clave dada
terrenos=[]
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
def guardar(ruta,destino):
    with open(ruta,"w") as file:
        file.write(str(destino))

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

"""
Buscar misil, esta funcion con un número que le den
debera buscar cuales misiles comparten esa clave
"""
#E: Un numero entero positivo
#S: La lista de [[Pais,tipo,cantidad de misiles con esa clave],...]
#R:
def buscar_misiles():
    global misiles,clave,misiles_con_x_clave
    misiles_con_x_clave=[]
    for pais in misiles:
        for misil in pais[3]:
            if misil[4]==clave:
                misiles_con_x_clave.append([pais[0],misil[0],misil[3]])

#Crear mensaje para los misiles encontrados
def crea_mensaje_misiles():
    global misiles_con_x_clave
    mensaje= f"Paises con misiles con esa clave: "
    for pais in misiles_con_x_clave:
        mensaje+= str(pais[0])+", "+str(pais[1])+", "+str(pais[2])+" | "
    mensaje= mensaje[0:-3] +"."
    return mensaje
     
#------------
#Funciones para entradas
#------------

#Pedir una cantidad de misiles
def pedir_misiles():
    global misiles_con_x_clave,entrada,cuenta
    pais=misiles_con_x_clave[0]
    if misiles_con_x_clave==[]:
        cuenta==9
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
    print(x,y)
    indicar_entradas_punto()
    

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
    global mapa,terrenos,PATH_MAPA
    i=1
    for pais in mapa:  #Aqui se saca el pais
        i=1
        for provincia in pais[i]: #aqui se saca la provincia pero primero
            if type(provincia)==str: #Se debe pasar el nombre
                pass
            else:
                for territorios in provincia: #Aqui es lo mismo que con la provincia
                    if type(territorios)== str:
                        pass
                    else:
                        for territorio in territorios:
                            x1= 472 + convertir_coordenadas_a_decimales(territorio[1][0][0])
                            y1= 314 - convertir_coordenadas_a_decimales(territorio[1][0][1])
                            x2= 472 + convertir_coordenadas_a_decimales(territorio[1][1][0])
                            y2= 314 - convertir_coordenadas_a_decimales(territorio[1][1][1])
                            terrenos.append([canvas.create_rectangle(x1,y1,x2,y2,outline="red"),territorio[0]])
            i+=1  

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
    x1= convertir_coordenadas_a_decimales(x)
    y1= convertir_coordenadas_a_decimales(y)
    canvas.create_oval(x1-10,y1-10,x1+10,y1+10,fill="black")
#########################
#Funciones de submenus
#########################
               
#Submenu IA Aleatoria
def submenu_IA_aleatoria():
    global cuenta,misiles_con_x_clave
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
        mostrar_disparo()
        
        
            
        
    


#########################
#Funciones de menus
#########################

#IA aleatoria
"""
Aqui se va abrir el menu donde
la IA debe adivinar un codigo y 
lanzar un mizil
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
    menu_principal()
    boton_continuar.pack_forget()

    
#########################
#Cargar archivos
#########################    
    
mapa= cargar(PATH_MAPA)
misiles= cargar(PATH_MISILES)

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