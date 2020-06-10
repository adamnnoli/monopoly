from objects2 import *


class Game2:
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
        self.players = self.createPlayers()
        self.currentPlayer = self.player[0]
        self.currentChanceIndex = 0
        self.currentCommunityChestIndex = 0
        self.hasRolled = False

    def createBoard(self):
        """
            Returns the Board object for the game
        """
        pass

    def createChanceCards(self):
        """
            Returns a list of Card objects representing the chance cards in the game
        """
        pass

    def createCommunityChestCards(self):
        """
            Returns a list of Card objects representing the community chest cards in the game
        """
        pass

    def createPlayers(self):
        """
            Returns a list of Player objects representing the players in the game
        """
        pass
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

            The player can build a house on the property if building would not break the build
            evenly rule and the property is not mortgaged
        """
        pass

    def getSellable(self):
        """
            Returns a list of the names of properties that the current player can sell a house from

            The player can sell a house on the property if there is at least one house, and selling 
            a house would not break the build evenly rule
        """
        pass

    def getMortgageable(self):
        """
            Returns a list of the names of properties that the current player can mortgage
        """
        pass

    def getUnmortgageable(self):
        """
            Returns a list of the names of properties that the current player can unmortgage
        """
        pass

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
    def advanceToRailRoadCard(self, player):
        """
            Advances player to the nearest railroad if it is owned the pays the owner double the
            amount owed. 

            Returns: A Buy log if the tile is unowned and a Rent log otherwise
        """
        pass

    def advanceToUtilityCard(self, player):
        """
            Advances player to the nearest utility if it is owned rolls the dice and pays the owner 
            10x the number rolled. 

            Returns: A Buy log if the tile is unowned and a Rent log otherwise 
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
