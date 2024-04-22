class clase:

    
    def __init__(self, id):
        self.ft = True
        self.id=self.metodo()
        

    def metodo(self):
        if(self.ft): 
            self.ft = False
            return 1
        else:
            return 2




lista=[]
a=clase(1)

b=a.id

c=clase(2)
d=c.id
e=a.id

lista.append(a)
a.id=2
lista.append(a)

for i in lista:
    print(i.id)