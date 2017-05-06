# Grid_World Version 1
# This program allows a player to play a memory game.
# The player selects tiles on a 4x4 board. When a tile is
# selected, an image is exposed until a second image is
# selected. If the two images match, the tiles remain
# exposed and one point is added to the score.
# If the exposed image does not match, both tiles remain
# exposed for one second, then they are hidden.
# Selecting an exposed image has no effect.
# The game ends when all tiles are exposed.
# The score is the time taken to expose all tiles so a lower
# score is better.
# This program requires 9 data files: image0 ... image8,
# where image0 is the hidden form of all tiles and image1
# ... image8 are the exposed tile images.

import pygame, sys, time, random
from pygame.locals import *
import numpy as np

# User-defined classes

class Tile:
    # An object in this class represents a single Tile that
    # has an image

    # initialize the class attributes that are common to all
    # tiles.

    borderColor = pygame.Color('black')
    borderWidth = 4  # the pixel width of the tile border
    image = pygame.image.load('marvin.jpg')

    def __init__(self, x, y, wall, surface, tile_size = (100,100)):
        # Initialize a tile to contain an image
        # - x is the int x coord of the upper left corner
        # - y is the int y coord of the upper left corner
        # - image is the pygame.Surface to display as the
        # exposed image
        # - surface is the window's pygame.Surface object

        self.wall = wall
        self.origin = (x, y)
        self.tile_coord = [x//100, y//100]
        self.surface = surface
        self.tile_size = tile_size

    def draw(self, pos, goal):
        # Draw the tile.

        rectangle = pygame.Rect(self.origin, self.tile_size)
        if self.wall:
            pygame.draw.rect(self.surface, pygame.Color('gray'), rectangle, 0)
        elif goal == self.tile_coord:
            pygame.draw.rect(self.surface, pygame.Color('green'), rectangle, 0)
        else:
            pygame.draw.rect(self.surface, pygame.Color('white'), rectangle, 0)

        if pos == self.tile_coord:
            self.surface.blit(Tile.image, self.origin)




        pygame.draw.rect(self.surface, Tile.borderColor, rectangle, Tile.borderWidth)


class Grid_World():
    # An object in this class represents a Grid_World game.
    tile_width = 100
    tile_height = 100
    def __init__(self, surface, board_size = (6,9), wall_coords=[], start_coord=(0,3), goal_coord=(5,8)):
        # Intialize a Grid_World game.
        # - surface is the pygame.Surface of the window

        self.surface = surface
        self.board = []
        self.bgColor = pygame.Color('black')
        self.board_size = list(board_size)
        if not wall_coords:
            self.wall_coords = [[2,i] for i in range(board_size[1]-1)]
        else:
            self.wall_coords = wall_coords

        self.start_coord = list(start_coord)
        self.goal_coord = list(goal_coord)
        self.position = list(start_coord)
        self.actions = range(4)
        self.board_position = self.find_board_coords(start_coord)

        self.createTiles()

    def find_board_coords(self, pos):
        x = pos[1]
        y = self.board_size[0] - pos[0] -1
        return [x,y]

    def createTiles(self):
        # Create the Tiles
        # - self is the Grid_World game
        for rowIndex in range(0, self.board_size[0]):
            row = []
            for columnIndex in range(0, self.board_size[1]):
                imageIndex = rowIndex * self.board_size[1] + columnIndex
                x = columnIndex * Grid_World.tile_width
                y = rowIndex * Grid_World.tile_height
                if [rowIndex,columnIndex] in self.wall_coords:
                    wall = True
                else:
                    wall = False
                tile = Tile(x, y, wall, self.surface)
                row.append(tile)
            self.board.append(row)

    def draw(self):
        # Draw the tiles.
        # - self is the Grid_World game
        pos = self.find_board_coords(self.position)
        goal = self.find_board_coords(self.goal_coord)
        print pos, goal
        self.surface.fill(self.bgColor)
        for row in self.board:
            for tile in row:
                tile.draw(pos, goal)

    def update(self):
        # Check if the game is over. If so return True.
        # If the game is not over,  draw the board
        # and return False.
        # - self is the TTT game

        if self.position == self.goal_coord:
            return True
        else:
            #print self.position
            #self.step(np.random.choice(range(4)))
            self.draw()
            return False

    def step(self, action):
        x,y = self.position
        if action == 0:   # Action Up
            if [x+1,y] not in self.wall_coords and x+1 < self.board_size[0]:
                self.position = [x+1,y]

        elif action == 1:   # Action Down
            if [x-1,y] not in self.wall_coords and x-1 >= 0:
                self.position = [x-1,y]

        elif action == 2:   # Action Right
            if [x,y+1] not in self.wall_coords and y+1 < self.board_size[1]:
                self.position = [x,y+1]

        else:   # Action Up
            if [x,y-1] not in self.wall_coords and y-1 >= 0 :
                self.position = [x,y-1]



def main():
    # Initialize pygame
    pygame.init()

    # Set window size and title, and frame delay
    surfaceSize = (1000, 600)
    windowTitle = 'Grid_World'
    pauseTime = 0.01  # smaller is faster game

    # Create the window
    surface = pygame.display.set_mode(surfaceSize, 0, 0)
    pygame.display.set_caption(windowTitle)

    # create and initialize objects
    gameOver = False
    board = Grid_World(surface)

    # Draw objects
    board.draw()

    # Refresh the display
    pygame.display.update()

    # Loop forever
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                # Handle additional events

        # Update and draw objects for next frame
        gameOver = board.update()
        if gameOver:
            break

        # Refresh the display
        pygame.display.update()

        # Set the frame speed by pausing between frames
        time.sleep(pauseTime)


main()