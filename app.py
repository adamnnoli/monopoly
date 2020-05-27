"""
  App Module for Monopoly

  Contains the classes and methods necessary from creating and playing the game.
"""
from tkinter import *
from consts import *
from game import Game
from functools import partial
# Used to Neaten Code
long = TILE_LONG
short = TILE_SHORT
longPlus = [long + i * short for i in range(1, 10)]  # longPlus[i] = long + (i + 1) * short
cLength = 2 * long + 9 * short

# Necessary Global Variables
playerColors = []  # Holds the variables that contain the player colors


class Monopoly:
    """
        The Main Class for the game.

        Contains the methods necessary for creating the game windows.
        Calls to methods in game.Game to implement functionality

        INSTANCE ATTRIBUTES
        _window: the main game window [tkinter.Tk()]
        _welcome: the frame that handles the pre-game set-up [tkinter.Frame]
        _board: canvas with the game board and pieces drawn on it [tkinter.Canvas]
        _controls: frame that contains the buttons for player actions [tkinter.Frame]
        _playerInfo: frame that displays the information of the current player [tkinter.Frame]
        _game: the Game object with the current game information [game.Game]
        _gameLog: frame with labels to log responses from the game [tkinter.Frame]
        _askPlayers: the frame displayed when asking the names and colors of players[tkinter.Frame]
        _buyWindow: the window prompting the user if they want to buy the property they are on[tkinter.Tk()]
        _tradeWindow: the window that handles trades in the game[tkinter.Tk()]
        _buildWindow: the window that handles building on properties[tkinter.Tk()]
        _auctionWindow: the window that handles auctions in the game[tkinter.Tk()]
    """

# START UP----------------------------------------------------------------------------
    def __init__(self):
        """
            Creates a instance of Monopoly

            Opens a Tkinter Window and adds a welcome frame to the window,
            the welcome frame takes over from there to implement most functionality
        """
        self._window = Tk()
        self._showWelcome(self._window)
        self._board = None
        self._controls = None
        self._playerInfo = None
        self._game = None
        self._gameLog = None
        self._askPlayers = None
        self._buyWindow = None
        self._tradeWindow = None
        self._buildWindow = None
        self._auctionWindow = None

    def run(self):
        """
            Runs the mainloop of the game window.
        """
        self._window.mainloop()

    def _showWelcome(self, root):
        """
            Creates a Welcome window frame and adds it to root.

            The welcome window asks how many people are playing, and what they want their names
            and colors to be. Upon clicking start, the window will be destroyed and the main game
            frame will be created.

            Parameter: root, the window that the welcome frame is added to.
            Requires: Must be of type tkinter.Tk()
        """
        # Frame To Hold Everything
        self._welcome = Frame(root)
        self._welcome.grid(row=0, column=0)

        # Instructions on what to do
        text = Label(self._welcome, text="How Many People Will Be Playing: ", padx=5)
        text.grid(row=0, column=0)

        # Ask how many players and create next dialogue box to get names and colors
        numPlayers = IntVar()
        maxPlayerList = [x for x in range(1, 5)]
        askPlayers = OptionMenu(self._welcome, numPlayers, *maxPlayerList,
                                command=lambda numPlayers: self._showPlayers(numPlayers))
        askPlayers.grid(row=0, column=1)

    def _showPlayers(self, numPlayers):
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
        self._askPlayers = Frame(self._welcome)

        # Create an place widgets in menu
        for i in range(1, numPlayers + 1):
            texti = Label(self._askPlayers, text=f"Player {i}:", padx=5)
            namei = Entry(self._askPlayers, width=15)

            playerIColor = StringVar()
            # Save Player colors for later
            playerColors.append(playerIColor)

            colori = OptionMenu(self._askPlayers, playerIColor, "red", "blue", "green", "yellow")
            texti.grid(row=i, column=0)
            namei.grid(row=i, column=1)
            colori.grid(row=i, column=2)

        # Create Start Button
        startButton = Button(self._askPlayers, text="Play!",
                             command=lambda: self._play(self._welcome, self._window, numPlayers))
        startButton.grid(row=numPlayers+1, column=0, columnspan=numPlayers+1)

        # Add frame to screen
        self._askPlayers.grid(row=1, column=0, columnspan=numPlayers+1)

    def _play(self, currWindow, root, numPlayers):
        """
            Begins the game

            Clears the current window, creates the game object, board canvas, and controls and
            adds them to their respective attributes

            Parameter: currWindow, the parent widget that has all of the welcome information
            Requires: Must be of type tkinter.frame

            Parameter: root, the parent window where the board and controls will be added to
            Requires: Must be of type tkinter.Tk()

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
                trueNames.append(f"Player {i}")
            else:
                trueNames.append(name)

        colors = map(lambda colorEntry: colorEntry.get(), playerColors)

        playerIds = list(range(1, numPlayers + 2))

        players = list(zip(playerIds, trueNames, colors))

        # Clear the root window
        currWindow.destroy()

        # Make the game object and add the board and controls to the root window
        self._game = Game(players)
        self._board = self._createBoard(self._window)
        self._controls = self._createControls(self._window)
        self._playerInfo = self._createPlayerInfo()
        self._createLog()

# DURING GAME--------------------------------------------------------------------------------

# Board
    def _createBoard(self, root):
        """
            Creates a canvas that has the board drawn on it and adds it to root.

            Creates a canvas object of size cLength x cLength and then calls upon helper methods
            to draw all of the tiles of the game.

            Parameter: root, the window that the board is drawn on
            Requires: Must be of type tkinter.Tk()
        """
        self._board = Canvas(root, width=cLength, height=cLength)
        self._board.create_rectangle(0, 0, cLength, cLength, fill="#c0e2ca")
        self._board.grid(row=0, column=0, rowspan=3)
        self._createTop(self._board)
        self._createLeft(self._board)
        self._createRight(self._board)
        self._createBottom(self._board)
        self._drawPlayers(self._board)

    def _createTop(self, cvs):
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

    def _createLeft(self, cvs):
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

    def _createRight(self, cvs):
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

    def _createBottom(self, cvs):
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

# Controls

# TODO: Add Buttons for Building and Trading, get rid of buy button.
    def _createControls(self, root):
        """
            Creates a frame and adds it to root.

            This frame contains all of the buttons needed to perform game actions, calling upon
            methods in game.Game to implement functionality.

            Parameter: root, the window that the controls are added to
            Requires: Must be of type tkinter.Tk()
        """
        # Frame to Hold Buttons
        self._controls = Frame(root)
        self._controls.grid(row=0, column=1)

        # Roll Dice Button
        rollDice = Button(self._controls, text="Roll Dice", padx=5, command=self._rollDice)
        rollDice.grid(row=0, column=0)

        # Build Button
        build = Button(self._controls, text="Build", padx=5, command=self._build)
        build.grid(row=0, column=1)

        # Trade Button
        trade = Button(self._controls, text="Trade", padx=5, command=self._trade)
        trade.grid(row=1, column=0)

        # End Turn Button
        endTurn = Button(self._controls, text="End Turn", padx=5, command=self._endTurn)
        endTurn.grid(row=1, column=1)

    def _rollDice(self):
        """
            Calls Helper Methods in Game to roll the dice and move the players, then redraws the 
            board and player info frame.
        """
        self._handleLog(self._game.rollDice())
        self._createBoard(self._window)
        self._createPlayerInfo()

    def _trade(self):
        self._createTradeWindow()

    def _build(self):
        pass

    def _endTurn(self):
        """
            Calls Helper method in game to end the current player's turn and redraws the player info
            frame
        """
        self._game.endTurn()
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

        tileName = self._game.getTileName(playerInfo["location"])

        if self._playerInfo is not None:
            self._playerInfo.destroy()

        frame = Frame(self._window)
        frame.grid(row=1, column=1)

        nameLabel = Label(frame, text=name).pack()
        cashLabel = Label(frame, text=cash).pack()
        locationLabel = Label(frame, text=tileName).pack()

        self._playerInfo = frame

# Players
    def _drawPlayers(self, board):
        """
            Draws the Players' pieces.
        """
        idsLocsColors = []
        players = self._game.getPlayers()
        for player in players:
            idsLocsColors.append((player["id"], player["location"], player["color"]))

        for id, loc, color in idsLocsColors:
            self._drawPiece(board, loc, color, (id - 1) * PIECE_SIZE)

    def _drawPiece(self, board, location, color, offset):
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
            board.create_rectangle(cLength - long + offset, longPlus[location-31],
                                   cLength - long + offsetPiece, longPlus[location-31] + PIECE_SIZE,
                                   fill=color)

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
            Adds an appropriate message to the gameLog if result is not "Success"

            Parameter: result, the result that might be logged
            Requires: Must be of type string
        """
        property = self._game.getCurrentTile()
        name = self._game.getCurrPlayer()["name"]
        if result == "Not Owned":
            self._createBuyWindow()
        elif result == "Buy Success":
            self._buyWindow.destroy()
            self._log(f"{name} bought {property}")
        elif result == "Not Enough Money":
            self._log(f"You don't have enough money to buy {property}")
        elif result == "Already Rolled":
            self._log("You already rolled.")

# Buying
    def _createBuyWindow(self):
        # TODO: this is not done. Make auction buttons work
        print("Making window")
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
            Calls Helper Method in game to buy the current property and redraws the player info frame
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

        acceptBtn = Button(self._tradeWindow, text="Accept Trade", command=self._acceptTrade)
        acceptBtn.grid(row=2, column=0, columnspan=2)

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
                # TODO: Get the properties of the player with name name, make sure to get the name
                # of the properties no the ids. Finish the rest of this function gridding the items
                # To the Screen, Decide what to actually do if the players did not give a name or
                # Don't have any properties.
        if len(p2PropNames) == 0:
            p2PropNames.append("")
        p1PropEntry = OptionMenu(p2Frame, props, *p2PropNames)
        p1PropEntry.grid(row=1, column=1)

        p1GetOutJail = Label(p2Frame, text=f"{name} Get Out of Jail Free Cards")
        p1GetOutJail.grid(row=2, column=0)

        p2JailEntry = Entry(p2Frame)
        p2JailEntry.grid(row=2, column=1)

        p2Frame.grid(row=1, column=1)

    def _acceptTrade(self):
        # TODO: fill in this function. It should call a helper in game with two trade objects maybe
        # I don't know how I want to represent the data yet, or how I even want to pass it into this
        # function, but you'll figure it out.
        pass

# Building

    def _createBuildWindow(self):
        # TODO: Fill in this function. Just ask what property to build on, what to build and then
        # accept button that calls helper in game. Use log function to make sure things went ok.
        # Don't forget that you need a monopoly to build on properties.
        pass
# Auctioning

    def _createAuctionWindow(self):
        # TODO: fill in this function. I don't know how I want to do auctions, maybe just ask each
        # player individually and highest bid wins.
        pass
# END GAME---------------------------------------------------------------------------------

    def _displaywinner(self):
        pass
