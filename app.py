"""
  APP Module for Monopoly

  Contains the classes and methods necessary from creating and playing the game.
"""
import tkinter as tk
from objects import GameConstants
from game import Game


class Monoply:
    def __init__(self):
        pass

    def create_board(self, root):
        pass

    def create_buttons(self, root):
        pass

    def create_gui(self):
        root = tk.Tk()
        self.create_board(root)
        self.create_buttons(root)

    def run(self):
        gui = create_gui
        gui.mainloop()
