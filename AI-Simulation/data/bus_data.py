import json
import random
import sys
sys.path.append('../Simulacion-de-la-Movilidad-Humana-mediante-automotores/AI-Simulation/')
from extra_classes.graph import *


def read_json(file):
    with open(f'AI-Simulation/data/{file}.json', 'r') as File:
        data = json.load(File)
    return data


def create_graph(busses, bus_stops):
    graph = Graph()
    for bus_stop in bus_stops:

        node = Bus_Stop(int(bus_stop['id']),bus_stop['municipality'],bus_stop['x'],bus_stop['y'],busses)

        for bus in busses:
            stop=bus['route']
            for i in range(len(stop)):
                if stop[i] == node.value:
                    try:

                        h=random.randint(1,3)
                        if not any(edge[0] == stop[i+1] for edge in node.edges):
                            node.add_edge((stop[i+1],h, [bus['name']]))

                        else:
                            index = next(j for j, edge in enumerate(node.edges) if edge[0] == stop[i+1])
                            node.edges[index][2].append(bus['name'])

                        if not any(edge[0] == (node.value, stop[i+1]) for edge in graph.edges):
                            graph.add_edge(((node.value, stop[i+1]),h, [bus['name']]))
                        else:
                            index = next(j for j, edge in enumerate(graph.edges) if edge[0] == (node.value, stop[i+1]))
                            graph.edges[index][2].append(bus['name'])

                        if(bus['name'] not in node.takeble_busses):
                            node.takeble_busses.append(bus['name'])

                    except:
                        pass
            
        graph.add_node(node)

    for node in graph.nodes:
            for edge in node.edges:
                if edge[0] not in node.neighbors:
                    node.add_neighbor(graph.nodes[edge[0]])
    
    return graph