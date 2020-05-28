"""
    Game Module for Monopoly.

    This module contains all of the functions needed to implement the game logic.
    It allows the players to take turns, give input, and play the game.
"""
import json
from objects import *
import random
import os


class Game:
    """
        A Class to Contain the main Game objects

        Contains all of the methods need to run the game

        INSTANCE ATTRIBUTES:
        _board: the game board object [Board]
        _chanceCards: the list of all Chance Cards in the game [Card list]
        _communityChestCards: the list of all Community Chest Cards in the game [Card list]
        _players: a list of the players in the game [Player list]
        _currPlayer: the player whose turn it currently is [Player]
    """
# Initialization----------------------------------------------------------------------------

    def __init__(self, players):
        """
            Creates a single Game object.

            Parameter: players, a list of tuples containing the ids, names, and colors of the players
            Requires: Must be of type (int, string, string) list
        """
        self._board = self._createBoard()
        cards = self._createCards()
        self._chanceCards = cards[0]
        self._communityChestCards = cards[1]
        self._players = self._createPlayers(players)
        self._currPlayer = self._players[0]

        self._hasRolled = False
        self._currChance = 0
        self._currCommunityChest = 0
# Board

    def _createBoard(self):
        """
            Initializes the board for the game.

            Creates the Board object with all of the tiles in game by loading them
            from board.json.

            Returns: A Board Object
        """
        possMonopolies = {}
        tiles = []
        with open(os.getcwd() + "\monopoly\\board.json") as boardJson:
            board = json.load(boardJson)
            for i, tile in enumerate(board["tiles"]):
                name = tile["name"]
                price = tile["price"]
                mortgage = tile["mortgage"]
                rents = tile["rents"]
                houseCost = tile["house cost"]
                color = tile["color"]
                newTile = BoardTile(i, name, price, rents, mortgage, houseCost, color)
                tiles.append(newTile)
                if possMonopolies.get(color) is None:
                    possMonopolies[color] = set()
                possMonopolies[color].add(i)
        del possMonopolies["white"]
        self._possMonopolies = possMonopolies
        return Board(tiles)
# Cards

    def _createCards(self):
        """
            Initializes the decks of cards for the game.

            Creates a list of Chance Card objects and a list of Community Chest
            Card Objects and returns the list that contains both of the above lists.
            I.e. [Chance Cards, Community Chest Cards]
        """
        return [self._createChanceCards(), self._createCommunityChestCards()]
# Chance

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
        def one(player): return player.advanceTo("Go")
        def two(player): return player.advanceTo("Illinois Ave", self._board)
        def three(player): return player.advanceTo("St. Charles Place", self._board)
        def four(player): return player.advanceToNearestUtility(self._board)
        def five(player): return player.advanceToNearestRailroad(self._board)
        def six(player): return player.giveCash(50)
        def seven(player): return player.giveGetOutOfJail()
        def eight(player): return player.move(-3)
        def nine(player): return player.goToJail()
        def ten(player): return player.makeRepairs(25, 100)
        def eleven(player): return player.takeCash(15)
        def twelve(player): return player.advanceTo("Reading Railroad", self._board)
        def thirteen(player): return player.advanceTo("Boardwalk", self._board)
        def fourteen(player): return player.giveToEach(50, self._players)
        def fifteen(player): return player.giveCash(150)
        return [zero, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen]

    def _createChanceCards(self):
        """
            Returns a list of Card objects for every chance card in the game.
        """
        chanceCards = []
        texts = self._chanceCardTexts()
        actions = self._chanceCardActions()
        for text, action in zip(texts, actions):
            chanceCards.append(Card(text, action))
        return chanceCards
# Community Chest

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
        def zero(player): return player.advanceTo("Go")
        def one(player): return player.giveCash(200)
        def two(player): return player.takeCash(50)
        def three(player): return player.giveCash(50)
        def four(player): return player.giveGetOutOfJail()
        def five(player): return player.goToJail()
        def six(player): return player.takeFromEach(50, self._players)
        def seven(player): return player.giveCash(100)
        def eight(player): return player.giveCash(20)
        def nine(player): return player.takeFromEach(10, self._players)
        def ten(player): return player.giveCash(100)
        def eleven(player): return player.takeCash(50)
        def twelve(player): return player.takeCash(50)
        def thirteen(player): return player.giveCash(50)
        def fourteen(player): return player.makeRepair(40, 115)
        def fifteen(player): return player.giveCash(10)
        def sixteen(player): return player.giveCash(100)
        return [zero, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen]

    def _createCommunityChestCards(self):
        """
            Returns an array of  Card Objects that represent all of the community
            chest cards in game.
        """
        communityChestCards = []
        texts = self._communityChestCardTexts()
        actions = self._communityChestCardActions()
        for text, action in zip(texts, actions):
            communityChestCards.append(Card(text, action))
        return communityChestCards

# Players
    def _createPlayers(self, players):
        """
            Creates the list of player objects for the game

            Parameter: players, a list of tuples containing the ids, names and colors of the players
            Requires: Must be of type (int, string, string) list
        """
        playerList = []
        for i, name, color in players:
            playerList.append(Player(i, name, color))
        return playerList

# Getters------------------------------------------------------------------------------------
    def getPlayers(self):
        """
            Returns a list of dictionaries that represent each player. 
        """
        return list(map(lambda player: player.to_dict(), self._players))

    def getCurrPlayer(self):
        """
            Returns a dictionary representation of the current player
        """
        return self._currPlayer.to_dict()

    def getTileName(self, tileID):
        """
            Returns the name of tile with id [tileID]

            Parameter: tileID, the id of the tile requested
            Requires: Must be of type int

        """
        return self._board.getName(tileID)
# Game Functionality-------------------------------------------------------------------------

# General
    def rollDice(self):
        """
            If the current player has not rolled yet then rolls the dice and moves the player by
            the number of places shown and returns "Success". Returns "Already Rolled" otherwise.
        """
        if not self._hasRolled:
            roll = random.randint(2, 12)
            self._currPlayer.move(roll)
            self._hasRolled = True
            return self._handleTile()
        else:
            return ("Already Rolled")

    def buy(self):
        """
            Returns a string and may purchase the current tile.


            Returns "Already Owned" if the tile the current player is on has an owner, "Not Buyable",
            the current tile is not a property tile, "Not Enough Money" if the current player
            cannot afford to buy the current tile, and "Success" if the current player can buy the
            current tile.
            If the player can buy the current tile then they will, I.e. cash is taken and ownership
            given.
        """
        player = self._currPlayer
        tileID = player.getLocation()
        price = self._board.getPrice(tileID)

        if price > player.getCash():
            return("Not Enough Money")
        else:
            self._board.setOwner(tileID, player)
            player.takeCash(price)
            player.giveProperty(tileID)
            self._checkMonopoly()
            return("Buy Success")

    def endTurn(self):
        """
            Returns "Success" and changes the current player if the player has rolled, "Has Not 
            Rolled" otherwise.
        """
        if self._hasRolled:
            nextPlayerIndex = (self._players.index(self._currPlayer) + 1) % len(self._players)
            self._currPlayer = self._players[nextPlayerIndex]
            self._hasRolled = False
            return "Success"
        else:
            return "Has Not Rolled"
# Board

    def _handleTile(self):
        # TODO: pay rent if necessary.
        tileID = self._currPlayer.getLocation()
        name = self._board.getName(tileID)
        if self._board.getPrice(tileID) != 0 and self._board.getOwner(tileID) is None:
            return "Not Owned"
        if name == "Chance" or name == "Community Chest":
            return self._drawCard()
        if name == "Income Tax":
            self._currPlayer.takeCash(200)
            return "Paid Income Tax"
        if name == "Luxury Tax":
            self._currPlayer.takeCash(100)
            return "Paid Luxury Tax"

    def getCurrentTile(self):
        return self._board.getName(self._currPlayer.getLocation())

    def _checkMonopoly(self):
        player = self.getCurrPlayer()
        for color, props in self._possMonopolies.items():
            if props <= player["propertyLocations"]:
                self._board.setMonopoly(player["name"], color)

    def getMonopolies(self, name):
        monopolies = []
        for color, owner in self._board.getMonopolies().items():
            if owner == name:
                monopolies.append(color)
        return monopolies
# Cards

    def _drawCard(self):
        tileID = self._currPlayer.getLocation()
        name = self._board.getName(tileID)
        if name == "Chance":
            card = self._chanceCards[self._currChance]
            action = card.getAction()
            action(self._currPlayer)
            self._currChance += 1
            return card.getText()
        else:
            card = self._communityChestCards[self._currCommunityChest]
            action = card.getAction()
            action(self._currPlayer)
            self._currCommunityChest += 1
            return card.getText()

# Trading
    def trade(self, p1Dict, p2Dict):
        if self._checkTrade(p1Dict, p2Dict) == "Good":
            p1 = self._currPlayer
            for player in self._player:
                if player.getName() == p2Dict["name"]:
                    p2 = player

            p1.giveCash(p2Dict["cash"])
            p2.giveCash(p1Dict["cash"])
            p1.takeCash(p1Dict["cash"])
            p2.takeCash(p2Dict["cash"])

            for prop in p1Dict["properties"]:
                p1.takeProperty(prop)
                p2.giveProperty(prop)
            for prop in p2Dict["properties"]:
                p1.giveProperty(prop)
                p2.takeProperty(prop)

            for i in range(p1Dict["numJail"]):
                p1.takeGetOutOfJail()
                p2.giveGetOutOfJail()
            for i in range(p2Dict["numJail"]):
                p1.giveGetOutOfJail()
                p2.takeGetOutOfJail()

        def _checkTrade(self, p1Dict, p2Dict):
            p1 = self._currPlayer
            for player in self._player:
                if player.getName() == p2Dict["name"]:
                    p2 = player
            p1Cash = p1Dict["cash"]
            p2Cash = p2Dict["cash"]
            p1Props = p1Dict["properties"]
            p2Props = p2Dict["properties"]
            p1Jail = p1Dict["numJail"]
            p2Jail = p2Dict["numJail"]

            if p1.getCash() < p1Cash:
                return f"{p1.getName} doesn't have ${p1Cash}"
            elif p2.getCash() < p2Cash:
                return f"{p2.getName} doesn't have ${p2Cash}"
            # Check Props
            # Check Jails
            else:
                return "Good"
