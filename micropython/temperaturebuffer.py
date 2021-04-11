# Ring buffer used to hold temperature values
class TemperatureBuffer:
    
    def __init__(self, capacity):
        self.capacity = capacity
        # Start with all values at 0
        self.buffer = [0] * capacity
        self.tail = -1
    
    def addValue(self, value):
        self.tail = (self.tail+1) % self.capacity
        self.buffer[self.tail] = value
        
    def getValues(self):
        if (self.tail == 0):
            return self.buffer
        
        return self.buffer[self.tail:]+self.buffer[0:self.tail]


        