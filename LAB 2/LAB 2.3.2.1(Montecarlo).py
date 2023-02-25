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
            x=-4+j*(12/(n-1))
            y=8-i*(12/(m-1))

            #matriz[i][j]=y+math.sin(math.pi*math.sqrt(x*x+y*y))                        #Las diferentes funciones que hemos utilizado, todas comentadas menos la que estamos probando
            #matriz[i][j]=math.sin(x)+math.cos(y)+math.sin(x)*math.cos(y)+math.sin(x*2)
            #matriz[i][j]=2*math.sin(x)*math.cos(y/2)+x+math.log(abs(y-math.pi/2))
            #matriz[i][j]=math.sin(x)*math.cos(y)+math.sqrt(x*y)
            #matriz[i][j]=math.sin(x*7)+math.cos((y+math.pi/4)*4)+(x*y)
            #matriz[i][j]=math.cos((x*x+y*y)*12)/(2*((x*x+y*y)*6.28+1))
            matriz[i][j]=2*(-math.sqrt(x*x+y*y)+(math.cos(y)+math.sin(x))*math.sin(y+x)) + 15*(math.sqrt((x+1)*(x+1)+y*y)-1)/((math.sqrt((x+1)*(x+1)+y*y)-1)*(math.sqrt(x*x+y*y)-1)+1)

    return matriz

#Algoriitmo que halla el maximo de la matriz recorriendola entera y comparando valores
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
            y2=y+1
            x2=x
            valor=matriz[x][y+1]
            find=True                                   #Se pone la variable boolean a True para seguir en el bucle
        
        if((y-1>=0) and matriz[x][y-1]>valor):          #Se hacen las comparaciones entre la casilla seleccionada y la de debajo, si esta ultima tiene un valor mayor serán la nueva casilla seleccionada
            y2=y-1
            x2=x
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


n=int(input("Introduzca el número de filas "))              #Se pide la anchura y longitud de la matriz sobre la que se va a trabajar
m=int(input("Introduzca el número de columnas "))
nveces=int(input("Introduzca el número de paracaidistas a tirar "))  #Se pide el numero de puntos que se van a lanzar para realizar el algoritmo

matriz =np.zeros((n,m))                                     #Se rellena la matriz de 0 para poder recorrerla más tarde
cont=0                                                      #Se inicia un contador a 0
Ppintados=[]
inicia = time.time()                                                #Se inicia una matriz vacia para introducir los puntos que posteriormente serán pintados
matriz=rellenaMatriz(matriz,n,m)                            #Se llama a rellenaMatriz para qu erellene la matriz con los valores adecuados
maxAbs=np.max(matriz)                                       #Se halla el maximo absoluto de la matriz para mas tarde hacer comparaciones
fina = time.time()
inic = time.time()
for i in range(nveces):                                     # Se llama al algortmo voraz el numero de veces que paracaidistas han pedido tirar y se halla el tiempo tardado
    cont=algoritmoVoraz(matriz,n,m,maxAbs,cont,Ppintados)
fin = time.time()

tiempoInic = fina-inicia
tiempoAlgor = fin-inic

inic = time.time()
maximoRecorriendo(matriz,n,m,np.min(matriz))                # Se llama a maximoRecorriendo y se halla el tiempo tardado
fin = time.time()

tiempoRecor = fin-inic


contador=0
#while(contador<len(Ppintados)):                             # Bucle que pinta los puntos almacenados en Ppintados de la matriz
#    matriz[Ppintados[contador][0]][Ppintados[contador][1]]=np.min(matriz)
#    contador=contador+1

#heat_map = sb.heatmap(matriz,cmap="viridis")                #Se crea el heatmap
#plt.show()

print("El porcentaje es")                                   # Se imprimen distintos datod
print(cont/nveces *100)
print()
print(" Tiempo inicializacion ")
print(tiempoInic)
print(" Tiempo algoritmo ")
print(tiempoAlgor)
print(" Tiempo total algoritmo ")
print(tiempoAlgor+tiempoInic)
print(" Tiempo recorrer ")
print(tiempoRecor)