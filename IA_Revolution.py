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
def cargar(ruta,destino):
    with open(ruta,"r") as file:
        lista_str=file.read()
        if is_lista(lista_str):
            destino=eval(lista_str)
        else:
            destino=[]
    return destino

#########################
#Ventana
#########################

#Se crea la ventana
root= tk.Tk()                
root.title("AI Revolution")

#Se crea el canva
canvas= tk.Canvas(root,width=950,height=455,bg="#77B5FE")
canvas.pack() 

mapa_mundi= tk.PhotoImage(file="mapa22.png")

canvas.create_image(475,210, image=mapa_mundi)


root.mainloop()