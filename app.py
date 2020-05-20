"""
  APP Module for Monopoly

  Contains the classes and methods necessary from creating and playing the game.
"""
from tkinter import *
import consts
from game import Game

long = consts.TILE_LONG
short = consts.TILE_SHORT


class Monopoly:

    def __init__(self):
        self._window = Tk()
        self._board = self.create_board(self._window)
        self._controls = self.create_controls(self._window)

    def run(self):
        self._window.mainloop()

    def create_controls(self, root):
        pass

    # Helper functions make game board

    def create_board(self, root):
        canvas = Canvas(root, bg="white", width=(
            2*long+8*short), height=(2*long+8*short))
        canvas.grid(row=0, column=0)
        self.create_top(canvas)
        self.create_left(canvas)
        self.create_right(canvas)
        self.create_bottom(canvas)

    def create_top(self, cvs):
        cvs.create_rectangle(0, 0, long, long)
        cvs.create_rectangle(long, 0, long + short, long)
        cvs.create_rectangle(long + short, 0, long + 2 * short, long)
        cvs.create_rectangle(long + 2 * short, 0, long + 3 * short, long)
        cvs.create_rectangle(long + 3 * short, 0, long + 4 * short, long)
        cvs.create_rectangle(long + 4 * short, 0, long + 5 * short, long)
        cvs.create_rectangle(long + 5 * short, 0, long + 6 * short, long)
        cvs.create_rectangle(long + 6 * short, 0, long + 7 * short, long)
        cvs.create_rectangle(long + 7 * short, 0, long + 8 * short, long)
        cvs.create_rectangle(long + 8 * short, 0, 2 * long + 8 * short, long)

    def create_left(self, cvs):
        cvs.create_rectangle(0, long, long, long + short)
        cvs.create_rectangle(0, long + short, long, long + 2 * short)
        cvs.create_rectangle(0, long + 2 * short, long, long + 3 * short)
        cvs.create_rectangle(0, long + 3 * short, long, long + 4 * short)
        cvs.create_rectangle(0, long + 4 * short, long, long + 6 * short)
        cvs.create_rectangle(0, long + 5 * short, long, long + 7 * short)
        cvs.create_rectangle(0, long + 6 * short, long, long + 8 * short)

    def create_right(self, cvs):
        cvs.create_rectangle(long + 8 * short, long,
                             2 * long + 8 * short, long + short)

        cvs.create_rectangle(long + 8 * short, long +
                             short, 2 * long + 8 * short, long + 2 * short)

        cvs.create_rectangle(long + 8 * short, long + 2 *
                             short, 2 * long + 8 * short, long + 3 * short)

        cvs.create_rectangle(long + 8 * short, long + 3 *
                             short, 2 * long + 8 * short, long + 4 * short)

        cvs.create_rectangle(long + 8 * short, long + 4 *
                             short, 2 * long + 8 * short, long + 6 * short)

        cvs.create_rectangle(long + 8 * short, long + 5 *
                             short, 2 * long + 8 * short, long + 7 * short)

        cvs.create_rectangle(long + 8 * short, long + 6 *
                             short, 2 * long + 8 * short, long + 8 * short)

    def create_bottom(self, cvs):
        cvs.create_rectangle(0, long + 8 * short, long, 2 * long + 8 * short)

        cvs.create_rectangle(long, long + 8 * short,
                             long + short, 2 * long + 8 * short)

        cvs.create_rectangle(long + short, long + 8 * short, long + 2 *
                             short, 2 * long + 8 * short)

        cvs.create_rectangle(long + 2 * short, long + 8 *
                             short, long + 3 * short, 2 * long + 8 * short)

        cvs.create_rectangle(long + 3 * short, long + 8 *
                             short, long + 4 * short, 2 * long + 8 * short)

        cvs.create_rectangle(long + 4 * short, long + 8 *
                             short, long + 5 * short, 2 * long + 8 * short)

        cvs.create_rectangle(long + 5 * short, long + 8 *
                             short, long + 6 * short, 2 * long + 8 * short)

        cvs.create_rectangle(long + 6 * short, long + 8 *
                             short, long + 8 * short, 2 * long + 8 * short)

        cvs.create_rectangle(long + 7 * short, long + 8 *
                             short, long + 8 * short, 2 * long + 8 * short)
        cvs.create_rectangle(long + 8 * short, long + 8 *
                             short, 2 * long + 8 * short, 2 * long + 8 * short)
