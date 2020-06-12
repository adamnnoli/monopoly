from consts import *
from game import *
from tkinter import *
from win32.win32api import GetSystemMetrics

longPlus = [TILE_LONG + i * TILE_SHORT for i in range(0, 10)]


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
        welcomeFrame.grid(row=0, column=0)

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

        selectionFrame = Frame(self.mainWindow)
        selectionFrame.grid(row=0, column=0)

        text = Label(selectionFrame, text="How Many People Will Be Playing: ", padx=5)
        text.grid(row=0, column=0)

        playersFrame = Frame(selectionFrame)
        playersFrame.grid(row=1, column=0, columnspan=2)

        playerInfo = []

        def showPlayers(numPlayers):
            """
                Populates playersFrame with a label, entry box, and dropdown for each player to
                select their name and color.

                Adds play button to playersFrame to begin the game

                Note: Using a closure because otherwise playersFrame and playerInfo would need to 
                be attributes
            """
            self._clear(playersFrame)
            playerInfo = []
            for i in range(1, numPlayers + 1):
                texti = Label(playersFrame, text=f"Player {i}:", padx=5)
                namei = Entry(playersFrame, width=15)

                playerIColor = StringVar()
                # Save Player colors in global variable for later
                playerInfo.append((namei, playerIColor))
                colors = ["red", "blue", "green", "yellow", "white", "black", "magenta", "cyan"]
                colori = OptionMenu(playersFrame, playerIColor, *colors)
                texti.grid(row=i, column=0)
                namei.grid(row=i, column=1)
                colori.grid(row=i, column=2)

            # Create Start Button
            startButton = Button(playersFrame, text="Play!", command=lambda: self.play(playerInfo))
            startButton.grid(row=numPlayers+1, column=0, columnspan=3)

        # Ask how many players and create next dialogue box to get names and colors
        numPlayers = IntVar()
        maxPlayerList = [x for x in range(1, 5)]
        askPlayers = OptionMenu(selectionFrame, numPlayers, *maxPlayerList,
                                command=lambda numPlayers: showPlayers(numPlayers))
        askPlayers.grid(row=0, column=1)

    def play(self, playerInfo):
        """
            Begins the Game with the player information given

            Parameter: playerInfo, the list of the variables containing the names, and colors of
            the players in the game
            Requires: Must be of type (StringVar, StringVar) list
        """
        players = []
        for playerId, nameColor in enumerate(playerInfo):
            name = nameColor[0].get()
            # Make sure every player has a name
            if name == "":
                name = f"Player {playerId}"
            players.append((playerId, name, nameColor[1].get()))

        self.game = Game(players)
        self.draw()

    def draw(self):
        """
            Clears the mainWindow and draws the board, playerInfo frame, controls frame, and game 
            log to the mainWindow
        """
        self._clear(self.mainWindow)
        self.drawBoard()
        self.createControls()

    def run(self):
        self.mainWindow.mainloop()
# GAME PLAY ----------------------------------------------------------------------------------------

    def drawBoard(self):
        """
            Adds a canvas to the mainWindow with the board drawn on it, drawing every tile, player,
            house, and hotel, with detailing showing mortgage and owner statuses of each tile.
        """
        board = Canvas(self.mainWindow, width=longPlus[9] +
                       TILE_LONG, height=longPlus[9]+TILE_LONG, bg="#c0e2ca")
        for tile in self.game.getBoard():
            self._drawTile(tile, board)
        board.grid(row=0, column=0, rowspan=3)

    def createControls(self):
        """
            Adds a frame with all of the buttons of possible game actions to the mainWindow
        """
        controlFrame = Frame(self.mainWindow)
        controlFrame.grid(row=0, column=1)

        # Roll Dice Button
        rollDice = Button(controlFrame, text="Roll Dice", padx=5, command=self._roll)
        rollDice.grid(row=0, column=0)

        # Build Button
        build = Button(controlFrame, text="Build", padx=5, command=self._build)
        build.grid(row=0, column=1)

        # Trade Button
        trade = Button(controlFrame, text="Trade", padx=5, command=self._trade)
        trade.grid(row=0, column=2)

        # End Turn Button
        endTurn = Button(controlFrame, text="End Turn", padx=5, command=self._endTurn)
        endTurn.grid(row=1, column=0)

        mortgage = Button(controlFrame, text="Mortgage", command=self._mortage)
        mortgage.grid(row=1, column=1)

        quitButton = Button(controlFrame, text="Quit", padx=5, command=self._quit)
        quitButton.grid(row=1, column=2)

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
    def _drawTile(self, tileDict, cvs):
        """
            Draws a tile with the information in tileDict to the board canvas

            Parameter: tileDict, the dictionary containing the tile information
            Requires: Must be of type dict
        """
        bigs = [0, 10, 20, 30]
        topLeft = self._getTopLeft(tileDict["id"])
        x = topLeft[0]
        y = topLeft[1]

        color = self._toHex(tileDict["color"])
        if tileDict["owner"] is not None:
            ownerColor = self._toHex(tileDict["owner"].toDict()["color"])
        else:
            ownerColor = "#ffffff"
        if tileDict["id"] in bigs:
            cvs.create_rectangle(x, y, x + longPlus[0], y + longPlus[0], fill=color)
        elif tileDict["id"] in range(1, 10) or tileDict["id"] in range(21, 30):
            cvs.create_rectangle(x, y, x + TILE_SHORT, y + longPlus[0], fill=color)
        elif tileDict["id"] in range(11, 20) or tileDict["id"] in range(31, 40):
            cvs.create_rectangle(x, y, x + longPlus[0], y + TILE_SHORT, fill=color)

    def _getTopLeft(self, tileId):
        """
            Returns an (x,y) representing the coordinates of the top-left corner of the tile with 
            id tileId

            Parameter: tileId, the id of the tile requested
            Requires: Must be of type int
        """
        if tileId < 10:
            return (longPlus[9-tileId], longPlus[9])
        elif tileId < 20:
            return (0, longPlus[19-tileId])
        elif tileId == 20:
            return (0, 0)
        elif tileId < 31:
            return (longPlus[tileId-21], 0)
        elif tileId < 40:
            return (longPlus[9], longPlus[tileId-31])
        else:
            return "Invalid tileId"

    def _toHex(self, color):
        """
            Returns a hex color code that matches color, changes white to the color of the monopoly
            board

            Parameter: color, the color requested
            Requires: Must be of type string
        """
        color = color.upper()
        if color == "RED":
            return "#ff0000"
        if color == "BLUE":
            return "#0000ff"
        if color == "GREEN":
            return "#00ff00"
        if color == "YELLOW":
            return "#ffff00"
        if color == "CYAN":
            return "#00ffff"
        if color == "MAGENTA":
            return "#ff00ff"
        if color == "WHITE":
            return "#c0e2ca"
        if color == "BLACK":
            return "#000000"
        if color == "BROWN":
            return "#8b4513"
        if color == "LIGHT BLUE":
            return "#add8e6"
        if color == "PINK":
            return "#ffc0cb"
        if color == "ORANGE":
            return "#ffa500"

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
 # General

    def _clear(self, window):
        """
            Clears window by destroying all of its children.
        """
        for child in window.winfo_children():
            child.destroy()
