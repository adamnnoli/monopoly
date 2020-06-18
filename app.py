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
        # self.mainWindow.geometry(f"0x0+{windowX}+{windowY}")
        self.mainWindow.configure(bg="#08ff8c")
        self._playerInfo = None
        self.gameLog = None
        self.showWelcome()

    def showWelcome(self):
        """
            Adds the Welcome Frame containing the rules to the mainWindow
        """
        welcomeFrame = Frame(self.mainWindow)
        welcomeFrame.grid(row=0, column=0, sticky=N+E+S+W)

        title = Label(welcomeFrame, text="Monopoly")
        title.grid(row=0, column=0)

        rules = Text(welcomeFrame)
        rules.insert(END, WELCOME_MESSAGE)
        rules.grid(row=1, column=0)
        rules.config(state=DISABLED, width=100)
        rules.tag_add("title", 0.0, 19.0)
        rules.tag_config("title", justify=CENTER)

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

        rollDice = Button(controlFrame, text="Roll Dice", padx=5, command=self._roll, bg="#03c2fc")
        rollDice.grid(row=0, column=0)

        build = Button(controlFrame, text="Build", padx=13, command=self._build, bg="#03c2fc")
        build.grid(row=0, column=1)

        trade = Button(controlFrame, text="Trade", padx=5, command=self._trade, bg="#03c2fc")
        trade.grid(row=0, column=2)

        endTurn = Button(controlFrame, text="End Turn", padx=5, command=self._endTurn, bg="#03c2fc")
        endTurn.grid(row=1, column=0)

        mortgage = Button(controlFrame, text="Mortgage", command=self._mortage, bg="#03c2fc")
        mortgage.grid(row=1, column=1)

        quitButton = Button(controlFrame, text="Quit", padx=9, command=self._quit, bg="red")
        quitButton.grid(row=1, column=2)

        helpButton = Button(controlFrame, text="Help", padx=5, command=self._help, bg="#03c2fc")
        helpButton.grid(row=2, column=1)

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

        nameLabel = Label(playerInfoFrame, text=f"Name: {name}").pack()
        cashLabel = Label(playerInfoFrame, text=f"Cash: {cash}").pack()
        locationLabel = Label(playerInfoFrame, text=f"Currently At: {tileName}").pack()

        self._playerInfo = playerInfoFrame

    def createGameLog(self):
        """
            Adds a frame with all of the logs to the mainWindow
        """
        if self.gameLog is not None:
            self.gameLog.destroy()
        self.gameLog = Frame(self.mainWindow)
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

    def _drawPlayers(self, cvs):
        """
            Draws every player to the canvas, cvs

            Parameter: cvs, the canvas to draw to
            Requires: Must be of type tk.Canvas
        """
        for playerNumber, player in enumerate(self.game.getPlayers(), start=1):
            color = None if player["color"] is None else self._toHex(player["color"])
            color = "#ffffff" if color == GAME_BOARD_COLOR else color
            x = self._getPlayerTopLeft(playerNumber, player["location"])[0]
            y = self._getPlayerTopLeft(playerNumber, player["location"])[1]
            cvs.create_rectangle(x, y, x+PIECE_SIZE, y+PIECE_SIZE, fill=color)

    def _getPlayerTopLeft(self, playerNumber, tileId):
        """
            Returns the (x,y) representing the top-left corner of the piece of the player
            with number playerNumber on the tile with id tileId

            Parameter: playerNumber, the id of the player(Player 1, Player 2, etc.)
            Requires: Must be of type int

            Parameter: tileId, the id of the tile the player is currently on
            Requires: Must be of type int
        """
        cLength = 2 * TILE_LONG + 9 * TILE_SHORT
        offset = playerNumber * PIECE_SIZE
        if tileId < 10:
            return (longPlus[9-tileId], cLength-offset)
        elif tileId < 20:
            return (offset-PIECE_SIZE, longPlus[19-tileId])
        elif tileId < 30:
            return (longPlus[tileId-20]-PIECE_SIZE, offset-PIECE_SIZE)
        elif tileId < 40:
            return (cLength-offset, longPlus[tileId-30]-PIECE_SIZE)
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
        text = Label(self._buyWindow, text=f"Buy {name}?")
        text.grid(row=0, column=0, columnspan=2)

        yesBtn = Button(self._buyWindow, text="Yes", command=self._buy)
        yesBtn.grid(row=1, column=0)

        noBtn = Button(self._buyWindow, text="No", command=self._auction)
        noBtn.grid(row=1, column=1)

    def _buy(self):
        """
            Command of the Yes Button in the Buy Window

            Calls handle log of the result of the buy function in game
        """
        self._handleLogs(self.game.buy())
  #  Build

    def _build(self):
        """
            Command of build button in controls

            Asks if the player would like to build or sell and opens the appropriate window
        """
        self._buildWindow = Toplevel()
        text = Label(self._buildWindow, text="What would you like to do?")
        text.grid(row=0, column=0, columnspan=2)

        buildButton = Button(self._buildWindow, text="Build", command=self._createBuildWindow)
        buildButton.grid(row=1, column=0)

        sellButton = Button(self._buildWindow, text="Sell", command=self._createSellWindow)
        sellButton.grid(row=1, column=1)

    def _createBuildWindow(self):
        """
            Clears the build window and adds a frame which allows the current player to build
            a house on a property
        """
        self._clear(self._buildWindow)

        frame = Frame(self._buildWindow)

        def _showPrice():
            pass
        propName = StringVar()
        text = Label(frame, text="Select Property: ")
        text.grid(row=0, column=0)
        availableProps = [""] if self.game.getBuildable() == [] else self.game.getBuildable()
        props = OptionMenu(frame, propName, *availableProps, command=_showPrice)
        props.grid(row=0, column=1)

        frame.grid(row=0, column=0)

    def _createSellWindow(self):
        """
            Clears the build window and adds a frame which allows the current player to sell
            a house on a property
        """
        def _showPrice():
            pass
        text = Label(self._buildAskWindow, text="Select Property: ")
        propName = StringVar()
        availableProps = [""] if self.game.getSellable() == [] else self.game.getSellable()
        props = OptionMenu(self._buildAskWindow, propName, *availableProps, command=_showPrice)
  # Trade

    def _trade(self):
        """
            Command of trade button in controls

            Creates a Top Level which allows the current player to trade with another player
        """
        self._tradeWindow = Toplevel()

        Label(self._tradeWindow, text="Select Player:").grid(row=0, column=0)
        currPlayerName = self.game.getCurrentPlayer()["name"]

        playerNames = []
        for player in self.game.getPlayers():
            if player["name"] != currPlayerName:
                playerNames.append(player["name"])

        playerNames = [""] if len(playerNames) == 0 else playerNames

        def _playerTwoTradeFrame(playerName):

            for player in self.game.getPlayers():
                if player['name'] == playerName:
                    player2Dict = player

            p2Frame = Frame(self._tradeWindow)

            Label(p2Frame, text=f"{playerName} Cash").grid(row=0, column=0)
            p2CashEntry = Entry(p2Frame)
            p2CashEntry.grid(row=0, column=1)

            Label(p2Frame, text=f"{playerName} Properties").grid(row=1, column=0)

            p2PropList = StringVar()
            p2OwnedProps = player2Dict["properties"] if player2Dict["properties"] != [] else [""]

            askP2Props = Listbox(p2Frame, listvariable=p2PropList)
            askP2Props.insert(END, *p2OwnedProps)
            askP2Props.grid(row=1, column=1)

            Label(p2Frame, text=f"{playerName} Get Out Of Jail Free Cards").grid(row=2, column=0)
            p2JailCards = IntVar()
            p2JailList = [""] if player2Dict["jailCards"] == 0 else list(
                range(1, player2Dict["jailCard"]))
            p2JailDropdown = OptionMenu(p2Frame, p2JailCards, *p2JailList)
            p2JailDropdown.grid(row=2, column=1)
            p2Frame.grid(row=1, column=1)
        
        player2 = StringVar()
        dropdown = OptionMenu(self._tradeWindow, player2, *playerNames,
                              command=lambda player2: _playerTwoTradeFrame(player2))
        dropdown.grid(row=0, column=1)
        self._playerOneTradeFrame()

    def _playerOneTradeFrame(self):
        """
            Creates the Frame that contains the entries for the current player to enter what
            they will give up in the trade
        """
        currentPlayer = self.game.getCurrentPlayer()
        p1Frame = LabelFrame(self._tradeWindow, text="Your Items")

        p1Cash = Label(p1Frame, text=f"{currentPlayer['name']} Cash")
        p1Cash.grid(row=0, column=0)
        p1CashEntry = Entry(p1Frame)
        p1CashEntry.grid(row=0, column=1)

        p1Props = Label(p1Frame, text=f"{currentPlayer['name']} Properties")
        p1Props.grid(row=1, column=0)
        props = [""] if len(currentPlayer["properties"]) == 0 else currentPlayer["properties"]
        propList = StringVar()
        askProps = Listbox(p1Frame, listvariable=propList)
        askProps.insert(END, *props)
        askProps.grid(row=1, column=1)

        p1GetOutJail = Label(p1Frame, text=f"{currentPlayer['name']} Get Out of Jail Free Cards")
        p1GetOutJail.grid(row=2, column=0)
        p1JailEntry = Entry(p1Frame)
        p1JailEntry.grid(row=2, column=1)

        p1Frame.grid(row=1, column=0)

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
        self._mortgageWindow = Toplevel()
        mainFrame = Frame(self._mortgageWindow)
        mainFrame.grid(row=0, column=0)
        question = Label(mainFrame, text="Mortgage or Unmortgage")
        question.grid(row=0, column=0, columnspan=2)

        mortgageButton = Button(mainFrame, text="Mortgage",
                                command=self._createMortgageWindow)
        mortgageButton.grid(row=1, column=0)

        unmortgageButton = Button(mainFrame, text="Unmortgage",
                                  command=self._createUnmortgageWindow)
        unmortgageButton.grid(row=1, column=1)

    def _createMortgageWindow(self):
        """
            Creates a Top Level which allows the current player to mortgage a property
        """
        if len(self._mortgageWindow.winfo_children()) > 1:
            self._mortgageWindow.winfo_children()[1].destroy()
        mortgageFrame = Frame(self._mortgageWindow)
        mortgageFrame.grid(row=1, column=0, columnspan=2)

        askProperty = Label(mortgageFrame, text="Select Property:")
        askProperty.grid(row=0, column=0)

        propName = StringVar()
        mortgageable = [""] if self.game.getMortgageable() == [] else self.game.getMortgageable()

        def _showPrice(propName):
            tile = self.game.getTile(self.game.getTileId(propName))
            priceLabel = Label(mortgageFrame, text=f"Would receive ${int(tile['price']/2)}")
            priceLabel.grid(row=1, column=0, columnspan=2)

            acceptButton = Button(mortgageFrame, text="Accept",
                                  command=lambda: self._handleLogs(self.game.mortgage(propName)))
            acceptButton.grid(row=2, column=0, columnspan=2)

        askPropertyDropdown = OptionMenu(mortgageFrame, propName, *mortgageable, command=_showPrice)
        askPropertyDropdown.grid(row=0, column=1)

    def _createUnmortgageWindow(self):
        """
            Creates a Top Level which allows the current player to unmortgage a property
        """
        if len(self._mortgageWindow.winfo_children()) > 1:
            self._mortgageWindow.winfo_children()[1].destroy()
        unmortgageFrame = Frame(self._mortgageWindow)
        unmortgageFrame.grid(row=2, column=0, columnspan=2)

        askProperty = Label(unmortgageFrame, text="Select Property:")
        askProperty.grid(row=0, column=0)

        propName = StringVar()
        unmortgageable = [""] if self.game.getUnmortgageable(
        ) == [] else self.game.getUnmortgageable()

        def _showPrice(propName):
            tile = self.game.getTile(self.game.getTileId(propName))
            priceLabel = Label(unmortgageFrame, text=f"Principal: ${int(tile['price']/2)}")
            priceLabel.grid(row=1, column=0)
            interestLabel = Label(unmortgageFrame, text=f"Interest: ${int(.1*tile['price'])}")
            interestLabel.grid(row=1, column=1)
            Label(unmortgageFrame,
                  text=f"Total: ${int(tile['price']*.6)}").grid(row=2, column=0, columnspan=2)
            acceptButton = Button(unmortgageFrame, text="Accept",
                                  command=lambda: self._handleLogs(self.game.unmortgage(propName)))
            acceptButton.grid(row=2, column=0, columnspan=2)

        askPropertyDropdown = OptionMenu(unmortgageFrame, propName,
                                         *unmortgageable, command=_showPrice)
        askPropertyDropdown.grid(row=0, column=1)

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
        pass
  # Help

    def _help(self):
        """
            Command of help button in controls

            Creates a Top Level displaying the rules of the Game
        """
        pass
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

    def _log(self, text):
        """
            Adds a label with text to the gameLog

            Parameter: text, the text to be logged
            Requires: Must be of type string
        """
        label = Label(self.gameLog, text=text)
        label.grid(row=self.gameLog.grid_size()[1]+1)

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
        if result[0] == "Trade Success":
            if self._tradeWindow is not None:
                self._tradeWindow.destroy
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
            self._createJailWindow()
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
