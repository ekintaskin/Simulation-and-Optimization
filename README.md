# Simulation-and-Optimization

## Classes
- Request class: -Keivan
  - time_creation
  - time_arrived
  - time_handled
  - time_served
  - group_id
  - movie_id
  - storage_id
  
- Group: -Ekin
  - Create a list of Request classes
  - Determine time_creation, time_arrived, group_id, movie_id, storage_id
  - Output: list of Request classes
  
- Storage -Tam
  - Input: list of Request classes
  - Calculate the time_handled and time_served
  - Output: list of Request classes
 
- Simulation: -Nicolaj
  - Run the simulation for the three storage unit

- Statistics: -Nathan
  - Think about possible statistics
  - Implement statistics
  - Statistics should be calculated inside the simulation loop
  - Input is the table of requests (list of Request classes)
# Statistics had to be renamed sts.py and not statistics.py due to a conflict with an existing python library
