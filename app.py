"""
  App Module for Monopoly

  Contains the classes and methods necessary from creating and playing the game.
"""
from tkinter import *
import consts
from game import Game

long = consts.TILE_LONG
short = consts.TILE_SHORT
cLength = 2*long+9*short


class Monopoly:

    def __init__(self):
        self._window = Tk()
        self._welcome = self.showWelcome(self._window)
        self._board = self.createBoard(self._window)
        self._controls = self.createControls(self._window)

    def run(self):
        self._window.mainloop()

    def showWelcome(self, root):
        pass

    def createControls(self, root):
        frame = Frame(root)
        frame.grid(row=0, column=1)

        rollDice = Button(frame, text="Roll Dice", padx=5)
        rollDice.grid(row=0, column=0)

        trade = Button(frame, text="Trade", padx=5)
        trade.grid(row=0, column=1)

    # Helper functions make game board

    def createBoard(self, root):
        canvas = Canvas(root, width=cLength, height=cLength)
        canvas.create_rectangle(0, 0, cLength, cLength, fill="#c0e2ca")
        canvas.grid(row=0, column=0)
        self.createTop(canvas)
        self.createLeft(canvas)
        self.createRight(canvas)
        self.createBottom(canvas)

    def createTop(self, cvs):
        cvs.create_rectangle(0, 0, long, long)
        cvs.create_rectangle(long, 0, long + short, long, fill="#d63e3e")
        cvs.create_rectangle(long + short, 0, long + 2 * short, long)
        cvs.create_rectangle(long + 2 * short, 0, long +
                             3 * short, long, fill="#d63e3e")
        cvs.create_rectangle(long + 3 * short, 0, long +
                             4 * short, long, fill="#d63e3e")
        cvs.create_rectangle(long + 4 * short, 0, long + 5 * short, long)
        cvs.create_rectangle(long + 5 * short, 0, long +
                             6 * short, long, fill="#e0fc08")
        cvs.create_rectangle(long + 6 * short, 0, long +
                             7 * short, long, fill="#e0fc08")
        cvs.create_rectangle(long + 7 * short, 0, long + 8 * short, long)
        cvs.create_rectangle(long + 8 * short, 0, long +
                             9 * short, long, fill="#e0fc08")
        cvs.create_rectangle(long + 9 * short, 0, 2 * long + 9 * short, long)

    def createLeft(self, cvs):
        cvs.create_rectangle(0, long, long, long + short, fill="#edbb32")
        cvs.create_rectangle(0, long + short, long,
                             long + 2 * short, fill="#edbb32")
        cvs.create_rectangle(0, long + 2 * short, long, long + 3 * short)
        cvs.create_rectangle(0, long + 3 * short, long,
                             long + 4 * short, fill="#edbb32")
        cvs.create_rectangle(0, long + 4 * short, long, long + 5 * short)
        cvs.create_rectangle(0, long + 5 * short, long,
                             long + 6 * short, fill="#e64cdb")
        cvs.create_rectangle(0, long + 6 * short, long,
                             long + 7 * short, fill="#e64cdb")
        cvs.create_rectangle(0, long + 7 * short, long, long + 8 * short)
        cvs.create_rectangle(0, long + 8 * short, long,
                             long + 9 * short, fill="#e64cdb")

    def createRight(self, cvs):
        cvs.create_rectangle(long + 9 * short, long, 2 *
                             long + 9 * short, long + short, fill="#34c926")
        cvs.create_rectangle(long + 9 * short, long +
                             short, 2 * long + 9 * short, long + 2 * short, fill="#34c926")
        cvs.create_rectangle(long + 9 * short, long + 2 *
                             short, 2 * long + 9 * short, long + 3 * short)
        cvs.create_rectangle(long + 9 * short, long + 3 *
                             short, 2 * long + 9 * short, long + 4 * short, fill="#34c926")
        cvs.create_rectangle(long + 9 * short, long + 4 *
                             short, 2 * long + 9 * short, long + 5 * short)
        cvs.create_rectangle(long + 9 * short, long + 5 *
                             short, 2 * long + 9 * short, long + 6 * short)
        cvs.create_rectangle(long + 9 * short, long + 6 *
                             short, 2 * long + 9 * short, long + 7 * short, fill="#245ac7")
        cvs.create_rectangle(long + 9 * short, long + 7 *
                             short, 2 * long + 9 * short, long + 8 * short)
        cvs.create_rectangle(long + 9 * short, long + 8 *
                             short, 2 * long + 9 * short, long + 9 * short, fill="#245ac7")

    def createBottom(self, cvs):
        cvs.create_rectangle(0, long + 9 * short, long, 2 * long + 9 * short)
        cvs.create_rectangle(long, long + 9 * short,
                             long + short, 2 * long + 9 * short, fill="#4ad6d9")
        cvs.create_rectangle(long + short, long + 9 * short, long + 2 *
                             short, 2 * long + 9 * short, fill="#4ad6d9")
        cvs.create_rectangle(long + 2 * short, long + 9 *
                             short, long + 3 * short, 2 * long + 9 * short)
        cvs.create_rectangle(long + 3 * short, long + 9 *
                             short, long + 4 * short, 2 * long + 9 * short, fill="#4ad6d9")
        cvs.create_rectangle(long + 4 * short, long + 9 *
                             short, long + 5 * short, 2 * long + 9 * short)
        cvs.create_rectangle(long + 5 * short, long + 9 *
                             short, long + 6 * short, 2 * long + 9 * short)
        cvs.create_rectangle(long + 6 * short, long + 9 *
                             short, long + 7 * short, 2 * long + 9 * short, fill="#574400")
        cvs.create_rectangle(long + 7 * short, long + 9 *
                             short, long + 8 * short, 2 * long + 9 * short)
        cvs.create_rectangle(long + 8 * short, long + 9 *
                             short, long + 9 * short, 2 * long + 9 * short, fill="#574400")
        cvs.create_rectangle(long + 9 * short, long + 9 *
                             short, 2 * long + 9 * short, 2 * long + 9 * short)
