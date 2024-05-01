import sys
sys.path.append('../AI-Simulation')
from enviroment.enviroment import *
from random import choice
from src.utils import *

class Person():
    """
    Represents a person within the simulation environment.

    Attributes:
        id (int): Unique identifier for the person.
        home_dir (str): The person's home directory.
        budget (float): The person's available budget.
        curfew_start (int): The time (in hours within a 24-hour cycle) when the person's curfew starts.
        curfew_end (int): The time (in hours within a 24-hour cycle) when the person's curfew ends.
        visited_dir (dict): A dictionary storing visited routes, keyed by tuples of (current_location, goal). Values are the corresponding routes.
        current_location (str): The person's current location.
        desired_destiny (str, optional): The person's desired destination, if any.
        states (list): List of possible states the person can be in.
        current_state (str, optional): The person's current state.
        actions (list): List of possible actions the person can take.
    """
    def __init__(self, id, home_dir, budget, curfew_start, curfew_end):
        self.id = id
        self.home_dir = home_dir
        self.budget = budget
        self.curfew_start = curfew_start
        self.curfew_end = curfew_end
        self.visited_dir  = {}
        self.current_location = home_dir
        self.desired_destiny = home_dir
        self.temporal_destiny = home_dir
        self.states = ["waiting", "on_the_way", "making_stay"]
        self.current_state = "making_stay"
        self.actions = ["move", "stay", "return_home"]
        self.analized_busses_options = None
        self.current_route = None
        self.waiting_bus = None
        self.first_obs = True
        
        #observations
        self.obs_time = 0
        self.obs_buses = []
        self.obs_places = []
        self.obs_bus_stops = []

    def add_visited_dir(self, loc, goal, route):
        self.visited_dir[(loc, goal)] = route
        
    def get_busses(self, bus_stops, pair):
        edge = 0
        for bus_stop in bus_stops:
            if(bus_stop.value == pair[0].value):
                for ed in bus_stop.edges:
                    if(ed[0] == pair[1].value):
                        edge = ed
        busses = edge[2]    
        return busses

    def calculate_busses_time(self,farthest_nodes):
        buses_node_time = {}
        busses = list(farthest_nodes.keys())
        for bus_stop in self.obs_bus_stops:
            for bus in bus_stop.busses:
                if(bus.name in busses):

                    time = bus.calculate_time(self.current_location)

                    if bus.name in buses_node_time.keys():
                        
                        actual_value = buses_node_time[bus.name]
                        if(actual_value[2] > time):
                            buses_node_time[bus.name] = (actual_value[0], actual_value[1], time)

                    else:
                        buses_node_time[bus.name] = (farthest_nodes[bus.name][0], farthest_nodes[bus.name][1], time)

        return buses_node_time
                         
    def ponder_time_distance(self, buses_node_time):
        pondered_nodes = {}
        for bus, value in buses_node_time.items():
            node, index_on_route, time_to_arrive = value
            pondered_nodes[bus] = (index_on_route - time_to_arrive, node)
            
        sorted_pondered_nodes = dict(sorted(pondered_nodes.items(), key=lambda item:item[1][0], reverse=True))
        return sorted_pondered_nodes
    
    def choose_at_convenience(self, farthest_nodes):
        buses_node_time = self.calculate_busses_time(farthest_nodes)
        sorted_pondered_nodes = self.ponder_time_distance(buses_node_time)
        self.temporal_destiny = list(sorted_pondered_nodes.values())[0][1]
        selected_bus = list(sorted_pondered_nodes.keys())[0] 
        
        return selected_bus
            
    def choose_transportation(self, route):
        
        pos_in_route = 0
        for i in range(len(route)):
            if(route[i] == self.current_location):
                pos_in_route = i
        
        pair = (route[pos_in_route], route[pos_in_route+1])
        busses = self.get_busses(self.obs_bus_stops, pair)
        farthest_nodes = {}
        
        for bus in busses:
            for i in range(pos_in_route, len(route)):
                node = route[i]
                if(bus in node.takeble_busses):
                    farthest_nodes[bus] = (node, i)
                else:
                    break
                    
        self.analized_busses_options = farthest_nodes
        selected_bus = self.choose_at_convenience(farthest_nodes)
        self.waiting_bus = selected_bus
        return selected_bus        
            
    def get_in_line(self, transport):

        self.current_state = "waiting"
        for bus_stop in self.obs_bus_stops:
            if(bus_stop.value == self.current_location):
                bus_stop.people_to_add.append((self,transport))
                if self in bus_stop.people_around:
                    bus_stop.people_around.remove(self)

    
    def move(self):
        if (self.current_location, self.desired_destiny) in self.visited_dir.keys():

            route = self.visited_dir[(self.current_location, self.desired_destiny)]


        else:

            current,destiny=get_nodes_by_value(self.current_location, self.desired_destiny, self.obs_bus_stops)
            route = aStar(current,destiny)
            id_route_values=[]
            for i in route:
                id_route_values.append(i.value)

            self.add_visited_dir(self.current_location, self.desired_destiny, route)
            
        transport = self.choose_transportation(route)
        self.get_in_line(transport)
        
    
    def analize(self, enviroment: Enviroment):
        self.obs_bus_stops = enviroment.bus_states
        self.obs_time = enviroment.time

        enviroment.busses


        if(self.first_obs):
            for bus_stop in self.obs_bus_stops:
                self.obs_places.append(bus_stop.value)
                if(bus_stop.value == self.current_location):
                    self.obs_buses = bus_stop.people_waiting
            self.first_obs = False 
        else:
            for bus_stop in self.obs_bus_stops:
                if(bus_stop.value == self.current_location):
                    self.obs_buses = bus_stop.people_waiting

    def evaluate_decision(self):
        initial_bus = self.waiting_bus
        new_decision = self.choose_at_convenience(self.obs_bus_stops, self.analized_busses_options)
        if(initial_bus != new_decision):
            self.get_in_line(new_decision, self.obs_buses)
            self.waiting_bus = new_decision
            
    
    def decide(self):
        if(self.obs_time % 24 >= self.curfew_start and self.obs_time % 24 < self.curfew_end):
            if(self.current_location != self.home_dir and self.desired_destiny != self.home_dir):
                self.desired_destiny = self.home_dir
                self.move()
        elif(self.current_state == "making_stay"):
            if(self.desired_destiny == self.current_location):
                action = choice(self.actions)
                if(action == "move"):
                    self.desired_destiny = choice(self.obs_places)
                    if(self.desired_destiny == self.current_location):
                        self.current_state = "making_stay"
                    else:
                        self.move()
                elif(action == "return_home"):
                    if(self.current_location != self.home_dir):
                        self.desired_destiny = self.home_dir
                        self.move()
                    else:
                        self.current_state = "making_stay"
                else:
                    self.desired_destiny = self.current_location
                    self.waiting_bus = None
                    self.current_route = None
            else: 
                self.move()
        elif(self.current_state == "waiting"):
            actual_node = None
            for bus_stop in self.obs_bus_stops:
                if(bus_stop.value == self.current_location):
                    actual_node = bus_stop
                    for bus in actual_node.busses:
                        if(bus.type == self.waiting_bus):
                            self.evaluate_decision()
        


        

class Busy_Person(Person):
    """
     Represents a person with some routine, schedule and interest place.

     Attributes:
    interest_place: The place where the person must go.
    start_time: The time when the person must go to the interest place.
    end_time: The time when the person can leave.
        
     """
    def __init__(self, id, home_dir, budget,curfew_start,curfew_end, interest_place, start_time, end_time):
        super().__init__( id, home_dir, budget,curfew_start,curfew_end)

        self.interest_place = interest_place
        self.start_time = start_time
        self.end_time = end_time

    def decide(self):
        if(self.obs_time % 24 == self.start_time - 1):
            self.desired_destiny = self.interest_place
            if self.desired_destiny != self.current_location:
                self.move()
        elif(self.obs_time % 24 > self.start_time and self.obs_time % 24 < self.end_time):
            return
        else:
            super().decide()