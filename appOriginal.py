from tkinter import *
from game import Game

class MonopolyOriginal:

# Jail

    def _createJailWindow(self):
        self._jailWindow = Toplevel()

        payButton = Button(self._jailWindow, text="Pay $50", command=self._pay)
        payButton.grid()
        rollButton = Button(self._jailWindow, text="Roll For Doubles", command=self._jailRoll)
        rollButton.grid(column=1)
        cardButton = Button(
            self._jailWindow, text="Use Get Out of Jail Free Card", command=self._useCard)
        cardButton.grid(column=2)

    def _jailRoll(self):
        self._handleLog(self._game.jailRoll())

    def _pay(self):
        self._handleLog(self._game.payJail())

    def _useCard(self):
        self._handleLog(self._game.useGetOutOfJailFreeCard())

