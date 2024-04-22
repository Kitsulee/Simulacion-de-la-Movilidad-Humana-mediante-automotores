import sys
sys.path.append('../AI-Simulation')
#from excep import *

class Transportation():

    def __init__(self, id,name, route, type, capacity,location,index):
        self.id = id
        self.name= name
        self.route = route
        self.type = type
        self.capacity = capacity
        self.__num_passengers = 0
        self.is_full = False
        self.is_in_way = False
        self.location= location
        self.index = index
        self.people = []
        self.course = 0


    # def complete_route(self,route):
        
    #     tmp=route.copy()
    #     tmp.reverse()
    #     tmp=tmp[1: len(tmp)-1]
    #     return route+tmp

    def board_passenger(self, passenger):
        if(not self.is_full):
            self.__num_passengers+= 1
            self.people.append(passenger)
            if(self.__num_passengers == self.capacity):
                self.is_full = True
            return True
        
        return False
        # else:
        #     raise Is_Full_Exception
        
    def disembark_passenger(self,passenger):
        self.__num_passengers-=1
        self.people.remove(passenger)
        if(self.__num_passengers < self.capacity):
            self.is_full = False

    def move(self,graph):

        time_left = 0

        for i in graph.nodes[self.location].edges:
            
            if (len(self.route)==self.index+1): ###########
                continue


            if(self.route[self.index+1] == i[0]):####
                time_left= i[1]

        if(self.course < time_left):
            self.course+=1 #time to travel
            return False
            
        else:
            
            self.course = 0
            self.index+=1
            
            if(self.index == len(self.route)):
                #self.is_in_way = False
                self.index = 0
                #graph.nodes[self.location].busses.remove(self)
                self.location = self.route[self.index]
                #graph.nodes[self.location].busses.append(self)

            else:

                #graph.nodes[self.location].busses.remove(self)
                self.location = self.route[self.index]
                #graph.nodes[self.location].busses.append(self)

            return True


    def calculate_time(self,bus_stop): #####
        time=0
        i=self.index
        while(self.route[i] != bus_stop):
            time+=1
            i+=1
            if(i == len(self.route)):
                i=0
        return time


        
class Bus(Transportation):

    def __init__(self, id,name, route, type, capacity,location,index):
        super().__init__(id,name, route, "bus", capacity,location,index)

class Gazelle(Transportation):

    def __init__(self, id,name, route, type, capacity,location,index):
        super().__init__(id,name, route, "gazelle", capacity,location,index)
    

        