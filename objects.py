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
#Getters and Setters

    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def getPrice(self):
        return self._price

    def getRents(self):
        return self._rents

    def getMortgage(self):
        return self._mortgage

    def getHouseCost(self):
        return self._houseCost

    def getColor(self):
        return self._houseCost

    def getOwner(self):
        return self._owner

    def getNumHouses(self):
        return self._numHouses

    def setOwner(self, owner):
        self._owner = owner


class Board:
    def __init__(self, tiles):
        self._tiles = tiles

#Getters and Setters
    def getID(self, tileName):
        for tile in self._tiles:
            if tile.getName() == tileName:
                return tile.getID()

    def getOwner(self, tileID):
        return self._findTile(tileID).getOwner()

    def getPrice(self, tileID):
        return self._findTile(tileID).getPrice()

    def getName(self, tileID):
        return self._findTile(tileID).getName()

    def getNumHouses(self, tileID):
        return self._findTile(tileID).getNumHouses()

    def setOwner(self, tileID, owner):
        return self._findTile(tileID).setOwner(owner)

    def _findTile(self, tileID):
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
        _propertiesIds: list of the ids of the properties the player owns [int list]
        _inJail: true if the player is currently in jail[bool]
        _numGetOutJail: the number of get out of jail free cards the player has[int]
    """

    def __init__(self, number, name, color):
        """
            Creates a single player object.

            Parameter: number, the number of the player. I.e player 1, 2, etc.
            Requires: Must be an int

            Parmeter: name, the player's name
            Requires: Must be of type string

            Parameter: color, the color of the player's piece.
            Requires: Must be a string
        """
        self._number = number
        self._name = name
        self._color = color
        self._cash = STARTING_CASH
        self._location = 0
        self._propertiesIds = []
        self._inJail = False
        self._numGetOutJail = 0

#Getters and Setters

    def getLocation(self):
        return self._location

    def getCash(self):
        return self._cash

    def to_dict(self):
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
        self._location += places
        if self._location >= 39:
            self._cash += 200
            self._location %= 39

    def takeCash(self, amount):
        self._cash -= amount

    def giveCash(self, amount):
        self._cash += amount

    def giveProperty(self, tileID):
        self._propertiesIds.append(tileID)

    def advanceTo(self, tileName, board):
        tileLoc = board.getID(tileName)
        if self._location > tileLoc:
            self.giveCash(200)
        self._location = tileLoc

    def giveToEach(self, amount, players):
        for player in players:
            player.giveCash(amount)
        self.takeCash(amount * len(players))

    def takeFromEach(self, amount, players):
        for player in players:
            player.takeCash(amount)
        self.giveCash(amount * len(players))

    def makeRepairs(self, perHouse, perHotel):
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
        self._location = 10
        self._inJail = True

    def giveGetOutOfJail(self):
        self._numGetOutJail += 1

    def advanceToNearestUtility(self, board):
        
        electricCompLoc = board.getID("Electric Company")
        waterWorksLoc = board.getID("Water Works")
        
        if self._location > waterWorksLoc or self._location < electricCompLoc:
            self.advanceTo("Electric Company", board)
        else:
            self.advanceTo("Water Works", board)

    def advanceToNearestRailroad(self, board):
        
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


class CommunityChestCard:
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

            Parmeter: text, the text on the card
            Requires: Must be of type string

            Parmeter: action, the action to be executed when the card is drawn
            Requires: Must be of type function
        """
        self._text = text
        self._action = action

    def getText(self):
        """
            Returns: The text of the chance card
        """
        self._text

    def getAction(self):
        """
            Returns: The action of the chance card
        """
        self._action


class ChanceCard:
    """
        A class to represent a Chance Card

        Contains all of the information that the card holds.

        INSTANCE ATTRIBUTES:
        _text: the text on the card
        _action: the function to be executed when the card is drawn.
    """

    def __init__(self, text, action):
        """
            Creates a single Chance Card.

            Parmeter: text, the text on the card
            Requires: Must be of type string

            Parmeter: action, the action to be executed when the card is drawn
            Requires: Must be of type function
        """
        self._text = text
        self._action = action

    def getText(self):
        """
            Returns: The text of the chance card
        """
        self._text

    def getAction(self):
        """
            Returns: The action of the chance card
        """
        self._action
