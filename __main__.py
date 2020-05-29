"""
    The primary application script for Monopoly

    This is the module with the application code. Relys on these modules:

        app.py      (the primary controller class)
        level.py    (the subcontroller for a single game level)
        models.py   (the model classes)
        consts.py   (the application constants)fdv
"""

from app import *

game = Monopoly()
game.run()
