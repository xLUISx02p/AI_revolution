#Importacion de librerias
import tkinter as tk
import random

#########################
#Constantes
#########################

PATH_MAPA= "mapa.txt"
PATH_MISILES="misiles.txt"

#########################
#Variables globales
#########################

mapa=[]
misiles=[]
terrenos=[]
botones=[]
entrada=""

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
def buscar_misiles(clave):
    global misiles
    misiles_disponibles=[]
    for pais in misiles:
        for misil in pais[3]:
            print(misil[4])
            if misil[4]==clave:
                misiles_disponibles.append([pais[0],misil[0],misil[3]])
    return misiles_disponibles
                    
#------------
#Funciones para entradas
#------------

#Funcion para pedir la entrada
def pedir_entrada():
    global entrada
    entrada= var_entrada.get()
    var_entrada.set("")
    return entrada

#Función para pedir un numero entero
#E: mensaje
#S: El numero introducido
def pedir_entero(mensaje):
    global entrada
    var_mensaje.set(mensaje)
    numero= entrada
    if es_entero(numero):
        return int(numero)
    else:
        var_error.set("Solo se aceptan números enteros positivos.")

#Pedir un punto(latitud y longitud)
def pedir_un_punto():
    label_entrada.pack()
    entrada.pack()
    boton_entrada.pack()
    label_error.pack()
    gradosy=pedir_entero("Introduce los grados de la longitud")
    print(gradosy)


    
    
    

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
     
     
#########################
#Funciones del menu
#########################
               
#IA aleatoria
"""
Aqui se va hacer el menu donde
la IA debe adivinar un codigo y 
lanzar un mizil
"""
def IA_aleatoria():
    ocultar_botones()
    pedir_un_punto()
    
    
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

label_entrada=tk.Label(root,textvariable=var_mensaje,bg="#3CF1E8")
label_error=tk.Label(root,textvariable=var_error,bg="#3CF1E8")

#Botones

boton_IA_auto= tk.Button(root,text="IA Aleatoria",command=IA_aleatoria)
boton_IA_auto.pack()
botones.append(boton_IA_auto)

boton_entrada= tk.Button(root,text="introducir",command=pedir_entrada)

#Entrada
entrada=tk.Entry(root,textvariable=var_entrada)

root.mainloop()