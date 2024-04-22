import sys
sys.path.append('../AI-Simulation')
from simulation.simulation import *


num_agents=2
num_iter=10

sim=Simulation()
sim.simulate(num_agents,num_iter)