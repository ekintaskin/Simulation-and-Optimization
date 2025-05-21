import os
import sys
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from optimization import Optimization


def run_optimization(
    num_runs=10,
):
    """
    Test the optimization class.
    """
    optimization_fct_names = [
        "random",
        "replace_one", 
        "replace_two", 
        "replace_three",
        "swap_one", 
        "swap_two",
        "swap_three",
        "replace_one_fill", 
        "replace_two_fill", 
        "replace_three_fill",
        "remove_one", 
        "remove_two",
        "remove_three",
    ]
    start_time = time.time()
    best_hashsets = []
    best_waiting_times = []
    for i in range(num_runs):

        optimization = Optimization(
            print_results=True,
            random_seed=i,
        )
        best_hashset, waiting_time_best = optimization(
            optimization_fct_names=optimization_fct_names,
            num_optimization_iters=100, 
            num_iters_per_optimization=250,
            metric_fct=np.mean,
            tolerance=0.01,
            use_control_variate=True,
            use_mean_rate_constraint=True,
            save_optimization_fct_history=True,
            choose_optimization_fct_randomly=True,
            decreasing_tolerance=True,
        )
        best_hashsets.append(best_hashset)
        best_waiting_times.append(waiting_time_best)

        print(f"\n\nFinal hashset: {best_hashset}")
        print(f"Final waiting time: {waiting_time_best:.2f}")

    print(f"\n\nBest hashsets: {best_hashsets}")
    print(f"Best waiting times: {best_waiting_times}")
    print(f"Average time per optimization: {(time.time() - start_time) / num_runs:.3f} seconds")
    print(f"Average waiting time: {np.mean(best_waiting_times):.3f}")
    print(f"Standard deviation of waiting time: {np.std(best_waiting_times):.3f}")
    print(f"Overall best hashset: {best_hashsets[np.argmin(best_waiting_times)]}")
    print(f"Overall best waiting time: {np.min(best_waiting_times):.3f}")

def analyze_optimization_fct_history():
    """
    Analyze the optimization function history.
    """
    # df = pd.read_csv("plots/optimization_fct_history.csv")
    df = pd.read_csv("optimization_constraint_on_fct_history.csv")
    df = df.rename(columns={"# iteration": "iteration"})
    df = df.rename(columns={" function_name": "function_name"})
    df = df.rename(columns={" metric_value": "metric_value"})


    # sort df according to the column iteration
    df = df.sort_values(by=["iteration"])
    df = df.reset_index(drop=True)

    # divide the df into 3 groups according to the iteration
    rs = [
        (0, 100),
        (0, 32),
        (33, 65),
        (66, 99),
    ]

    fct_colors = {
        "random": "grey",
        "replace_one": "yellow",
        "replace_two": "orange",
        "replace_three": "darkorange",
        "swap_one": "pink",
        "swap_two": "magenta",
        "swap_three": "darkmagenta",
        "replace_one_fill": "lime",
        "replace_two_fill": "green",
        "replace_three_fill": "darkgreen",
        "remove_one": "darkblue",
        "remove_two": "blue",
        "remove_three": "cyan",
    }

    fig, axs = plt.subplots(1, 2, figsize=(12, 8), tight_layout=True)
    axs = axs.flatten()

    ax = axs[0]
    ax.scatter(
        df["iteration"],
        df["metric_value"],
        c=[fct_colors[fct[1:]] for fct in df["function_name"]],
        s=30,
    )
    ax.hlines(
        y=10,
        xmin=df["iteration"].min(),
        xmax=df["iteration"].max(),
        color="black",
        linestyle="--",
        label="10s threshold",
    )
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Mean Waiting Time [s]")
    ax.set_title("Mean Waiting Time vs Iteration")
    ax.set_xlim(0, df["iteration"].max())
    ax.set_ylim(9, 16)

    # add legend
    handles = []
    for fct in fct_colors.keys():
        handles.append(plt.Line2D([0], [0], marker='o', color='w', label=fct, markerfacecolor=fct_colors[fct], markersize=10))
    ax.legend(handles=handles, title="Function name", loc='upper right')


    thrs = [10]
    for i, thr in enumerate(thrs):
        df_thr = df[df["metric_value"] < thr]

        df_count = df_thr["function_name"].value_counts()
        df_count = df_count / df_count.sum()

        df_count = df_count.sort_index()
        colors = [fct_colors[fct[1:]] for fct in df_count.index]

        ax = axs[i+1]
        ax.pie(df_count, labels=df_count.index, colors=colors, autopct='%1.1f%%', startangle=140)
        ax.set_title(f"Methods below {thr}s mean waiting time")
        ax.axis('equal')

    plt.show()

def main():
    """
    Main function to run the optimization and analyze the results.
    """
    # run_optimization(
    #     num_runs=10,
    # )
    analyze_optimization_fct_history()


if __name__ == "__main__":
    main()