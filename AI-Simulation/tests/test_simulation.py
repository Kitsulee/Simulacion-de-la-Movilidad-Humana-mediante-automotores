import sys
sys.path.append('../Simulacion-de-la-Movilidad-Humana-mediante-automotores/AI-Simulation/')
from simulation.simulation import *


num_agents=50
num_iter=80

sim=Simulation()
sim.simulate(num_agents,num_iter)