"""
  App Module for Monopoly

  Contains the classes and methods necessary from creating and playing the game.
"""
from tkinter import *
from consts import *
from game import Game

# Used to Neaten Code
long = TILE_LONG
short = TILE_SHORT
longPlus = [long + i * short for i in range(1, 10)]  # longPlus[i] = long + (i + 1) * short
cLength = 2 * long + 9 * short



class MonopolyOriginal:
    """
        The Main Class for the game.

        Contains the methods necessary for creating the game windows.
        Calls to methods in game.Game to implement functionality

        INSTANCE ATTRIBUTES
        _window: the main game window [tkinter.Tk()]
        _welcome: the frame that handles the pre-game set-up [tkinter.Frame]
        _playerInfo: frame that displays the information of the current player [tkinter.Frame]
        _game: the Game object with the current game information [game.Game]
        _gameLog: frame with labels to log responses from the game [tkinter.Frame]
        _askPlayers: the frame displayed when asking the names and colors of players[tkinter.Frame]
        _buyWindow: the window prompting the user if they want to buy the property they are on[tkinter.Toplevel]
        _tradeWindow: the window that handles trades in the game[tkinter.Toplevel]
        _buildWindow: the window that handles building on properties[tkinter.Toplevel]
        _auctionWindow: the window that handles auctions in the game[tkinter.Toplevel]
        _mortgageWindow: the window that handles mortgaging properties [tkinter.Toplevel]
    """

# START UP----------------------------------------------------------------------------
# Auctioning

    def _createAuctionWindow(self):
        # TODO: fill in this function. I don't know how I want to do auctions, maybe just ask each
        # player individually and highest bid wins.
        pass
# Jail

    def _createJailWindow(self):
        self._jailWindow = Toplevel()

        payButton = Button(self._jailWindow, text="Pay $50", command=self._pay)
        payButton.grid()
        rollButton = Button(self._jailWindow, text="Roll For Doubles", command=self._jailRoll)
        rollButton.grid(column=1)
        cardButton = Button(
            self._jailWindow, text="Use Get Out of Jail Free Card", command=self._useCard)
        cardButton.grid(column=2)

    def _jailRoll(self):
        self._handleLog(self._game.jailRoll())

    def _pay(self):
        self._handleLog(self._game.payJail())

    def _useCard(self):
        self._handleLog(self._game.useGetOutOfJailFreeCard())

# END GAME---------------------------------------------------------------------------------

    def _displaywinner(self):
        pass

# BUTTON FUNCTIONS ---------------------------------------------------------------------------------
    # Functions that make frames based on dropdowns
    def showPlayers(self, numPlayers, frame):
        pass

# HELPERS -----------------------------------------------------------------------------------------
    def clear(self, window):
        """
            Removes all of the children in window

            Parameter: window, the window to clear
            Requires: Must be a tkinter widget
        """
        for child in window.winfo_children():
            child.destroy()

    def run(self):
        """
            Begins the main loop of the game
        """
        self.mainWindow.mainloop()
