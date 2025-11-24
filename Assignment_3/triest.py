import random
from collections import defaultdict

class TriestBase:
    
    def __init__(self, M):
        self.M = M                      # sample size
        self.t = 0                      # processed edges
        self.S = set()                  # sampled edges
        self.neighbors = defaultdict(set)

        self.tau_global = 0             # global triangle count estimator
        self.tau_local = defaultdict(int)

    # ----------------------------------------------------------
    # Utility functions
    # ----------------------------------------------------------

    def normalize(self, u, v):
        """Normalize edge to ensure consistent representation (u < v)"""
        return (u, v) if u < v else (v, u)

    def add_to_sample(self, edge):
        u, v = edge
        self.S.add(edge)
        self.neighbors[u].add(v)
        self.neighbors[v].add(u)

    def remove_from_sample(self, edge):
        u, v = edge
        self.S.remove(edge)
        self.neighbors[u].remove(v)
        self.neighbors[v].remove(u)

    # ----------------------------------------------------------
    # Counter Updates
    # ----------------------------------------------------------

    def update_counters(self, op, edge):
        """
        Update global and local triangle counters when an edge is added (+)
        or removed (-) from the sample.
        """
        u, v = edge
        shared = self.neighbors[u].intersection(self.neighbors[v])

        sign = +1 if op == "+" else -1

        # Each triangle (u,v,c) should be counted exactly once
        for c in shared:
            self.tau_global += sign
            self.tau_local[u] += sign
            self.tau_local[v] += sign  
            self.tau_local[c] += sign

    # ----------------------------------------------------------
    # Reservoir Sampling Rule
    # ----------------------------------------------------------

    def sample_edge(self, edge):
        if self.t <= self.M:
            return True  # always insert until reservoir is full

        # keep edge w.p. M / t
        if random.random() < self.M / self.t:
            # Remove a random edge BEFORE adding the new one
            removed = random.choice(tuple(self.S))
            
            # Update counters for removal BEFORE actually removing
            self.update_counters("-", removed)
            self.remove_from_sample(removed)
            
            return True

        return False

    # ----------------------------------------------------------
    # Main API: process one edge (u,v)
    # ----------------------------------------------------------

    def process_edge(self, edge):
        """
        Process new edge in the insertion-only stream.
        """
        self.t += 1

        u, v = edge
        e = self.normalize(u, v)  # Using instance method

        if self.sample_edge(e):
            self.add_to_sample(e)
            self.update_counters("+", e)

    # ----------------------------------------------------------
    # Return estimate
    # ----------------------------------------------------------

    def estimate_global(self):
        """
        Return unbiased estimate of number of triangles in the graph.
        """
        if self.t <= self.M:
            return self.tau_global  # exact

        t = self.t
        M = self.M

        xi = max(1, (t * (t - 1) * (t - 2)) / (M * (M - 1) * (M - 2)))
        return xi * self.tau_global

    def get_sample(self):
        """Return current sample of edges"""
        return self.S

    def get_triangle_estimate(self):
        """Convenience method that returns the global estimate"""
        return self.estimate_global()