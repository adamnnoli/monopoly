class gameConstants:
  numPlayers = 4
  startingCash = 1500

class boardTile:
  pass

class player:
  pass

class communityChestCard:
  def __init__(self, text, action):
    self._text = text 
    self._action = action 
  
  def getText(self):
    self._text 
  
  def getAction(self): 
    self._action 

class chanceCard:
  def __init__(self, text, action):
    self._text = text 
    self._action = action 
  
  def getText(self):
    self._text 
  
  def getAction(self): 
    self._action