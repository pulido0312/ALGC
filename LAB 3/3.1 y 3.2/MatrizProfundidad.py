import numpy as np

import seaborn as sb

import matplotlib.pyplot as plt

import time

from SyncRNG import SyncRNG

''' Creacion de la clase nodo.
    Pide que se ingrese el valor del nodo(id del nodo) y un estado(id del nodo padre) para la inicialización de un nodo.
    Los demas metodos son los set y get de estos atributos'''
class Nodo:
    def __init__(self,valor,estado):
        self.valor = valor
        self.estado = estado
    def setValor(self,valor):
        self.valor = valor
    def setEstado(self,estado):
        self.estado=estado
    def getValor(self):
        return self.valor
    def getEstado(self):
        return self.estado

''' Metodo para hallar la fila de un nodo a traves de su id y el numero de columnas total'''
def fila(ind, c):
    return int(ind/c)
''' Metodo para hallar la columna de un nodo a traves de su id y el numero de columnas total'''
def columna(ind, c):
    return int(ind%c)
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
    E = np.zeros(((f*c),(f*c)))
    ran = SyncRNG(seed = semilla)
    for i in range(f):
        for j in range(c):
            V.append(Nodo(id(i,j,c),-1))
            if(i>0 and ran.rand()<prob):
                E[id(i,j, c)][id(i-1,j,c)]=1
                E[id(i-1,j, c)][id(i,j,c)]=1
            if(j>0 and ran.rand()<prob):
                E[id(i,j, c)][id(i,j-1,c)]=1
                E[id(i,j-1, c)][id(i,j,c)]=1
    return E
 
''' Metodo utilizado para recorrer el grafo. En este caso es el algoritmo primero en profundidad. Retorna los nodos visistados.
Si se elige primero en anchura la pila actuará como una cola'''
def primeroProf(V,E,flag):
    visitados=[]
    pila=[]
    pila.append(V[0])
    while pila:
        if(flag==1):                                                         
            actual=pila.pop()                                               
        else:
            actual=pila.pop(0)
        if actual not in visitados:
            visitados.append(actual)
            if(V[0].getEstado()==-1):
                V[0].setEstado(actual.getValor())
        for i in range(len(V)):
            if V[i] not in visitados and E[actual.getValor()][V[i].getValor()]==1:
                pila.append(V[i])
                V[i].setEstado(actual.getValor())
    return visitados

'''Método que recorre la lista de ejes y el array de nodos para añadir valores a una matriz que será pintada en un heatmap'''
def recorre(visitados,E, f, c):
    mat=[]
    mat=inic(f,c)
    for i in range(f):
        for j in range(c):
            mat[i*2+1][j*2+1] = 10
            if(i<f-1 and E[id(i,j, c)][id(i+1,j,c)] != 0):
                mat[i*2+2][j*2+1] = 10
            if(j<c-1 and E[id(i, j, c)][id(i, j+1, c)] != 0):
                mat[i*2+1][j*2+2] = 10

    for k in range(len(visitados)):
        mat[(fila(visitados[k].getValor(),c)*2+1)][(columna(visitados[k].getValor(),c)*2+1)]=20
        mat[media(fila(visitados[k].getValor(),c)*2+1,fila(visitados[k].getEstado(),c)*2+1)][media((columna(visitados[k].getValor(),c))*2+1,(columna(visitados[k].getEstado(),c))*2+1)]=20       
    return mat

#*********************************************************************************************
#*********************************************************************************************
#*********************************************************************************************
#cod2
V = []
prueba=[]
p=10
flag= 1
'''Se pide al usuario las variables que se utilizarán para la creación del laberinto'''
f = 50#int(input("Introduce las filas: "))
c = 50#int(input("Introduce las columnas: "))
while(p<0 or p>1):
    p = float(input("Introduce la probabilidad con valor entre 0 y 1: "))
s = int(input("Introduce la semilla: "))
#while(flag!=0 and flag!=1):
#    flag = int(input("Para usar primero en profundidad introduzca un 1, para primero en anchura introduzca un 0: "))

'''Se llama a los metodos necesarios en orden'''
E=generaLaberinto(V,f,c,p,s)
t1=time.time()
ordenada=primeroProf(V,E,flag)
t2=time.time()
mat = recorre(ordenada, E, f, c)
print(t2-t1)
'''Se impime la matriz mediante un mapa de calor'''
plt.imshow(mat, cmap='viridis', origin='upper')
plt.colorbar()
plt.show()