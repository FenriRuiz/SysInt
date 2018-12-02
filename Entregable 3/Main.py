import json
import time

from Frontera import Frontera
from NodoArbol import NodoArbol
from Problema import Problema

BFS = 1
DFS = 2
DFS_IT = 3
COST = 4
VORAZ = 5
A = 6

def heuristica(nodoSucesor):
    list_distancias = []
    for n in nodoSucesor.listaPendientes:
        list_distancias.append(prob.distance(nodoSucesor.nodoActual, n))
    if not(list_distancias):
        return 0
    return min(list_distancias) 

def calcularF(estrategia, coste, profundidad, nodoSucesor):
    if estrategia == DFS:
        return -(profundidad)
    elif estrategia == BFS:
        return float(profundidad)
    elif estrategia == COST:
        return coste
    elif estrategia == VORAZ:
        return heuristica(nodoSucesor)
    elif estrategia == A:
        return coste + heuristica(nodoSucesor)

def creaListaNodosArbol(listaSucesiones, nodoActual, profMax, estrategia):
    listNodosArbol = []
    for sucesion in listaSucesiones:
        profundidad = nodoActual.profundidad + 1
        if profundidad <= profMax:
            #print("[NODO ACTUAL]: " + sucesion[1].nodoActual)
            coste = float(nodoActual.costoCamino) + float(sucesion[2])
            f = calcularF(estrategia, coste, profundidad, sucesion[1])
            nodoNuevo = NodoArbol(nodoActual, sucesion[1], profundidad, coste, f)
            listNodosArbol.append(nodoNuevo)
    return listNodosArbol

def recorreNodoPadre(nodo):
    if nodo != None:
        recorreNodoPadre(nodo.nodoPadre)
        print(nodo.accion + "\n")
        print('\nEstoy en ' + nodo.estado.nodoActual + " tengo que visitar" +
              str(nodo.estado.listaPendientes))

def creaSolucion(nodoActual, numNodos):
    recorreNodoPadre(nodoActual)
    print('Nodos generados-->' + str(numNodos))
    print('Profundidad-->' + str(nodoActual.profundidad))
    print('Costo-->' + str(nodoActual.costoCamino))
    return True

def busquedaAcotada(prob, estrategia, profMax):
    frontera = Frontera()
    nodoInicial = NodoArbol(None, prob.estadoInicial, 0, 0, 0)
    listVisitados = []
    frontera.insert(nodoInicial)
    solucion = False

    while (solucion == False) and (not frontera.isEmpty()):
        nodoActual = frontera.delete()
        listVisitados.append((nodoActual.estado.identificador, nodoActual.f))
        #print("\n[ACCION] "+nodoActual.accion)
        print("[Pendientes] "+ str(nodoActual.estado.listaPendientes))

        if prob.esObjetivo(nodoActual.estado):
            solucion = True
        else:
            listaSucesiones = prob.espacioEstados.sucesores(nodoActual.estado)
            #Metodo que crea nodos arboles por la lista de estados
            listaNodos = creaListaNodosArbol(listaSucesiones, nodoActual, profMax, estrategia)
            for n in listaNodos:
                if not(any(n.estado.identificador == nodoRecorrido[0] for nodoRecorrido in listVisitados)) or any(n.f < nodoRecorrido[1] for nodoRecorrido in listVisitados):
                    frontera.insert(n)
    if solucion == True:
        return creaSolucion(nodoActual, len(listVisitados))
    else:
        return None

def busquedaIterativa(prob, estrategia, profMax, incProf):
    profActual = incProf
    Solucion = None
    while Solucion == None and profActual <= profMax:
        Solucion = busquedaAcotada(prob, estrategia, profActual)
        profActual = profActual + incProf
    return Solucion

def menu():
    print("Seleccione la estrategia de búsqueda a usar")
    print("\t 1 - Busqueda en ANCHURA")
    print("\t 2 - Busqueda en PROFUNDIDAD SIMPLE")
    print("\t 3 - Busqueda en PROFUNDIDAD ITERATIVA")
    print("\t 4 - Busqueda por COSTE")
    print("\t 5 - Busqueda por VORAZ")
    print("\t 6 - Busqueda por A*")
    print("\t 9 - Salir")

data = open("Anchuras.json", "r")
datos = data.read()
prob = Problema(json.loads(datos))
print("MENU")
while True:
    menu()
    opcionMenu = int(input(""))

    if opcionMenu == BFS:
        print("Digame la profundidad máxima")
        profMax = int(input(""))
        incProf = 1

        tComienzo = time.time()
        busquedaAcotada(prob, BFS, profMax, incProf)
        tFinal = time.time()

        print('Estrategia--> Anchura')
        print(tFinal - tComienzo)

    elif opcionMenu == DFS:
        print("Digame la profundidad máxima")
        profMax = int(input(""))
        incProf = 1
        tComienzo = time.time()
        busquedaAcotada(prob, DFS, profMax, incProf)
        tFinal = time.time()

        print('Estrategia--> Profundidad')
        print(tFinal - tComienzo)

    elif opcionMenu == DFS_IT:
        print("Digame la profundidad máxima")
        profMax = int(input(""))
        print("Digame la incremento en la profundidad")
        incProf = int(input(""))

        tComienzo = time.time()
        busquedaIterativa(prob, DFS_IT, profMax, incProf)
        tFinal = time.time()

        print('Estrategia--> Profundidad Iterativa')

    elif opcionMenu == COST:
        print("Digame la profundidad máxima")
        profMax = int(input(""))
        incProf = 1

        tComienzo = time.time()
        busquedaAcotada(prob, COST, profMax, incProf)
        tFinal = time.time()

        print('Estrategia--> Coste')
        print(tFinal - tComienzo)

    elif opcionMenu == VORAZ:
        print("Digame la profundidad máxima")
        profMax = int(input(""))
        incProf = 1

        tComienzo = time.time()
        busquedaAcotada(prob, VORAZ, profMax, incProf)
        tFinal = time.time()
        
        print('Estrategia--> Voraz')
        print(tFinal - tComienzo)

    elif opcionMenu == A:
        print("Digame la profundidad máxima")
        profMax = int(input(""))
        incProf = 1

        tComienzo = time.time()
        busquedaAcotada(prob, A, profMax, incProf)
        tFinal = time.time()

        print('Estrategia--> A*')
        print(tFinal - tComienzo)

    elif opcionMenu == 9:
        break