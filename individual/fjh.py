#!/user/bin/python
# vim: et sw=2 ts=2 sts=2

# Allows access to the bwx_adventure module
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from bwx_adventure.advent import Game, Location, Connection, Object, Animal, Robot, Pet, Player, Verb, Say, SayOnNoun, SayOnSelf
from bwx_adventure.advent import NORTH, SOUTH, EAST, WEST, UP, DOWN, RIGHT, LEFT, IN, OUT, FORWARD, BACK, NORTHWEST, NORTHEAST, SOUTHWEST, SOUTHEAST, NOT_DIRECTION

# Create a new game
game = Game("zombie infesed village Adventure")
bh
# EEH - A couple of test locations.
in_front_of_office = game.new_location(
    "In Front of a zombie hut ",
    "In front of you stands a zombiefied hut a\n"
    "zombie hut.  The front door is wide open.  Strangely, you hear no\n"
    "sounds except for the moaning of zombies.")

vestibule = game.new_location(
    "Vestibule",
    "A small area at the bottom of a flight of stairs.\n"
    "There are seven(!) doors.")

# EEH - A test connection
game.new_connection("Open"
                    in_front_of_office, vestibule,
                    [IN, NORTH], [OUT, SOUTH])

# Assign where the player starts
player = game.new_player(in_front_of_office)

# Run the game
game.run()
