
import random


class GameOriginal:
    """
        A Class to Contain the main Game objects

        Contains all of the methods need to run the game

        INSTANCE ATTRIBUTES:
        _board: the game board object [Board]
        _chanceCards: the list of all Chance Cards in the game [Card list]
        _communityChestCards: the list of all Community Chest Cards in the game [Card list]
        _players: a list of the players in the game [Player list]
        _currPlayer: the player whose turn it currently is [Player]

        _hasRolled: true if the current player has already rolled[bool]
        _currChance: the index of the top chance card[int]
        _currCommunityChest: the index of the top Community Chest Card[int]
        _possMonopolies: dictionary of the color and properties in each monopoly[string:int set dict]
    """
# Game Functionality-------------------------------------------------------------------------

    def _updateMonopoly(self):
        """
            Updates the monopolies on the board if there are any.
        """
        player = self._currPlayer.toDict()
        for color, props in self._possMonopolies.items():
            if props <= player["propertyLocations"]:
                self._board.setMonopoly(player["name"], color)

    def getMonopolies(self, player):
        """
            Returns a list of all of colors that player has monopolized.

            Parameter: player, the player requested
            Requires: Must be of type Player
        """
        monopolies = []
        for color, owner in self._board.getMonopolies().items():
            if owner == player:
                monopolies.append(color)
        return monopolies

# Jail

    def jailRoll(self):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        if dice1 == dice2:
            self._currPlayer.leaveJail()
            return self._move(dice1+dice2)
        return "You are still in jail"

    def payJail(self):
        if self._currPlayer.getCash() < 50:
            name = self._currPlayer.toDict()["name"]
            return f"{name} does not have $50"
        else:
            self._currPlayer.takeCash(50)
            self._currPlayer.leaveJail()
            return "Paid to Leave Jail"

    def useGetOutOfJailFreeCard(self):
        if self._currPlayer.getNumJailCards() < 1:
            name = self._currPlayer.toDict()["name"]
            return f"{name} does not have any Get Out Of Jail Free Cards"
        else:
            self._currPlayer.takeGetOutOfJail()
            self.leaveJail()
            return "Used Card to Leave Jail"
