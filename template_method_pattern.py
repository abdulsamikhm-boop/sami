from abc import ABC, abstractmethod

class AIModule(ABC):
    @abstractmethod
    def forward(self, x):
        pass

    def __call__(self, x):
        print("Framework Hooks Running (e.g., logging gradients)...")
        return self.forward(x)

class LinearLayer(AIModule):
    def __init__(self, weights):
        self.weights = weights 
        
    def forward(self, x):
        return x * self.weights

model = LinearLayer(weights=0.5)
output = model(10) 