import numpy as np
from gridworld import Tile, Grid_World
from q_learner import Q_learning
import pygame, sys, time, random
from pygame.locals import *
import threading

num_episodes = 300
board_size = [6,9]
original_wall = [[2,i] for i in range(board_size[1]-1)]
new_wall = [[2,i] for i in range(1,board_size[1])]
pauseTime = 0.01  # smaller is faster game
action_dict = {'0': "Up",
               '1': "Down",
               '2': "Right",
               '3': "Left",
               }
render_env = False
transition_timestep = 3000
final_epsilon = 0.01
anneal_epsilon_episodes = 10
epsilon_anneal_rate = (1.0 - final_epsilon)/float(anneal_epsilon_episodes)

def get_features(pos):
    return pos[0]*(board_size[1] - 1) + pos[1]

def learner_thread(thread_id, agent, ):
    # Initialize pygame
    pygame.init()

    # Set window size and title, and frame delay
    surfaceSize = (1000, 600)
    windowTitle = 'Grid_World'

    # Create the window
    surface = pygame.display.set_mode(surfaceSize, 0, 0)
    pygame.display.set_caption(windowTitle)


    n = board_size[0]*board_size[1]


    # Data storage initialization
    return_mem = []
    timestep_mem = []
    greedy_return_mem = []
    timesteps = 0

    # Loop forever
    for i_episode in range(num_episodes):
        # create and initialize objects
        gameOver = False
        if timesteps >= transition_timestep:
            board = Grid_World(surface, board_size, new_wall)
            agent.epsilon = 1.0
        else:
            board = Grid_World(surface, board_size, original_wall)

        # Draw objects
        board.draw()

        # Refresh the display
        pygame.display.update()

        # Q learner specific initializations
        current_state = board.position
        current_features = get_features(board.position)
        episode_return = 0
        episode_timesteps = 0


        while not gameOver:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    # Handle additional events
            # Choose and execute an action
            action = agent.sample_action(current_features)
            board.step(action)

            # Transition to next state
            next_state = board.position
            next_features = get_features(next_state)

            # Q-learning update
            agent.master_func(current_features, next_features, board.reward, action)

            current_features = next_features

            episode_return += board.reward
            episode_timesteps += 1
            timesteps += 1

            if timesteps >= transition_timestep:
                board.change_the_wall(new_wall)

            # print "Board position = ", board.position, " Action = ", action_dict[str(action)],\
            #    "Q-value = ", agent.q_value, "TD Error = ", agent.delta, "Timesteps = ", episode_timesteps

            # Update and draw objects for next frame
            gameOver = board.update()

            # Refresh the display
            pygame.display.update()

            # Set the frame speed by pausing between frames
            time.sleep(pauseTime)
        print "Episode ", i_episode+1, " ended in ", episode_timesteps, " timesteps and return = ", episode_return, \
            "Total Timesteps = ", timesteps
        return_mem.append(episode_return)
        timestep_mem.append(episode_timesteps)
        #eval_return, eval_time = eval_policy(agent, surface)
        #greedy_return_mem.append([eval_return, eval_time])

if __name__ == "__main__":
    agent = Q_learning(alpha=0.5, gamma=0.95, lmbda=0.0, epsilon=0.1, n=n, num_actions=4)

