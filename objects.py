"""
    Objects Module for Monopoly

    This module contains the class information for all of the objects used in the
    game.
"""
from consts import *


class BoardTile:
    """
        A Class to Represent a tile on the board.

        Contains all of the information related to that tile and contains methods
        to allow actions to be done on the tile such as buying and building.
    """

    def __init__(self, id, name, price, rents, mortgage, houseCost, color):
        """
            Creates a single Tile object.

            Parameter: id, the number of the tile, starts at 0 for Go increase by 1
            for every tile over.
            Precondition: Must be an int

            Parameter: price, the price to buy the tile.
            Precondition: Must be an int

            Parameter: rents, A list of rents for the property. rents[0] is the rents
            with 0 houses, rents[1] is with 1 house, etc. rents[5] is with hotel
            Precondition: Must be an int list

            Parameter: mortgage, the amount the player would receive if they
            mortgaged the property. IF the tile is not mortgagable then it must be 0.
            Precondition: Must be an int

            Parameter: houseCost, the cost to buy a house on this property, if
            you cannot build on the tile then it must be 0
            Precondition: Must be an int

            Parameter: color, the color of the tile. If the tile does not have a
            color then it must be "white"
            Precondition: Must be a string
        """
        self._id = id
        self._name = name
        self._price = price
        self._rents = rents
        self._mortgage = mortgage
        self._houseCost = houseCost
        self._color = color
        self._owner = None
        self._numHouses = 0
# Getters and Setters

    def getId(self):
        """
            Returns the id of the tile
        """
        return self._id

    def toDict(self):
        """
            Returns a dictionary representation of the tile
        """
        tileDict = {
            "id": self._id,
            "name": self._name,
            "price": self._price,
            "rents": self._rents,
            "mortgage": self._mortgage,
            "houseCost": self._houseCost,
            "color": self._color,
            "owner": self._owner,
            "numHouses": self._numHouses
        }
        return tileDict

    def build(self, numHouses):
        """
            Adds numHouses to the tile. 

            Requires: New total number of houses is at most 5 

            Parameter: numHouses, the number of houses to build
            Requires: Must be of type int
        """
        self._numHouses += numHouses

    def setOwner(self, owner):
        """
            Sets the owner of tile to owner.

            Parameter: owner, the new owner of the tile
            Requires: Must be of type Player

        """
        self._owner = owner


class Board:
    """
        Represents the game board as a list of BoardTiles.

        INSTANCE ATTRIBUTES:
        _tiles: the list of BoardTiles in the game [BoardTile list]
        _monopolies: dictionary of all of the monopolies owned [string:string dict]
    """

    def __init__(self, tiles):
        """
            Creates a single Board Object

            Parameter: tiles, the list of tiles on the board
            Requires: Must be of type BoardTile List

        """
        self._tiles = tiles
        self._monopolies = {}

# Getters and Setters
    def getTile(self, tileID):
        return self._findTile(tileID).toDict()

    def getID(self, tileName):
        """
            Returns the id of the tile with tileName

            Parameter: tileName, the name of the tile requested
            Requires: Must be of type string

        """
        for tile in self._tiles:
            if tile.getName() == tileName:
                return tile.getId()

    def setOwner(self, tileID, owner):
        """
            Returns the owner of the tile with id tileID

            Parameter: tileID, the id of tile requested
            Requires: Must be of type int

            Parameter: owner, the new owner of the tile
            Requires: Must be of type Player
        """
        return self._findTile(tileID).setOwner(owner)

    def getMonopolies(self):
        """
            Returns the dictionary of all of the monopolies owned
        """
        return self._monopolies

    def setMonopoly(self, name, color):
        """
            Sets the owner of the monopoly of the color tiles, to name 

            Parameter: name, the name of the monopoly owner
            Requires: Must be of type string

            Parameter: color, the color of the monopoly owned
            Requires: Must be of type string
        """
        self._monopolies[color] = name

    def buildHouses(self, tileID, numHouses):
        """
            Adds numHouses to the tile with id tileID

            Parameter: tileID, the id of the tile requested
            Requires: Must be of type int 

            Parameter: numHouses, the number of houses to build
            Requires: Must be of type int
        """
        self._findTile(tileID).build(numHouses)

    def _findTile(self, tileID):
        """
            Returns the BoardTile object with id tileID

            Parameter: tileID, the id of tile requested
            Requires: Must be of type int
        """
        for tile in self._tiles:
            if tile.getId() == tileID:
                return tile


class Player:
    """
        A class to represent a player in the game.

        Contains all of the information about an individual player and contains
        the necessary methods to move them around the board, add or subtract money,
        and give or take properties.

        INSTANCE ATTRIBUTES:

        _number: the player number [int]
        _name: the player's name [string]
        _color: the color of the player's piece [string]
        _cash: the amount of money the player currently has [int]
        _location: the id of the tile the player is currently on [int]
        _propertiesIds: list of the ids of the properties the player owns [int set]
        _inJail: true if the player is currently in jail[bool]
        _turnsInJail: the number of turns that the player has been in jail for [int]
        _numGetOutJail: the number of get out of jail free cards the player has[int]
    """

    def __init__(self, number, name, color):
        """
            Creates a single player object.

            Parameter: number, the number of the player. I.e player 1, 2, etc.
            Requires: Must be an int

            Parameter: name, the player's name
            Requires: Must be of type string

            Parameter: color, the color of the player's piece.
            Requires: Must be a string
        """
        self._number = number
        self._name = name
        self._color = color
        self._cash = STARTING_CASH
        self._location = 0
        self._propertiesIds = set()
        self._inJail = False
        self._turnsInJail = 0
        self._numGetOutJail = 0

# Getters and Setters

    def toDict(self):
        """
            Returns a dictionary representation of the player.
        """
        dict = {
            "id": self._number,
            "name": self._name,
            "color": self._color,
            "cash": self._cash,
            "location": self._location,
            "propertyLocations": self._propertiesIds
        }
        return dict

# Actions
    def move(self, places):
        """
            Moves the player over by [places] spaces.

            Parameter: places, the number of spaces to move the player
            Requires: Must be of type int
        """
        self._location += places
        if self._location >= 39:
            self._cash += 200
            self._location %= 39

    def takeCash(self, amount):
        """
            Reduces the player's cash by amount.

            Parameter: amount, the amount to reduce the cash by  
            Requires: Must be of type int
        """
        self._cash -= amount

    def giveCash(self, amount):
        """
            Increase the player's cash by amount.

            Parameter: amount, the amount to increase the cash by
            Requires: Must be of type int
        """
        self._cash += amount

    def giveProperty(self, tileID):
        """
            Gives the player the property with id tileID.

            Parameter: tileID, the id of the property to be given
            Requires: Must be of type int
        """
        self._propertiesIds.add(tileID)

    def takeProperty(self, tileID):
        """
            Takes the property with id tileID from player

            Parameter: tileID, the id of the property to be given
            Requires: Must be of type int
        """
        self._propertiesIds.discard(tileID)

    def advanceTo(self, tileName, board):
        """
            Advances the player to the tile with name tileName.

            Parameter: tileName, the name of tile to advance to
            Requires: Must be of type string

            Parameter: board, the game board that the tile is on
            Requires: Must be of type Board
        """
        tileLoc = board.getID(tileName)
        if self._location > tileLoc:
            self.giveCash(200)
        self._location = tileLoc

    def giveToEach(self, amount, players):
        """
            Gives every player in players amount of cash.

            Parameter: amount, the amount to give each players
            Requires: Must be of type int 

            Parameter: players, the list of players to give cash
            Requires: Must be of type Player list
        """
        for player in players:
            player.giveCash(amount)
        self.takeCash(amount * len(players))

    def takeFromEach(self, amount, players):
        """
            Takes amount from every player in players.

            Parameter: amount, the amount to give each players
            Requires: Must be of type int 

            Parameter: players, the list of players to give cash
            Requires: Must be of type Player list
        """
        for player in players:
            player.takeCash(amount)
        self.giveCash(amount * len(players))

    def makeRepairs(self, perHouse, perHotel):
        """
            Pays perHouse for every house owned and perHotel for every hotel owned.

            Parameter: perHouse, the amount to pay for each house owned
            Requires: Must be of type int

            Parameter: perHotel, the amount to pay for each hotel owned
            Requires: Must be of type int
        """
        numHouses = 0
        numHotels = 0

        for tileID in self._propertiesIds:
            housesOnProperty = Board.getNumHouses(tileID)
            if housesOnProperty == 5:
                numHotels += 1
            else:
                numHouses += housesOnProperty

        self.takeCash(perHouse * numHouses)
        self.takeCash(perHotel * numHotels)

    def goToJail(self):
        """
            Moves the player to the Jail tile and sets their status as in Jail
        """
        self._location = 10
        self._inJail = True

    def giveGetOutOfJail(self):
        """
            Gives the player 1 get out of jail free card.
        """
        self._numGetOutJail += 1

    def takeGetOutOfJail(self):
        """
            Takes 1 get out of jail free card from the player.
        """
        self._numGetOutJail -= 1

    def advanceToNearestUtility(self, board):
        """
            Advances the player to the nearest utility.

            Parameter: board, the game board the player is on
            Requires: Must be of type Board
        """
        electricCompLoc = board.getID("Electric Company")
        waterWorksLoc = board.getID("Water Works")

        if self._location > waterWorksLoc or self._location < electricCompLoc:
            self.advanceTo("Electric Company", board)
        else:
            self.advanceTo("Water Works", board)

    def advanceToNearestRailroad(self, board):
        """
            Advances the player to the nearest railroad.

            Parameter: board, the game board the player is on
            Requires: Must be of type Board
        """
        readingLoc = board.getID("Reading Railrod")
        pennsylvaniaLoc = board.getID("Pennsylvania Railroad")
        bAndOLoc = board.getID("B. & O. Railroad")
        shortLoc = board.getID("Short Line")

        if self._location < readingLoc or self._location > shortLoc:
            self.advanceTo("Reading Railroad", board)
        elif self._location < pennsylvaniaLoc:
            self.advanceTo("Pennsylvania Railroad", board)
        elif self._location < bAndOLoc:
            self.advanceTo("B. & O. Railroad", board)
        else:
            self.advanceTo("Short Line")

    def inJail(self):
        return self._inJail

    def numTurnsInJail(self):
        return self._turnsInJail

    def leaveJail(self):
        self._inJail = False


class Card:
    """
        A class to represent a Community Chest Card

        Contains all of the information that the card holds.

        INSTANCE ATTRIBUTES:
        _text: the text on the card
        _action: the function to be executed when the card is drawn.
    """

    def __init__(self, text, action):
        """
            Creates a single Chance Card.

            Parameter: text, the text on the card
            Requires: Must be of type string

            Parameter: action, the action to be executed when the card is drawn
            Requires: Must be of type function
        """
        self._text = text
        self._action = action

    def getText(self):
        """
            Returns: The text of the chance card
        """
        return self._text

    def getAction(self):
        """
            Returns: The action of the chance card
        """
        return self._action
