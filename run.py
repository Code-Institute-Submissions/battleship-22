import os
from random import randint
from time import sleep
import pyfiglet
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import track


console = Console()


greeting = pyfiglet.figlet_format("BattleShip")
winner = pyfiglet.figlet_format("You Win!")
loser = pyfiglet.figlet_format("You Lose!")


# Stackoverflow https://bit.ly/stack_overflow
def cls():
    """
    Function to clear the console before running next command.
    """
    os.system("cls" if os.name == "nt" else "clear")


def fire():
    """
    Function simulate firing sequence via progress bar.
    """
    for _ in track(range(3), description="Firing..."):
        sleep(0.3)


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
                self.Grid[x][y] = "@ "


def random_point(size):
    """
    Helper function that returns a random coordinate
    """
    return randint(0, size - 1)


def valid_point(x, y, Grid, type="computer"):
    """
    Checks if the row and column input is within bounds and
    if spot has been hit.
    """
    try:
        get_coords = Grid.Grid[x][y]
        if get_coords in ["~ ", "@ "]:
            return True
        elif type == "player":
            console.print(
                "You have already tried those coordinates."
                "Let's Try again!\n",
                style="bold red",
            )
    except IndexError:
        console.print(
            "Your missile can't target outside the game area."
            "Let's Try again!\n",
            style="bold red",
        )
    return False


def grid_placement(Grid):
    """
    Helper function that places ships on the grid.
    """
    for _ in range(Grid.num_ships):
        x = random_point(Grid.size)
        y = random_point(Grid.size)
        while occupied_grid(x, y, Grid):
            x = random_point(Grid.size)
            y = random_point(Grid.size)
        Grid.add_ship(x, y)


def occupied_grid(x, y, Grid):
    """
    Helper function that checks if the
    coordinates are already occupied with a ship.
    """
    get_coords = Grid.Grid[x][y]
    return get_coords == "@ "


def user_input_row():
    '''
    Requests user row input with validation and
    returns player guess
    '''
    console.print("Hit * | Miss x | Water ~ | Ship @", style="bold")
    console.print("Targeting System Activated", style="bold red")
    while True:
        human_row = console.input("[bold]Enter ROW number:[/] \n")
        try:
            human_row_num = int(human_row)
        except ValueError:
            console.print(
                "You need to enter a number.\n",
                style="bold red",
            )
            return user_input_row()
        else:
            break
    return human_row_num


def user_input_col():
    '''
    Requests user column input with validation and
    returns player guess
    '''
    while True:
        human_col = console.input("[bold]Enter COLUMN number:[/]\n")
        try:
            human_col_num = int(human_col)
        except ValueError:
            console.print(
                "You need to enter a number between 0 and 9.\n",
                style="bold red",
            )
            return user_input_col()
        else:
            break
    return human_col_num


def ask_player_guess(ai_grid):
    """
    Checks if both guesses from user are valid.
    Loops until correct guess entered and returns player guess.
    """
    row_p = user_input_row()
    col_p = user_input_col()
    while not (valid_point(row_p, col_p, ai_grid, "player")):
        row_p = user_input_row()
        col_p = user_input_col()
    return ai_grid.guess(row_p, col_p)


def generate_computer_guess(human_grid):
    """
    Checks if generated input from computer is valid.
    Loops until correct guess entered and returns computer guess.
    """
    row_ai = random_point(human_grid.size)
    col_ai = random_point(human_grid.size)
    while not (valid_point(row_ai, col_ai, human_grid)):
        row_ai = random_point(human_grid.size)
        col_ai = random_point(human_grid.size)
    return human_grid.guess(row_ai, col_ai)


def set_grid(ai_grid, human_grid):
    """
    Helper function that displays the grids and
    proceeds to asking for user input/guess.
    """
    display_grid(human_grid)
    display_grid(ai_grid)
    player_result = ask_player_guess(ai_grid)
    computer_result = generate_computer_guess(human_grid)
    next_round(player_result, computer_result, human_grid, ai_grid)


def display_grid(Grid):
    """
    Formats and prints the grid.
    """
    console.print(
        Panel.fit(Grid.name + "'s Grid:", style=" bold bright_green")
    )
    print("  " + "   ".join(map(str, range(Grid.size))))
    for row_num, row in enumerate(Grid.Grid):
        print(row_num, "  ".join(row))
    print(" ")


def end_of_game():
    '''
    Helper function to generate end of game message
    and ask to continue or quit.
    '''
    if console.input(
        "[bold underline]Type (Y) to restart a new game"
        "or any other key to (QUIT)[/]\n"
    ) == "y":
        cls()
        run_game()
    else:
        cls()
        quit()


def next_round(player_result, computer_result, human_grid, ai_grid):
    """
    Launches load sequence progress bar. Outputs results
    of guess and checks if game is over. If not, will
    call set_grid to start another sequence.
    """
    cls()
    fire()
    cls()
    row_p, col_p = ai_grid.guesses[len(ai_grid.guesses) - 1]
    row_ai, col_ai = human_grid.guesses[len(human_grid.guesses) - 1]
    console.print(
        f"Your missile hit grid vector[{row_p},{col_p}],"
        f"which resulted in a {player_result}",
        style="bold",
    )
    if player_result == "Win!":
        cls()
        console.print(
            Panel.fit(
                f"Your missile hit [{row_p},{col_p}]"
                f" which sunk all AI ships"
            ),
            style="bold green",
        )
        display_grid(ai_grid)
        console.print(Panel.fit(winner, style="bold green"))
        print("\n")
        end_of_game()
    console.print(
        f"AI missile hit grid vector "
        f"[{row_ai},{col_ai}]"
        f", which resulted in a {computer_result}",
        style="bold",
    )
    if computer_result == "Win!":
        cls()
        console.print(
            Panel.fit(
                f"You missed and AI missile hit "
                f"[{row_ai},{col_ai}]"
                f", which sunk your last ship"
            ),
            style="bold red",
        )
        display_grid(human_grid)
        console.print(Panel.fit(loser, style="bold red"))
        print("\n")
        end_of_game()
    set_grid(ai_grid, human_grid)


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
        "Grid is 5 x 5 | Each player has 4 ships\n",
        style="bold",
    )
    console.print(
        "Let's generate the grid and randomly place the ships",
        style="cyan"
    )


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


if __name__ == "__main__":
    run_game()
