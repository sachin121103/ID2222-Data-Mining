import random

class ReservoirSampling:
    def __init__(self, M):
        self.M = M
        self.counter = 0
        self.sample_storage = []

    def add_edge(self, edge):
        self.counter += 1

        if len(self.sample_storage) < self.M:
            self.sample_storage.append(edge)
        
        else:
            r = random.random()
            threshold = self.M/self.counter

            if r < threshold:
                removed_int = random.randint(0, len(self.sample_storage)-1)
                self.sample_storage.pop(removed_int)
                self.sample_storage.append(edge)


