# GridWorld and Q-learning
In this repo, I've created my own Gridworld testbed using pygame. It also contains python implementations of Q-learning. 

## Requirements
* Python 2.7
* [Pygame](https://www.pygame.org/download.shtml)

To see what the testbed GUI looks like:

```python
python gridworld.py
```

The coordinate frame within the GUI and the coordinate frame we normally use is quite different. Nevertheless, it has the standard coordinate frame. 
For e.g., bottom-left corner is (0,0) and top-right corner is (n,n).
 
Arguments for the initializing the class:
```
board_size = (6,9)  :This is (num_rows,num_cols)
wall_coords=[]  : List of 2D coordinates designating walls
start_coord=(0,3) : starting point for the agent (coordinates in [0,board_size-1]) 
goal_coord=(5,8) : terminal point for the agent (coordinates in [0,board_size-1]) 
```
###Additional features of the grid:
Can change the wall/obstacle coordinates at any point of time using the method calls:
```python
Grid.change_the_wall(wall_coords)
Grid.change_the_goal(goal)
```
Grid is basically the class which takes care of rendering the GUI and evaluating grid positions, reward, etc.

## Q-learning (Part-1)
In this example, the obstacles change after 3000 timesteps. The agent subsequently learns the optimal policy for the new goal state. 

```python
python learning_agent.py
```

The file q_learner.py contains the implementation of the Q-learning algorithm using classes in python. 
```
alpha=0.5, gamma=0.95, lmbda=0.0, epsilon=0.1, n=num_weights, num_actions=4 
```
These are the initial parameters of the learning algorithm. Once the obstacles are shifted (@3000 timesteps), epsilon is changes to 0.5.



