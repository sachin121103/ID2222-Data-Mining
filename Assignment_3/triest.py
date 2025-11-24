class TriestFD(TriestBaseClass):
    def __init__(self, M):
        super().__init__(M)
        self.s = 0       # number of active edges in graph
        self.di = 0      # unpaired sampled deletions
        self.do = 0      # unpaired non-sampled deletions

    def sample_edge(self, edge):
        # If no pending deletions --> reservoir mode
        if self.di + self.do == 0:
            if len(self.S) < self.M:
                return True

            return random.random() < self.M / self.t

        # Random pairing mode
        if random.random() < self.di / (self.di + self.do):
            self.di -= 1
            return True
        else:
            self.do -= 1
            return False

    def process(self, sign, edge):
        """Process + or - edges."""
        self.t += 1
        u, v = self.normalize(*edge)
        e = (u, v)

        if sign == "+":
            self.s += 1
            kept = self.sample_edge(e)

            if kept:
                self.update_counters("+", e)
                self.add_to_sample(e)

        else:  # deletion
            self.s -= 1
            if e in self.S:
                self.update_counters("-", e)
                self.remove_from_sample(e)
                self.di += 1
            else:
                self.do += 1

    # -----------------------------
    # Estimator ρ(t)
    # -----------------------------
    def estimate_global(self):
        M_t = len(self.S)
        if M_t < 3:
            return 0

        s = self.s
        d = self.di + self.do
        w = min(self.M, s + d)

        # compute κ(t)
        from math import comb
        denom = comb(s + d, w)
        κ = 1 - sum(comb(s, j) * comb(d, w - j) / denom for j in range(3))

        scale = (s*(s-1)*(s-2)) / (M_t*(M_t-1)*(M_t-2))
        return (self.tau_global / κ) * scale