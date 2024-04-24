import queue

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_edge(self, start, end):
        try:
            return next(edge for edge in self.edges if edge[0] == (start, end))
        except:
            return None

    def __str__(self):
        return f'Graph with {len(self.nodes)} nodes and {len(self.edges)} edges'

    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.nodes)
    
    def __getitem__(self, key):
        return self.nodes[key]
    
    def __iter__(self):
        return iter(self.nodes)
    
    def __contains__(self, item):
        return item in self.nodes
    
class Node:
    def __init__(self, value):
        self.value = value
        self.edges = []
        self.neighbors = []
        self.G=0
        self.H=0
        self.parent=None
        
    def add_edge(self, edge):
        self.edges.append(edge)

    def get_edge(self,goal):
        try:
            return next(edge for edge in self.edges if edge[0] == goal)
        except:
            return None

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
    
    def __str__(self):
        return f'Node({self.value})'
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.edges)
    
    def __getitem__(self, key):
        return self.edges[key]
    
    def __iter__(self):
        return iter(self.edges)
    
    def __contains__(self, item):
        return item in self.edges
    
class Bus_Stop(Node):
    def __init__(self, value, municipality,x,y,busses):
        super().__init__(value)
        self.municipality = municipality
        self.x=x
        self.y=y
        self.busses = []
        self.gazelles = []
        self.people_waiting = self.init_people_waiting(busses)
        self.people_around = []
        self.takeble_busses = []
        self.people_to_add = []

    def init_people_waiting(self,busses):
        people_waiting = {}

        for bus in busses:
            people_waiting[bus['name']] = []
        return people_waiting
        
    def add_bus(self, bus):
        self.busses.append(bus)
        
    def add_gazelles(self, gazelle):
        self.gazelles.append(gazelle)