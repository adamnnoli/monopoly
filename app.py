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
        self._playerInfo = None
        self.gameLog = None
        self.showWelcome()

    def showWelcome(self):
        """
            Adds the Welcome Frame containing the rules to the mainWindow
        """
        welcomeFrame = Frame(self.mainWindow)
        welcomeFrame.grid(row=0, column=0, sticky=N+E+S+W)

        Label(welcomeFrame, text="Monopoly").grid(row=0, column=0)

        rules = Text(welcomeFrame)
        rules.insert(END, WELCOME_MESSAGE)
        rules.grid(row=1, column=0)
        rules.config(state=DISABLED, width=100)
        rules.tag_add("title", 0.0, 2.0)
        rules.tag_config("title", justify=CENTER, font=TITLE_FONT)
        rules.tag_add("content", 2.0, END)
        rules.tag_config("content", font=GENERAL_TEXT_FONT)

        Button(welcomeFrame, text="Start", command=self.showPlayerSelection).grid(row=2, column=0)

    def showPlayerSelection(self):
        """
            Clears the mainWindow and adds the player selection frame
        """
        self._clear(self.mainWindow)

        selectionFrame = Frame(self.mainWindow)
        selectionFrame.grid(row=0, column=0)

        Label(selectionFrame, text="How Many People Will Be Playing: ", padx=5).grid(row=0, column=0)

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
                Label(playersFrame, text=f"Player {i}:", padx=5).grid(row=i, column=0)

                namei = Entry(playersFrame, width=15)
                namei.grid(row=i, column=1)

                playerIColor = StringVar()
                colors = ["red", "blue", "green", "yellow", "white", "black", "magenta", "cyan"]
                OptionMenu(playersFrame, playerIColor, *colors).grid(row=i, column=2)

                # Save Info to Use when making game
                playerInfo.append((namei, playerIColor))

            # Create Start Button
            startButton = Button(playersFrame, text="Play!", command=lambda: self.play(playerInfo))
            startButton.grid(row=numPlayers+1, column=0, columnspan=3)

        # Ask how many players and create next dialogue box to get names and colors
        numPlayers = IntVar()
        OptionMenu(selectionFrame, numPlayers, *[x for x in range(1, 6)],
                   command=lambda numPlayers: showPlayers(numPlayers)).grid(row=0, column=1)

    def play(self, playerInfo):
        """
            Begins the Game with the player information given

            Parameter: playerInfo, the list of the variables containing the names, and colors of
            the players in the game
            Requires: Must be of type (StringVar, StringVar) list
        """
        players = []
        for playerId, nameColor in enumerate(playerInfo, start=1):
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
        self.createPlayerInfo()
        self.createGameLog()

    def run(self):
        self.mainWindow.mainloop()
# GAME PLAY ----------------------------------------------------------------------------------------

    def redraw(self):
        """
            Redraws the board and playerInfo Frame
        """
        self.drawBoard()
        self.createPlayerInfo()

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
        self._drawPlayers(board)

    def createControls(self):
        """
            Adds a frame with all of the buttons of possible game actions to the mainWindow
        """
        controlFrame = LabelFrame(self.mainWindow, text="Controls", labelanchor='n')
        controlFrame.grid(row=0, column=1)

        Button(controlFrame, text="Roll Dice", padx=5,
               command=self._roll, bg="#03c2fc").grid(row=0, column=0)

        Button(controlFrame, text="Build", padx=13,
               command=self._build, bg="#03c2fc").grid(row=0, column=1)

        Button(controlFrame, text="Trade", padx=5,
               command=self._trade, bg="#03c2fc").grid(row=0, column=2)

        Button(controlFrame, text="End Turn", padx=5,
               command=self._endTurn, bg="#03c2fc").grid(row=1, column=0)

        Button(controlFrame, text="Mortgage", command=self._mortage,
               bg="#03c2fc").grid(row=1, column=1)

        Button(controlFrame, text="Quit", padx=9, command=self._quit, bg="red").grid(row=1, column=2)

        Button(controlFrame, text="Help", padx=5, command=self._help,
               bg="#03c2fc").grid(row=2, column=1)

    def createPlayerInfo(self):
        """
            Adds a frame with the stats of the current player to the mainWindow
        """
        if self._playerInfo is not None:
            self._playerInfo.destroy()
        playerInfoFrame = Frame(self.mainWindow)
        playerInfoFrame.grid(row=1, column=1)

        playerInfo = self.game.getCurrentPlayer()
        name = playerInfo["name"]
        cash = playerInfo["cash"]

        tileName = self.game.getTile(playerInfo["location"])["name"]

        Label(playerInfoFrame, text=f"Name: {name}").pack()
        Label(playerInfoFrame, text=f"Cash: {cash}").pack()
        Label(playerInfoFrame, text=f"Currently At: {tileName}").pack()

        self._playerInfo = playerInfoFrame

    def createGameLog(self):
        """
            Adds a frame with all of the logs to the mainWindow
        """
        if self.gameLog is not None:
            self.gameLog.destroy()
        self.gameLog = Text(self.mainWindow, width=50, height=15, state=DISABLED)
        self.gameLog.grid(row=2, column=1)

# END GAME -----------------------------------------------------------------------------------------
    def showWinner(self):
        pass

# HELPERS ------------------------------------------------------------------------------------------
  # Board
    def _drawTile(self, tileDict, cvs):
        """
            Draws a tile with the information in tileDict to cvs

            Parameter: tileDict, the dictionary containing the tile information
            Requires: Must be of type dict

            Parameter: cvs, the canvas to draw the tile on
            Requires: Must be of type tk.Canvas
        """
        x = self._getTopLeft(tileDict["id"])[0]  # Get Coordinates
        y = self._getTopLeft(tileDict["id"])[1]
        color = self._toHex(tileDict["color"])  # Fill Color

        # Outline Color
        if tileDict["owner"] is not None:
            ownerColor = self._toHex(tileDict["owner"].toDict()["color"])
            ownerColor = "#ffffff" if ownerColor == GAME_BOARD_COLOR else ownerColor
        else:
            ownerColor = "#000000"
        # Dash to Show Mortgaged
        dashPattern = (1, 1) if tileDict["mortgaged"] else None

        # Draw the tile
        if tileDict["id"] in [0, 10, 20, 30]:
            cvs.create_rectangle(x, y, x + longPlus[0], y + longPlus[0],
                                 fill=color, outline=ownerColor, dash=dashPattern, width=2)
        elif tileDict["id"] in range(1, 10) or tileDict["id"] in range(21, 30):
            cvs.create_rectangle(x, y, x + TILE_SHORT, y + longPlus[0],
                                 fill=color, outline=ownerColor, dash=dashPattern, width=2)
        elif tileDict["id"] in range(11, 20) or tileDict["id"] in range(31, 40):
            cvs.create_rectangle(x, y, x + longPlus[0], y + TILE_SHORT,
                                 fill=color, outline=ownerColor, dash=dashPattern, width=2)
        self._drawHouses(cvs, tileDict)

    def _drawPlayers(self, cvs):
        """
            Draws every player to the canvas, cvs

            Parameter: cvs, the canvas to draw to
            Requires: Must be of type tk.Canvas
        """
        pieceSize = int((TILE_LONG - HOUSE_SIZE) / len(self.game.getPlayers()))
        for playerNumber, player in enumerate(self.game.getPlayers(), start=1):
            color = None if player["color"] is None else self._toHex(player["color"])
            color = "#ffffff" if color == GAME_BOARD_COLOR else color
            x = self._getPlayerTopLeft(playerNumber, player["location"], pieceSize)[0]
            y = self._getPlayerTopLeft(playerNumber, player["location"], pieceSize)[1]
            cvs.create_rectangle(x, y, x+pieceSize, y+pieceSize, fill=color)

    def _drawHouses(self, cvs, tile):
        """
            Draws the houses on the tile specified in tile to the canvas,cvs

            Parameter: cvs, the canvas to draw to
            Requires: Must be of type tk.Canvas

            Parameter: tile, the dictionary containing the tile information
            Requires: Must be of type dict
        """
        if tile["id"] < 10:
            if tile["numHouses"] == 5:
                x = longPlus[9-tile["id"]]
                y = longPlus[9]
                cvs.create_rectangle(x, y, x + (4 * HOUSE_SIZE), y + HOUSE_SIZE, fill=HOTEL_COLOR)
            else:
                for i in range(tile["numHouses"]):
                    x = longPlus[9-tile["id"]] + (i * HOUSE_SIZE)
                    y = longPlus[9]
                    cvs.create_rectangle(x, y, x+HOUSE_SIZE, y+HOUSE_SIZE, fill=HOUSE_COLOR)
        elif tile["id"] < 20:
            if tile["numHouses"] == 5:
                x = longPlus[0] - HOUSE_SIZE
                y = longPlus[19 - tile["id"]]
                cvs.create_rectangle(x, y, x + HOUSE_SIZE, y + (4 * HOUSE_SIZE), fill=HOTEL_COLOR)
            else:
                for i in range(tile["numHouses"]):
                    x = longPlus[0] - HOUSE_SIZE
                    y = longPlus[19 - tile["id"]] + (i * HOUSE_SIZE)
                    cvs.create_rectangle(x, y, x + HOUSE_SIZE, y + HOUSE_SIZE, fill=HOUSE_COLOR)
        elif tile["id"] < 30:
            if tile["numHouses"] == 5:
                x = longPlus[tile["id"]-21]
                y = longPlus[0] - HOUSE_SIZE
                cvs.create_rectangle(x, y, x + (4 * HOUSE_SIZE), y + HOUSE_SIZE, fill=HOTEL_COLOR)
            else:
                for i in range(tile["numHouses"]):
                    x = longPlus[tile["id"]-21] + (i * HOUSE_SIZE)
                    y = longPlus[0] - HOUSE_SIZE
                    cvs.create_rectangle(x, y, x + HOUSE_SIZE, y + HOUSE_SIZE, fill=HOUSE_COLOR)
        elif tile["id"] < 40:
            if tile["numHouses"] == 5:
                x = longPlus[9]
                y = longPlus[tile["id"]-31]
                cvs.create_rectangle(x, y, x + HOUSE_SIZE, y + (4 * HOUSE_SIZE), fill=HOTEL_COLOR)
            else:
                for i in range(tile["numHouses"]):
                    x = longPlus[9]
                    y = longPlus[tile["id"]-31] + (i * HOUSE_SIZE)
                    cvs.create_rectangle(x, y, x + HOUSE_SIZE, y + HOUSE_SIZE, fill=HOUSE_COLOR)

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

    def _getPlayerTopLeft(self, playerNumber, tileId, pieceSize):
        """
            Returns the (x,y) representing the top-left corner of the piece of the player
            with number playerNumber on the tile with id tileId

            Parameter: playerNumber, the id of the player(Player 1, Player 2, etc.)
            Requires: Must be of type int

            Parameter: tileId, the id of the tile the player is currently on
            Requires: Must be of type int
        """
        cLength = 2 * TILE_LONG + 9 * TILE_SHORT
        offset = playerNumber * pieceSize
        if tileId < 10:
            return (longPlus[9-tileId], cLength-offset)
        elif tileId < 20:
            return (offset-pieceSize, longPlus[19-tileId])
        elif tileId < 30:
            return (longPlus[tileId-20]-pieceSize, offset-pieceSize)
        elif tileId < 40:
            return (cLength-offset, longPlus[tileId-30]-pieceSize)

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
            return GAME_BOARD_COLOR
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
        self._handleLogs(self.game.roll())
        self.redraw()
  # Buy

    def _createBuyWindow(self):
        """
            Creates a TopLevel Window asking the player if they would like to buy the property they
            are currently on.
        """
        self._buyWindow = Toplevel()

        name = self.game.getTile(self.game.getCurrentPlayer()["location"])["name"]

        Label(self._buyWindow, text=f"Buy {name}?").grid(row=0, column=0, columnspan=2)
        Button(self._buyWindow, text="Yes", command=self._buy).grid(row=1, column=0)
        Button(self._buyWindow, text="No", command=self._auction).grid(row=1, column=1)

    def _buy(self):
        """
            Command of the Yes Button in the Buy Window

            Calls handle log of the result of the buy function in game
        """
        self._handleLogs(self.game.buy())
        self.redraw()
  # Build

    def _build(self):
        """
            Command of build button in controls

            Asks if the player would like to build or sell and opens the appropriate window
        """
        self._buildWindow = Toplevel()

        Label(self._buildWindow, text="What would you like to do?").grid(
            row=0, column=0, columnspan=2)
        Button(self._buildWindow, text="Build", command=self._createBuildWindow).grid(row=1, column=0)
        Button(self._buildWindow, text="Sell", command=self._createSellWindow).grid(row=1, column=1)

    def _createBuildWindow(self):
        """
            Clears the build window and adds a frame which allows the current player to build
            a house on a property
        """
        buildFrame = Frame(self._buildWindow)
        buildFrame.grid(row=2, column=0, columnspan=2)

        def _showPrice():
            """
                Adds a label to the buildFrame showing the cost of building a house on the tile
                with name propName. Adds an accept button to execute the build

                Parameter: propName, the name of the property to sell a house on
                Requires: Must be of type string
            """
            amount = int(self.game.getTile(self.game.getTileId(propName))['houseCost'])
            Label(buildFrame, text=f"Would cost: {amount}").grid(row=1, column=0, columnspan=2)
            Button(buildFrame, text="Accept", command=lambda: self._executeBuild(
                propName)).grid(row=2, column=0, columnspan=2)

        Label(buildFrame, text="Select Property: ").grid(row=0, column=0)

        propName = StringVar()
        availableProps = [""] if self.game.getBuildable() == [] else self.game.getBuildable()
        OptionMenu(buildFrame, propName, *availableProps, command=_showPrice).grid(row=0, column=1)

    def _createSellWindow(self):
        """
            Clears the build window and adds a frame which allows the current player to sell
            a house on a property
        """
        sellFrame = Frame(self._buildWindow)
        sellFrame.grid(row=2, column=0, columnspan=2)

        def _showPrice(propName):
            """
                Adds a label to the sellFrame showing the proceeds from selling a house on the tile
                with name propName. Adds an accept button to execute the sale

                Parameter: propName, the name of the property to sell a house on
                Requires: Must be of type string
            """
            amount = int(self.game.getTile(self.game.getTileId(propName))['houseCost']/2)
            Label(sellFrame, text=f"Would receive: {amount}").grid(row=1, column=0, columnspan=2)
            Button(sellFrame, text="Accept", command=lambda: self._executeSell(
                propName)).grid(row=2, column=0, columnspan=2)

        Label(sellFrame, text="Select Property: ").grid(row=0, column=0)
        propName = StringVar()
        availableProps = [""] if self.game.getSellable() == [] else self.game.getSellable()
        OptionMenu(sellFrame, propName, *availableProps,
                   command=lambda: _showPrice(propName)).grid(row=0, column=1)

    def _executeSell(self, propName):
        """
            Sells a house on the tile with name, propName. Handles the logs that arise and redraws
            the board and player info frame 

            Parameter: propName, the name of the property to sell a house on
            Requires: Must be of type string
        """
        self._handleLogs(self.game.sell(propName))
        self.redraw()

    def _executeBuild(self, propName):
        """
            Builds a house on the tile with name, propName. Handles the logs that arise and redraws
            the board and player info frame 

            Parameter: propName, the name of the property to build a house on
            Requires: Must be of type string
        """
        self._handleLogs(self.game.build(propName))
        self.redraw()
  # Trade

    def _trade(self):
        """
            Command of trade button in controls

            Creates a Top Level which allows the current player to trade with another player
        """
        self._tradeWindow = Toplevel()

        Label(self._tradeWindow, text="Select Player:").grid(row=0, column=0)
        currPlayerName = self.game.getCurrentPlayer()["name"]
        p1TradeInfo = self._playerOneTradeFrame()

        playerNames = []
        for player in self.game.getPlayers():
            if player["name"] != currPlayerName:
                playerNames.append(player["name"])

        playerNames = [""] if len(playerNames) == 0 else playerNames
        p2TradeInfo = ()

        def _playerTwoTradeFrame(playerName):
            """
                Creates a frame in the trade window that contains entries for the player with name
                playerName to enter what they will give up in the trade

                Parameter: playerName, the name of the other player that will be trading
                Requires: Must be of type string

                Must be a closure in order to store information of the other player's trade
            """
            for player in self.game.getPlayers():
                if player['name'] == playerName:
                    player2Dict = player

            p2Frame = Frame(self._tradeWindow)

            # Cash
            Label(p2Frame, text=f"{playerName} Cash").grid(row=0, column=0)
            checker = Label(p2Frame).register(str.isnumeric)
            p2CashEntry = Entry(p2Frame, validate="all", validatecommand=(checker, "%P"))
            p2CashEntry.grid(row=0, column=1)

            # Properties
            Label(p2Frame, text=f"{playerName} Properties").grid(row=1, column=0)
            p2PropList = StringVar()
            p2OwnedProps = player2Dict["properties"] if player2Dict["properties"] != [] else [""]
            askP2Props = Listbox(p2Frame, listvariable=p2PropList,
                                 exportselection=False, selectmode=MULTIPLE)
            askP2Props.insert(END, *p2OwnedProps)
            askP2Props.grid(row=1, column=1)
            # Jail Cards
            Label(p2Frame, text=f"{playerName} Get Out Of Jail Free Cards").grid(row=2, column=0)
            p2JailCards = IntVar()
            p2JailList = [""] if player2Dict["jailCards"] == 0 else list(
                range(1, player2Dict["jailCards"]))
            OptionMenu(p2Frame, p2JailCards, *p2JailList).grid(row=2, column=1)
            p2Frame.grid(row=1, column=1)

            p2TradeInfo = (playerName, p2CashEntry, p2PropList, p2JailCards)
            Button(self._tradeWindow, text="Accept",
                   command=lambda: self._executeTrade(p1TradeInfo, p2TradeInfo)).grid(row=2, column=0, columnspan=2)

        player2 = StringVar()
        dropdown = OptionMenu(self._tradeWindow, player2, *playerNames,
                              command=lambda player2: _playerTwoTradeFrame(player2))
        dropdown.grid(row=0, column=1)

    def _playerOneTradeFrame(self):
        """
            Creates the Frame that contains the entries for the current player to enter what
            they will give up in the trade

            Returns: The variables that have the information of the current player's trade
                     type (Entry, StringVar, IntVar)
        """
        currentPlayer = self.game.getCurrentPlayer()
        p1Frame = LabelFrame(self._tradeWindow, text="Your Items")

        # Cash
        Label(p1Frame, text=f"{currentPlayer['name']} Cash").grid(row=0, column=0)
        checker = Label(p1Frame).register(str.isnumeric)
        p1CashEntry = Entry(p1Frame, validate="all", validatecommand=(checker, "%P"))
        p1CashEntry.grid(row=0, column=1)

        # Properties
        Label(p1Frame, text=f"{currentPlayer['name']} Properties").grid(row=1, column=0)
        props = [""] if len(currentPlayer["properties"]) == 0 else currentPlayer["properties"]
        propList = StringVar()
        askProps = Listbox(p1Frame, listvariable=propList,
                           exportselection=False, selectmode=MULTIPLE)
        askProps.insert(END, *props)
        askProps.grid(row=1, column=1)

        # Jail Cards
        Label(p1Frame, text=f"{currentPlayer['name']} Get Out Of Jail Free Cards").grid(
            row=2, column=0)
        p1JailCards = IntVar()
        p1JailList = [""] if currentPlayer["jailCards"] == 0 else list(
            range(1, currentPlayer["jailCards"]))
        OptionMenu(p1Frame, p1JailCards, *p1JailList).grid(row=2, column=1)

        p1Frame.grid(row=1, column=0)
        return (p1CashEntry, propList, p1JailCards)

    def _executeTrade(self, p1Trade, p2Trade):
        tradeDicts = self._createTrade(p1Trade, p2Trade)
        self._handleLogs(self.game.trade(tradeDicts[0], tradeDicts[1]))
        self.redraw()

    def _createTrade(self, p1Trade, p2Trade):
        """
            Uses the entries given in p1Trade and p2Trade to create dictionaries that are valid
            inputs in Game's Trade function

            Parameter: p1Trade, tuple of inputs of what the current player will give up in the trade
            Requires: Must be of type (Entry, StringVar, IntVar)

            Parameter: p2Trade, tuple of inputs of what the other player will give up in the trade
            Requires: Must be of type (string, Entry, StringVar, IntVar)

            Returns: A tuple contain both dictionaries; (dict, dict)
        """
        def getProps(propString):
            """
                Turns a tuple in the form of a string into a list of strings
                Ex: "('ant', 'bee', 'cicada')" -> ['ant', 'bee', 'cicada']

                Parameter: propString, the string to convert
                Requires: Must be of type string
            """
            result = []
            for entry in propString.strip('()').split(','):
                fixed = entry.strip(' ').strip('\'')
                if fixed != '':
                    result.append(fixed)
            return result

        p1TradeDict = {
            "cash": int(p1Trade[0].get()) if p1Trade[0].get() != '' else 0,
            "properties": getProps(p1Trade[1].get()),
            "jailCards": p1Trade[2].get()
        }
        p2TradeDict = {
            "name": p2Trade[0],
            "cash": int(p2Trade[1].get()) if p2Trade[1].get() != '' else 0,
            "properties": getProps(p2Trade[2].get()),
            "jailCards": p2Trade[3].get()
        }

        return (p1TradeDict, p2TradeDict)
  # Mortgage

    def _mortage(self):
        """
            Command of mortgage button in controls

            Asks the player if they want to mortgage or unmortgage a property and then creates
            the appropriate window
        """
        self._mortgageWindow = Toplevel()

        mainFrame = Frame(self._mortgageWindow)
        mainFrame.grid(row=0, column=0)

        Label(mainFrame, text="Mortgage or Unmortgage").grid(row=0, column=0, columnspan=2)
        Button(mainFrame, text="Mortgage", command=self._createMortgageWindow).grid(row=1, column=0)
        Button(mainFrame, text="Unmortgage", command=self._createUnmortgageWindow).grid(row=1, column=1)

    def _createMortgageWindow(self):
        """
            Creates a Top Level which allows the current player to mortgage a property
        """
        mortgageFrame = Frame(self._mortgageWindow)
        mortgageFrame.grid(row=1, column=0, columnspan=2)

        Label(mortgageFrame, text="Select Property:").grid(row=0, column=0)

        propName = StringVar()
        mortgageable = [""] if self.game.getMortgageable() == [] else self.game.getMortgageable()

        def _showPrice(propName):
            """
                Adds a label to the mortgage frame with the proceeds from mortgaging the property
                with name propName, adds an accept button the mortgage frame to execute the mortgage.

                Parameter: propName, the name of the property to mortgage
                Requires: Must be of type string
            """
            amount = int(self.game.getTile(self.game.getTileId(propName))['price']/2)
            Label(mortgageFrame,
                  text=f"Would receive ${amount}").grid(row=1, column=0, columnspan=2)

            Button(mortgageFrame, text="Accept", command=lambda: self._executeMortgage(
                propName)).grid(row=2, column=0, columnspan=2)

        OptionMenu(mortgageFrame, propName, *mortgageable, command=_showPrice).grid(row=0, column=1)

    def _createUnmortgageWindow(self):
        """
            Creates a Top Level which allows the current player to unmortgage a property
        """
        unmortgageFrame = Frame(self._mortgageWindow)
        unmortgageFrame.grid(row=1, column=0, columnspan=2)

        Label(unmortgageFrame, text="Select Property:").grid(row=0, column=0)

        propName = StringVar()
        unmortgageable = [""] if self.game.getUnmortgageable(
        ) == [] else self.game.getUnmortgageable()

        def _showPrice(propName):
            """
                Adds labels to the mortgage frame with the cost to unmortgage broken down into the
                principal and interest, adds an accept button the mortgage frame to execute the 
                unmortgage.

                Parameter: propName, the name of the property to unmortgage
                Requires: Must be of type string
            """
            price = self.game.getTile(self.game.getTileId(propName))['price']
            Label(unmortgageFrame, text=f"Principal: ${int(price/2)}").grid(row=1, column=0)
            Label(unmortgageFrame, text=f"Interest: ${int(.1*price)}").grid(row=1, column=1)
            Label(unmortgageFrame,
                  text=f"Total: ${int(price*.6)}").grid(row=2, column=0, columnspan=2)
            Button(unmortgageFrame, text="Accept", command=lambda: self._executeUnmortgage(
                propName)).grid(row=2, column=0, columnspan=2)

        askPropertyDropdown = OptionMenu(unmortgageFrame, propName,
                                         *unmortgageable, command=_showPrice)
        askPropertyDropdown.grid(row=0, column=1)

    def _executeMortgage(self, propName):
        """
            Mortgages the tile with name propName. Handles the logs that arise and redraws the 
            board and player info frame

            Parameter: propName, the name of the tile to unmortgage
            Requires: Must be of type string
        """
        self._handleLogs(self.game.mortgage(propName))
        self.redraw()

    def _executeUnmortgage(self, propName):
        """
            Unmortgages the tile with name propName. Handles the logs that arise and redraws the 
            board and player info frame

            Parameter: propName, the name of the tile to unmortgage
            Requires: Must be of type string
        """
        self._handleLogs(self.game.unmortgage(propName))
        self.redraw()
  # End Turn

    def _endTurn(self):
        """
            Command of End Turn button in controls

            Handles the log of the end turn function in Game
        """
        self._handleLogs(self.game.endTurn())
        self.redraw()
  # Quit

    def _quit(self):
        """
            Command of quit button in controls

            Creates a Top Level asking the current player if they want to leave the game.
            If so, handles the log of the quit function in Game
        """
        self._quitWindow = Toplevel()
        Label(self._quitWindow, text="Are you sure?").grid(row=0, column=0, columnspan=2)
        Button(self._quitWindow, text="Yes", command=self._executeQuit).grid(row=1, column=0)
        Button(self._quitWindow, text="No", command=self._quitWindow.destroy).grid(row=1, column=1)

    def _executeQuit(self):
        """
            Removes the current player from the game, forfeiting their assets to the bank, handles
            the logs that arise and redraws the screen
        """
        self._handleLogs(self.game.quit())
        self.redraw()
  # Help

    def _help(self):
        """
            Command of help button in controls

            Creates a Top Level displaying the rules of the Game
        """
        helpWindow = Toplevel()
        rules = Text(helpWindow)
        rules.insert(END, HELP_MESSAGE)
        rules.grid(row=1, column=0)
        rules.config(state=DISABLED, width=100)
        rules.tag_add("title", 0.0, 2.0)
        rules.tag_config("title", justify=CENTER, font=TITLE_FONT)
        rules.tag_add("content", 2.0, END)
        rules.tag_config("content", font=GENERAL_TEXT_FONT)

  # Auction

    def _auction(self, propName):
        """
            Called when a player is bankrupt and owes money to the bank or when a player refuses
            to buy a property

            Creates a Top Level asking every remaining player what their bid on property is.

            Parameter: propName, the name of the property being auctioned
            Requires: Must be of type string
        """
        pass
  # Log

    def _log(self, newText):
        """
            Adds a label with text to the gameLog

            Parameter: text, the text to be logged
            Requires: Must be of type string
        """
        self.gameLog.config(state=NORMAL)
        self.gameLog.insert(END, newText+"\n")
        self.gameLog.config(state=DISABLED)
        self.gameLog.yview(END)

    def _handleLogs(self, logs):
        """
            Performs the necessary actions associated with each log in logs.
            A list of accept logs and what actions they result in can be found in the notes file.

            Parameter: logs, the list of logs to log
            Requires: Must be of type (string, string) list
        """
        if logs is None or logs == []:
            return
        buyLogs = ["Buy", "Buy Success", "Buy Fail"]
        buildLogs = ["Build Success", "Build Fail"]
        mortgageLogs = ["Mortgage Success", "Mortgage Interest"]
        tradeLogs = ["Trade Success", "Trade Fail"]
        jailLogs = ["Jail", "Jail Success", "Jail Fail"]
        bankruptcyLogs = ["Bankruptcy Player", "Bankruptcy Bank"]
        otherLogs = ["Rent", "Tax", "Roll"]

        for log in logs:
            if log[0] == "Card" or log[0] == "Auction" or log[0] in otherLogs:
                self._log(log[1])
            elif log[0] in buyLogs:
                self._buyLog(log)
            elif log[0] in buildLogs:
                self._buildLog(log)
            elif log[0] in mortgageLogs:
                self._mortgageLog(log)
            elif log[0] in tradeLogs:
                self._tradeLog(log)
            elif log[0] in jailLogs:
                self._jailLog(log)
            elif log[0] in bankruptcyLogs:
                self._bankruptcyLog(log)
            elif log[0] == "Quit":
                self._quitLog(log)
            else:
                print(log)

    def _buyLog(self, result):
        """
            Creates a Top Level displaying the players options if result is a Buy log, closes
            the Top Level buy window and logs the message in result if result is a Buy Success
            log, and logs the message in result if result is a Buy Fail log

            Parameter: result, the log to handle
            Requires: Must be of type (string, string); Must be a Buy, Buy Success, or Buy Fail log
        """
        if result[0] == "Buy":
            self._createBuyWindow()
        if result[0] == "Buy Success":
            self._log(result[1])
            if self._buyWindow is not None:
                self._buyWindow.destroy()
        if result[0] == "Buy Fail":
            self._log(result[1])

    def _buildLog(self, result):
        """
            Logs the message in result, closes the Top Level build window if result is a Build
            Success log

            Parameter: result, the log to handle
            Requires: Must be of type (string,string); Must be a Build Success or Build Fail log
        """
        if result[0] == "Build Success":
            if self._buildWindow is not None:
                self._buildWindow.destroy()
        self._log(result[1])

    def _mortgageLog(self, result):
        """
            Logs the message in result, closes the Top Level mortgage window if result is a Mortgage
            Success log

            Parameter: result, the log to handle
            Requires: Must be of type (string,string); Must be a Mortgage Success or Mortgage Fail log
        """
        if result[0] == "Mortgage Success":
            if self._mortgageWindow is not None:
                self._mortgageWindow.destroy()
        self._log(result[1])

    def _tradeLog(self, result):
        """
            Logs the message in result, closes the Top Level trade window if result is a Trade
            Success log

            Parameter: result, the log to handle
            Requires: Must be of type (string,string); Must be a Trade Success or Trade Fail log
        """
        print(result)
        if result[0] == "Trade Success":
            if self._tradeWindow is not None:
                self._tradeWindow.destroy()
        self._log(result[1])

    def _jailLog(self, result):
        """
            Creates a Top Level displaying the players options if result is a Jail log, closes
            the Top Level jail window and logs the message in result if result is a Jail Success
            log, and logs the message in result if result is a Jail Fail log

            Parameter: result, the log to handle
            Requires: Must be of type (string, string); Must be a Jail, Jail Success, or Jail Fail log
        """
        if result[0] == "Jail":
            self._jail()
        if result[0] == "Jail Success":
            if self._jailWindow is not None:
                self._jailWindow.destroy()
            self._log(result[1])
        if result[0] == "Jail Fail":
            self._log(result[1])

    def _bankruptcyLog(self, result):
        """
            Creates the appropriate Top level window to display the players options depending on
            if result is a Bankruptcy Player or Bankruptcy Bank log

            Parameter: result, the log to handle
            Requires: Must be of type (string, string); Must either be a Bankruptcy Player or 
                Bankruptcy Bank log
        """
        if result[0] == "Bankruptcy Player":
            self._createPlayerBankruptcyWindow()
        else:
            self._createBankBankruptcyWindow()

    def _quitLog(self,result):
        """
            Logs the message in result, closes the Top Level quit window if result is a Quit log

            Parameter: result, the log to handle
            Requires: Must be of type (string,string); Must be a Quit Log
        """
        self._log(result[1])
        if self._quitWindow is not None:
            self._quitWindow.destroy()
    def _jail(self):
        """
            Creates a Top Level displaying the current players options if they are in jail
        """
        self._jailWindow = Toplevel()
        Frame(self._jailWindow, text="What will you do?").grid(row=0, column=0, columnspan=3)
        Button(self._jailWindow, text="Pay $50", command=self._payJail).grid(row=1, column=0)
        Button(self._jailWindow, text="Roll For Doubles",
               command=self._rollJail).grid(row=1, column=2)
        Button(self._jailWindow, text="Use Get Out Of Jail Free Card",
               command=self._cardJail).grid(row=1, column=2)

    def _payJail(self):
        """
            Attempts to pay $50 to get the current player out of jail. Handles the logs that arise
            and redraws the screen
        """
        self._handleLogs(self.game.payJail())
        self.redraw()

    def _rollJail(self):
        """
            Attempts to roll doubles to get the current player out of jail. Handles the logs that
            arise and redraws the screen
        """
        self._handleLogs(self.game.rollJail())
        self.redraw()

    def _cardJail(self):
        """
            Attempts to have the current player use a get out of jail free card. Handles the logs
            that arise and redraws the screen.
        """
        self._handleLogs(self.game.cardJail())
        self.redraw()
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
