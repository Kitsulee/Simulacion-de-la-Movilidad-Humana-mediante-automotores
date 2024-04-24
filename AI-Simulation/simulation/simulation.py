import random
import sys
sys.path.append('../AI-Simulation')
from agents.person import *
from data.bus_data import *  ######
from enviroment.enviroment import *
from pln.reporter import *


class Simulation:
    """A class to simulate the model.

    Attributes:
        agents (list): A list of agent objects.
        graph (Graph): A graph object.
        events (list): A list of event objects.
    """

    def __init__(self):
        """Initialize the simulation.

        Args:
            self (Simulation): The simulation object.

        Returns:
            None
        """
        self.agents = []
        self.graph = None
        self.events = []
        self.places = []
        self.busses = []
        self.bus_data = None #####

    def simulate(self, num_agents, num_iter):
        """Simulate the model.

        Args:
            self (Simulation): The simulation object.

        Returns:
            None
        """
        self._initialize(num_agents)
        self._run(num_iter)
        self._finalize()

    def _initialize(self, num_agents):
        """Initialize the simulation.

        Args:
            self (Simulation): The simulation object.

        Returns:
            None
        """
        self._create_graph()
        self._create_agents(num_agents)
        self._ubicate_agents()
        self._create_busses()
        self._ubicate_busses()
        #self._create_events()

    def _run(self, num_iter):

        enviroment=Enviroment(self.graph,self.busses)

        for i in range(num_iter):

            eliminated_busses = []

            for node in self.graph.nodes:

                for agent in node.people_around:####

                    agent.analize(enviroment)####
                    agent.decide()

                
                temp_eliminated_busses = []
                for bus in node.busses:####

                    eliminated_people = []

                    for passenger in bus.people:

                        if passenger.desired_destiny == node.value or passenger.temporal_destiny.value == node.value:
                            eliminated_people.append(passenger)
                            passenger.current_state = "making_stay"
                            passenger.current_location = node.value
                            node.people_around.append(passenger)#######

                    for passenger in eliminated_people:
                        bus.disembark_passenger(passenger)


                    embarked = []
                    for agent in node.people_waiting[bus.name]:
                        if(bus.board_passenger(agent)):

                            agent.current_state = "on_the_way" 
                            # bus.board_passenger(agent)
                            embarked.append(agent)
                    
                    for agent in embarked:
                        node.people_waiting[bus.name].remove(agent)########

                    removed=bus.move(self.graph) #####
                    if(removed):
                        temp_eliminated_busses.append(bus)

                eliminated_busses.append(temp_eliminated_busses)
                

                for people_list in node.people_waiting.values():
                    for agent in people_list:
                        agent.analize(enviroment)
                        agent.decide()

                for ppladd in node.people_to_add:
                    node.people_waiting[ppladd[1]].append(ppladd[0])

                node.people_to_add=[]


            ######
            j=0
            for nd in eliminated_busses:
                for bus in nd:
                    self.graph.nodes[j].busses.remove(bus)
                    self.graph.nodes[bus.location].busses.append(bus)
                j+=1

            ######

            event=enviroment.clone()

            self._create_events(i, event)####

            enviroment.tick()

    def _finalize(self):
        """Finalize the simulation.

        Args:
            self (Simulation): The simulation object.

        Returns:
            None
        """

        reporter=Reporter(self.events)
        reporter.report()

    def _create_agents(self, num_agents):
        """Create the agents.

        Args:
            self (Simulation): The simulation object.

        Returns:
            None
        """
        self.agents = []
        for i in range(num_agents):

            type= random.choice([0,1]) # 0 = person, 1 = busy_person
            budget = random.choice(["low", "high"]) 
            home_dir = random.choice(self.places) # home_dir is a place


            curfew_start = random.choice([23,24,1])
            curfew_end = random.randint(5,6)

            if type == 0:
                agent = Person(i,home_dir,budget,curfew_start,curfew_end)

            elif type == 1:

                temp_places=self.places.copy()
                temp_places.remove(home_dir)
                interest_place = random.choice(temp_places)

                start_time = random.randint(7,9)
                end_time = random.randint(14,16)

                agent = Busy_Person(i,home_dir,budget,curfew_start,curfew_end,interest_place,start_time,end_time)

            self.agents.append(agent)

    def _create_busses(self):
        """Create the busses.

        Args:
            self (Simulation): The simulation object.

        Returns:
            None
        """

        ids=0
        for i in self.bus_data:

            rnd=random.randint(1,2) ######

            for j in range(rnd):
                rnd=random.randint(0,len(i['route'])-1)
                bus = Bus(ids,i['name'],i['route'],"bus", i['capacity'], i['route'][rnd],rnd)
                self.busses.append(bus)
                ids+=1    

    def _ubicate_agents(self):
        """Ubicate the agents.

        Args:
            self (Simulation): The simulation object.

        Returns:
            None
        """
        for agent in self.agents:
            self.graph.nodes[int(agent.home_dir)].people_around.append(agent) ####people waiting?

    def _ubicate_busses(self):
        """Ubicate the busses.

        Args:
            self (Simulation): The simulation object.

        Returns:
            None
        """
        for bus in self.busses:
            self.graph.nodes[int(bus.location)].busses.append(bus)

    def _create_graph(self):
        """Create the graph.

        Args:
            self (Simulation): The simulation object.

        Returns:
            None
        """

        bus_data=read_json('bus_data')
        self.bus_data = bus_data  #####
        bus_stops_data=read_json('bus_stops_data')
        for stops in bus_stops_data:
            self.places.append(int(stops['id']))
        graph = create_graph(bus_data, bus_stops_data)
        self.graph = graph

    def _create_events(self, num_event, enviroment):
        """Create the events.

        Args:
            self (Simulation): The simulation object.

        Returns:
            None
        """

        text=f"Evento occurrido a las {num_event} horas."

        for env in enviroment.bus_states:
            count=0
            for que in env.people_waiting.values():
                count+=len(que)
                # for ppl in que:
                #     count+=len(ppl)
            
            count+=len(env.people_around)

            text+=f"Habian {count} personas en la parada de buses de {env.municipality}."

        for bus in enviroment.busses:

            count=len(bus.people)
            text+=f"Habian {count} personas en un bus {bus.name}."

        self.events.append(text)
        # self.events.append(Event(num_event, enviroment))####
        