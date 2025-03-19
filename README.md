# Simulation-and-Optimization

## Classes
- Request class:
  - time_creation
  - time_arrived
  - time_handled
  - time_served
  - group_id
  - movie_id
  - storage_id
  
- Group:
  - Create a list of Request classes
  - Determine time_creation, time_arrived, group_id, movie_id, storage_id
  - Output: list of Request classes
  
- Storage
  - Input: list of Request classes
  - Calculate the time_handled and time_served
  - Output: list of Request classes
 
- Simulation:
  - Run the simulation for the three storage unit

- Statistics:
  - Think about possible statistics
  - Implement statistics
  - Statistics should be calculated inside the simulation loop
  - Input is the table of requests (list of Request classes)
