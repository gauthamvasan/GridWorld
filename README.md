# GridWorld and Q-learning
In this repo, I've created my own Gridworld testbed using pygame. It also contains python implementations of Q-learning. 

## Requirements
* Python 2.7
* [Pygame](https://www.pygame.org/download.shtml)

To see what the testbed GUI looks like:

## Grid World GUI 

```python
python gridworld.py
```

The coordinate frame within the GUI and the coordinate frame we normally use are quite different. Nevertheless, I'm using the standard coordinate frame (i.e., bottom-left corner is (0,0) and top-right corner is (n,n) ).
 
Arguments for the initializing the class:
```
board_size = (6,9)  :This is (num_rows,num_cols)
wall_coords=[]  : List of 2D coordinates designating walls
start_coord=(0,3) : starting point for the agent (coordinates in [0,board_size-1]) 
goal_coord=(5,8) : terminal point for the agent (coordinates in [0,board_size-1]) 
```

```
reward = 0 everywhere except terminal state
reward = 1 if at terminal state
```

### Additional features of the grid
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

### Comments
I tried getting it to learn within 1000 steps, but it happens quite rarely. A lot of times, just the 1st episode takes >500 timesteps to complete. Since we do not use eligibility traces, there is not straightforward mechanism for credit assignment. It can only learn when it re-encounters previous transition states close to the reward. My intuition is that since we have terminal rewards, it'd take some exploration before it can learn the optimal policy. 

One additional thing I wanted to do was anneal the epsilon for the second obstacle. It starts at 0.5 which provides the much-needed exploration. But annealing the exploration factor epsilon would lead to better performance in terms of accumulated reward (something fairly straightforward to do). 

### Results
The graphs are attached as .png files in this repo. You can also use the rudimentary matplotlib-based "plotte.py" to plot the saved data in the directory /Graph Data. Since the cumulative reward can't exceed 1 (only terminal rewards), I've plotted the timesteps it takes to converge over each episode. It is clearly seen that the Q-learner learns the optimal policy within 300 timesteps and is able to adapt and learn a new optimal policy when the obstacles are shifted by a tile.

## Part 2 (Asynchronous q-learning)
I've to figure out ways to make pygame work in parallel. It results in segmentation faults (core dumped). But that is not relevant to the task at hand. It used the module "threading". Right now, it doesn't render the grid. But given some time, it can be fixed. But the state transitions still work without any issues.  

```python
python async_learner.py
```

It hasn't worked yet. But from what I can see, the code is right. Maybe the right hyper-parameters are required.

```python
T_max = 180000
num_threads = 4
I_async_update = 5

```

The results I obtained are disappointing. Regardless of the task, it takes ~300 steps (high variance) to terminate an episiode. Unless I've overlooked something in my code, this is my reasoning:
* When we use a neural network, all the weights depend on every input neuron. In this scenario, it's alright to accumulate all the updates and calculate the gradient later to update the weights.

* But in the tabular case, each weight is correlated only to one input. In this scenario, accumulating the gradient means we're capturing the TD/Bellman error over multiple state transitions. So we'd actually be updating the weights of a particular tile in the grid based on other tiles. But in the tabular case all the weights are uncorrelated, so is it really valid to update them based on other weights?

I think asynchronous implementation is still quite possible in the tabular case. Except, it wouldn't have accumulated gradient updates - it would just be parallel threads doing their own online updates to the global shared weights/model. 

There's a lot of things to try out here:
* Parameter sweep
* Real-time plotting tools using PyQt (super fast!), etc.

   


