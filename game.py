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
        self.communityChestCard = self.createCommunityChestCards
        self.players = self.createPlayers(players)
        self.currentPlayer = self.players[0]
        self.currentChanceIndex = 0
        self.currentCommunityChestIndex = 0
        self.hasRolled = False

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
                possMonopolies[tile["color"]].add(i)
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
            pass
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
            pass

        def sell(self):
            """
                Sells a house on the tile with name, tileName

                Returns: A Build Success log

                Parameter: tileName, the name of the tile to sell from
                Requires: Must be of type string

                Requires: Selling must not break the build evenly rule, the tile must have at least
                one house
            """
            pass
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
            pass
    # Mortgaging

        def mortgage(self, tileName):
            """
                Sets the status of the tile with name, tileName to mortgaged, giving the player
                the proceeds

                Returns: A Mortgage Success Log 

                Parameter: tileName, the name of the tile to mortgage
                Requires: Must be of type string
            """
            pass

        def unmortgage(self, tileName):
            """
                Attempts to unmortgage the tile with name tileName

                Returns: A Mortgage Success log if the player had enough cash, A Mortgage Fail log
                otherwise 

                Parameter: tileName, the name of the tile to unmortgage
                Requires: Must be of type string
            """
            pass
    # Quitting

        def quit(self):
            """
                Removes the current player from the game, forfeiting all assets to the bank

                Returns: A Quit Log
            """
            pass
    # Jail

        def payJail(self):
            """
                Attempts to pay $50 to remove the current player from jail

                Returns: A Jail Success log if the player had enough money, A Jail Fail log
                otherwise
            """
            pass

        def rollJail(self):
            """
                Rolls the dice, if the result is a double, removes the current player from jail
                and moves them the amount rolled, returning a list of logs with the log of leaving
                jail and the log from rolling the dice
                If the result is not a double returns A Jail Success Log
            """
            pass

        def cardJail(self):
            """
                Attempts to use a Get Out Of Jail Free Card to remove the current player to jail.

                Returns: A Jail Success Log if the player had a Get Out of Jail Free Card, a Jail
                Fail Log otherwise
            """
            pass
    # End Turn

        def endTurn(self):
            """
                Attempts to end the current player's turn and begin the next player's turn 

                Returns: A log appropriate based on the result of the attempt
            """
            pass
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
        def one(): return self._advanceTo("Go")
        def two(): return self._advanceTo("Illinois Ave")
        def three(): return self._advanceTo("St. Charles Place")
        def four(): return self._advanceToNearestUtility()
        def five(): return self._advanceToNearestRailroad()
        def six(player): return player.giveCash(50)
        def seven(player): return player.giveGetOutOfJail()
        def eight(): return self._move(-3)
        def nine(player): return player.goToJail()
        def ten(player): return player.makeRepairs(25, 100)
        def eleven(player): return player.takeCash(15)
        def twelve(): return self._advanceTo("Reading Railroad")
        def thirteen(): return self._advanceTo("Boardwalk")
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

            Returns: A Buy log if the tile is unowned and a Rent log otherwise
        """
        pass

    def _advanceToNearestRailRoad(self):
        """
            Advances player to the nearest railroad if it is owned the pays the owner double the
            amount owed. 

            Returns: A Buy log if the tile is unowned and a Rent log otherwise
        """
        pass

    def _advanceToNearestUtility(self):
        """
            Advances player to the nearest utility if it is owned rolls the dice and pays the owner 
            10x the number rolled. 

            Returns: A Buy log if the tile is unowned and a Rent log otherwise 
        """
        pass

    def _move(self, spaces):
        """
            Moves the current player spaces places. And handles the effects on landing on the new
            tile.

            Returns: A list of logs associated with landing on the new tile.
        """
        pass
# Rolling Helpers

    def _handleTile(self):
        """
            Calls the necessary functions and performs the necessary actions to be executed when 
            the current player lands on the current tile.

            Returns: A list of appropriate logs
        """
        pass

    def _drawCard(self):
        """
            If the current player is on a chance card tile, draws the current chance card, if the 
            current player is on a community chest card tile, draws the current community chest
            card.

            Returns: A list of logs, the first being the log for the card text, the rest of the list
            is the logs that arise from executing the card action
        """
        pass

    def _takeRent(self):
        """
            Pays rent owed to the owner of the current tile.

            Returns: A list TODO: finish this, should it be you have negative money and when you 
            declare your assets go to the bank or is it that the player gets your money or your 
            assets.
        """
        pass
# Jail Helpers

    def _goToJail(self):
        """
            Sends the current player to jail
        """
        pass

    def _forceJail(self):
        """
            Forces the player to pay 50 dollars to get out of jail.

            Returns: A Jail Fail log if the player was able to pay, a Bankruptcy log otherwise.
        """
        pass
# Trade Helpers

    def _checkTrade(self):
        """
            Verifies that the current player owns everything in the p1Dict, and the player with name
            p2Dict["name"] has everything in p2Dict.
            Returns: A Trade Fail log if one of the players is missing something, None otherwise
        """
        pass

# Build and Mortgage Helpers
    def _getOwnedTiles(self):
        """
            Returns a list of dictionaries representing every tile that the current player owns
        """
        return list(map(lambda propName: self.board.getTile(self.board.getTileId(propName)),
                        self.currentPlayer.toDict(["properties"])))
