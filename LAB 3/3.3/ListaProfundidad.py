import numpy as np

import seaborn as sb

import matplotlib.pyplot as plt

import time

import statistics as stats

from SyncRNG import SyncRNG

''' Creacion de la clase nodo.
    Pide que se ingrese el valor del nodo(id del nodo), un estado(id del nodo padre) y una etiqueta(Nº de profundidad) para la inicialización de un nodo.
    Los demas metodos son los set y get de estos atributos'''
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
    def getValor(self):
        return self.valor
    def getEstado(self):
        return self.estado
    def getEtiqueta(self):
        return self.etiqueta

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
    ran = SyncRNG(seed = semilla)
    for i in range(f):
        for j in range(c):
            V.append(Nodo(id(i,j,c),-1,1))
            if(i>0 and ran.rand()<prob):
                E.append(([Nodo(id(i,j,c),0,1)], [Nodo(id(i-1,j,c),0,1)]))
                E.append(([Nodo(id(i-1,j, c),0,1)], [Nodo(id(i,j,c),0,1)]))
            if(j>0 and ran.rand()<prob):
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
def primeroProf(V,E,num):
    visitados=[]
    pila=[]
    pila.append(V[num])
    while pila:
        actual=pila.pop()
        if actual not in visitados:
            visitados.append(actual)
            if(V[num].getEstado()==-1):
                V[num].setEstado(actual.getValor())
        for i in range(len(V)):
            if V[i] not in visitados and (([actual], [V[i]])) in E:
                V[i].setEstado(actual.getValor())
                V[i].setEtiqueta(actual.getEtiqueta()+1)
                pila.append(V[i])
    return visitados
    
'''Método que recorre la lista de ejes y el array de nodos para añadir valores a una matriz que será pintada en un heatmap'''
def recorre(visitados, E, f, c,cont):
    mat=[]
    mat=inic(f,c)
    for i in range(f):
        for j in range(c):
            mat[i*2+1][j*2+1] = 15
            if(i<f-1 and (([id(i,j, c)], [id(i+1,j,c)])) in E):
                mat[i*2+2][j*2+1] = 15
            if(j<c-1 and (([id(i, j, c)], [id(i, j+1, c)])) in E):
                mat[i*2+1][j*2+2] = 15
    for k in range(len(visitados)):
        cont=cont+1
        mat[int((fila(visitados[k].getValor(),c)))*2+1][(int(columna(visitados[k].getValor(),c)))*2+1] = 20
        plt.text((int(columna(visitados[k].getValor(),c)))*2+1,int((fila(visitados[k].getValor(),c)))*2+1,visitados[k].getEtiqueta(),fontsize=10,color='black',verticalalignment='center',horizontalalignment='center')
        mat[media(fila(visitados[k].getValor(),c)*2+1,fila(visitados[k].getEstado(),c)*2+1)][media((columna(visitados[k].getValor(),c))*2+1,(columna(visitados[k].getEstado(),c))*2+1)]=20
    return mat

'''Método que pasa de una matriz de objetos a una matriz de valores'''
def destransformaMatriz(matrizNodo,f):
    matriz=[]
    for i in range(len(matrizNodo)):
        matriz.append(([matrizNodo[i][0][0].getValor()],[matrizNodo[i][1][0].getValor()]))
    return matriz

'''Método que recorre el array de nodos e inicia el algoritmo de busqueda en los nodos no recorridos '''
def ciclos(V,E,prueba):
    for i in range(len(V)):
        if(V[i] not in prueba):
            prueba2 = primeroProf(V,E,i)
            prueba.extend(prueba2)

'''Método que convierte en paredes las casillas no recorridas por el algoritmo'''
def detectaCiclos(matrizAd2,f,c):
    for i in range(f):
        for j in range(c):
            if(matrizAd2[i*2+2][j*2+1]==15):
                plt.text(j*2+1,i*2+2,'cc',fontsize=10,color='black',verticalalignment='center',horizontalalignment='center')
            if(matrizAd2[i*2+1][j*2+2]==15):
                plt.text(j*2+2,i*2+1,'cc',fontsize=10,color='black',verticalalignment='center',horizontalalignment='center')
                
#*********************************************************************************************
#*********************************************************************************************
#*********************************************************************************************
#codigo3
'''Se inicializa la lista de nodos, la de ejes y las variables necesafrias para el funcinamiento del programa'''
V=[]
prueba=[]
p=10

'''Se pide al usuario las variables que se utilizarán para la creación del laberinto'''
f = int(input("Introduce las filas: "))
c = int(input("Introduce las columnas: "))
while(p<0 or p>1):
    p = float(input("Introduce la probabilidad con valor entre 0 y 1: "))
s = int(input("Introduce la semilla: "))

'''Se llama a los metodos necesarios en orden'''
E = generaLaberinto(V,f,c,p,s)
igualar(V,E)
ordenado=primeroProf(V,E,0)
ciclos(V,E,ordenado)
Eprima=destransformaMatriz(E,len(E))
matriz = recorre(ordenado, Eprima, f, c,0)
detectaCiclos(matriz,f,c)

'''Se impime la matriz mediante un mapa de calor'''
plt.imshow((matriz),cmap="nipy_spectral",origin='upper')
plt.colorbar()
plt.show()