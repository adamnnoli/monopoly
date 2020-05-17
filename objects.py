"""
    Objects Module for Monopoly

    This module contains the class information for all of the objects used in the
    game.
"""


class GameConstants:
    startingCash = 1500


class BoardTile:
    """
        A Class to Represent a tile on the board.

        Contains all of the information related to that tile and contains methods
        to allow actions to be done on the tile such as buying and building.
    """

    def __init__(self, id, price, rents, mortgage, houseCost, color):
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

            Parameter: mortgage, the amount the player would recieve if they
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
        self._price = price
        self._rents = rents
        self._mortgage = mortgage
        self._houseCost = houseCost
        self._color = color
        self._owner = None


class Player:
    """
        A class to represent a player in the game.

        Contains all of the information about an individual player and contains
        the necessary methods to move them around the board, add or subtract money,
        and give or take properties.

        INSTANCE ATTRIBUTES:

        _number: the player number [int]
        _color: the color of the player's peice [string]
        _cash: the amount of money the player currently has [int]
        _location: the id of the tile the player is currently on [int]
        _propertiesIds: list of the ids of the properties the player owns [int list]
    """

    def __init__(self, number, color):
        """
            Creates a single player object.

            Parameter: number, the number of the player. I.e player 1, 2, etc.
            Precondtion: Must be an int

            Parameter: color, the color of the player's piece.
            Precondition: Must be a string
        """
        self._number = number
        self._color = color
        self._cash = GameConstants.startingCash
        self._location = 0
        self._propertiesIds = []


class CommunityChestCard:
    """
        A class to represent a Community Chest Card

        Contains all of the information that the card holds.

        INSTANCE ATTRIBUTES:
        _text: the text on the card
        _action: the function to be executed when the card is drawn.
    """

    def __init__(self, text, action):
        self._text = text
        self._action = action

    def getText(self):
        self._text

    def getAction(self):
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
        self._text = text
        self._action = action

    def getText(self):
        self._text

    def getAction(self):
        self._action
