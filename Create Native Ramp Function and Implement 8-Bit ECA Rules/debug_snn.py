import sys
sys.path.insert(0,'/home/ubuntu')
from soliton_eca import *
neurons=[LIFNeuron(i,tau=10,threshold=1,refractory=2) for i in range(4)]
n=SolitonSNN(neurons,(Connection(2,3,1,delay=2),))
n.inject((AERSpike(0,0,2,1,.6),AERSpike(0,1,2,1,.6)))
print(n.run())
print(n.delivered)
print(n.weights())
print(n.neurons[3].voltage)
