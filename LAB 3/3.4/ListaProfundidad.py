import numpy as np

import seaborn as sb

import matplotlib.pyplot as plt

import time

from SyncRNG import SyncRNG

''' Creacion de la clase nodo.
    Pide que se ingrese el valor del nodo(id del nodo), un estado(id del nodo padre) y una etiqueta(Nº de profundidad) para la inicialización de un nodo.
    Los demas metodos son los set y get de estos atributos a excepcion de setColor y getColor que no se pide al iniciar un nodo'''
class Nodo:
    def __init__(self,valor,estado,etiqueta):
        self.valor = valor
        self.estado = estado
        self.etiqueta= etiqueta
    def setValor(self,valor):
        self.valor = valor
    def setEstado(self,estado):
        self.estado=estado
    def setEtiqueta(self,etiqueta):
        self.etiqueta=etiqueta
    def setColor(self,color):
        self.color=color
    def getValor(self):
        return self.valor
    def getEstado(self):
        return self.estado
    def getEtiqueta(self):
        return self.etiqueta
    def getColor(self):
        return self.color

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

''' Metodo que  genera un laberinto aleatorio a partir de una semilla.
    Como argumentos tiene un array V, que se rellenará de nodos, el número de filas,
    el número de columnas, la semilla y  la probabilidad con las que se crearan pasillos'''
def generaLaberinto(V,f, c, prob,semilla):
    E = []
    numero = SyncRNG(seed = semilla)
    for i in range(f):
        for j in range(c):
            V.append(Nodo(id(i,j,c),-1,1))                                          #Rellena V de nodos con nodo padre -1 y etiqueta 1
            if(i>0 and numero.rand()<prob):                                       #Se rellena el array de ejes 
                E.append(([Nodo(id(i,j,c),0,1)], [Nodo(id(i-1,j,c),0,1)]))
                E.append(([Nodo(id(i-1,j, c),0,1)], [Nodo(id(i,j,c),0,1)]))
            if(j>0 and numero.rand()<prob):
                E.append(([Nodo(id(i,j,c),0,1)], [Nodo(id(i,j-1,c),0,1)]))
                E.append(([Nodo(id(i,j-1, c),0,1)], [Nodo(id(i,j,c),0,1)]))
    return E

''' Metodo que iguala los objetos nodos por valor, es decir un par de nodos que tienen el mismo valor(id) serán el mismo objeto
    Este metodo lo he creado porque los nodos del array V y los del array E,aunque su id sea el mismo el objeto era distinto,
    tras pasar por el método serán el mismo'''
def igualar(V,E):
    for i in range(len(V)):
        for j in range(len(E)):
            if(V[i].getValor()==E[j][0][0].getValor()):
                E[j][0][0]=V[i]
                
    for i in range(len(V)):
        for j in range(len(E)):
            if(V[i].getValor()==E[j][1][0].getValor()):
                E[j][1][0]=V[i]

''' Metodo utilizado para recorrer el grafo. En este caso es el algoritmo primero en profundidad. Retorna los nodos visistados'''
def primeroProf(V,E,num,color):
    visitados=[]
    pila=[]
    pila.append(V[num])                                                 #Se escoge el nodo de origen en la pila
    while pila:                                                        #Se itera siempre que halla un nodo en la pila
        actual=pila.pop()                                               #Se desapila un nodo de la pila
        if actual not in visitados:                                     #Si el nodo actual no ha sido visitado se convertirá en el nodo escogido
            actual.setColor(color)                                      #Se le añaden atributos como el color y  el nodo padre, si este ultimo no existe se pondra como padre a el mismo
            visitados.append(actual)
            if(V[num].getEstado()==-1):
                V[num].setEstado(actual.getValor())
        for i in range(len(V)):                                         #Para cada nodo que el nodo actual tiene como destino y no ha sido visitado se apila en la pila
            if V[i] not in visitados and (([actual], [V[i]])) in E:     
                V[i].setEstado(actual.getValor())
                V[i].setEtiqueta(actual.getEtiqueta()+1)
                pila.append(V[i])
    return visitados

'''Método que recorre la lista de ejes y el array de nodos para añadir valores a una matriz que será pintada en un heatmap'''
def recorre(visitados, E, f, c):
    mat=[]
    mat=inic(f,c)
    for i in range(f):
        for j in range(c):
            mat[i*2+1][j*2+1] = 10                                      #Se da valor 10 a las casillas que se pueden recorrer del laberinto
            if(i<f-1 and (([id(i,j, c)], [id(i+1,j,c)])) in E):
                mat[i*2+2][j*2+1] = 10
            if(j<c-1 and (([id(i, j, c)], [id(i, j+1, c)])) in E):
                mat[i*2+1][j*2+2] = 10
    for k in range(len(visitados)):                                     
        mat[int((fila(visitados[k].getValor(),c)))*2+1][(int(columna(visitados[k].getValor(),c)))*2+1] = int(visitados[k].getColor()) #Se da valor "color" a los nodos recorridos por el algoritmo
        mat[media(fila(visitados[k].getValor(),c)*2+1,fila(visitados[k].getEstado(),c)*2+1)][media((columna(visitados[k].getValor(),c))*2+1,(columna(visitados[k].getEstado(),c))*2+1)]=visitados[k].getColor()#Se da valor o"color" a los pasillos que unen a los nodos recorridos en funcion del algoritmo
    return mat

'''Método que pasa de una matriz de objetos a una matriz de valores'''
def destransformaMatriz(matrizNodo,f):
    matriz=[]
    for i in range(len(matrizNodo)):
        matriz.append(([matrizNodo[i][0][0].getValor()],[matrizNodo[i][1][0].getValor()]))
    return matriz

'''Método que recorre el array de nodos e inicia el algoritmo de busqueda en los nodos no recorridos '''
def ciclos(V,E,prueba,color):
    for i in range(len(V)):
        if(V[i] not in prueba):
            color=color+10
            prueba2 = primeroProf(V,E,i,color)
            prueba.extend(prueba2)

'''Método que convierte en paredes las casillas no recorridas por el algoritmo'''
def detectaCiclos(matrizAd2,f,c):
    for i in range(f):
        for j in range(c):
            if(matrizAd2[i*2+2][j*2+1]==10):
                matrizAd2[i*2+2][j*2+1]=0              #Convierte la posicion no recorrida en una pared
            if(matrizAd2[i*2+1][j*2+2]==10):
                matrizAd2[i*2+1][j*2+2]=0               #Convierte la posicion no recorrida en una pared

'''Método que se encarga de detectar las separaciones entre componentes conexas'''              
def detectaCosturas(V,mat,f,c):
    longitud1=f                     #Detecta costuras horizontalmente
    inicFil=0
    while(longitud1>0):
        for i in range(inicFil,inicFil+c -1):
            if(V[i].getColor()!=V[i+1].getColor()):
                mat[media(fila(V[i].getValor(),c)*2+1,fila(V[i+1].getValor(),c)*2+1)][media(columna(V[i].getValor(),c)*2+1,columna(V[i+1].getValor(),c)*2+1)]=650
                plt.text(media(columna(V[i].getValor(),c)*2+1,columna(V[i+1].getValor(),c)*2+1),media(fila(V[i].getValor(),c)*2+1,fila(V[i+1].getValor(),c)*2+1),'co',fontsize=10,color='black',verticalalignment='center',horizontalalignment='center')
        inicFil = inicFil+c
        longitud1=longitud1-1

    longitud2=0                    #Detecta costuras verticalmente
    while(longitud2<c*(f-1)):
        if(V[longitud2].getColor()!=V[longitud2+(c)].getColor()):
            mat[media(fila(V[longitud2].getValor(),c)*2+1,fila(V[longitud2+(c)].getValor(),c)*2+1)][media(columna(V[longitud2].getValor(),c)*2+1,columna(V[longitud2+(c)].getValor(),c)*2+1)]=650
            plt.text(media(columna(V[longitud2].getValor(),c)*2+1,columna(V[longitud2+(c)].getValor(),c)*2+1),media(fila(V[longitud2].getValor(),c)*2+1,fila(V[longitud2+(c)].getValor(),c)*2+1),'co',fontsize=10,color='black',verticalalignment='center',horizontalalignment='center')
        longitud2=longitud2+1

#*********************************************************************************************
#*********************************************************************************************
#*********************************************************************************************
'''Se inicializa la lista de nodos, la de ejes y las variables necesafrias para el funcinamiento del programa'''
V=[]
prueba=[]
color=40
p=10
'''Se pide al usuario las variables que se utilizarán para la creación del laberinto'''
f = int(input("Introduce las filas: "))
c = int(input("Introduce las columnas: "))
while(p<0 or p>1):
    p = float(input("Introduce la probabilidad con valor entre 0 y 1: "))
s = int(input("Introduce la semilla: "))

'''Se llama a los metodos necesarios en orden'''
E = generaLaberinto(V,f, c, p,s)                        #Se crea lista de ejes y array de nodos
igualar(V,E)                                            #Se igualan los objetos para poder compararlos
ordenada=primeroProf(V,E,0,color)                         #Se recorre en profundidaz el grafo
ciclos(V,E,ordenada,color)                                #Se hace el recorrido en todos los nodos
Eprima=destransformaMatriz(E,len(E))                    #Se pasa de objetos a valores
matriz = recorre(ordenada, Eprima, f, c)             #Se crea una matriz para ser pintada
detectaCiclos(matriz,f,c)                            #Se detectan ciclos y costuras
detectaCosturas(V,matriz,f,c)

'''Se impime la matriz mediante un mapa de calor'''
plt.imshow((matriz),cmap="nipy_spectral",origin='upper')
plt.colorbar()
plt.show()