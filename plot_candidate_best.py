import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("pareto_output/pareto_stats.csv")

# Separate candidates and bests
candidates = df[df["type"] == "candidate"]
best = df[df["type"] == "best"]

# Plot maximum vs mean waiting time pareto plot
plt.figure(figsize=(8, 6))

plt.scatter(candidates["max_wait"].to_numpy(), candidates["mean_wait"].to_numpy(),alpha=0.3, label="Candidates", color="gray")
plt.plot(best["max_wait"].to_numpy(), best["mean_wait"].to_numpy(),'o-', label="Best", color="orange")
plt.xlabel("Maximum Waiting Time")
plt.ylabel("Mean Waiting Time")
plt.title("Maximum vs Mean Waiting Time")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("pareto_output/max_vs_mean_wait.png", dpi=600)

# Plot mean waiting time vs request rate pareto plot
plt.figure(figsize=(8, 6))

plt.scatter(candidates["rate"].to_numpy(), candidates["mean_wait"].to_numpy(),alpha=0.3, label="Candidates", color="gray")
plt.plot(best["rate"].to_numpy(), best["mean_wait"].to_numpy(),'o-', label="Best", color="orange")
plt.xlabel("Request Rate")
plt.ylabel("Mean Waiting Time")
plt.title("Request Rate vs Mean Waiting Time")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("pareto_output/request_rate_vs_mean_wait.png", dpi=600)

plt.show()

# Check Pareto dominance
def is_pareto_efficient(points):
    is_efficient = np.ones(points.shape[0], dtype=bool)
    for i, c in enumerate(points):
        if is_efficient[i]:
            is_efficient[is_efficient] = np.any(points[is_efficient] < c, axis=1) | np.all(points[is_efficient] == c, axis=1)
            is_efficient[i] = True
    return is_efficient

objectives = candidates[["max_wait", "min_wait"]].to_numpy()
pareto_mask = is_pareto_efficient(objectives)
pareto_front = candidates[pareto_mask].copy()

pareto_front.sort_values(by="max_wait", inplace=True)

plt.figure(figsize=(8, 6))
plt.scatter(candidates["max_wait"].to_numpy(), candidates["min_wait"].to_numpy(), alpha=0.3, label="Candidates", color="gray")
plt.plot(pareto_front["max_wait"].to_numpy(), pareto_front["min_wait"].to_numpy(), 'o-', label="Pareto Front", color="orange")

plt.xlabel("Maximum Waiting Time")
plt.ylabel("Minimum Waiting Time")
plt.title("Pareto Front: Maximum vs Minimum Waiting Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("pareto_output/pareto_max_min_pareto_front.png", dpi=300)
plt.show()