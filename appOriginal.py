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

# DURING GAME--------------------------------------------------------------------------------

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
