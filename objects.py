from consts import *


class Tile:
    # Initialization
    def __init__(self, tileId, name, price, rents, houseCost, color):
        """
            Creates a single Tile Object 

            Parameter: tileId, the id of the tile 
            Requires: Must be of type int 

            Parameter: name, the name of the tile
            Requires: Must be of type string

            Parameter: price, the price to buy the tile, 0 if unbuyable
            Requires: Must be of type int

            Parameter: rents, rents[i] is the rent owed with i houses
            Requires: Must be of type int list 

            Parameter: houseCost, the cost to buy a house on the tile, 0 if unbuildable
            Requires: Must be of type int

            Parameter: color, the color of the tile
            Requires: Must be of type string            
        """
        self.id = tileId
        self.name = name
        self.price = price
        self.rents = rents
        self.houseCost = houseCost
        self.color = color
        self.numHouses = 0
        self.mortgaged = False
        self.owner = None

    # Getters and Setters
    def getId(self):
        """
            Returns the id of the tile
        """
        return self.id

    def toDict(self):
        """
            Returns a dictionary representation of the tile
        """
        tileDict = {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "rents": self.rents,
            "houseCost": self.houseCost,
            "color": self.color,
            "numHouses": self.numHouses,
            "mortgaged": self.mortgaged,
            "owner": self.owner
        }
        return tileDict

    def setOwner(self, newOwner):
        """
            Sets the owner of the tile to newOwner.

            Parameter: newOwner, the new owner of the tile
            Requires: Must be of type Player
        """
        self.owner = newOwner

    def setMortgage(self):
        """
            Reverses the mortgaged property of the tile, if it is currently mortgaged will
            unmortgaged, if currently unmortgaged, will mortgage
        """
        self.mortgaged = not self.mortgaged
    # Functionality

    def build(self):
        """
            Adds 1 house to the tile
        """
        self.numHouses += 1

    def sell(self):
        """
            Removes 1 houses from the tile

            Requires: Tile must have at least 1 house
        """
        self.numHouses -= 1


class Board:
    def __init__(self, tiles):
        """
            Creates a single Board object with the tiles given 

            Parameter: tiles, a list of the tiles on the board
            Requires: Must be of type Tile list
        """
        self.tiles = tiles
        self.monopolies = {}

    def toDict(self):
        """
            Returns a dictionary representation of every tile on the board
        """
        return list(map(Tile.toDict, self.tiles))

    def getTile(self, tileId):
        """
            Returns a dictionary representation of the tile with id, tileId

            Parameter: tileId, the id of the tile requested
            Requires: Must be of type int
        """
        return self._findTile(tileId).toDict()

    def getTileId(self, tileName):
        """
            Returns the id of the tile with name, tileName

            Parameter: tileName, the name of the tile requested
            Requires: Must be of type string
        """
        for tile in self.tiles:
            if tile.toDict()["name"] == tileName:
                return tile.toDict()["id"]

    def getTileObject(self, tileId):
        """
            Returns the tile object with id tileId

            Parameter: tileId, the id of the tile requested
            Requires: Must be of type int
        """
        return self._findTile(tileId)

    def getMonopolies(self):
        """
            Returns a dictionary of color: player.name pairs where player name has a monopoly on 
            color group
        """
        return self.monopolies

    def setMonopoly(self, colorGroup, playerName):
        """
            Sets the monopoly of color group to playerName

            Parameter: colorGroup, the color group of the new monopoly
            Requires: Must be of type string 

            Parameter: playerName, the name of the player that has the new monopoly
            Requires: Must be of type string
        """
        self.monopolies[colorGroup] = playerName

    def _findTile(self, tileId):
        """
            Returns the tile object with id, tileId

            Parameter: tileId, the id of the tile requested
            Requires: Must be of type int
        """
        for tile in self.tiles:
            if tile.toDict()["id"] == tileId:
                return tile


class Player:
    def __init__(self, playerId, playerName, color):
        """
            Creates a single Player object 

            Parameter: playerId, the id of the player
            Requires: Must be of type int

            Parameter: playerName, the name of the player
            Requires: Must be of type string

            Parameter: color, the color of the player's piece
            Requires: Must be of type string
        """
        self.id = playerId
        self.name = playerName
        self.color = color
        self.location = 0
        self.cash = STARTING_CASH
        self.properties = set()
        self.inJail = False
        self.numTurnsInJail = 0
        self.jailCards = 0

#Getters and Setters

    def toDict(self):
        """
            Returns a dictionary representation of the player
        """
        playerDict = {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "location": self.location,
            "cash": self.cash,
            "properties": self.properties,
            "inJail": self.inJail,
            "numTurnsInJail": self.numTurnsInJail,
            "jailCards": self.jailCards
        }
        return playerDict
# Main Functionality

    def move(self, spaces):
        """
            Moves the player forward by spaces

            Parameter: spaces, the number of spaces to move by
            Requires: Must be of type int
        """
        self.location += spaces
        if self.location > 39:
            self.location % 39
            self.cash += 200 

    def giveCash(self, amount):
        """
            Adds amount to the player's cash 

            Parameter: amount, the amount to give the player
            Requires: Must be of type int
        """
        self.cash += amount

    def takeCash(self, amount):
        """
            Takes amount from the player's cash 

            Parameter: amount, the amount to give the player
            Requires: Must be of type int
        """
        self.cash -= amount

    def giveProperty(self, tileId):
        """
            Gives the player the tile with id, tileId

            Parameter: tileId, the id of the tile to give
            Requires: Must be of type int
        """
        self.properties.add(Board.getTile(tileId)["name"])

    def takeProperty(self, tileId):
        """
            Takes the tile with id, tileId, from the player 

            Parameter: tileId, the id of the tile to take
            Requires: Must be of type int
        """
        self.properties.discard(Board.getTile(tileId)["name"])

    def goToJail(self):
        """
            Sends the player to jail and sets their status as in jail

            Requires: the player must not be in jail
        """
        self.inJail = True

    def endTurnInJail(self):
        """
            Increments the number of turns the player has spent in jail

            Requires: the player must be in jail
        """
        self.numTurnsInJail += 1

    def leaveJail(self):
        """
            Resets the player's jail status

            Requires: the player must be in jail
        """
        self.inJail = False
        self.numTurnsInJail = 0

    def useJailCard(self):
        """
            Uses a Get Out Of Jail Free Card to reset the player's jail status

            Requires: the player has at least 1 Get Out Of Jail Free Card
        """
        self.inJail = False
        self.numTurnsInJail = 0
        self.jailCards -= 1
# Card Functions

    def advanceTo(self, tileName, board):
        """
            Moves the player forward until they reach tile with name, tileName

            Parameter: tileName, the name of the tile to go to
            Requires: Must be of type string

            Parameter: board, the board that the player is on
            Requires: Must be of type Board
        """
        tileLocation = board.getTileId(tileName)
        if tileLocation < self.location:
            self.giveCash(200)
        self.location = tileLocation

    def giveToEach(self, amount, players):
        """
            Gives amount of cash to every player in players 

            Parameter: amount, the amount of cash to give
            Requires: Must be of type int 

            Parameter: players, the list of players to give cash to
            Requires: Must be of type Player list
        """
        for player in players:
            player.giveCash(amount)
            self.takeCash(amount)

    def takeFromEach(self, amount, players):
        """
            Takes amount of cash from every player in players 

            Parameter: amount, the amount of cash to take
            Requires: Must be of type int 

            Parameter: players, the list of players to take cash from
            Requires: Must be of type Player list
        """
        for player in players:
            player.takeCash(amount)
            self.giveCash(amount)

    def makeRepairs(self, perHouse, perHotel):
        """
            Pays perHouse for every house owned and perHotel for every hotel owned

            Parameter: perHouse, the amount to pay for each house owned
            Requires: Must be of type int

            Parameter: perHotel, the amount to pay for each hotel owned
            Requires: Must be of type int
        """
        numHouses = 0
        numHotels = 0

        for tileName in self.properties:
            housesOnProperty = Board.getTile(Board.getTileId(tileName))["numHouses"]
            if housesOnProperty == 5:
                numHotels += 1
            else:
                numHouses += housesOnProperty

        self.takeCash(perHouse * numHouses)
        self.takeCash(perHotel * numHotels)

    def advanceToNearestRailroad(self):
        """
            Moves the player forward until they reach the nearest railroad
        """
        readingLoc = Board.getTileId("Reading Railrod")
        pennsylvaniaLoc = Board.getTileId("Pennsylvania Railroad")
        bAndOLoc = Board.getTileId("B. & O. Railroad")
        shortLoc = Board.getTileId("Short Line")

        if self._location < readingLoc or self._location > shortLoc:
            self.advanceTo("Reading Railroad")
        elif self._location < pennsylvaniaLoc:
            self.advanceTo("Pennsylvania Railroad")
        elif self._location < bAndOLoc:
            self.advanceTo("B. & O. Railroad")
        else:
            self.advanceTo("Short Line")

    def advanceToNearestUtility(self):
        """
            Moves the player forward until they reach the nearest utility
        """
        electricCompLoc = Board.getTileId("Electric Company")
        waterWorksLoc = Board.getTileId("Water Works")

        if self._location > waterWorksLoc or self._location < electricCompLoc:
            self.advanceTo("Electric Company")
        else:
            self.advanceTo("Water Works")

    def giveJailCard(self):
        """
            Gives the player 1 Get Out of Jail Free Card
        """
        self.jailCards += 1


class Card:
    def __init__(self, text, action):
        """
            Creates a single Card object with the text and action give 

            Parameter: text, the text on the card
            Requires: Must be of type string 

            Parameter: action, the action to be executed once the card is drawn
            Requires: Must be of type function
        """
        self.text = text
        self.action = action

    def getText(self):
        """
            Returns the text on the card
        """
        return self.text

    def getAction(self):
        """
            Returns the action to be executed if the card is drawn
        """
        return self.action
