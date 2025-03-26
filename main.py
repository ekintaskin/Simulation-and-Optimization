from simulation import Simulation




def main():
    # Parameters
    num_runs = 100
    print_results = True

    # Simulation class
    simulation = Simulation()

    for i in range(num_runs):
        if print_results:
            print(f"Run {i + 1}")
        
        # run simulation
        requests = simulation.run()

        # calculate statistics here

if __name__ == "__main__":
    main()