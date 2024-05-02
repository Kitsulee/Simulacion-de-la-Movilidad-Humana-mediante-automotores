import sys
sys.path.append('../Simulacion-de-la-Movilidad-Humana-mediante-automotores/AI-Simulation/')
from simulation.simulation import *
import numpy as np
import matplotlib.pyplot as plt


def simple_simulation():
    num_agents = int(input("Ingrese el numero de agentes: "))
    num_iter = int(input("Ingrese el numero de iteraciones: "))

    sim=Simulation()
    sim.simulate(num_agents,num_iter)

def complex_simulation():
    num_agents = int(input("Ingrese el numero de agentes: "))
    num_iter = int(input("Ingrese el numero de iteraciones: "))
    num_sim = int(input("Ingrese el numero de simulaciones: "))

    stadistics = {}
    stadistics_busses = {}



    for i in range(num_sim):

        sim=Simulation()
        sim.simulate(num_agents,num_iter)
        if(i==0):
            for j in sim.places_names:
                stadistics[j]=0

            for j in sim.busses:
                stadistics_busses[j.name] = 0

        for j in sim.places_names:

            if(j not in stadistics):
                continue
            else:
                stadistics[j]+=(sim.stadistics[j])/num_iter

        for j in sim.busses:

            if(j.name not in stadistics_busses):
                continue
            else:
                stadistics_busses[j.name]+=(sim.stadistics_busses[j.name])/num_iter


    for i in stadistics:
        stadistics[i]=stadistics[i]/num_sim

    for i in stadistics_busses:
        stadistics_busses[i]=stadistics_busses[i]/num_sim

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(stadistics.keys(), stadistics.values())
    plt.title('Promedio de resultados por paradas')
    plt.show()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(stadistics_busses.keys(), stadistics_busses.values())
    plt.title('Promedio de resultados por buses')
    plt.show()

    reporter=Reporter([],stadistics,stadistics_busses)
    reporter.report_stadistics()

    
        


if __name__ == "__main__":

    print("Bienvenido a la simulación de la movilidad humana mediante automotores.")
    print("¿Qué tipo de simulación desea realizar?")
    print("1. Simulación simple")
    print("2. Simulación compleja")
    option = int(input("Ingrese el número de la opción deseada: "))

    if option == 1:
        simple_simulation()
    elif option == 2:
        complex_simulation()
    else:
        print("Opción inválida. Por favor, intente de nuevo.")