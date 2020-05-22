"""
  App Module for Monopoly

  Contains the classes and methods necessary from creating and playing the game.
"""
from tkinter import *
import consts
from game import Game

long = consts.TILE_LONG
short = consts.TILE_SHORT
longPlus = [long + i * short for i in range(1, 10)]
cLength = 2*long+9*short


class Monopoly:

    def __init__(self):
        self._window = Tk()
        self._welcome = self.showWelcome(self._window)
        # self._board = self.createBoard(self._window)
        # self._controls = self.createControls(self._window)

    def run(self):
        self._window.mainloop()

    def showWelcome(self, root):
        frame = Frame(root)
        frame.grid(row=0, column=0)

        text = Label(frame, text="How Many People Will Be Playing: ", padx=5)
        text.grid(row=0, column=0)

        numPlayers = IntVar()
        askPlayers = OptionMenu(frame, numPlayers, 1, 2, 3, 4)
        askPlayers.grid(row=0, column=1)
        getPlayers = Button(frame, text="Select",
                            command=lambda: self.showPlayers(root, frame, numPlayers))
        getPlayers.grid(row=0, column=2)
        startButton = Button(frame, text="Play!")
        startButton.grid(row=3, column=0, columnspan=numPlayers.get()+1)

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
        cvs.create_rectangle(long, 0, longPlus[0], long, fill="#d63e3e")
        cvs.create_rectangle(longPlus[0], 0, longPlus[1], long)
        cvs.create_rectangle(longPlus[1], 0, longPlus[2], long, fill="#d63e3e")
        cvs.create_rectangle(longPlus[2], 0, longPlus[3], long, fill="#d63e3e")
        cvs.create_rectangle(longPlus[3], 0, longPlus[4], long)
        cvs.create_rectangle(longPlus[4], 0, longPlus[5], long, fill="#e0fc08")
        cvs.create_rectangle(longPlus[5], 0, longPlus[6], long, fill="#e0fc08")
        cvs.create_rectangle(longPlus[6], 0, longPlus[7], long)
        cvs.create_rectangle(longPlus[7], 0, longPlus[8], long, fill="#e0fc08")
        cvs.create_rectangle(longPlus[8], 0, cLength, long)

    def createLeft(self, cvs):
        cvs.create_rectangle(0, long, long, longPlus[0], fill="#edbb32")
        cvs.create_rectangle(0, longPlus[0], long,  longPlus[1], fill="#edbb32")
        cvs.create_rectangle(0, longPlus[1], long, longPlus[2])
        cvs.create_rectangle(0, longPlus[2], long,  longPlus[3], fill="#edbb32")
        cvs.create_rectangle(0, longPlus[3], long, longPlus[4])
        cvs.create_rectangle(0, longPlus[4], long, longPlus[5], fill="#e64cdb")
        cvs.create_rectangle(0, longPlus[5], long, longPlus[6], fill="#e64cdb")
        cvs.create_rectangle(0, longPlus[6], long, longPlus[7])
        cvs.create_rectangle(0, longPlus[7], long, longPlus[8], fill="#e64cdb")

    def createRight(self, cvs):
        cvs.create_rectangle(longPlus[8], long, cLength, longPlus[0], fill="#34c926")
        cvs.create_rectangle(longPlus[8], longPlus[0], cLength, longPlus[1], fill="#34c926")
        cvs.create_rectangle(longPlus[8], longPlus[1], cLength, longPlus[2])
        cvs.create_rectangle(longPlus[8], longPlus[2], cLength, longPlus[3], fill="#34c926")
        cvs.create_rectangle(longPlus[8], longPlus[3], cLength, longPlus[4])
        cvs.create_rectangle(longPlus[8], longPlus[4], cLength, longPlus[5])
        cvs.create_rectangle(longPlus[8], longPlus[5], cLength, longPlus[6], fill="#245ac7")
        cvs.create_rectangle(longPlus[8], longPlus[6], cLength, longPlus[7])
        cvs.create_rectangle(longPlus[8], longPlus[7], cLength, longPlus[8], fill="#245ac7")

    def createBottom(self, cvs):
        cvs.create_rectangle(0, longPlus[8], long, cLength)
        cvs.create_rectangle(long, longPlus[8], longPlus[0], cLength, fill="#4ad6d9")
        cvs.create_rectangle(longPlus[0], longPlus[8], longPlus[1], cLength, fill="#4ad6d9")
        cvs.create_rectangle(longPlus[1], longPlus[8], longPlus[2], cLength)
        cvs.create_rectangle(longPlus[2], longPlus[8], longPlus[3], cLength, fill="#4ad6d9")
        cvs.create_rectangle(longPlus[3], longPlus[8], longPlus[4], cLength)
        cvs.create_rectangle(longPlus[4], longPlus[8], longPlus[5], cLength)
        cvs.create_rectangle(longPlus[5], longPlus[8], longPlus[6], cLength, fill="#574400")
        cvs.create_rectangle(longPlus[6], longPlus[8], longPlus[7], cLength)
        cvs.create_rectangle(longPlus[7], longPlus[8], longPlus[8], cLength, fill="#574400")
        cvs.create_rectangle(longPlus[8], longPlus[8], cLength, cLength)

    def showPlayers(self, root, frame, numPlayers):
        for i in range(1, numPlayers.get() + 1):
            texti = Label(frame, text=f"Player {i}:", padx=5)
            namei = Entry(root)
            playerIColor = StringVar()
            colori = OptionMenu(frame, playerIColor, "red", "blue", "green", "yellow")

            texti.grid(row=1, column=i)
            namei.grid(row=1, column=i+1)
            colori.grid(row=2, column=i, columnspan=2)
