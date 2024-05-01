import sys
sys.path.append('../Simulacion-de-la-Movilidad-Humana-mediante-automotores/AI-Simulation/')
from simulation.simulation import *

if __name__ == "__main__":

    num_agents = int(input("Ingrese el numero de agentes: "))
    num_iter = int(input("Ingrese el numero de iteraciones: "))

    sim=Simulation()
    sim.simulate(num_agents,num_iter)