"""
    Game Module for Monopoly.

    This module contains all of the functions needed to implement the game logic.
    It allows the players to take turns, give input, and play the game.
"""


class Game:
    """
        A Class to Contain the main Game objects

        Contains all of the methods need to run the game

        INSTANCE ATTRIBUTES:
        _board
    """

    def __init__(self):
        pass

    def createBoard(self):
        """
            Initializes the board for the game.

            Creates the Board object with all of the tiles in game by loading them
            from board.json.

            Returns: A Board Object
        """
        pass

    def createCards(self):
        """
            Initializes the decks of cards for the game.

            Creates a list of Chance Card objects and a list of Community Chest
            Card Objects and returns the list that contains both of the above lists.
            I.e. [Chance Cards, Community Chest Cards]
        """
        pass

    def createPlayers(self):
        pass

    def play(self):
        pass

    def run(self):
        createBoard()
        createCards()
        createPlayers()
        play()
