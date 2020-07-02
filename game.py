import json
from objects import *
import os
import random


class Game:
    # INITIALIZATION -----------------------------------------------------------------------------------
    def __init__(self, players):
        """
            Creates a Game Object with the players given

            Parameter: players, a list of tuples with the player information (id,name,color)
            Requires: Must be of type (int, string, string) list
        """
        self.board = self.createBoard()
        self.chanceCards = self.createChanceCards()
        self.communityChestCards = self.createCommunityChestCards()
        self.players = self.createPlayers(players)
        self.currentPlayer = self.players[0]
        self.currentChanceIndex = 0
        self.currentCommunityChestIndex = 0
        self.numRolled = 0
        self.hasRolled = False
        self.numDoublesRolled = 0

    def createBoard(self):
        """
            Returns the Board object for the game
        """
        possMonopolies = {}
        tiles = []
        with open(os.getcwd() + "\monopoly\\board.json") as boardJson:
            board = json.load(boardJson)
            for i, tile in enumerate(board["tiles"]):
                newTile = Tile(i, tile["name"], tile["price"], tile["rents"],
                               tile["house cost"], tile["color"])
                tiles.append(newTile)
                if possMonopolies.get(tile["color"]) is None:
                    possMonopolies[tile["color"]] = set()
                possMonopolies[tile["color"]].add(tile["name"])
        del possMonopolies["white"]
        self.possMonopolies = possMonopolies
        return Board(tiles)

    def createChanceCards(self):
        """
            Returns a list of Card objects representing the chance cards in the game
        """
        result = []
        for text, action in zip(self._chanceCardTexts(), self._chanceCardActions()):
            result.append(Card(text, action))
        return result

    def createCommunityChestCards(self):
        """
            Returns a list of Card objects representing the community chest cards in the game
        """
        result = []
        for text, action in zip(self._communityChestCardTexts(), self._communityChestCardActions()):
            result.append(Card(text, action))
        return result

    def createPlayers(self, players):
        """
            Returns a list of Player objects representing the players in the game

            Parameter: players, list of the id, name, and color for each player
            Requires: Must be of type int, string, string list
        """
        return list(map(lambda player: Player(player[0], player[1], player[2]), players))
# GETTERS AND SETTERS ------------------------------------------------------------------------------

    def getBoard(self):
        """
            Returns a dictionary representation of every tile on the board
        """
        return self.board.toDict()

    def getTile(self, tileId):
        """
            Returns a dictionary representation of the tile with id, tileId

            Parameter: tileId, the id of the tile requested
            Requires: Must be of type int
        """
        return self.board.getTile(tileId)

    def getTileId(self, tileName):
        """
            Returns the id of the tile with name, tileName

            Parameter: tileName, the name of the tile requested
            Requires: Must be of type string
        """
        return self.board.getTileId(tileName)

    def getCurrentPlayer(self):
        """
            Returns a dictionary representation of the player whose turn it is
        """
        return self.currentPlayer.toDict()

    def getPlayers(self):
        """
            Returns a list of dictionaries representing every player in the game
        """
        return list(map(lambda player: player.toDict(), self.players))

    def getBuildable(self):
        """
            Returns a list of the names of properties that the current player can build a house
            or hotel on

            The player can build a house on the property if
                They own the property
                They have a monopoly on the properties color group
                Building a house would not break the build evenly rule
                The property is not mortgaged
        """
        playerMonopolies = {}
        playerName = self.currentPlayer.toDict()["name"]
        for colorGroup, owner in self.board.getMonopolies().items():
            if owner == playerName:
                playerMonopolies[colorGroup] = 5

        ownedTiles = self._getOwnedTiles()
        for tile in ownedTiles:
            if tile["color"] in playerMonopolies:
                if playerMonopolies[tile["color"]] > tile["numHouses"]:
                    playerMonopolies[tile["color"]] = tile["numHouses"]

        result = []
        for tile in ownedTiles:
            if tile["numHouses"] == playerMonopolies[tile["color"]]:
                result.append(tile["name"])
        return result

    def getSellable(self):
        """
            Returns a list of the names of properties that the current player can sell a house from

            The player can sell a house on the property if there is at least one house, and selling
            a house would not break the build evenly rule
        """
        playerMonopolies = {}
        playerName = self.currentPlayer.toDict()["name"]
        for colorGroup, owner in self.board.getMonopolies().items():
            if owner == playerName:
                playerMonopolies[colorGroup] = 5

        ownedTiles = self._getOwnedTiles()
        for tile in ownedTiles:
            if tile["color"] in playerMonopolies:
                if playerMonopolies[tile["color"]] < tile["numHouses"]:
                    playerMonopolies[tile["color"]] = tile["numHouses"]

        result = []
        for tile in ownedTiles:
            if tile["numHouses"] == playerMonopolies[tile["color"]]:
                result.append(tile["name"])
        return result

    def getMortgageable(self):
        """
            Returns a list of the names of properties that the current player can mortgage
        """
        result = []
        for tile in self._getOwnedTiles():
            if not tile["mortgaged"]:
                result.append(tile["name"])
        return result

    def getUnmortgageable(self):
        """
            Returns a list of the names of properties that the current player can unmortgage
        """
        result = []
        for tile in self._getOwnedTiles():
            if tile["mortgaged"]:
                result.append(tile["name"])
        return result
# GAME FUNCTIONALITY -------------------------------------------------------------------------------
    # Rolling

    def roll(self):
        """
            If the current player can roll, rolls the dice and moves the player's piece,
            returning a list of logs appropriate based on the result of this action.
            If the current player cannot roll, returns a log with that message.
        """
        logs = []
        if self.hasRolled:
            logs.append(("Roll", "You already rolled"))
            return logs
        if self.currentPlayer.toDict()["inJail"]:
            logs.append(("Roll", "You are in Jail"))
            return logs
        else:
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            if dice1 != dice2:
                self.hasRolled = True
            else:
                self.numDoublesRolled += 1
                if self.numDoublesRolled >= 3:
                    self._goToJail()
                    self.hasRolled = True
                    return [("Roll", "You rolled 3 doubles in a row, Go To Jail")]
                logs.append(("Roll", "You rolled doubles, roll again"))
            self.currentPlayer.move(dice1+dice2)
            self.numRolled = dice1 + dice2
            result = self._handleTile()
            if result is None:
                return logs
            else:
                return (logs + result)

    # Buying
    def buy(self):
        """
            If the current player can buy the current tile, takes the cash necessary and transfers
            ownership returning a Buy Success log, if not returns a Buy Fail log
        """
        currentPlayer = self.currentPlayer.toDict()
        currentTile = self.board.getTile(currentPlayer["location"])
        if (currentTile["owner"] is None) and currentTile["price"] < currentPlayer["cash"]:
            self.board.getTileObject(currentPlayer["location"]).setOwner(self.currentPlayer)
            self.currentPlayer.takeCash(currentTile["price"])
            self.currentPlayer.giveProperty(currentPlayer["location"], self.board)
            self._updateMonopolies()
            return [("Buy Success", f"{currentPlayer['name']} bought {currentTile['name']}")]
        else:
            return [("Buy Fail", f"{currentPlayer['name']} cannot buy {currentTile['name']}")]

    # Building
    def build(self, tileName):
        """
            Tries to build a house on the tile with name, tileName.

            Returns: A Build Success log if the house was a built, a Build Fail log otherwise

            Parameter: tileName, the name of the tile to build on
            Requires: Must be of type string

            Requires: Building must not break the build evenly rule, the tile must not be
            mortgaged
        """
        tileDict = self.board.getTile(self.board.getTileId(tileName))
        tile = self.board.getTileObject(self.board.getTileId(tileName))
        currentPlayer = self.currentPlayer.toDict()

        if tileDict["mortgaged"]:
            return [("Build Fail", f"{tileName} is mortgaged")]
        elif tileName not in self.getBuildable():
            return [("Build Fail", "You must build evenly")]
        elif tileDict["houseCost"] > currentPlayer["cash"]:
            return [("Build Fail", f"{currentPlayer['name']} doesn't have enough money to build a house on {tileName}")]
        else:
            self.currentPlayer.takeCash(tileDict["houseCost"])
            tile.build()
            return [("Build Success", f"{currentPlayer['name']} built a house on {tileName}")]

    def sell(self, tileName):
        """
            Sells a house on the tile with name, tileName

            Returns: A Build Success log

            Parameter: tileName, the name of the tile to sell from
            Requires: Must be of type string

            Requires: Selling must not break the build evenly rule, the tile must have at least
            one house
        """
        tile = self.board.getTile(self.board.getTileId(tileName))
        if tile["numHouses"] < 1:
            return [("Build Fail", f"{tileName} does not have any houses.")]
        elif tileName not in self.getSellable():
            return [("Build Fail", "You must sell evenly")]
        else:
            self.currentPlayer.giveCash(int(tile["houseCost"]/2))
            self.board.getTileObject(self.board.getTileId(tileName)).sell()
            return [("Build Success", f"{self.currentPlayer.toDict()['name']} sold a house on {tileName}")]

    # Trading
    def trade(self, p1Trade, p2Trade):
        """
            Attempts to have the current player trade the items in p1Trade for the items in
            p2Trade with the player that has name p2Dict["name"]

            Returns: A Trade Fail log if one of the players is missing an item, a Trade Success
            log otherwise

            Parameter: p1Trade, the dictionary specifying what player 1 gives to player 2
            Requires: Must be of type dict

            Parameter: p2Trade, the dictionary specifying what player 2 gives to player 1
            Requires: Must be of type dict
        """
        result = self._checkTrade(p1Trade, p2Trade)

        if result is not None:
            return [result]

        for player in self.players:
            if player.toDict()["name"] == p2Trade["name"]:
                player2 = player

        self.currentPlayer.takeCash(p1Trade["cash"])
        player2.giveCash(p1Trade["cash"])
        player2.takeCash(p2Trade["cash"])
        self.currentPlayer.giveCash(p2Trade["cash"])

        for prop in p1Trade["properties"]:
            tileId = self.getTileId(prop)
            self.currentPlayer.takeProperty(tileId, self.board)
            player2.giveProperty(tileId, self.board)
            self.board.getTileObject(tileId).setOwner(player2)

        for prop in p2Trade["properties"]:
            tileId = self.getTileId(prop)
            self.currentPlayer.giveProperty(tileId, self.board)
            player2.takeProperty(tileId, self.board)
            self.board.getTileObject(tileId).setOwner(self.currentPlayer)

        for i in range(p1Trade["jailCards"]):
            self.currentPlayer.takeJailCard()
            player2.giveJailCard()

        for i in range(p2Trade["jailCards"]):
            self.currentPlayer.giveJailCard()
            player2.takeJailCard()

        self._updateMonopolies()
        return [("Trade Success", self._makeTradeString(p1Trade, p2Trade))]

    # Mortgaging
    def mortgage(self, tileName):
        """
            Sets the status of the tile with name, tileName to mortgaged, giving the player
            the proceeds

            Returns: A Mortgage Success Log

            Parameter: tileName, the name of the tile to mortgage
            Requires: Must be of type string
        """
        amount = int(self.board.getTile(self.board.getTileId(tileName))['price']/2)
        self.currentPlayer.giveCash(amount)
        self.board.getTileObject(self.board.getTileId(tileName)).setMortgage()

        return [("Mortgage Success", f"{self.currentPlayer.toDict()['name']} mortgage {tileName} for ${amount}")]

    def unmortgage(self, tileName):
        """
            Attempts to unmortgage the tile with name tileName

            Returns: A Mortgage Success log if the player had enough cash, A Mortgage Fail log
            otherwise

            Parameter: tileName, the name of the tile to unmortgage
            Requires: Must be of type string
        """
        tile = self.board.getTile(self.board.getTileId(tileName))
        currentPlayer = self.currentPlayer.toDict()
        cost = int(.6*tile['price'])
        if currentPlayer["cash"] > cost:
            self.currentPlayer.takeCash(cost)
            self.board.getTileObject(self.board.getTileId(tileName)).setMortgage()
            return [("Mortgage Success",
                     f"{currentPlayer['name']} paid ${cost} to unmortgage {tileName}")]
        else:
            return [("Mortgage Fail",
                     f"{currentPlayer['name']} doesn't have enough money to unmortgage {tileName}")]

    def auction(self, tileName, winningBid, winningBidder):
        """
            Has the player with name, winningBidder, purchase the tile with name, tileName, for the
            amount of winningBid

            Requires: the player must have enough cash 
            Returns: An auction log summarizing the transaction

            Parameter: tileName, the name of the tile won
            Requires: Must be of type string

            Parameter: winningBid, the amount the winning player Bid
            Requires: Must be of type int

            Parameter: winningBidder, the name of the player one the auction
            Requires: Must be of type string
        """

        for player in self.players:
            if player.toDict()["name"] == winningBidder:
                playerObj = player

        playerObj.takeCash(winningBid)
        playerObj.giveProperty(self.board.getTileId(tileName), self.board)
        self.board.getTileObject(self.board.getTileId(tileName)).setOwner(playerObj)

        return [("Auction", f"{winningBidder} won {tileName} at an auction by bidding {winningBid}")]

    # Quitting

    def quit(self):
        """
            Removes the current player from the game, forfeiting all assets to the bank

            Returns: A Quit Log
        """
        for tile in self.getBoard():
            if tile["owner"] == self.currentPlayer:
                tileObj = self.board.getTileObject(tile["id"])
                tileObj.setOwner(None)
                if tile["mortgaged"]:
                    tileObj.setMortgage()
                for i in range(tile["numHouses"]):
                    tileObj.sell()
        playerToDelete = self.currentPlayer
        nextPlayerIndex = (self.players.index(self.currentPlayer) + 1) % len(self.players)
        self.currentPlayer = self.players[nextPlayerIndex]
        self.players.remove(playerToDelete)
        return [("Quit", f"{playerToDelete.toDict()['name']} quit the game")]

    # Jail
    def payJail(self):
        """
            Attempts to pay $50 to remove the current player from jail

            Returns: A Jail Success log if the player had enough money, A Jail Fail log
            otherwise
        """
        currentPlayer = self.currentPlayer.toDict()
        if currentPlayer["cash"] >= 50:
            self.currentPlayer.takeCash(50)
            self.currentPlayer.leaveJail()
            return [("Jail Success", f"{currentPlayer['name']} paid $50 to get out of jail")]
        else:
            return [("Jail Fail", f"{currentPlayer['name']} does not have $50")]

    def rollJail(self):
        """
            Rolls the dice, if the result is a double, removes the current player from jail
            and moves them the amount rolled, returning a list of logs with the log of leaving
            jail and the log from rolling the dice
            If the result is not a double returns A Jail Success Log
        """
        name = self.currentPlayer.toDict()["name"]
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        if dice1 == dice2:
            self.currentPlayer.leaveJail()
            self.currentPlayer.move(dice1+dice2)
            self.numRolled = dice1 + dice2
            result = self._handleTile()
            if result is None:
                return [("Jail Success", f"{name} rolled doubles to get out of jail")]
            else:
                return ([("Jail Success", f"{name} rolled doubles to get out of jail")] + result)
        else:
            return [("Jail Fail", f"{name} did not roll doubles and is still in jails")]

    def cardJail(self):
        """
            Attempts to use a Get Out Of Jail Free Card to remove the current player to jail.

            Returns: A Jail Success Log if the player had a Get Out of Jail Free Card, a Jail
            Fail Log otherwise
        """
        currentPlayer = self.currentPlayer.toDict()
        if currentPlayer["jailCards"] >= 1:
            self.currentPlayer.useJailCard()
            return [("Jail Success", f"{currentPlayer['name']} used a Get Out of Jail Free Card")]
        else:
            return [("Jail Fail", f"{currentPlayer['name']} does not have a Get Out of Jail Free Card")]

    # End Turn
    def endTurn(self):
        """
            Attempts to end the current player's turn and begin the next player's turn

            Returns: A log appropriate based on the result of the attempt
        """
        if not self.hasRolled:
            return [("Roll", "You haven't rolled yet.")]
        nextPlayerIndex = (self.players.index(self.currentPlayer) + 1) % len(self.players)
        self.currentPlayer = self.players[nextPlayerIndex]
        self.hasRolled = False
        self.numRolled = 0
        self.numDoublesRolled = 0
        return self._checkJail()
# HELPERS

    # Init Helpers
    def _chanceCardTexts(self):
        """
            Returns a list of the texts for every chance card in the game.
        """
        zero = "You have won a crossword competition. Collect $100."
        one = "Advance To Go. Collect $200"
        two = "Advance to Illinois Ave. If you pass Go, collect $200."
        three = "Advance to St. Charles Place. If you pass Go, collect $200."
        four = "Advance to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total 10 times the amount thrown."
        five = "Advance to the nearest Railroad and pay owner twice the rental to which they is otherwise entitled. If Railroad is unowned, you may buy it from the Bank. "
        six = "Bank pays you dividend of $50."
        seven = "Get out of Jail Free. This card may be kept until needed, or traded/sold."
        eight = "Go Back Three Spaces."
        nine = "Go to Jail. Do not pass GO, do not collect $200."
        ten = "Make general repairs on all your property: For each house pay $25, For each hotel pay $100."
        eleven = "Pay poor tax of $15 "
        twelve = "Take a trip to Reading Railroad. If you pass Go, collect $200."
        thirteen = "Take a walk on the Boardwalk."
        fourteen = "You have been elected Chairman of the Board. Pay each player $50."
        fifteen = "Your building and loan matures. Collect $150."

        return [zero, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen]

    def _chanceCardActions(self):
        """
            Returns a list of the actions for every chance card in the game.

            Ordered to match the text of the cards.
        """
        def zero(player): return player.giveCash(100)
        def one(player): return self._advanceTo("Go")
        def two(player): return self._advanceTo("Illinois Avenue")
        def three(player): return self._advanceTo("St. Charles Place")
        def four(player): return self._advanceToNearestUtility()
        def five(player): return self._advanceToNearestRailroad()
        def six(player): return player.giveCash(50)
        def seven(player): return player.giveGetOutOfJail()
        def eight(player): return self._move(-3)
        def nine(player): return player.goToJail()
        def ten(player): return player.makeRepairs(25, 100)
        def eleven(player): return player.takeCash(15)
        def twelve(player): return self._advanceTo("Reading Railroad")
        def thirteen(player): return self._advanceTo("Boardwalk")
        def fourteen(player): return player.giveToEach(50, self.players)
        def fifteen(player): return player.giveCash(150)
        return [zero, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen]

    def _communityChestCardTexts(self):
        """
            Returns an array with all of the texts for the Community Chest Cards
        """
        zero = "Advance to Go."
        one = "Bank error in your favor. Collect $200."
        two = "Doctor's fees. Pay $50."
        three = "From sale of stock you get $50."
        four = "Get Out of Jail Free. This card may be kept until needed or sold/traded."
        five = "Go to Jail.Do not pass Go, Do not collect $200."
        six = "Grand Opera Night. Collect $50 from every player for opening night seats."
        seven = "Holiday Fund matures. Collect $100."
        eight = "Income tax refund. Collect $20."
        nine = "It's your birthday. Collect $10 from every player."
        ten = "Life insurance matures – Collect $100"
        eleven = "Hospital Fees. Pay $50."
        twelve = "School fees. Pay $50."
        thirteen = "Receive $25 consultancy fee."
        fourteen = "You are assessed for street repairs: Pay $40 per house and $115 per hotel you own."
        fifteen = "You have won second prize in a beauty contest. Collect $10."
        sixteen = "You inherit $100."
        return [zero, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen]

    def _communityChestCardActions(self):
        """
            Returns an array with all of the actions for the Community Chest Cards.

            Order matches the order of the Community Chest Card Texts
        """
        def zero(player): return self._advanceTo("Go")
        def one(player): return player.giveCash(200)
        def two(player): return player.takeCash(50)
        def three(player): return player.giveCash(50)
        def four(player): return player.giveGetOutOfJail()
        def five(player): return player.goToJail()
        def six(player): return player.takeFromEach(50, self.players)
        def seven(player): return player.giveCash(100)
        def eight(player): return player.giveCash(20)
        def nine(player): return player.takeFromEach(10, self.players)
        def ten(player): return player.giveCash(100)
        def eleven(player): return player.takeCash(50)
        def twelve(player): return player.takeCash(50)
        def thirteen(player): return player.giveCash(50)
        def fourteen(player): return player.makeRepair(40, 115)
        def fifteen(player): return player.giveCash(10)
        def sixteen(player): return player.giveCash(100)
        return [zero, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen]

    def _advanceTo(self, tileName):
        """
            Advaces the current player to the tile with name, tileName.

            Returns: A list of logs associated with landing on the new tile
        """
        self.currentPlayer.advanceTo(tileName, self.board)
        return self._handleTile()

    def _advanceToNearestRailRoad(self):
        """
            Advances player to the nearest railroad if it is owned the pays the owner double the
            amount owed.
            Returns: A Buy log if the tile is unowned and a Rent log if the current player can
            pay double the rent owed, a Bankruptcy Log otherwise
        """
        readingLoc = self.board.getTileId("Reading Railroad")
        pennsylvaniaLoc = self.board.getTileId("Pennsylvania Railroad")
        bAndOLoc = self.board.getTileId("B. & O. Railroad")
        shortLoc = self.board.getTileId("Short Line")
        currentLocation = self.currentPlayer.toDict()["location"]

        if currentLocation < readingLoc or currentLocation > shortLoc:
            self.currentPlayer.advanceTo("Reading Railroad", self.board)
        elif currentLocation < pennsylvaniaLoc:
            self.currentPlayer.advanceTo("Pennsylvania Railroad", self.board)
        elif currentLocation < bAndOLoc:
            self.currentPlayer.advanceTo("B. & O. Railroad", self.board)
        else:
            self.currentPlayer.advanceTo("Short Line", self.board)
        return self._handleAdvanceToRail(self)

    def _handleAdvanceToRail(self):
        """
            Returns a Buy Log if the current tile is not owned, if it is owned, pays the owner
            twice the amount owed

            Requires: The current tile is a railroad tile
        """
        currentPlayer = self.currentPlayer.toDict()
        tile = self.board.getTile(currentPlayer["location"])
        if tile["owner"] is None:
            return [("Buy", "Not owned")]
        else:
            railroads = ["Reading Railroad", "Pennsylvania Railroad",
                         "B. & O. Railroad", "Short Line"]
            numOwned = self._numOwned(tile["owner"], railroads)
            if numOwned == 1:
                return self._attemptTakeRent(tile["owner"], 50)
            elif numOwned == 2:
                return self._attemptTakeRent(tile["owner"], 100)
            elif numOwned == 3:
                return self._attemptTakeRent(tile["owner"], 200)
            elif numOwned == 4:
                return self._attemptTakeRent(tile["owner"], 400)

    def _advanceToNearestUtility(self):
        """
            Advances player to the nearest utility if it is owned rolls the dice and pays the owner
            10x the number rolled.

            Returns: A Buy log if the tile is unowned and a Rent log if the current player can
            pay double the rent owed, a Bankruptcy Log otherwise
        """
        electricCompLoc = self.board.getTileId("Electric Company")
        waterWorksLoc = self.board.getTileId("Water Works")
        currentLocation = self.currentPlayer.toDict()["location"]

        if currentLocation > waterWorksLoc or currentLocation < electricCompLoc:
            self.currentPlayer.advanceTo("Electric Company", self.board)
            currentPlayer = self.currentPlayer.toDict()
            tile = self.board.getTile(currentPlayer["location"])
            if tile["owner"] is None:
                return [("Buy", "Not owned")]
            else:
                return self._attemptTakeRent(tile["owner"], random.randint(2, 12)*10)
        else:
            self.currentPlayer.advanceTo("Water Works", self.board)
            currentPlayer = self.currentPlayer.toDict()
            tile = self.board.getTile(currentPlayer["location"])
            if tile["owner"] is None:
                return [("Buy", "Not owned")]
            else:
                return self._attemptTakeRent(tile["owner"], random.randint(2, 12)*10)

    def _move(self, spaces):
        """
            Moves the current player spaces places. Awards cash if the current player passed GO
        """
        self.currentPlayer.move(spaces)
# Rolling Helpers

    def _handleTile(self):
        """
            Calls the necessary functions and performs the necessary actions to be executed when
            the current player lands on the current tile.

            Returns: A list of appropriate logs
        """
        tile = self.board.getTile(self.currentPlayer.toDict()["location"])

        if tile["name"] == "Chance" or tile["name"] == "Community Chest":
            return self._drawCard()
        if tile["name"] == "Income Tax" or tile["name"] == "Luxury Tax":
            return self._takeTax()
        if tile["owner"] is not None and tile["owner"] != self.currentPlayer and not tile["mortgaged"]:
            return self._takeRent()
        if tile["owner"] is None and tile["price"] > 0:
            return [("Buy", "Not Owned")]

    def _drawCard(self):
        """
            If the current player is on a chance card tile, draws the current chance card, if the
            current player is on a community chest card tile, draws the current community chest
            card.

            Returns: A list of logs, the first being the log for the card text, the rest of the list
            is the logs that arise from executing the card action
        """
        tileName = self.board.getTile(self.currentPlayer.toDict()["location"])["name"]

        if tileName == "Chance":
            card = self.chanceCards[self.currentChanceIndex]
            self.currentChanceIndex = (self.currentChanceIndex + 1) % len(self.chanceCards)
            logs = [("Card", card.getText())]
            actionReturn = card.getAction()(self.currentPlayer)
            if actionReturn is not None:
                logs + actionReturn
            return logs

        if tileName == "Community Chest":
            card = self.communityChestCards[self.currentCommunityChestIndex]
            self.currentCommunityChestIndex = (
                self.currentCommunityChestIndex + 1) % len(self.communityChestCards)
            logs = [("Card", card.getText())]
            actionReturn = card.getAction()(self.currentPlayer)
            if actionReturn is not None:
                logs + actionReturn
            return logs

    def _takeRent(self):
        """
            Pays rent owed to the owner of the current tile.

            Returns: A rent log if the current player can pay the rent, a Bankruptcy Player log otherwise
        """
        tile = self.board.getTile(self.currentPlayer.toDict()["location"])
        railroads = ["Reading Railroad", "Pennsylvania Railroad", "B. & O. Railroad", "Short Line"]
        utilities = ["Electric Company", "Water Works"]
        if tile["name"] in railroads:
            numOwned = self._numOwned(tile["owner"], railroads)
            if numOwned == 1:
                return self._attemptTakeRent(tile["owner"], 25)
            elif numOwned == 2:
                return self._attemptTakeRent(tile["owner"], 50)
            elif numOwned == 3:
                return self._attemptTakeRent(tile["owner"], 100)
            elif numOwned == 4:
                return self._attemptTakeRent(tile["owner"], 200)
        if tile["name"] in utilities:
            numOwned = self._numOwned(tile["owner"], utilities)
            if numOwned == 1:
                return self._attemptTakeRent(tile["owner"], 4 * self.numRolled)
            if numOwned == 2:
                return self._attemptTakeRent(tile["owner"], 10 * self.numRolled)
        else:
            return self._attemptTakeRent(tile["owner"], self._getOwedRent(tile))

    def _attemptTakeRent(self, owner, amount):
        """
            Takes amount from the current player and gives it to owner, returning a Rent log if this
            was successful, a Bankruptcy Log if the current player does not have amount

            Parameter: owner, the player that will receive the rent
            Requires: Must be of type Player

            Parameter: amount, the amount of cash to give the owner
            Requires: Must be of type int
        """
        currentPlayer = self.currentPlayer.toDict()
        if amount > currentPlayer["cash"]:
            return [("Bankruptcy Player", f"You owe {amount} to {owner.toDict()['name']}")]
        else:
            self.currentPlayer.takeCash(amount)
            owner.giveCash(amount)
            return [('Rent', f"{currentPlayer['name']} paid ${amount} to {owner.toDict()['name']}")]

    def _takeTax(self):
        """
            Takes the appropriate amount of tax from the current player

            Returns: A tax log if the player can pay the tax, a Bankruptcy Bank log otherwise
        """
        currentPlayer = self.currentPlayer.toDict()
        tileName = self.board.getTile(currentPlayer["location"])["name"]
        if tileName == "Income Tax":
            if currentPlayer["cash"] < 200:
                return [("Bankruptcy Bank", "You owe $200 to the Bank")]
            else:
                self.currentPlayer.takeCash(200)
                return [("Tax", f"{currentPlayer['name']} paid $200 in Income Tax")]
        if tileName == "Luxury Tax":
            if currentPlayer["cash"] < 100:
                return [("Bankruptcy Bank", "You owe $100 to the Bank")]
            else:
                self.currentPlayer.takeCash(100)
                return [("Tax", f"{currentPlayer['name']} paid $100 in Luxury Tax")]

    def _numOwned(self, owner, props):
        """
            Returns the number of properties in props that are owned by owner.

            Parameter: owner, the owner requested
            Requires: Must be of type Player

            Parameter: props, list of the names of properties to check
            Requires: Must be of type string list
        """
        total = 0
        for prop in props:
            if self.board.getTile(self.board.getTileId(prop))["owner"] == owner:
                total += 1
        return total

    def _getOwedRent(self, tile):
        """
            Returns the amount of rent that would be paid if a player landed on the tile described
            in tile

            Parameter: tile, the dictionary describing the tile requested
            Requires: Must be of type dict
        """
        currentMonopolies = self.board.getMonopolies()
        if tile["color"] not in currentMonopolies:
            return tile["rents"][0]
        elif tile["numHouses"] == 0:
            return tile["rents"][0] * 2
        else:
            return tile["rents"][tile["numHouses"]]
# Jail Helpers

    def _checkJail(self):
        """
            If the current player is not jail, return none, if the current player is in jail, but 
            has turns remaining, returns a Jail log, if the current player is in jail and does not
            have turns remaining, forces them to pay $50 to leave jail returning Jail Success or 
            Bankruptcy Log depending on the results of the action
        """
        currentPlayer = self.currentPlayer.toDict()
        if not currentPlayer["inJail"]:
            return None
        elif currentPlayer["inJail"] and currentPlayer["numTurnsInJail"] < 3:
            return [("Jail", "Began Turn")]
        else:
            if currentPlayer["cash"] >= 50:
                self.currentPlayer.takeCash(50)
                self.currentPlayer.leaveJail()
                return [("Jail Success", f"{currentPlayer['name']} was forced to pay $50 to get out of jail")]
            else:
                return [("Bankruptcy Bank", "You owe $50 to the Bank")]

    def _goToJail(self):
        """
            Sends the current player to jail
        """
        self.currentPlayer.goToJail()

# Trade Helpers

    def _checkTrade(self, p1Dict, p2Dict):
        """
            Verifies that the current player owns everything in the p1Dict, and the player with name
            p2Dict["name"] has everything in p2Dict.
            Returns: A Trade Fail log if one of the players is missing something, None otherwise

            Parameter: p1Dict, the dictionary specifying what player 1 gives to player 2
            Requires: Must be of type dict

            Parameter: p2Dict, the dictionary specifying what player 2 gives to player 1
            Requires: Must be of type dict
        """
        currentPlayer = self.currentPlayer.toDict()
        for player in self.getPlayers():
            if player["name"] == p2Dict["name"]:
                player2 = player

        if currentPlayer['cash'] < p1Dict['cash']:
            return ("Trade Fail", f"{currentPlayer['name']} doesn't have ${p1Dict['cash']}")
        if player2['cash'] < p2Dict["cash"]:
            return ("Trade Fail", f"{player2['name']} doesn't have ${p2Dict['cash']}")

        for propName in p1Dict['properties']:
            if propName not in currentPlayer['properties']:
                return ("Trade Fail", f"{currentPlayer['name']} doesn't own {propName}")

        for propName in p2Dict['properties']:
            if propName not in player2['properties']:
                return ("Trade Fail", f"{player2['name']} doesn't own {propName}")

        if currentPlayer['jailCards'] < p1Dict['jailCards']:
            return ("Trade Fail", f"{currentPlayer['name']} doesn't have {p1Dict['jailCards']} Get Out of Jail Free Cards")
        if player2['jailCards'] < p2Dict['jailCards']:
            return ("Trade Fail", f"{player2['name']} doesn't have {p2Dict['jailCards']} Get Out of Jail Free Cards")

    def _makeTradeString(self, p1Dict, p2Dict):
        """
            Returns a string summarizing what player 1 trade with player 2

            Parameter: p1Dict, the dictionary specifying what player 1 gives to player 2
            Requires: Must be of type dict

            Parameter: p2Dict, the dictionary specifying what player 2 gives to player 1
            Requires: Must be of type dict
        """
        def makeProper(stringList):
            if len(stringList) == 0:
                return ""
            if len(stringList) == 1:
                return stringList[0]
            if len(stringList) == 2:
                return f"{stringList[0]} and {stringList[1]}"
            result = ""
            for entry in stringList[:-1]:
                result += f"{entry}, "
            result += f"and {stringList[-1]}"
            return result

        p1CashString = '' if p1Dict['cash'] == 0 else f"${p1Dict['cash']}"
        p2CashString = '' if p2Dict['cash'] == 0 else f"${p2Dict['cash']}"

        p1Props = makeProper(p1Dict['properties'])
        p1Props = ', ' + p1Props if p1Props != '' else p1Props
        p2Props = makeProper(p2Dict['properties'])
        p2Props = ', ' + p2Props if p2Props != '' else p2Props

        if p1Dict['jailCards'] == 0:
            p1JailString = ''
        else:
            p1JailString = f", and {p1Dict['jailCards']} Get Out of Jail Free Cards"

        if p2Dict['jailCards'] == 0:
            p2JailString = ''
        else:
            p2JailString = f", and {p2Dict['jailCards']} Get Out of Jail Free Cards"

        tradeString = (f"{self.currentPlayer.toDict()['name']} traded "
                       f"{p1CashString}{p1Props}{p1JailString} with {p2Dict['name']} "
                       f"for {p2CashString}{p2Props}{p2JailString}.")
        return tradeString
# Build and Mortgage Helpers

    def _getOwnedTiles(self):
        """
            Returns a list of dictionaries representing every tile that the current player owns
        """
        return list(map(lambda propName: self.board.getTile(self.board.getTileId(propName)),
                        self.currentPlayer.toDict()["properties"]))

    def _updateMonopolies(self):
        """
            Updates the monopolies on the board to reflect the current game status
        """
        for playerDict in self.getPlayers():
            for color, props in self.possMonopolies.items():
                if props <= playerDict["properties"]:
                    self.board.setMonopoly(playerDict["name"], color)
