import sys
sys.path.append('../AI-Simulation')
from extra_classes.graph import *
from src.utils import *
from data.bus_data import *

bus=read_json('bus_data')
bus_stops=read_json('bus_stops_data')

graph = create_graph(bus, bus_stops)

start=graph.nodes[1]
goal=graph.nodes[8]

route=aStar(start,goal)

print("a")
# x=graph.get_edge(1,2)
# y=graph.get_edge(2,1)
# print("a")
# z=graph.nodes[1].get_edge(2)
# print("a")