# imports
import os
from random import randint
from time import sleep
import pyfiglet
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import track

# console needs to be defined for rich
console = Console()

# pyfiglet message variables
greeting = pyfiglet.figlet_format("BattleShip")
winner = pyfiglet.figlet_format("You Win!")
loser = pyfiglet.figlet_format("You Lose!") 

# Stackoverflow https://bit.ly/stack_overflow
def cls():
    """
    Function to clear the console before running next command.
    """
    os.system("cls" if os.name == "nt" else "clear")

# fucntion to simulate firing sequence
def fire():
    """
    Function simulate firing sequence via progress bar.
    """
    for _ in track(range(3), description="Firing..."):
        sleep(0.3)

# main grid class

# helper function for random coordinates

# helper function row and col within bounds and hit or miss

# helper function places ships on grid

# helper function is ship already there

# player guess row validation 

# player guess col validation

# player guess helper function

# player input validation and return guess

# checks if input is valid and returns computer guess

# sets the grid

# displays the grid

# end of game function

# next round 

# welcome message

# run the game

# name == main