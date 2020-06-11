from tkinter import *
from consts import *
from win32.win32api import GetSystemMetrics


class Monopoly:
    # START UP ---------------------------------------------------------------------------------------
    def __init__(self):
        """
            Creates a Single Monopoly Object and begins the game
        """
        self.mainWindow = Tk()
        width = GAME_WIDTH
        height = GAME_HEIGHT
        screenWidth = GetSystemMetrics(0)
        screenHeight = GetSystemMetrics(1)
        windowX = int((screenWidth-width)/2)
        windowY = int((screenHeight-height)/2)
        self.mainWindow.geometry(f"{width}x{height}+{windowX}+{windowY}")
        self.showWelcome()

    def showWelcome(self):
        """
            Adds the Welcome Frame containing the rules to the mainWindow
        """
        welcomeFrame = Frame(self.mainWindow)
        welcomeFrame.grid()

        title = Label(welcomeFrame, text="Monopoly")
        title.grid(row=0, column=0)

        rules = Text(welcomeFrame)
        rules.insert(END, WELCOME_MESSAGE)
        rules.grid(row=1, column=0)
        rules.config(state=DISABLED)

        startButton = Button(welcomeFrame, text="Start", command=self.showPlayerSelection)
        startButton.grid(row=2, column=0)

    def showPlayerSelection(self):
        """
            Clears the mainWindow and adds the player selection frame
        """
        self._clear(self.mainWindow)
        
        selectionFrame= Frame(self.mainWindow)
        selectionFrame.grid()

    def play(self):
        """
            Begins the Game with the player information given 

            Parameter: playerInfo, the list of the id, names, and colors of the players in the game
            Requires: Must be of type (int, string, string )list
        """
        pass

    def draw(self):
        """
            Draws the board and playerInfo frame to the mainWindow
        """
        pass

    def run(self):
        self.mainWindow.mainloop()
# GAME PLAY ----------------------------------------------------------------------------------------

    def drawBoard(self):
        """
            Adds a canvas to the mainWindow with the board drawn on it, drawing every tile, player,
            house, and hotel, with detailing showing mortgage and owner statuses of each tile.
        """
        pass

    def createControls(self):
        """
            Adds a frame with all of the buttons of possible game actions to the mainWindow
        """
        pass

    def createPlayerInfo(self):
        """
            Adds a frame with the stats of the current player to the mainWindow
        """
        pass

    def createGameLog(self):
        """
            Adds a frame with all of the logs to the mainWindow
        """
        pass

# END GAME -----------------------------------------------------------------------------------------
    def showWinner(self):
        pass

# HELPERS ------------------------------------------------------------------------------------------
  # Board
    def _drawTile(self, tileDict):
        """
            Draws a tile with the information in tileDict to the board canvas

            Parameter: tileDict, the dictionary containing the tile information
            Requires: Must be of type dict 
        """
        pass
  # Roll

    def _roll(self):
        """
            Command of roll button in controls
            Calls handle log of the result of the roll function in Game
        """
        pass
  #  Build

    def _build(self):
        """
            Command of build button in controls

            Asks if the player would like to build or sell and opens the appropriate window 
        """
        pass

    def _createBuildWindow(self):
        """
            Creates a Top Level which allows the current player to build a house on a property
        """
        pass

    def _createSellWindow(self):
        """
            Creates a Top Level which allows the current player to sell a house on a property
        """
        pass
  # Trade

    def _trade(self):
        """
            Command of trade button in controls

            Creates a Top Level which allows the current player to trade with another player
        """
        pass

    def _playerOneTradeFrame(self):
        """
            Creates the Frame that contains the entries for the current player to enter what
            they will give up in the trade
        """
        pass

    def _createTrade(self, p1Trade, p2Trade):
        """
            Uses the entries given in p1Trade and p2Trade to create dictionaries that are valid
            inputs in Game's Trade function

            Parameter: p1Trade, tuple of inputs of what the current player will give up in the trade
            Requires: Must be of type (Entry, RadioButton list, IntVar)

            Parameter: p2Trade, tuple of inputs of what the other player will give up in the trade
            Requires: Must be of type (StringVar, Entry, RadioButton list, IntVar)
        """
        pass
  # Mortgage

    def _mortage(self):
        """
            Command of mortgage button in controls

            Asks the player if they want to mortgage or unmortgage a property and then creates
            the appropriate window
        """
        pass

    def _createMortgageWindow(self):
        """
            Creates a Top Level which allows the current player to mortgage a property
        """
        pass

    def _createUnmortgageWindow(self):
        """
            Creates a Top Level which allows the current player to unmortgage a property
        """
        pass
  # End Turn

    def _endTurn(self):
        """
            Command of End Turn button in controls

            Handles the log of the end turn function in Game
        """
        pass
  # Quit

    def _quit(self):
        """
            Command of quit button in controls

            Creates a Top Level asking the current player if they want to leave the game.
            If so, handles the log of the quit function in Game
        """
        pass
  # Help

    def _help(self):
        """
            Command of help button in controls

            Creates a Top Level displaying the rules of the Game 
        """
        pass
  # Log

    def _handleLogs(self, logs):
        """
            Performs the necessary actions associated with each log in logs.
            A list of accept logs and what actions they result in can be found in the notes file.

            Parameter: logs, the list of logs to log
            Requires: Must be of type (string, string) list
        """
        pass
  # Jail

    def _jail(self):
        """
            Creates a Top Level displaying the current players options if they are in jail
        """
        pass
  # Bankruptcy

    def _bankruptcy(self):
        """
        """
        pass

    def _clear(self, window):
        pass
