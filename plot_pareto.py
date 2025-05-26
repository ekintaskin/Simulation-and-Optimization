import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("pareto_output/pareto_stats.csv")

# Separate candidates and bests
candidates = df[df["type"] == "candidate"]
pareto = df[df["type"] == "best"]

# Plot maximum vs mean waiting time pareto plot
plt.figure(figsize=(8, 6))

plt.scatter(candidates["max_wait"].to_numpy(), candidates["mean_wait"].to_numpy(),alpha=0.3, label="Candidates", color="gray")
plt.plot(pareto["max_wait"].to_numpy(), pareto["mean_wait"].to_numpy(),'o-', label="Pareto Front", color="orange")
plt.xlabel("Maximum Waiting Time")
plt.ylabel("Mean Waiting Time")
plt.title("Pareto Front: Maximum vs Mean Waiting Time")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("pareto_output/pareto_max_vs_mean_wait.png", dpi=300)

# Plot mean waiting time vs request rate pareto plot
plt.figure(figsize=(8, 6))

plt.scatter(candidates["rate"].to_numpy(), candidates["mean_wait"].to_numpy(),alpha=0.3, label="Candidates", color="gray")
plt.plot(pareto["rate"].to_numpy(), pareto["mean_wait"].to_numpy(),'o-', label="Pareto Front", color="orange")
plt.xlabel("Request Rate")
plt.ylabel("Mean Waiting Time")
plt.title("Pareto Front: Request Rate vs Mean Waiting Time")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("pareto_output/pareto_request_rate_vs_mean_wait.png", dpi=300)


plt.show()
