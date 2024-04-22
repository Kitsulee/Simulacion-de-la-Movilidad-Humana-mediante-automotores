import json
import random
import sys
sys.path.append('../AI-Simulation/')
from extra_classes.graph import *


def read_json(file):
    with open(f'data/{file}.json', 'r') as File:
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
                            #d=euclidean_distance(node.x,node.y,bus_stops[stop[i+1]]['x'],bus_stops[stop[i+1]]['y'])
                            # h=random.randint(1,3)
                            node.add_edge((stop[i+1],h, [bus['name']]))

                        else:
                            index = next(j for j, edge in enumerate(node.edges) if edge[0] == stop[i+1])
                            node.edges[index][2].append(bus['name'])

                        if not any(edge[0] == (node.value, stop[i+1]) for edge in graph.edges):
                            #d=euclidean_distance(node.x,node.y,bus_stops[stop[i+1]]['x'],bus_stops[stop[i+1]]['y'])
                            # h=random.randint(1,3)
                            graph.add_edge(((node.value, stop[i+1]),h, [bus['name']]))
                        else:
                            index = next(j for j, edge in enumerate(graph.edges) if edge[0] == (node.value, stop[i+1]))
                            graph.edges[index][2].append(bus['name'])

                        if(bus['name'] not in node.takeble_busses):
                            node.takeble_busses.append(bus['name'])

                    except:
                        pass
            
        graph.add_node(node)

        # for bus in bus_stop['busses']:
        #     node.add_bus(bus)
        # for gazelle in bus_stop['gazelles']:
        #     node.add_gazelle(gazelle)
        # for person in bus_stop['people_waiting']:
        #     node.add_person_waiting(person)
        # for person in bus_stop['people_around']:
        #     node.add_person_around(person)

    for node in graph.nodes:
            for edge in node.edges:
                if edge[0] not in node.neighbors:
                    node.add_neighbor(graph.nodes[edge[0]])
    
    return graph

# def euclidean_distance(x1, y1, x2, y2):
#     return ((x1-x2)**2 + (y1-y2)**2)**0.5




# bus=read_json('bus_data')
# bus_stops=read_json('bus_stops_data')
# graph = create_graph(bus, bus_stops)
# print("a")
# x=graph.get_edge(1,2)
# y=graph.get_edge(2,1)
# print("a")
# z=graph.nodes[1].get_edge(2)
# print("a")