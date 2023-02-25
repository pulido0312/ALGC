from queue import PriorityQueue 

from matplotlib.colors import Colormap

import numpy as np

import seaborn as sb

import matplotlib.pyplot as plt

import time

from SyncRNG import SyncRNG

import copy

'''Método para insertar diccionarios en otro diccionario'''
def dict1(sample_dict, key, list_of_values,peso):
    if key not in sample_dict:
        sample_dict[key] = {}
    sample_dict[key][list_of_values]=peso
    return sample_dict

'''Método que haya la distancia manhatan de un nodo hasta otro'''
def distManhatan(nodo, destino):
    nodox = int((fila(nodo,c)))
    nodoy = int((columna(nodo,c)))

    destinox = int((fila(destino,c)))
    destinoy = int((columna(destino,c)))

    return (abs(nodox-destinox) + abs(nodoy-destinoy))

''' Metodo para hallar la fila de un nodo a traves de su id y el numero de columnas total'''
def fila(id, c):
    return int(id/c)

''' Metodo para hallar la columna de un nodo a traves de su id y el numero de columnas total'''
def columna(id, c):
    return int(id%c)

''' Metodo para hallar la id de un nodo a traves de su fila, columna y el numero total de columnas'''
def id(fil, col, c):
    return fil*c +col

'''Método de inicialización de una matriz del doble de columnas y filas + 1 de los dados'''
def inic(fil, col):
    matriz = []
    matriz=np.zeros((fil*2+1,col*2+1))
    return matriz

''' Metodo para calcular la media entera de dos valores dados'''
def media(a,b):
    return int((a+b)/2)
''' Metodo para hallar el menor número de 2 dados'''
def menorNum(a,b):
    menor=a
    if(b<a):
        menor=b
    return menor

''' Metodo que  genera un laberinto aleatorio a partir de una semilla.
    Como argumentos tiene el número de filas,
    el número de columnas, las semillas y  la probabilidad con las que se crearan pasillos'''
def generaLaberinto(f,c,prob,semillaNodo,semillaEje):
    Eprom={}
    ran = SyncRNG(seed = semillaNodo)
    eje = SyncRNG(seed = semillaEje)
    for i in range(f):
        for j in range(c):
            if(i>0 and ran.rand()<prob):
                ejeran = eje.randi()%12+1
                Eprom = dict1(Eprom,id(i, j, c),id(i-1, j, c),ejeran)
                Eprom = dict1(Eprom,id(i-1, j, c),id(i, j, c),ejeran)
            if(j>0 and ran.rand()<prob):
                ejeran = eje.randi()%12+1
                Eprom = dict1(Eprom,id(i, j, c),id(i, j-1, c),ejeran)
                Eprom = dict1(Eprom,id(i, j-1, c),id(i, j, c),ejeran)
    return Eprom


''' Metodo utilizado para recorrer el grafo. En este caso es el algoritmo de dijktra. Retorna los nodos visistados y los explorados.'''
def dijkstra(E,inic,fin):
    #Inicializamos las estructuras de datos necesaria
    menorDistancia = {}
    predecesor = {}
    noVisitados = E
    cola = PriorityQueue()
   
    camino = []
    infinito = 999999999
    #Relleno la lista con las distancias tentativas
    for nodo in noVisitados:
        menorDistancia[nodo]=infinito
        cola.put((menorDistancia[nodo],nodo))
    menorDistancia[inic] = 0
    cola.put((0,inic))
    #Mientras la lista no esté vacia
    while cola:
        #Obtengo los nodos de menor distancia tentativa
        nodoMenorDistancia = cola.get()[1]
        #Si se llega al final se acaba el bucle
        if(nodoMenorDistancia==fin):
            break        
        #Obtengo sus descendientes
        opcionesCamino = list(E[nodoMenorDistancia].items())
        #Para cada nodo hijo se actualiza la distancia tentativa si se cumple el if
        for nodoHijo in opcionesCamino:
            if nodoHijo[1] + menorDistancia[nodoMenorDistancia]<menorDistancia[nodoHijo[0]]:
                menorDistancia[nodoHijo[0]]= nodoHijo[1] + menorDistancia[nodoMenorDistancia]
                predecesor[nodoHijo[0]]=nodoMenorDistancia
                #Se suma la distancia manhatan a la distancia tentativa del nodo
                cola.put((menorDistancia[nodoHijo[0]]+(2*distManhatan(nodoHijo[0],fin)),nodoHijo[0]))
    nodoActual = fin
    #Se insertan el camino recorrido en un array 
    while nodoActual!=inic:
        try:
            camino.insert(0,nodoActual)
            nodoActual=predecesor[nodoActual]
        except KeyError:
            print("No se puede encontar el camino")
            break

    camino.insert(0,inic)

    if menorDistancia[fin] != infinito:
        print("la menor distancia es "+ str(menorDistancia[fin]))
        print("El camino optimo es"+ str(camino))

    return camino,menorDistancia

'''Método que recorre el grafo y el array de nodos para añadir valores a una matriz que será pintada en un heatmap'''
def recorre(E, f, c,ini,fin,camino,Dtentativas):
    mat=[]
    mat=inic(f,c) 
    for i in range(f):
        for j in range(c):
            mat[i*2+1][j*2+1] = 10
            for n in range(13):
                if(i<f-1 and E.get(id(i+1,j,c)) and (id(i,j, c) in E.get(id(i+1,j,c)))):
                    mat[i*2+2][j*2+1] = 10
                if(j<c-1 and E.get(id(i, j+1, c)) and (id(i, j, c) in E.get(id(i, j+1, c)))):
                    mat[i*2+1][j*2+2] = 10

    "Pinta las habitaciones que han sido explorados"
    for clave in Dtentativas:
        if(Dtentativas[clave] >= 999999999):
            Dtentativas[clave] = -1      
        mat[fila(clave,c)*2+1][columna(clave,c)*2+1]=Dtentativas[clave]

    "Pinta los pasillos que han sido explorados"
    for i in range(len(E)):
        if(i in E):
            for j in range(len(E[i])):
                distTent = menorNum(Dtentativas[i],Dtentativas[list(E[i].keys())[j]])
                mat[media(fila(i,c)*2+1,fila(list(E[i].keys())[j],c)*2+1)][media(columna(i,c)*2+1,columna(list(E[i].keys())[j],c)*2+1)]=distTent

    "Pinta las habitaciones del camino recorrido"
    for i in range(len(camino)):
        mat[fila(camino[i],c)*2+1][columna(camino[i],c)*2+1]=650
    "Pinta los pasillos del camino recorrido"
    for j in range(len(camino)-1):
        mat[media(fila(camino[j],c)*2+1,fila(camino[j+1],c)*2+1)][media((columna(camino[j],c))*2+1,(columna(camino[j+1],c))*2+1)]=650

    "Pinta la casilla de llegada y de salida"
    mat[fila(ini,c)*2+1][columna(ini,c)*2+1]=660
    mat[fila(fin,c)*2+1][columna(fin,c)*2+1]=660
    return mat

#*********************************************************************************************
#*********************************************************************************************
#*********************************************************************************************
p=2
'''Se pide al usuario las variables que se utilizarán para la creación del laberinto'''
f =int(input("Introduce las filas: "))
c = int(input("Introduce las columnas: "))
while(p<0 or p>1):
    p = float(input("Introduce la probabilidad con valor entre 0 y 1: "))
s = int(input("Introduce la semilla conexiones de Nodo: "))
se =int(input("Introduce la semilla pesos Eje: "))
nod =int(input("Introduce la semilla de los nodos de principio y fin: "))

semNod = SyncRNG(seed = nod)
primerNodo = semNod.randi()%(f*c)
segundoNodo = semNod.randi()%(f*c)

'''Se llama a los metodos necesarios en orden'''
Eprom = generaLaberinto(f,c,p,s,se)
E=Eprom.copy()

a=time.time()
camino,Dtentativas = dijkstra(Eprom,primerNodo,segundoNodo)
b=time.time()

print("tiempo: ")
print(b-a)

matriz = recorre(E, f, c,primerNodo,segundoNodo,camino,Dtentativas)


'''Se impime la matriz mediante un mapa de calor'''
cmap = copy.copy(plt.get_cmap("viridis"))
cmap.set_under('blue')
cmap.set_bad('red')
sb.heatmap(matriz,mask=matriz == 650,vmin=0,cmap=cmap,cbar_kws={'extend':'min','extendrect':True}, annot=None, fmt="")
plt.show()