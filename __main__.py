"""
    The primary application script for Monopoly

    This is the module with the application code. Relies on these modules:

        app.py      (the primary game class)
        game.py     (controls game functions)
        objects.py  (classes for each game object)
        consts.py   (the application constants)f
"""

from retry import *

game = Monopoly2()
game.run()
