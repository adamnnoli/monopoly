class Game2:
    # INITIALIZATION -----------------------------------------------------------------------------------
    def __init__(self):
        pass

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

    def getCurrentPlayer(self):
        """
            Returns a dictionary representation of the player whose turn it is
        """
        pass

    def getPlayers(self):
        """
            Returns a list of dictionaries representing every player in the game
        """
        pass

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
            pass
    # Building

        def build(self, tileName):
            """
                Tries to build a house on the tile with name, tileName.

                Returns: the appropriate log depending on the outcome of the attempt

                Parameter: tileName, the name of the tile to build on
                Requires: Must be of type string

                Requires: Building must not break the build evenly rule, the tile must not be 
                mortgaged
            """
            pass

        def sell(self):
            """
                Sells a house on the tile with name, tileName

                Returns: ("Build Success", "{Player Name} sold a house on {tileName}")

                Parameter: tileName, the name of the tile to sell from
                Requires: Must be of type string

                Requires: Selling must not break the build evenly rule, the tile must have at least
                one house
            """
            pass
    # Trading

        def trade(self, p1Trade, p2Trade):
            """
                If player 1 owns all of the items specified in p1Trade and player 2 owns all of the
                items specified in p2Trade, the players will transfer ownership of the items to 
                each other. and the Trade Success log will be returned.
                If not the appropriate log that details what a player is missing will be returned

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

                Returns: ("Mortgage Success", "{Player name} mortgaged {tile name} for {amount}")

                Parameter: tileName, the name of the tile to mortgage
                Requires: Must be of type string
            """
            pass

        def unmortgage(self, tileName):
            """
                Attempts to unmortgage the tile with name tileName

                Returns: A log appropriate based on the result of the attempt 

                Parameter: tileName, the name of the tile to unmortgage
                Requires: Must be of type string
            """
            pass
    # Quitting

        def quit(self):
            """
                Removes the current player from the game, forfeiting all assets to the bank
            """
            pass
    # Jail

        def payJail(self):
            """
                Attempts to pay $50 to remove the current player from jail

                Returns: A log appropriate based on the result of the attempt
            """
            pass

        def rollJail(self):
            """
                Rolls the dice, if the result is a double, removes the current player from jail
                and moves them the amount rolled, returning a list of logs with the log of leaving
                jail and the log from rolling the dice
                If the result is not a double returns:
                    ("Jail Success", "{Player name} did not roll doubles and is still in jail")
            """
            pass

        def cardJail(self):
            """
                Attempts to use a Get Out Of Jail Free Card to remove the current player to jail.

                Returns: A log appropriate based on the result of the attempt
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
            pass

        def advanceToUtilityCard(self, player):
            pass
    # Rolling Helpers

        def _handleTile(self):
            pass

        def _drawCard(self):
            pass

        def _takeRent(self):
            pass
    # Jail Helpers

        def _goToJail(self):
            pass

        def _forceJail(self):
            pass
    # Trade Helpers

        def _checkTrade(self):
            pass
