class Game2:
    # INITIALIZATION -----------------------------------------------------------------------------------
    def __init__(self):
        pass

    def createBoard(self):
        pass

    def createCards(self):
        pass

    def createPlayers(self):
        pass
# GETTERS AND SETTERS ------------------------------------------------------------------------------

    def getBoard(self):
        pass

    def getTile(self):
        pass

    def getTileId(self):
        pass

    def getCurrentPlayer(self):
        pass

    def getPlayers(self):
        pass

    def getBuildable(self):
        pass

    def getSellable(self):
        pass

    def getMortgageable(self):
        pass

    def getUnmortgageable(self):
        pass

# GAME FUNCTIONALITY -------------------------------------------------------------------------------
    # Rolling
        def roll(self):
            pass
    # Building

        def build(self):
            pass

        def sell(self):
            pass
    # Trading

        def trade(self):
            pass
    # Mortgaging

        def mortgage(self):
            pass

        def unmortgage(self):
            pass
    # Quitting

        def quit(self):
            pass
    # Jail

        def payJail(self):
            pass

        def rollJail(self):
            pass

        def cardJail(self):
            pass
    # End Turn

        def endTurn(self):
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
