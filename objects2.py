class Tile:
    # Initialization
    def __init__(self):
        pass

    # Getters and Setters
    def getId(self):
        """
            Returns the id of the tile
        """
        pass

    def toDict(self):
        """
            Returns a dictionary representation of the tile
        """
        pass

    def setOwner(self, owner):
        """
            Sets the owner of the tile to owner.

            Parameter: owner, the new owner of the tile
            Requires: Must be of type Player
        """
        pass

    def setMortgage(self):
        """
            Reverses the mortgaged property of the tile, if it is currently mortgaged will
            unmortgaged, if currently unmortgaged, will mortgage
        """
        pass
    # Functionality

    def build(self):
        """
            Adds 1 house to the tile
        """
        pass

    def sell(self):
        """
            Removes 1 houses from the tile
        """
        pass


class Board:
    def __init(self):
        pass

    def toDict(self):
        """
            Returns a dictionary representation of every tile on the board
        """
        pass

    def getTile(self, tileId):
        """
            Returns a dictionary representation of the tile with id, tileId

            Parameter: tileId, the id of the tile requested
            Requires: Must be of type int
        """
        pass

    def getTileId(self, tileName):
        """
            Returns the id of the tile with name, tileName

            Parameter: tileName, the name of the tile requested
            Requires: Must be of type string
        """
        pass

    def getTileObject(self, tileId):
        """
            Returns the tile object with id tileId

            Parameter: tileId, the id of the tile requested
            Requires: Must be of type int
        """
        pass

    def getMonopolies(self):
        """
            Returns a dictionary of color: player.name pairs where player name has a monopoly on 
            color group
        """
        pass

    def setMonopoly(self, colorGroup, playerName):
        """
            Sets the monopoly of color group to playerName

            Parameter: colorGroup, the color group of the new monopoly
            Requires: Must be of type string 

            Parameter: playerName, the name of the player that has the new monopoly
            Requires: Must be of type string
        """
        pass


class Player:
    def __init__(self):
        pass
#Getters and Setters

    def toDict(self):
        """
            Returns a dictionary representation of the player
        """
        pass
# Main Functionality

    def move(self, spaces):
        """
            Moves the player forward by spaces

            Parameter: spaces, the number of spaces to move by
            Requires: Must be of type int
        """
        pass

    def giveCash(self, amount):
        """
            Adds amount to the player's cash 

            Parameter: amount, the amount to give the player
            Requires: Must be of type int
        """
        pass

    def takeCash(self, amount):
        """
            Takes amount from the player's cash 

            Parameter: amount, the amount to give the player
            Requires: Must be of type int
        """
        pass

    def giveProperty(self, tileId):
        """
            Gives the player the tile with id, tileId

            Parameter: tileId, the id of the tile to give
            Requires: Must be of type int
        """
        pass

    def takeProperty(self, tileId):
        """
            Takes the tile with id, tileId, from the player 

            Parameter: tileId, the id of the tile to take
            Requires: Must be of type int
        """
        pass

    def goToJail(self):
        """
            Sends the player to jail and sets their status as in jail
        """
        pass

    def endTurnInJail(self):
        """
            Increments the number of turns the player has spent in jail
        """
        pass

    def leaveJail(self):
        """
            Resets the player's jail status
        """
        pass

    def useJailCard(self):
        """
            Uses a Get Out Of Jail Free Card to reset the player's jail status
        """
        pass

# Card Functions
    def advanceTo(self, tileName):
        """
            Moves the player forward until they reach tile with name, tileName

            Parameter: tileName, the name of the tile to go to
            Requires: Must be of type string
        """
        pass

    def giveToEach(self, amount, players):
        """
            Gives amount of cash to every player in players 

            Parameter: amount, the amount of cash to give
            Requires: Must be of type int 

            Parameter: players, the list of players to give cash to
            Requires: Must be of type Player list
        """
        pass

    def takeFromEach(self, amount, players):
        """
            Takes amount of cash from every player in players 

            Parameter: amount, the amount of cash to take
            Requires: Must be of type int 

            Parameter: players, the list of players to take cash from
            Requires: Must be of type Player list
        """
        pass

    def makeRepairs(self, perHouse, perHotel):
        """
            Pays perHouse for every house owned and perHotel for every hotel owned

            Parameter: perHouse, the amount to pay for each house owned
            Requires: Must be of type int

            Parameter: perHotel, the amount to pay for each hotel owned
            Requires: Must be of type int
        """
        pass

    def advanceToNearestRailroad(self):
        """
            Moves the player forward until they reach the nearest railroad
        """
        pass

    def advanceToNearestUtility(self):
        """
            Moves the player forward until they reach the nearest utility
        """
        pass

    def giveJailCard(self):
        """
            Gives the player 1 Get Out of Jail Free Card
        """
        pass


class Card:
    def __init__(self):
        pass

    def getAction(self):
        """
            Returns the action to be executed if the card is drawn
        """
        pass

    def getText(self):
        """
            Returns the text on the card
        """
        pass
