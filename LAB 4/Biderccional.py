from queue import PriorityQueue 

from matplotlib.colors import Colormap

import numpy as np

import seaborn as sb

import matplotlib.pyplot as plt

import time

from SyncRNG import SyncRNG

import collections

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

def menorNum(a,b):
    menor=a
    if(b<a):
        menor=b
    return menor

''' Metodo que  genera un laberinto aleatorio a partir de una semilla.
    Como argumentos tiene un array V, que se rellenará de nodos, el número de filas,
    el número de columnas, la semilla y  la probabilidad con las que se crearan pasillos'''
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


''' Metodo utilizado para recorrer el grafo. En este caso es el algoritmo primero en profundidad. Retorna los nodos visistados.
Si se elige primero en anchura la pila actuará como una cola'''
def Astar(E,inic,fin):
    #Inicializamos las estructuras de datos necesarias para los dos caminos
    menorDistanciaSalida = {}
    menorDistanciaDestino = {}

    predecesorSalida = {}
    predecesorDestino = {}

    colaSalida = PriorityQueue()
    colaDestino = PriorityQueue()
    camino = {}
    caminoSal = {}
    caminoDes = {}
    infinito = 999999999
    Corte=None
    lon=1

    #Relleno colas de prioridad
    for nodo in E:
        menorDistanciaSalida[nodo]=infinito
        menorDistanciaDestino[nodo]=infinito
        colaSalida.put((infinito,nodo))
        colaDestino.put((infinito,nodo))

    menorDistanciaSalida[inic] = 0
    menorDistanciaDestino[fin] = 0

    #Nodo de salida en la cola de salida con distancia cero, y con el destino igual
    colaSalida.put((0,inic))
    colaDestino.put((0,fin))

    #Mientras las colas no están vacias
    while (colaSalida and colaDestino):
        #Obtengo los nodos de menor distancia tentativa en cada cola
        nodoMenorDistanciaSalida = colaSalida.get()
     
        nodoMenorDistanciaDestino= colaDestino.get()
        #Obtengo sus descendientes
        opcionesCaminoSalida = E[nodoMenorDistanciaSalida[1]].items()
        opcionesCaminoDestino = E[nodoMenorDistanciaDestino[1]].items()

        camino[nodoMenorDistanciaSalida[1]]=0
        #Si el camino que se inicia en el destino va a recorrer una casilla ya recorrida se sale del bucle
        if(nodoMenorDistanciaDestino[1] in camino.keys()):
            Corte = nodoMenorDistanciaDestino[1]
            print("Se corta en: ")
            print(Corte)
            break

        #Para cada nodo hijo se actualiza la distancia tentativa si se cumple el if
        for nodoHijoSalida in opcionesCaminoSalida:
            if nodoHijoSalida[1] + menorDistanciaSalida[nodoMenorDistanciaSalida[1]]<menorDistanciaSalida[nodoHijoSalida[0]]:
                menorDistanciaSalida[nodoHijoSalida[0]]= nodoHijoSalida[1] + menorDistanciaSalida[nodoMenorDistanciaSalida[1]]
                predecesorSalida[nodoHijoSalida[0]]=nodoMenorDistanciaSalida[1]
                #sumamos distancia manhatan a la distancia del nodo en la cola
                colaSalida.put((menorDistanciaSalida[nodoMenorDistanciaSalida[1]]+(5*distManhatan(nodoMenorDistanciaSalida[1],fin)),nodoHijoSalida[0]))

        for nodoHijoDestino in opcionesCaminoDestino:
            if nodoHijoDestino[1] + menorDistanciaDestino[nodoMenorDistanciaDestino[1]]<menorDistanciaDestino[nodoHijoDestino[0]]:
                menorDistanciaDestino[nodoHijoDestino[0]]= nodoHijoDestino[1] + menorDistanciaDestino[nodoMenorDistanciaDestino[1]]
                predecesorDestino[nodoHijoDestino[0]]=nodoMenorDistanciaDestino[1]
                #sumamos distancia manhatan a la distancia del nodo en la cola
                colaDestino.put((menorDistanciaDestino[nodoMenorDistanciaDestino[1]]+(5*distManhatan(nodoMenorDistanciaDestino[1],inic)),nodoHijoDestino[0]))
        #Si se llega al final se acaba el bucle
        if(nodoMenorDistanciaSalida[1] == fin):
            break
        if(nodoMenorDistanciaDestino[1] == inic):
            break

    nodoActual= fin
    predecesor=predecesorSalida

    #Se insertan los caminos recorridos en un array 
    camino = []
    flag = 2
    corte=Corte
    caminoDes=[]
    while flag > 0:

        if(Corte==None):
            print("/////////////////////")
            print("No hay camino")
            print("////////////////////")
            break
        while corte!=nodoActual:
            try:
                camino.insert(0,corte)
                corte=predecesor[corte]
            except KeyError:
                break
        if flag==2:
            caminoSal = camino
            print(camino)
        if flag ==1:
            caminoDes = camino
            print(camino)
        corte=Corte
        camino = []       
        nodoActual=inic
        predecesor=predecesorDestino
        flag = flag-1

        lon = len(caminoSal)
        caminoSal.extend(caminoDes)
    return caminoSal,menorDistanciaSalida,menorDistanciaDestino,lon


''' Metodo utilizado para recorrer el grafo. En este caso es el algoritmo primero en profundidad. Retorna los nodos visistados.
Si se elige primero en anchura la pila actuará como una cola'''
def dijkstra(E,inic,fin):
    #Inicializamos las estructuras de datos necesarias para los dos caminos
    menorDistanciaSalida = {}
    menorDistanciaDestino = {}

    predecesorSalida = {}
    predecesorDestino = {}

    colaSalida = PriorityQueue()       
    colaDestino = PriorityQueue()
    camino = {}
    caminoSal = {}
    caminoDes = {}
    infinito = 999999999
    Corte=None
    lon=1

    #Relleno colas de prioridad
    for nodo in E:
        menorDistanciaSalida[nodo]=infinito
        menorDistanciaDestino[nodo]=infinito
        colaSalida.put((infinito,nodo))
        colaDestino.put((infinito,nodo))

    menorDistanciaSalida[inic] = 0
    menorDistanciaDestino[fin] = 0
    #Nodo de salida en la cola de salida con distancia cero, y con el destino igual
    colaSalida.put((0,inic))
    colaDestino.put((0,fin))

    #Mientras las colas no están vacias
    while (colaSalida and colaDestino):
        #Obtengo los nodos de menor distancia tentativa en cada cola
        nodoMenorDistanciaSalida = colaSalida.get()
        nodoMenorDistanciaDestino= colaDestino.get()
        #Obtengo sus descendientes
        opcionesCaminoSalida = E[nodoMenorDistanciaSalida[1]].items()
        opcionesCaminoDestino = E[nodoMenorDistanciaDestino[1]].items()

        camino[nodoMenorDistanciaSalida[1]]=0

        #Si el camino que se inicia en el destino va a recorrer una casilla ya recorrida se sale del bucle
        if(nodoMenorDistanciaDestino[1] in camino.keys()):
            Corte = nodoMenorDistanciaDestino[1]
            print("Se corta en: ")
            print(Corte)
            break

        #Para cada nodo hijo se actualiza la distancia tentativa si se cumple el if
        for nodoHijoSalida in opcionesCaminoSalida:
            if nodoHijoSalida[1] + menorDistanciaSalida[nodoMenorDistanciaSalida[1]]<menorDistanciaSalida[nodoHijoSalida[0]]:
                menorDistanciaSalida[nodoHijoSalida[0]]= nodoHijoSalida[1] + menorDistanciaSalida[nodoMenorDistanciaSalida[1]]
                predecesorSalida[nodoHijoSalida[0]]=nodoMenorDistanciaSalida[1]
                colaSalida.put((menorDistanciaSalida[nodoMenorDistanciaSalida[1]],nodoHijoSalida[0]))

        for nodoHijoDestino in opcionesCaminoDestino:
            if nodoHijoDestino[1] + menorDistanciaDestino[nodoMenorDistanciaDestino[1]]<menorDistanciaDestino[nodoHijoDestino[0]]:
                menorDistanciaDestino[nodoHijoDestino[0]]= nodoHijoDestino[1] + menorDistanciaDestino[nodoMenorDistanciaDestino[1]]
                predecesorDestino[nodoHijoDestino[0]]=nodoMenorDistanciaDestino[1]
                colaDestino.put((menorDistanciaDestino[nodoMenorDistanciaDestino[1]],nodoHijoDestino[0]))
        
        #Si se llega al final se acaba el bucle
        if(nodoMenorDistanciaSalida[1] == fin):
            break
        if(nodoMenorDistanciaDestino[1] == inic):
            break

    nodoActual= fin
    predecesor=predecesorSalida
    #Se insertan los caminos recorridos en un array 
    camino = []
    flag = 2
    corte=Corte
    caminoDes=[]
    while flag > 0:

        if(Corte==None):
            print("//////////////////////")
            print("////No hay camino////")
            print("////////////////////")
            break
        while corte!=nodoActual:
            try:
                camino.insert(0,corte)
                corte=predecesor[corte]
            except KeyError:
                break
        if flag==2:
            caminoSal = camino
            print(camino)
        if flag ==1:
            caminoDes = camino
            print(camino)
        corte=Corte
        camino = []       
        nodoActual=inic
        predecesor=predecesorDestino
        flag = flag-1

        lon = len(caminoSal)
        
        caminoSal.extend(caminoDes)
        
    return caminoSal,menorDistanciaSalida,menorDistanciaDestino,lon
'''Método que recorre la lista de ejes y el array de nodos para añadir valores a una matriz que será pintada en un heatmap'''
def recorre(Corte, E, f, c,ini,fin,camino,Dtentativas,DtentativasDes):
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
    
    for clave in DtentativasDes:
        if(DtentativasDes[clave] >= 999999999):
            DtentativasDes[clave] = -1

        if(DtentativasDes[clave]!=-1): 
            mat[fila(clave,c)*2+1][columna(clave,c)*2+1]=DtentativasDes[clave]


    "Pinta los pasillos que han sido explorados"
    for i in range(len(E)):
        if(i in E):
            for j in range(len(E[i])):
                distTent = menorNum(Dtentativas[i],Dtentativas[list(E[i].keys())[j]])
                mat[media(fila(i,c)*2+1,fila(list(E[i].keys())[j],c)*2+1)][media(columna(i,c)*2+1,columna(list(E[i].keys())[j],c)*2+1)]=distTent 
                distTent = menorNum(DtentativasDes[i],DtentativasDes[list(E[i].keys())[j]])
                if(distTent!= -1):
                    mat[media(fila(i,c)*2+1,fila(list(E[i].keys())[j],c)*2+1)][media(columna(i,c)*2+1,columna(list(E[i].keys())[j],c)*2+1)]=distTent
    
    "Pinta las habitaciones del camino recorrido"
    for i in range(len(camino)):
        mat[fila(camino[i],c)*2+1][columna(camino[i],c)*2+1]=650
        
    "Pinta los pasillos del camino recorrido"
    for j in range(len(camino)-1):
        if(j!=Corte):
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
c =int(input("Introduce las columnas: "))
while(p<0 or p>1):
    p = float(input("Introduce la probabilidad con valor entre 0 y 1: "))
s = int(input("Introduce la semilla conexiones de Nodo: "))
se = int(input("Introduce la semilla pesos Eje: "))
nod = int(input("Introduce la semilla de los nodos de principio y fin: "))
ord = int(input("Introduce un 1 para Dijsktra o un 0 para A*: "))

semNod = SyncRNG(seed = nod)
primerNodo = semNod.randi()%(f*c)
segundoNodo = semNod.randi()%(f*c)

'''Se llama a los metodos necesarios en orden'''
Eprom = generaLaberinto(f,c,p,s,se)
E=Eprom.copy()

a=time.time()
if(ord==1):
    camino,Dtentativas,DtentativasDes,Corte = dijkstra(Eprom,primerNodo,segundoNodo)
elif(ord==0):
    camino,Dtentativas,DtentativasDes,Corte= Astar(Eprom,primerNodo,segundoNodo)
b=time.time()

print("tiempo: ")
print(b-a)

matriz = recorre(Corte-1, E, f, c,primerNodo,segundoNodo,camino,Dtentativas,DtentativasDes)

'''Se impime la matriz mediante un mapa de calor'''
cmap = copy.copy(plt.get_cmap("viridis"))
cmap.set_under('blue')
cmap.set_bad('red')
sb.heatmap(matriz,mask=matriz == 650,vmin=0,cmap=cmap,cbar_kws={'extend':'min','extendrect':True}, annot=None, fmt="")
plt.show()