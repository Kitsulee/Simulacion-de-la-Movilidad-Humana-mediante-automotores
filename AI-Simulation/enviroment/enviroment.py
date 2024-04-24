from experta import Fact, Field
import sys
sys.path.append('../AI-Simulation')
from extra_classes.transportation import *
from data.bus_data import *

class Enviroment():

    def __init__(self, graph,busses):

        self.bus_states = graph.nodes
        self.busses = busses
        self.time=0
 
    def tick(self):

        self.time+=1

    def clone(self):

        env=Enviroment(Graph(),[])
        env.bus_states=self.bus_states.copy()
        env.busses=self.busses.copy()

        return env
