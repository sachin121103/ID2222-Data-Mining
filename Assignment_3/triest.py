import random
from collections import defaultdict

class TriestBase:
    def __init__(self, M):
        self.M = M
        self.t = 0
        self.S = set()
        self.neighbors = defaultdict(set)
        self.tau_global = 0
        self.tau_local = defaultdict(int)
    
    def normalize(self, u, v):
        return (u, v) if u < v else (v, u)
    
    def add_to_sample(self, edge):
        u, v = edge
        
        # Should never hit this now, but defensive programming
        if edge in self.S:
            return
        
        self.S.add(edge)
        self.neighbors[u].add(v)
        self.neighbors[v].add(u)
    
    def remove_from_sample(self, edge):
        u, v = edge
        self.S.remove(edge)
        self.neighbors[u].remove(v)
        self.neighbors[v].remove(u)
    
    def update_counters(self, op, edge):
        u, v = edge
        shared = self.neighbors[u].intersection(self.neighbors[v])
        sign = +1 if op == "+" else -1
        
        for c in shared:
            self.tau_global += sign
            self.tau_local[u] += sign
            self.tau_local[v] += sign
            self.tau_local[c] += sign
    
    def sample_edge(self, edge):
        if self.t <= self.M:
            return True
        
        if random.random() < self.M / self.t:
            removed = random.choice(tuple(self.S))
            self.update_counters("-", removed)
            self.remove_from_sample(removed)
            return True
        
        return False
    
    def process_edge(self, edge):
        u, v = edge
        e = self.normalize(u, v)
        
        # Skip duplicates BEFORE incrementing counter
        if e in self.S:
            return
        
        # Only increment for unique edges
        self.t += 1
        
        if self.sample_edge(e):
            self.update_counters("+", e)
            self.add_to_sample(e)
    
    def estimate_global(self):
        if self.t <= self.M:
            return self.tau_global
        
        t = self.t
        M = self.M
        xi = max(1, (t * (t - 1) * (t - 2)) / (M * (M - 1) * (M - 2)))
        return xi * self.tau_global
    
    def get_sample(self):
        return self.S
    
    def get_triangle_estimate(self):
        return self.estimate_global()