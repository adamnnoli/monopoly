import random


class GameOriginal:
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
