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

#########################
#Funciones
#########################

#------------
#Commons
#------------

# is_lista
#E: Sting
#S: Bool
# retorn True si el valor puede ser una lista
def is_lista(str_value):
    try:
        eval_value=eval(str_value)
        if type(eval_value)==list:
            return True
        return False
    except:
        return False
    
#------------
#Funciones para archivos
#------------

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
a decimales. la formula es grados + minutos/60 + segundos/3600
"""
#E: 3 numeros(grados,minutos y segundos) para las coordenadas
#S: las coordenadas en decimal
#R:
def convertir_coordenadas_a_decimales(grados,minutos,segundos):
    coordenada_decimal= abs(grados) + minutos/60 + segundos/3600
    if grados<0:
        return -1*coordenada_decimal
    return coordenada_decimal

#------------
#Funciones para la interfaz grafica
#------------

#Escribir los grados verticales
def escribir_grados_verticales():
    y=68
    x=32
    cuenta= 170
    canvas.create_text(10,y,text="180",font=("Arial",10))
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
    canvas.create_text(x,545,text=f"{str(abs(cuenta))} S",font=("Arial",10))
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

#Hacer cuadricula para ver las coordenadas
#def hacer_cuadricula():

#Cargar mapa (grafica los territorios)
#def cargar_mapa():
#    global mapa,PATH_MAPA
#    mapa= cargar(PATH_MAPA)
#    for pais in mapa:
#        for provincia in pais:
#            for territorio in provincia:
#                x1= 475 + convertir_coordenadas_a_decimales(territorio[1][0])
#                x1= 950 + convertir_coordenadas_a_decimales(territorio[1][0])
                
    

#########################
#Ventana
#########################

#Se crea la ventana
root= tk.Tk()                
root.title("AI Revolution")

#Se crea el canva
canvas= tk.Canvas(root,width=1000,height=550,bg="#77B5FE")
canvas.pack() 

mapa_mundi= tk.PhotoImage(file="mapa22.png")
canvas.create_image(475,305, image=mapa_mundi)
    
crear_grafica()
canvas.create_text(475,10,text="Mapa mundi",font=("Arial",12))


root.mainloop()