import os
import sys
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

    for i in range(num_runs):

        optimization = Optimization(
            print_results=True,
            random_seed=i,
        )
        best_hashset, waiting_time_best = optimization(
            optimization_fct_names=optimization_fct_names,
            num_optimization_iters=10, 
            num_iters_per_optimization=100,
            metric_fct=np.mean,
            use_control_variate=True,
            use_mean_rate_constraint=False,
            save_optimization_fct_history=True,
            choose_optimization_fct_randomly=True,
        )

        print(f"\n\nFinal hashset: {best_hashset}")
        print(f"Final waiting time: {waiting_time_best:.2f}")

def analyze_optimization_fct_history():
    """
    Analyze the optimization function history.
    """
    df = pd.read_csv("plots/optimization_fct_history.csv")
    df = df.rename(columns={"# iteration": "iteration"})
    df = df.rename(columns={" function_name": "function_name"})
    df = df.rename(columns={" metric_value": "metric_value"})


    # sort df according to the column iteration
    df = df.sort_values(by=["iteration"])
    df = df.reset_index(drop=True)

    # divide the df into 3 groups according to the iteration
    dfs = [
        df,
        df[(df["iteration"] >= 0) & (df["iteration"] < 33)],
        df[(df["iteration"] >= 33) & (df["iteration"] < 66)],
        df[(df["iteration"] >= 66) & (df["iteration"] < 100)],
    ]
    ranges = [
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
        "remove_one": "cyan",
        "remove_two": "blue",
        "remove_three": "darkblue",
    }


    fig, axs = plt.subplots(2, 2, figsize=(12, 8), tight_layout=True)
    axs = axs.flatten()

    for ax, df_, range in zip(axs, dfs, ranges):
        df_count = df_["function_name"].value_counts()
        df_count = df_count / df_count.sum()

        df_count = df_count.sort_index()
        colors = [fct_colors[fct[1:]] for fct in df_count.index]

        ax.pie(df_count, labels=df_count.index, colors=colors, autopct='%1.1f%%', startangle=140)
        ax.set_title(f"Iterations: {range[0]}-{range[1]}, number of samples: {df_.shape[0]}")
        ax.axis('equal')

    plt.show()

def main():
    """
    Main function to run the optimization and analyze the results.
    """
    run_optimization(
        num_runs=10,
    )
    analyze_optimization_fct_history()


if __name__ == "__main__":
    main()