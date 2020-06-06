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

# Necessary Global Variables
# Holds the variables that contain the player colors [StringVar() List]
playerColors = []

# Holds the variables that contain trade information [(IntVar, StringVar() List, IntVar) List]
tradeInfo = []


class Monopoly:
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
    def __init__(self):
        """
            Creates a instance of Monopoly

            Opens a Tkinter Window and adds a welcome frame to the window,
            the welcome frame takes over from there to implement most functionality
        """
        self._window = Tk()
        self.showWelcome()
        self._playerInfo = None
        self._game = None
        self._gameLog = None
        self._askPlayers = None
        self._buyWindow = None
        self._tradeWindow = None
        self._buildWindow = None
        self._auctionWindow = None
        self._mortgageWindow = None
        self._bankruptcyWindow = None

        self._showWelcome()

    def showWelcome(self):
        """
            Creates the initial Welcome Frame and adds it to the main window.

            Has the title, game rules, and a start button which opens the player selection frame.
        """
        welcomeFrame = Frame(self.mainWindow)
        welcomeFrame.grid(row=0, column=0)

        title = Label(welcomeFrame, text="MONOPOLY")
        title.grid(row=0, column=0)
        instructions = self.instructionsFrame(welcomeFrame)
        instructions.grid()

        start = Button(welcomeFrame, text="Start", command=self.showPlayerSelection)

    def run(self):
        """
            Runs the mainloop of the game window.
        """
        self._window.mainloop()

    def showPlayerSelection(self):
        """
            Clears the main window and begins the player selection process.


        """
        self.clear(self.mainWindow)

        selectionFrame = Frame(self.mainWindow)
        selectionFrame.grid(row=0, column=0)

        # Instructions on what to do
        text = Label(selectionFrame, text="How Many People Will Be Playing: ", padx=5)
        text.grid(row=0, column=0)

        # Ask how many players and create next dialogue box to get names and colors
        numPlayers = IntVar()
        maxPlayerList = [x for x in range(1, 5)]
        askPlayers = OptionMenu(selectionFrame, numPlayers, *maxPlayerList,
                                command=lambda numPlayers: self.showPlayers(numPlayers, selectionFrame))
        askPlayers.grid(row=0, column=1)

    def showPlayers(self, numPlayers, welcomeFrame):
        """
            Displays the Player Selection Menu

            Gives every player an text field to select their name and a dropdown menu to select
            their color

            Parameter: numPlayers, the number of players in the game
            Requires: Must be an int
        """
        if self._askPlayers is not None:
            self._askPlayers.destroy()

        # Frame to hold the Selection menu
        self._askPlayers = Frame(welcomeFrame)

        # Create an place widgets in menu
        for i in range(1, numPlayers + 1):
            texti = Label(self._askPlayers, text=f"Player {i}:", padx=5)
            namei = Entry(self._askPlayers, width=15)

            playerIColor = StringVar()
            # Save Player colors in global variable for later
            playerColors.append(playerIColor)
            colors = ["red", "blue", "green", "yellow", "white", "black", "magenta", "cyan"]
            colori = OptionMenu(self._askPlayers, playerIColor, *colors)
            texti.grid(row=i, column=0)
            namei.grid(row=i, column=1)
            colori.grid(row=i, column=2)

        # Create Start Button
        startButton = Button(self._askPlayers, text="Play!",
                             command=lambda: self._play(welcomeFrame, numPlayers))
        startButton.grid(row=numPlayers+1, column=0, columnspan=3)

        # Add frame to screen
        self._askPlayers.grid(row=1, column=0, columnspan=2)

    def _play(self, currWindow, numPlayers):
        """
            Begins the game

            Clears the current window, creates the game object, board canvas, and controls and
            adds them to their respective attributes

            Parameter: currWindow, the parent widget that has all of the welcome information
            Requires: Must be of type tkinter.frame

            Parameter: numPlayers, the number of players in the game
            Requires: Must be of type int
        """
        # Get the frame that has all of the player information
        playersFrame = currWindow.winfo_children()[-1].winfo_children()

        # Make a list of (id, name, color)
        names = map(lambda nameEntry: nameEntry.get(), playersFrame[1:(3*numPlayers - 1):3])
        trueNames = []
        for i, name in enumerate(names, start=1):
            if name == "":
                trueNames.append(f"Player {i}")  # Make Sure Every player has a name
            else:
                trueNames.append(name)

        colors = map(lambda colorEntry: colorEntry.get(), playerColors)

        playerIds = list(range(1, numPlayers + 2))

        players = list(zip(playerIds, trueNames, colors))

        # Clear the root window
        self.clear(self.mainWindow)
        # Make the game object and add create the frames in the window window
        self._game = Game(players)
        self._createBoard()
        self._createControls()
        self._createPlayerInfo()
        self._createLog()

# DURING GAME--------------------------------------------------------------------------------

# Board
    def createBoard(self):
        """
            Creates a canvas that has the board drawn on it and adds it to root.

            Creates a canvas object of size cLength x cLength and then calls upon helper methods
            to draw all of the tiles of the game.

            Parameter: root, the window that the board is drawn on
            Requires: Must be of type tkinter.Tk()
        """
        board = Canvas(self._window, width=cLength, height=cLength, bg="#c0e2ca")
        board.grid(row=0, column=0, rowspan=3)
        self.createTop(board)
        self.createLeft(board)
        self.createRight(board)
        self.createBottom(board)
        self.drawPlayers(board)

    def createTop(self, cvs):
        """
            Draws the top row of the monopoly board on cvs.

            Parameter: cvs, the canvas that the row is drawn on
            Requires: Must be of type tkinter.Canvas
        """
        cvs.create_rectangle(0, 0, long, long)
        cvs.create_rectangle(long, 0, longPlus[0], long, fill="#d63e3e")
        cvs.create_rectangle(longPlus[0], 0, longPlus[1], long, fill="#cb75e0")
        cvs.create_rectangle(longPlus[1], 0, longPlus[2], long, fill="#d63e3e")
        cvs.create_rectangle(longPlus[2], 0, longPlus[3], long, fill="#d63e3e")
        cvs.create_rectangle(longPlus[3], 0, longPlus[4], long, fill="#7e7f85")
        cvs.create_rectangle(longPlus[4], 0, longPlus[5], long, fill="#e0fc08")
        cvs.create_rectangle(longPlus[5], 0, longPlus[6], long, fill="#e0fc08")
        cvs.create_rectangle(longPlus[6], 0, longPlus[7], long, fill="white")
        cvs.create_rectangle(longPlus[7], 0, longPlus[8], long, fill="#e0fc08")
        cvs.create_rectangle(longPlus[8], 0, cLength, long)

    def createLeft(self, cvs):
        """
            Draws the left side of the monopoly board on cvs. Does not draw free parking or jail
            tiles.

            Parameter: cvs, the canvas that the side is drawn on
            Requires: Must be of type tkinter.Canvas
        """
        cvs.create_rectangle(0, long, long, longPlus[0], fill="#edbb32")
        cvs.create_rectangle(0, longPlus[0], long,  longPlus[1], fill="#edbb32")
        cvs.create_rectangle(0, longPlus[1], long, longPlus[2], fill="#5462ba")
        cvs.create_rectangle(0, longPlus[2], long,  longPlus[3], fill="#edbb32")
        cvs.create_rectangle(0, longPlus[3], long, longPlus[4], fill="#7e7f85")
        cvs.create_rectangle(0, longPlus[4], long, longPlus[5], fill="#e64cdb")
        cvs.create_rectangle(0, longPlus[5], long, longPlus[6], fill="#e64cdb")
        cvs.create_rectangle(0, longPlus[6], long, longPlus[7], fill="white")
        cvs.create_rectangle(0, longPlus[7], long, longPlus[8], fill="#e64cdb")

    def createRight(self, cvs):
        """
            Draws the right side of the monopoly board on cvs. Does not draw GO or Go to Jail
            tiles.

            Parameter: cvs, the canvas that the side is drawn on
            Requires: Must be of type tkinter.Canvas
        """
        cvs.create_rectangle(longPlus[8], long, cLength, longPlus[0], fill="#34c926")
        cvs.create_rectangle(longPlus[8], longPlus[0], cLength, longPlus[1], fill="#34c926")
        cvs.create_rectangle(longPlus[8], longPlus[1], cLength, longPlus[2], fill="#5462ba")
        cvs.create_rectangle(longPlus[8], longPlus[2], cLength, longPlus[3], fill="#34c926")
        cvs.create_rectangle(longPlus[8], longPlus[3], cLength, longPlus[4], fill="#7e7f85")
        cvs.create_rectangle(longPlus[8], longPlus[4], cLength, longPlus[5], fill="#cb75e0")
        cvs.create_rectangle(longPlus[8], longPlus[5], cLength, longPlus[6], fill="#245ac7")
        cvs.create_rectangle(longPlus[8], longPlus[6], cLength, longPlus[7], fill="black")
        cvs.create_rectangle(longPlus[8], longPlus[7], cLength, longPlus[8], fill="#245ac7")

    def createBottom(self, cvs):
        """
            Draws the bottom row of the monopoly board on cvs.

            Parameter: cvs, the canvas that the side is drawn on
            Requires: Must be of type tkinter.Canvas
        """
        cvs.create_rectangle(0, longPlus[8], long, cLength)
        cvs.create_rectangle(long, longPlus[8], longPlus[0], cLength, fill="#4ad6d9")
        cvs.create_rectangle(longPlus[0], longPlus[8], longPlus[1], cLength, fill="#4ad6d9")
        cvs.create_rectangle(longPlus[1], longPlus[8], longPlus[2], cLength, fill="#cb75e0")
        cvs.create_rectangle(longPlus[2], longPlus[8], longPlus[3], cLength, fill="#4ad6d9")
        cvs.create_rectangle(longPlus[3], longPlus[8], longPlus[4], cLength, fill="#7e7f85")
        cvs.create_rectangle(longPlus[4], longPlus[8], longPlus[5], cLength, fill="black")
        cvs.create_rectangle(longPlus[5], longPlus[8], longPlus[6], cLength, fill="#574400")
        cvs.create_rectangle(longPlus[6], longPlus[8], longPlus[7], cLength, fill="#5462ba")
        cvs.create_rectangle(longPlus[7], longPlus[8], longPlus[8], cLength, fill="#574400")
        cvs.create_rectangle(longPlus[8], longPlus[8], cLength, cLength)
    # Players

    def drawPlayers(self, board):
        """
            Draws the Players' pieces.
        """
        idsLocsColors = []
        players = self._game.getPlayers()
        for player in players:
            idsLocsColors.append((player["id"], player["location"], player["color"]))

        for id, loc, color in idsLocsColors:
            self.drawPiece(board, loc, color, (id - 1) * PIECE_SIZE)

    def drawPiece(self, board, location, color, offset):
        """
            Draws a square on the board, PIECE_SIZE x PIECE_SIZE, in tile number location,
            with color color, moved overed from the edge of the board by offset.

            Parameter: board, the board that the piece is drawn on
            Requires: Must be of type tkinter.Canvas

            Parameter: location, the tile number where the piece will be drawn
            Requires: Must be of type int

            Parameter: color, the color of the piece
            Requires: Must be of type string

            Parameter: offset, number of pixels away from board edge the piece will be drawn
            Requires: Must be of type int
        """
        longPiece = long + PIECE_SIZE
        offsetPiece = offset + PIECE_SIZE
        if location == 0:
            board.create_rectangle(cLength - long, cLength - offsetPiece,
                                   cLength - long + PIECE_SIZE, cLength-offset, fill=color)
        elif location < 10:
            board.create_rectangle(cLength - longPlus[location-1], cLength - offsetPiece,
                                   cLength - longPlus[location-1] + PIECE_SIZE, cLength-offset, fill=color)
        elif location == 10:
            board.create_rectangle(offset, cLength-PIECE_SIZE, offsetPiece, cLength, fill=color)
        elif location < 19:
            board.create_rectangle(
                offset, longPlus[18-location], offsetPiece, longPlus[18-location] + PIECE_SIZE, fill=color)
        elif location == 19:
            board.create_rectangle(offset, long, offsetPiece, longPiece, fill=color)
        elif location == 20:
            board.create_rectangle(long-PIECE_SIZE, offset, long, offset+PIECE_SIZE, fill=color)
        elif location < 31:
            board.create_rectangle(longPlus[location-21]-PIECE_SIZE, offset,
                                   longPlus[location-21], offset+PIECE_SIZE, fill=color)
        elif location == 31:
            board.create_rectangle(cLength - long + offset, long, cLength - long + offsetPiece,
                                   longPiece, fill=color)
        else:
            board.create_rectangle(cLength - long + offset, longPlus[location-32],
                                   cLength - long + offsetPiece, longPlus[location-32] + PIECE_SIZE,
                                   fill=color)
# Controls

    def _createControls(self):
        """
            Creates a frame and adds it to root.

            This frame contains all of the buttons needed to perform game actions, calling upon
            methods in game.Game to implement functionality.

            Parameter: root, the window that the controls are added to
            Requires: Must be of type tkinter.Tk()
        """
        # Frame to Hold Buttons
        controls = LabelFrame(self._window, text="Options")
        controls.grid(row=0, column=1)
        # Roll Dice Button
        rollDice = Button(controls, text="Roll Dice", padx=5, command=self._rollDice)
        rollDice.grid(row=0, column=0)

        # Build Button
        build = Button(controls, text="Build", padx=5, command=self._createBuildWindow)
        build.grid(row=0, column=1)

        # Trade Button
        trade = Button(controls, text="Trade", padx=5, command=self._createTradeWindow)
        trade.grid(row=0, column=2)

        # End Turn Button
        endTurn = Button(controls, text="End Turn", padx=5, command=self._endTurn)
        endTurn.grid(row=1, column=0)

        mortgage = Button(controls, text="Mortgage", command=self._createMortgageWindow)
        mortgage.grid(row=1, column=1)

        quitButton = Button(controls, text="Quit", padx=5)
        quitButton.grid(row=1, column=2)

    def _rollDice(self):
        """
            Calls Helper Methods in Game to roll the dice and move the players, then redraws the
            board and player info frame.
        """
        self._handleLog(self._game.rollDice())
        self._createBoard()
        self._createPlayerInfo()

    def _endTurn(self):
        """
            Calls Helper method in game to end the current player's turn and redraws the player info
            frame
        """
        self._handleLog(self._game.endTurn())
        self._createPlayerInfo()
# Player Info

    def _createPlayerInfo(self):
        """
            Creates the Player info frame.

            The frame contains the current player's name, how much money they have, the name of
            the tile they are located on, and a list of the names of the properties they own.
        """
        playerInfo = self._game.getCurrPlayer()
        name = playerInfo["name"]
        cash = playerInfo["cash"]

        tileName = self._game.getTile(playerInfo["location"])["name"]

        if self._playerInfo is not None:
            self._playerInfo.destroy()

        frame = LabelFrame(self._window, text="Player Information")
        frame.grid(row=1, column=1)
        nameLabel = Label(frame, text=f"Name: {name}").pack()
        cashLabel = Label(frame, text=f"Cash: {cash}").pack()
        locationLabel = Label(frame, text=f"Currently At: {tileName}").pack()

        self._playerInfo = frame

# Game Log

    def _createLog(self):
        """
            Creates the Game Log

            The Log will have labels for events in the game, such as buying properties, displaying
            text from game cards, alerting the player with the results of the action they want to do,
            etc.
        """
        self._gameLog = Frame(self._window)
        self._gameLog.grid(row=2, column=1, rowspan=3)

    def _log(self, text):
        """
            Adds a label with text to the gameLog

            Parameter: text, the text to be logged
            Requires: Must be of type string
        """
        label = Label(self._gameLog, text=text)
        label.grid(row=self._gameLog.grid_size()[1]+1)

    def _handleLog(self, result):
        """
            Handles the returns from functions in the game module

            Will add an appropriate message to the game log and create the appropriate game window.

            Parameter: result, the return value of the function, tuple of category and description
            Requires: Must be of type (string, string) tuple
        """
        buyLogs = ["Buy", "Buy Success", "Buy Fail"]
        buildLogs = ["Build Success", "Build Fail"]
        mortgageLogs = ["Mortgage Success", "Mortgage Interest"]
        tradeLogs = ["Trade Success", "Trade Fail"]
        jailLogs = ["Jail", "Jail Success", "Jail Fail"]
        otherLogs = ["Rent", "Tax", "Roll", "Bankruptcy"]

        if result[0] == "Card" or result[0] == "Auction" or result[0] in otherLogs:
            self._log(result[1])
        elif result[0] in buyLogs:
            self._buyLog(result)
        elif result[0] in buildLogs:
            self._buildLog(result)
        elif result[0] in mortgageLogs:
            self._mortgageLog(result)
        elif result[0] in tradeLogs:
            self._tradeLog(result)
        elif result[0] in jailLogs:
            self._jailLog(result)
        else:
            print(result)

        def _buyLog(self, result):
            if result[0] == "Buy":
                self._createBuyWindow()
            if result[0] == "Buy Success":
                self._log(result[1])
                if self._buyWindow is not None:
                    self._buyWindow.destroy()
            if result[0] == "Buy Fail":
                self._log(result[1])

        def _buildLog(self, result):
            if result[0] == "Build Success":
                if self._buildWindow is not None:
                    self._buildWindow.destroy()
            self._log(result[1])

        def _mortgageLog(self, result):
            if result[0] == "Mortgage Success":
                if self._mortgageWindow is not None:
                    self._mortgageWindow.destroy()
            self._log(result[1])

        def _tradeLog(self, result):
            if result[0] == "Trade Success":
                if self._tradeWindow is not None:
                    self._tradeWindow.destroy
            self._log(result[1])

        def _jailLog(self, result):
            if result[0] == "Jail":
                self._createJailWindow()
            if result[0] == "Jail Success":
                if self._jailWindow is not None:
                    self._jailWindow.destroy()
                self._log(result[1])
            if result[0] == "Jail Fail":
                self._log(result[1])
# Buying

    def _createBuyWindow(self):
        # TODO: this is not done. Make auction buttons work
        self._buyWindow = Toplevel()

        name = self._game.getCurrentTile()
        text = Label(self._buyWindow, text=f"Buy {name}?")
        text.grid(row=0, column=0, columnspan=2)

        yesBtn = Button(self._buyWindow, text="Yes", command=lambda: self._handleLog(self._buy()))
        yesBtn.grid(row=1, column=0)

        noBtn = Button(self._buyWindow, text="No", command=lambda: self._handleLog(self._auction()))
        noBtn.grid(row=1, column=1)

    def _buy(self):
        """
            Calls Helper Method in game to buy the current propertyand redraws the player info frame

            Returns the result of the buy attempt.
        """
        result = self._game.buy()
        self._createPlayerInfo()
        return result
# Trading

    def _createTradeWindow(self):
        # TODO: Fill in the rest of this function, make a separate frame to put all of the player
        # 1 stuff in and then make a function that's called with the player dropdown selection menu
        # that makes the other frame. Make entries and dropdowns to select properties and stuff and
        # make the accept button work with the function below
        self._tradeWindow = Toplevel()

        prompt = Label(self._tradeWindow, text="Select who you want to trade with: ")
        prompt.grid(row=0, column=0)

        currPlayerName = self._game.getCurrPlayer()["name"]

        playerNames = []
        for player in self._game.getPlayers():
            if player["name"] != currPlayerName:
                playerNames.append(player["name"])

        if len(playerNames) == 0:
            playerNames.append("")

        player2 = StringVar()
        dropdown = OptionMenu(self._tradeWindow, player2, *playerNames,
                              command=lambda player2: self._makePlayer2(player2))
        dropdown.grid(row=0, column=1)
        self._makePlayer1()

    def _makePlayer1(self):
        name = self._game.getCurrPlayer()["name"]
        p1Frame = LabelFrame(self._tradeWindow, text="Your Items")

        p1Cash = Label(p1Frame, text=f"{name} Cash")
        p1Cash.grid(row=0, column=0)
        p1CashEntry = Entry(p1Frame)
        p1CashEntry.grid(row=0, column=1)

        props = StringVar()
        p1Props = Label(p1Frame, text=f"{name} Properties")
        p1Props.grid(row=1, column=0)
        # Names of Properties the Current Player Owns
        p1PropNames = list(map(lambda prop: self._game.getTileName(
            prop), self._game.getCurrPlayer()["propertyLocations"]))
        # Make sure propnames is not empty, optionMenu needs at least 1 value
        if len(p1PropNames) == 0:
            p1PropNames.append("")
        p1PropEntry = OptionMenu(p1Frame, props, *p1PropNames)
        p1PropEntry.grid(row=1, column=1)

        p1GetOutJail = Label(p1Frame, text=f"{name} Get Out of Jail Free Cards")
        p1GetOutJail.grid(row=2, column=0)
        p1JailEntry = Entry(p1Frame)
        p1JailEntry.grid(row=2, column=1)

        p1Frame.grid(row=1, column=0)

        self._tradeInfo.append((p1CashEntry, props, p1JailEntry))

    def _makePlayer2(self, name):

        p2Frame = LabelFrame(self._tradeWindow, text="Their Items")

        p2Cash = Label(p2Frame, text=f"{name} Cash")
        p2Cash.grid(row=0, column=0)
        p2CashEntry = Entry(p2Frame)
        p2CashEntry.grid(row=0, column=1)

        props = StringVar()
        p2Props = Label(p2Frame, text=f"{name} Properties")
        p2Props.grid(row=1, column=0)
        for player in self._game.getPlayers():
            if player["name"] == name:
                p2PropNames = list(map(lambda prop: self._game.getTileName(
                    prop), player["propertyLocations"]))
        if len(p2PropNames) == 0:
            p2PropNames.append("")
        p2PropEntry = OptionMenu(p2Frame, props, *p2PropNames)
        p2PropEntry.grid(row=1, column=1)

        p2GetOutJail = Label(p2Frame, text=f"{name} Get Out of Jail Free Cards")
        p2GetOutJail.grid(row=2, column=0)

        p2JailEntry = Entry(p2Frame)
        p2JailEntry.grid(row=2, column=1)

        p2Frame.grid(row=1, column=1)

        acceptBtn = Button(self._tradeWindow, text="Accept Trade", command=self._acceptTrade)
        acceptBtn.grid(row=2, column=0, columnspan=2)

    def _acceptTrade(self):
        # TODO: fill in this function. It should call a helper in game with two trade objects maybe
        # I don't know how I want to represent the data yet, or how I even want to pass it into this
        # function, but you'll figure it out.
        p1Frame = self._tradeWindow.winfo_children()[2]
        p2Frame = self._tradeWindow.winfo_children()[4]
        print(p1Frame.winfo_children())
        print(p2Frame.winfo_children())
# Building

    def _createBuildWindow(self):
        # TODO: Fill in this function. Just ask what property to build on, what to build and then
        # accept button that calls helper in game. Use log function to make sure things went ok.
        # Don't forget that you need a monopoly to build on properties.
        self._buildWindow = Toplevel()
        playerName = self._game.getCurrPlayer()["name"]
        monopolyProps = list(map(self._game.getTileName, self._game.getMonopolies(playerName)))
        if len(monopolyProps) == 0:
            monopolyProps.append("")
        nameLabel = Label(self._buildWindow, text="Select Property")
        nameLabel.grid(row=0, column=0)
        name = StringVar()
        nameDrop = OptionMenu(self._buildWindow, name, *monopolyProps,
                              command=lambda name: self._askHouses(name))
        nameDrop.grid(row=0, column=1)

    def _askHouses(self, name):
        numHouses = IntVar()
        numHousesLabel = Label(self._buildWindow, text="How Many Houses To Build?")
        numHousesLabel.grid(row=1)
        numHousesEntry = OptionMenu(self._buildWindow, numHouses, 1, 2, 3, 4, 5,
                                    command=lambda numHouses: self._showPrice(name, numHouses))
        numHousesEntry.grid(row=1, column=1)

    def _showPrice(self, name, numHouses):
        # How Much does the total build cost?
        houseCost = self._game.getHouseCost(self._game.getTileID(name))
        price = houseCost * numHouses
        priceCalcLabel = Label(self._buildWindow, text=f"Total Cost: {price}")
        priceCalcLabel.grid(row=2, columnspan=2)
        acceptButton = Button(self._buildWindow, text="Accept",
                              command=lambda: self._executeBuild(name, numHouses))
        acceptButton.grid(row=3, columnspan=2)

    def _executeBuild(self, name, numHouses):
        tileID = self._game.getTileID(name)
        self._handleLog(self._game.build(tileID, numHouses))
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
# Mortgaging

    def _createMortgageWindow(self):
        self._mortgageWindow = Toplevel()
        playerDict = self._game.getCurrPlayer()

        propLabel = Label(self._mortgageWindow, text="Select the property: ")
        propLabel.grid()

        props = map(self._game.getTileName, playerDict["propertyLocations"])
        prop = StringVar()
        propDropdown = OptionMenu(self._mortgageWindow, prop, *props,
                                  command=lambda prop: self._showMortgageAccept(prop))
        propDropdown.grid(column=1)

    def _showMortgageAccept(self, propName):
        price = self._game.getTileByName(propName)["Mortgage"]
        acceptButton = Button(self._mortgageWindow, text="Accept",
                              command=lambda propName: self._mortgage(propName))
        acceptButton.grid(row=2, columnspan=2)

    def _mortage(self, propName):
        self._handLog(self._game.mortgage(propName))
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
