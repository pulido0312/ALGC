import numpy as np

import seaborn as sb

import matplotlib.pyplot as plt

import math

import random

import time

#Algoritmo que rellena las casillas de un matriz con los valores resultantes de una función dada
def rellenaMatriz(matriz,n,m):
    for i in range(n):                                                                  #Se recorre la matriz
        for j in range(m):    
            x=-1.5+j*(4/(n-1))                                                         #Se calculan los valores de X e Y
            y=2.5-i*(4/(m-1))

            #matriz[i][j]=y+math.sin(math.pi*math.sqrt(x*x+y*y))                        #Las diferentes funciones que hemos utilizado, todas comentadas menos la que estamos probando
            #matriz[i][j]=math.sin(x)+math.cos(y)+math.sin(x)*math.cos(y)+math.sin(x*2)
            #matriz[i][j]=2*math.sin(x)*math.cos(y/2)+x+math.log(abs(y-math.pi/2))
            #matriz[i][j]=math.sin(x)*math.cos(y)+math.sqrt(x*y)
            #matriz[i][j]=math.sin(x*7)+math.cos((y+math.pi/4)*4)+(x*y)
            matriz[i][j]=math.cos((x*x+y*y)*12)/(2*((x*x+y*y)*3.14+1))

    return matriz

#Algoritmo que halla el maximo de la matriz recorriendola entera y comparando valores
def maximoRecorriendo(matriz,n,m,valMax):
    for i in range(n):
        for j in range(m):
            valMax = max(valMax,matriz[i][j])
    return valMax

#Algoritmo voraz, que halla el maximo recorriendo los valores de la matriz desde un punto al azar hasta el maximo local

def algoritmoVoraz(matriz,n,m,maxAbs,cont,Ppintados):
    #random.seed(300)
    #x=random.randint(0, n)
    #x=random.randint(0, m)
    x=random.randrange(0, n)                            #Genera un punto al azar donde empezar el algoritmo
    y=random.randrange(0, m)
    find=True                                           #Se inicializa un boolean a True para que se inicie el bucle

    while(find):
        valor=matriz[x][y]                              #Se escoge el valor de la casilla seleccionada 
        x2=x                                            #Se inician las variables auxiliares de X e Y
        y2=y
        find=False                                      #Se cambia la variable boolean a False oara que se salga del bucle
        if((x+1<n) and matriz[x+1][y]>valor):           #Se hacen las comparaciones entre la casilla seleccionada y la de su derecha, si esta ultima tiene un valor mayor serán la nueva casilla seleccionada
            x2=x+1
            y2=y
            valor=matriz[x+1][y]
            find=True                                   #Se pone la variable boolean a True para seguir en el bucle

        if((x-1>=0) and matriz[x-1][y]>valor):          #Se hacen las comparaciones entre la casilla seleccionada y la de su izq, si esta ultima tiene un valor mayor serán la nueva casilla seleccionada
            x2=x-1
            y2=y
            valor=matriz[x-1][y]
            find=True                                   #Se pone la variable boolean a True para seguir en el bucle
        
        if((y+1<m) and matriz[x][y+1]>valor):           #Se hacen las comparaciones entre la casilla seleccionada y la de encima, si esta ultima tiene un valor mayor serán la nueva casilla seleccionada
            x2=x
            y2=y+1
            valor=matriz[x][y+1]
            find=True                                   #Se pone la variable boolean a True para seguir en el bucle
        
        if((y-1>=0) and matriz[x][y-1]>valor):          #Se hacen las comparaciones entre la casilla seleccionada y la de debajo, si esta ultima tiene un valor mayor serán la nueva casilla seleccionada
            x2=x
            y2=y-1
            valor=matriz[x][y-1]
            find=True                                   #Se pone la variable boolean a True para seguir en el bucle

        Ppintados.append([x,y])                         #Se añaden los puntos seleccionados por el algoritmo a una matriz
        x=x2                                            #X e Y toman los valores de sus variables auxiliare respectivamente
        y=y2        
    if(valor==maxAbs):                                  #Si se ha llegado al maximo absoluto se suma uno al contador
        cont=+1   
    return cont

#*******************************************************************************************************************************************************************************#

#*******************************************************************************************************************************************************************************#

#*******************************************************************************************************************************************************************************#



n=int(input("Introduzca el número de filas "))                                          #Se pide la anchura y longitud de la matriz sobre la que se va a trabajar
m=int(input("Introduzca el número de columnas "))
nveces=int(input("Introduzca el número de paracaidistas a tirar "))                     #Se pide el numero de puntos que se van a lanzar para realizar el algoritmo
repeticiones=int(input("Introduzca el número de veces que se ejecutará el programa "))

matriz =np.zeros((n,m))                                     #Se rellena la matriz de 0 para poder recorrerla más tarde
matriz=rellenaMatriz(matriz,n,m)                            #Se llama a rellenaMatriz para que rellene la matriz con los valores adecuados
maxAbs=np.max(matriz)                                       #Se halla el maximo absoluto de la matriz para mas tarde hacer comparaciones                                                    
Ppintados=[]                                                #Se inicia una matriz vacia para introducir los puntos que posteriormente serán pintados
probabilidad=0                                              #Se inicia un contador a 0 en el que se almacenará las veces en las que la ejecución de un progtrama ha tenido exito(ha llegado al maximo absoluto)
inic = time.time()

for k in range(repeticiones):                                                   #Se inicia un bucle que se repetira el numero de veces pedido
    matrizAux=matriz                                                            #Matriz Auxuliar se iguala a la matriz original
    cont=0
    for i in range(nveces):                                                     #Se llama al algortmo voraz el numero de veces que paracaidistas han pedido tirar
        cont=algoritmoVoraz(matrizAux,n,m,maxAbs,cont,Ppintados)
    if(cont>0):
        probabilidad=probabilidad+1

fin = time.time()

tiempoAlgor = fin-inic                                      #Se halla el tiempo tardado del algoritmo

inic = time.time()
maximoRecorriendo(matriz,n,m,np.min(matriz))                #Se llama a maximoRecorriendo y se halla el tiempo tardado
fin = time.time()

tiempoRecor = fin-inic                                      #Se halla el tiempo tardado de recorrer la matriz para hallar el maximo


#contador=0
#while(contador<len(Ppintados)):                             # Bucle que pinta los puntos almacenados en Ppintados de la matriz
#    matriz[Ppintados[contador][0]][Ppintados[contador][1]]=np.min(matriz)
#    contador=contador+1

#heat_map = sb.heatmap(matriz,cmap="viridis")                #Se crea y muestra el heatmap
#plt.show()

print("El porcentaje de paracaidistas que llegan al maximo es")                                   # Se imprimen distintos datos
print(cont/nveces *100)
print()
print(" Tiempo algoritmo ")
print(tiempoAlgor)
print(" Tiempo recorrer ")
print(tiempoRecor)

print("El programa ha alcanzado el maximo absoluto en un porcentaje de: ")
print(probabilidad/repeticiones *100)
