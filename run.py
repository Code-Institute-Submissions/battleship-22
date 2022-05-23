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
class Grid:
    """
    Main Grid class. Sets Grid size, the number of ships, the player's name
    and the Grid type (player Grid or computer).
    Has methods for adding ships and guesses and printing the Grid.
    """

    def __init__(self, size, num_ships, name, type):
        self.size = size
        self.Grid = [["~ " for _ in range(size)] for _ in range(size)]
        self.num_ships = num_ships
        self.name = name
        self.type = type
        self.guesses = []
        self.ships = []
        self.hits = 0

    def guess(self, x, y):
        self.guesses.append((x, y))
        self.Grid[x][y] = "X "

        if (x, y) in self.ships:
            self.Grid[x][y] = "* "
            self.hits += 1
            if self.hits == self.num_ships:
                return "Win!"
            return "* "
        else:
            return "x "

    def add_ship(self, x, y):
        if len(self.ships) >= self.num_ships:
            print("Error: you cannot add anymore ships!")
        else:
            self.ships.append((x, y))
            if self.type == "player":
                self.Grid[x][y] = "+ "

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
def welcome_message():
    '''
    Helper function that prints the welcome message,
    rules and game key.
    '''
    console.print(Panel.fit(greeting, style="bold green"))
    print(Panel.fit("OBJECT OF THE GAME:", style="bold green"))
    console.print("[bold green]WIN![/] by sinking all AI ships", style="bold")
    console.print(
        "[bold red]LOSE![/] if AI sinks your ships first",
        style="bold",
    )
    console.print(Panel.fit("GAMEPLAY:", style="bold green"))
    console.print("Hit * | Miss x | Water ~ | Ship @", style="bold")
    console.print(
        "Grid is 3 x 3 | Each player has 4 ships\n",
        style="bold",
    )
    console.print(
        "Let's generate the grid and randomly place the ships",
        style="cyan"
    )

# run the game
def run_game():
    """
    Sets the size of the grid and number of ships.
    Prints the welcome message and gets player name.
    Sets the AI and human grid and starts the game.
    """
    size = 5
    num_ships = 4
    welcome_message()
    while True:
        player_name = console.input(
            "[bold]What is your first name?[/] \n"
        ).capitalize()
        if not player_name.isalpha():
            console.print(
                "Your name cannot be numbers or empty",
                style="bold red",
            )
        else:
            break
    cls()
    ai_grid = Grid(size, num_ships, "AI", type="computer")
    human_grid = Grid(size, num_ships, player_name, type="player")
    cls()
    grid_placement(human_grid)
    grid_placement(ai_grid)

    set_grid(ai_grid, human_grid)

# name == main
if __name__ == "__main__":
    run_game()