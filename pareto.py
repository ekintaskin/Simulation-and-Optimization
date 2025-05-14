import numpy as np
import matplotlib.pyplot as plt

from optimization import Optimization
from simulation import Simulation
from stats import Stats

class ParetoPlotter:
    """
    Plot Pareto curve with conflicting objectives:
      - Hit ratio on ASNs (maximize)
      - Mean waiting time on ASNs (minimize)
    """
    def __init__(self, n_samples: int = 300):
        self.n_samples = n_samples
        self.sim       = Simulation()
        self.opt       = Optimization()

    def run(self) -> np.ndarray:
        data = []
        for _ in range(self.n_samples):
            # Generate configuration using swap_one heuristic
            movie_hashsets, _ = self.opt(
                optimization_fct_names=['swap_two'],
                num_optimization_iters=1,
                num_iters_per_optimization=50
            )

            reqs = self.sim.run(movie_hashsets=movie_hashsets)
            stats = Stats(reqs)
            waits = stats.get_waiting_time()

            hits = sum(1 for r in reqs if r.storage_id in ('ASN1', 'ASN2'))
            hit_ratio = hits / len(reqs) if len(reqs) > 0 else 0.0

            asn_waits = [r.get_waiting_time() for r in reqs
                         if r.storage_id in ('ASN1', 'ASN2') and isinstance(r.get_waiting_time(), (int, float))]
            mean_asn_wait = np.mean(asn_waits) if asn_waits else 0.0

            data.append((hit_ratio, mean_asn_wait))

        return np.array(data)

    @staticmethod
    def pareto_mask(points: np.ndarray) -> np.ndarray:
        n = len(points)
        mask = np.ones(n, dtype=bool)
        for i in range(n):
            h_i, w_i = points[i]

            better = (points[:,0] >= h_i) & (points[:,1] <= w_i)
            strict = (points[:,0] >  h_i) | (points[:,1] < w_i)
            if np.any(better & strict):
                mask[i] = False
        return mask

    def plot(self):
        pts = self.run()
        mask = self.pareto_mask(pts)
        pareto = pts[mask]

        order = np.argsort(pareto[:,0])
        pareto = pareto[order]

        plt.figure(figsize=(10, 6))
        plt.scatter(pts[:,0], pts[:,1], s=30, alpha=0.4, color='gray', label='All Points')
        plt.plot  (pareto[:,0], pareto[:,1], '-o', color='red', label='Pareto Front')

        plt.title('Local Storage Efficiency: Hit Ratio vs Mean ASN Waiting Time')
        plt.xlabel('Hit Ratio on ASNs')
        plt.ylabel('Mean Waiting Time on ASNs')
        plt.grid(alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    plotter = ParetoPlotter(n_samples=300)
    plotter.plot()