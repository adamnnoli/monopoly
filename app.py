"""
  App Module for Monopoly

  Contains the classes and methods necessary from creating and playing the game.
"""
from tkinter import *
import consts
from game import Game

# Used to Neaten Code
long = consts.TILE_LONG
short = consts.TILE_SHORT
longPlus = [long + i * short for i in range(1, 10)]
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
        _welcome: the frame that handles the pre-game set-up[tkinter.Frame]
        _board: canvas with the game board and pieces drawn on it [tkinter.Canvas]
        _controls: frame that contains the buttons for player actions: [tkinter.frame]
        _playerInfo: frame that displays the information of the current player [tkinter.frame]
        _game: the Game object with the current game information [game.Game]
    """

# START UP----------------------------------------------------------------------------
    def __init__(self):
        """
            Creates a instance of Monopoly

            Opens a Tkinter Window and adds a welcome frame to the window,
            the welcome frame takes over from here to implement most functionality
        """
        self._window = Tk()
        self._showWelcome(self._window)
        self._board = None
        self._controls = None
        self._playerInfo = None

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
        askPlayers = OptionMenu(self._welcome, numPlayers, 1, 2, 3, 4)
        askPlayers.grid(row=0, column=1)
        getPlayers = Button(self._welcome, text="Select",
                            command=lambda: self._showPlayers(self._welcome, numPlayers.get()))
        getPlayers.grid(row=0, column=2)

        # Start the Game
        startButton = Button(self._welcome, text="Play!",
                             command=lambda: self._play(self._welcome, root, numPlayers.get()))
        startButton.grid(row=3, column=0, columnspan=numPlayers.get()+1)

    def _showPlayers(self, outerFrame, numPlayers):
        """
            Displays the Player Selection Menu

            Gives every player an text field to select their name and a dropdown menu to select
            their color

            Parameter: outerFrame, the frame that the Menu is placed on.
            Requires: Must be a tkinter.Frame

            Parameter: numPlayers, the number of players in the game
            Requires: Must be an int
        """
        # Frame to hold the Selection menu
        innerFrame = Frame(outerFrame)

        # Create an place widgets in menu
        for i in range(1, numPlayers + 1):
            texti = Label(innerFrame, text=f"Player {i}:", padx=5)
            namei = Entry(innerFrame)

            playerIColor = StringVar()
            # Save Player colors for later
            playerColors.append(playerIColor)

            colori = OptionMenu(innerFrame, playerIColor, "red", "blue", "green", "yellow")
            texti.grid(row=1, column=i-1)
            namei.grid(row=1, column=i)
            colori.grid(row=2, column=i-1, columnspan=2)

        # Add frame to screen
        innerFrame.grid(row=1, column=0, columnspan=numPlayers+1)

    def _play(self, currWindow, root, numPlayers):
        """
            Begins the game

            Clears the current window, creates the game object, board canvas, and controls and
            adds them to their respective attributes

            Parmeter: currWindow, the parent widget that has all of the welcome information
            Requires: Must be of type tkinter.frame

            Parmeter: root, the parent window where the board and controls will be added to
            Requires: Must be of type tkinter.Tk()

            Parmeter: numPlayers, the number of players in the game
            Requires: Must be of type int
        """
        # Get the frame that has all of the player information
        playersFrame = currWindow.winfo_children()[-1].winfo_children()

        # Make a list of (id, name, color)
        names = map(lambda nameEntry: nameEntry.get(), playersFrame[1:(3*numPlayers - 1):3])
        colors = map(lambda colorEntry: colorEntry.get(), playerColors)
        playerIds = list(range(1, numPlayers + 2))

        players = list(zip(playerIds, names, colors))

        # Clear the root window
        currWindow.destroy()

        # Make the game object and add the board and controls to the root window
        self._game = Game(players)
        self._board = self._createBoard(self._window)
        self._controls = self._createControls(self._window)

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
        self._board.grid(row=0, column=0)
        self._createTop(self._board)
        self._createLeft(self._board)
        self._createRight(self._board)
        self._createBottom(self._board)

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
        rollDice = Button(self._controls, text="Roll Dice", padx=5,
                          command=self._rollDice)
        rollDice.grid(row=0, column=0)

        # Trade Button
        trade = Button(self._controls, text="Trade", padx=5,
                       command=self._trade)
        trade.grid(row=0, column=1)

    def _rollDice(self):
        self._game.rollDice()

    def _trade(self):
        pass

# Player Info
    def _createPlayerInfo(self):
        playerInfo = self._game.getCurrPlayerInfo()

# Players
    def _drawPlayers(self):
        """
            Draws the Players' pieces.
        """
        locColors = []
        with self._game.getPlayers() as players:
            for player in players:
                locColors.append((player["loc"], player["color"]))
        for loc, color in locColors:
            self._drawPiece(loc, color)

    def _drawPiece(self, location, color, offset):
        """
            Draws a square on the board, PIECE_SIZE x PIECE_SIZE, in tile number location,
            with color color, moved overed from the edge of the board by offset.

            Parmeter: location, the tile number where the piece will be drawn
            Requires: Must be of type int

            Parmeter: color, the color of the piece
            Requires: Must be of type string

            Parmeter: offset, number of pixels away from board edge the piece will be drawn
            Requires: Must be of type int
        """
        if location < 10:
            pass

# END GAME---------------------------------------------------------------------------------

    def _displaywinner(self):
        pass