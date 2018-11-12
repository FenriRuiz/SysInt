import networkx as nx 
import json
import os
import time

from Frontera import Frontera
from NodoArbol import NodoArbol
from Problema import Problema

BFS = 1
DFS = 2
DFS_IT = 3
COST = 4

def calcularF(estrategia,coste,profundidad):
    if(estrategia==DFS):
        return float(1/profundidad)
    elif(estrategia==BFS):
        return float(profundidad)
    elif(estrategia==COST):
        return coste

def creaListaNodosArbol(listaSucesiones,nodoActual,profMax,estrategia):
    listNodosArbol=[]
    for sucesion in listaSucesiones:
        profundidad = nodoActual.profundidad+1
        coste = float(nodoActual.costoCamino) + float(sucesion[2])
        f = calcularF(estrategia,coste, profundidad)
        
        nodoNuevo = NodoArbol(nodoActual, sucesion[1], profundidad, coste, f)
        
        listNodosArbol.append(nodoNuevo)
    
    return listNodosArbol
def creaSolucion(nodoActual,numNodos):
    
    while not(nodoActual.nodoPadre==None):
        print(nodoActual.accion)
    print('Nodos generados-->'+str(numNodos))
    print('Profundidad-->'+str(nodoActual.profundidad))
    print('Costo-->'+str(nodoActual.costoCamino))  
    return True

def busquedaAcotada(prob,estrategia,profMax):
    frontera=Frontera()
    nodoInicial=NodoArbol(None,prob.estadoInicial,0,0,0)
    listCaminoNodos=[]
    frontera.insert(nodoInicial)
    solucion=False

    while (solucion==False) and (not frontera.isEmpty()):
        nodoActual=frontera.delete()
        listCaminoNodos.append(nodoActual)
        #print("\n[ACCION] "+nodoActual.accion)

        print("[Pendientes] "+ str(nodoActual.estado.listaPendientes))
        if(prob.esObjetivo(nodoActual.estado)):
            solucion=True
            #frontera.frontera=[]
        else:
            listaSucesiones = prob.espacioEstados.sucesores(nodoActual.estado)
            listaNodos= creaListaNodosArbol(listaSucesiones,nodoActual,profMax,estrategia) #Metodo que crea nodos arboles por la lista de estados
            for n in listaNodos:
                if (not(any(n.estado.nodoActual== nodoRecorrido.estado.nodoActual for nodoRecorrido in listCaminoNodos))) or any(n.f < nodoRecorrido.f for nodoRecorrido in listCaminoNodos) :
                    frontera.insert(n)
    if (solucion==True):
        return creaSolucion(nodoActual,len(listCaminoNodos))
    else :
        return None


def busqueda(prob,estrategia,profMax,incProf):
    profActual=incProf
    Solucion=False
    while Solucion==False and (profActual <= profMax):
        Solucion=busquedaAcotada(prob,estrategia,profActual)
        profActual=profActual+incProf
    return Solucion

def menu():
    #os.system('clear')
    print("Seleccione la estrategia de búsqueda a usar")
    print("\t 1 - Busqueda en ANCHURA")
    print("\t 2 - Busqueda en PROFUNDIDAD SIMPLE")
    print("\t 3 - Busqueda en PROFUNDIDAD ITERATIVA")
    print("\t 4 - Busqueda por COSTE")
    print("\t 9 - Salir")


data=open("fichero.json","r")
datos=data.read()
prob=Problema(json.loads(datos))
print("MENU")
while True:
    menu()

    opcionMenu = int(input(""))
    if opcionMenu == BFS:
        print("Digame la profundidad máxima")
        profMax = int(input(""))
        incProf = 1
        ts=time.time()
        busqueda(prob,BFS,profMax,incProf)
        print('Estrategia--> Anchura')
        tf=time.time()
        print(tf-ts)
    elif opcionMenu == DFS:
        print("Digame la profundidad máxima")
        profMax = int(input(""))
        incProf = 1
        ts=time.time()
        busqueda(prob,DFS,profMax,incProf)
        tf=time.time()
        print('Estrategia--> Profundidad')
        print(tf-ts)
    elif opcionMenu == DFS_IT:
        print("Digame la profundidad máxima")
        profMax = int(input(""))
        print("Digame la incremento en la profundidad")
        incProf = input("")
        #busqueda(prob,DFS_IT,profMax,incProf)
        print('Estrategia--> Profundidad Iterativa')
    elif opcionMenu == COST:
        print("Digame la profundidad máxima")
        profMax = int(input(""))
        incProf = 1
        ts=time.time()
        busqueda(prob,COST,profMax,incProf)
        tf=time.time()
        print('Estrategia--> Coste')
        print(tf-ts)