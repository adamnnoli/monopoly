"""
  Contains all of the Game Constants
"""

# Length of the Long Side of a Board TIle
TILE_LONG = 100
# Length of the Short Side of a Board TIle
TILE_SHORT = 50

# The amount of money each player starts with
STARTING_CASH = 1500

# Length of one side of a game piece
PIECE_SIZE = 15

# Length of one side of a house piece
HOUSE_SIZE = 12

GAME_WIDTH = 1050
GAME_HEIGHT = 700

GAME_BOARD_COLOR = "#c0e2ca"

HOUSE_COLOR = "#006b1d"

HOTEL_COLOR = "#ba2800"

WELCOME_MESSAGE = """Welcome to Monopoly!
The object of the game is to become the last player standing by forcing all other players to become bankrupt.
To play the game roll the dice. Your piece will move for you. Depending on where you land you may
be able to buy real estate, pay rent, pay taxes, draw a Chance or Community Chest, Go To Jail, etc.
If you roll doubles, then after taking your turn you will be able to roll again. But be careful,
if you roll three doubles in a row, you will be forced to go to jail.
If you land on, or pass, GO then you will get an extra $200.
If you land on an unowned property then you can buy it at the stated price. If you do not want to 
buy the property than it will go up for auction and any player can bid on it.
If you land on an owned property, than you will have to pay the owner the rent list on its Title Deed Card.
If you land on Income Tax then you will have to pay $200 to the bank.
If you land on Luxury Tax,then you will have to pay $100 to the bank. 
If you land on a Chance or Community Chest Card, you will draw the top card and follow the instructions on it.
If the card is a Get Out of Jail Free Card, then you can keep it until you use it, sell it to another player,
or use it to Get Out of Jail Free
Jail
  You enter jail if you land on Go To Jail, you draw a Go To Jail Card, or you roll doubles 3x in a row.
  While in Jail you can still collect rents, trade with other players, and improve properties.
Monopolies
Building and Selling
Mortgages
Bankruptcy
  If the property is mortgaged, no rent can be collected. When a
  property is mortgaged, its Title Deed card is placed face down in front
  of the owner.
  It is an advantage to hold all the Title Deed cards in a color-group
  (e.g., Boardwalk and Park Place; or Connecticut, Vermont and Oriental
  Avenues) because the owner may then charge double rent for
  unimproved properties in that color-group. This rule applies to
  unmortgaged properties even if another property in that color-group
  is mortgaged.
  It is even more advantageous to have houses or hotels on properties
  because rents are much higher than for unimproved properties.
  The owner may not collect the rent if he/she fails to ask for it before
  the second player following throws the dice.

  “JAIL”… You land in Jail when… (1) your token lands on the space
  marked “Go to Jail”; (2) you draw a card marked “Go to Jail”; or
  (3) you throw doubles three times in succession.
  When you are sent to Jail you cannot collect your $200 salary in that
  move since, regardless of where your token is on the board, you must
  move it directly into Jail. Yours turn ends when you are sent to Jail.
  If you are not “sent” to Jail but in the ordinary course of play land
  on that space, you are “Just Visiting,” you incur no penalty, and you
  move ahead in the usual manner on your next turn.
  You get out of Jail by… (1) throwing doubles on any of your next
  three turns; if you succeed in doing this you immediately move
  forward the number of spaces shown by your doubles throw; even
  though you had thrown doubles, you do not take another turn;
  (2) using the “Get Out of Jail Free” card if you have it; (3) purchasing
  the “Get Out of Jail Free” card from another player and playing it;
  (4) paying a fine of $50 before you roll the dice on either of your next
  two turns.
  If you do not throw doubles by your third turn, you must pay the
  $50 fine. You then get out of Jail and immediately move forward the
  number of spaces shown by your throw.
  Even though you are in Jail, you may buy and sell property, buy
  and sell houses and hotels and collect rents.

  HOUSES… When you own all the properties in a color-group you
  may buy houses from the Bank and erect them on those properties.
  If you buy one house, you may put it on any one of those
  properties. The next house you buy must be erected on one of the
  unimproved properties of this or any other complete color-group you
  may own.
  The price you must pay the Bank for each house is shown on your
  Title Deed card for the property on which you erect the house.
  The owner still collects double rent from an opponent who lands on
  the unimproved properties of his/her complete color-group.
  Following the above rules, you may buy and erect at any time as
  many houses as your judgement and financial standing will allow. But
  you must build evenly, i.e., you cannot erect more than one house on
  any one property of any color-group until you have built one house on
  every property of that group. You may then begin on the second row
  of houses, and so on, up to a limit of four houses to a property. For
  example, you cannot build three houses on one property if you have
  only one house on another property of that group.
  As you build evenly, you must also break down evenly if you sell
  houses back to the Bank (see SELLING PROPERTY).

  HOTELS… When a player has four houses on each property of a
  complete color-group, he/she may buy a hotel from the Bank and
  erect it on any property of the color-group. He/she returns the four
  houses from that property to the Bank and pays the price for the hotel
  as shown on the Title Deed card. Only one hotel may be erected on
  any one property.

  SELLING PROPERTY… Unimproved properties, railroads and
  utilities (but not buildings) may be sold to any player as a private
  transaction for any amount the owner can get; however, no property
  can be sold to another player if buildings are standing on any
  properties of that color-group. Any buildings so located must be sold
  back to the Bank before the owner can sell any property of that color-group.
  Houses and hotels may be sold back to the Bank at any time for
  one-half the price paid for them.
  All houses on one color-group must be sold one by one, evenly, in
  reverse of the manner in which they were erected.
  All hotels on one color-group may be sold at once, or they may be
  sold one house at a time (one hotel equals five houses), evenly, in
  reverse of the manner in which they were erected.

  MORTGAGES… Unimproved properties can be mortgaged through
  the Bank at any time. Before an improved property can be mortgaged,
  all the buildings on all the properties of its color-group must be sold
  back to the Bank at half price. The mortgage value is printed on each
  Title Deed card.
  No rent can be collected on mortgaged properties or utilities, but
  rent can be collected on unmortgaged properties in the same group.
  In order to lift the mortgage, the owner must pay the Bank the
  amount of the mortgage plus 10% interest. When all the properties of a
  color-group are no longer mortgaged, the owner may begin to buy
  back houses at full price.
  The player who mortgages property retains possession of it and no
  other player may secure it by lifting the mortgage from the Bank.
  However, the owner may sell this mortgaged property to another
  player at any agreed price. If you are the new owner, you may lift the
  mortgage at once if you wish by paying off the mortgage plus 10%
  interest to the Bank. If the mortgage is not lifted at once, you must pay
  the Bank 10% interest when you buy the property and if you lift the
  mortgage later you must pay the Bank an additional 10% interest as
  well as the amount of the mortgage.

  BANKRUPTCY… You are declared bankrupt if you owe more than
  you can pay either to another player or to the Bank. If your debt is to
  another player, you must turn over to that player all that you have of
  value and retire from the game. In making this settlement, if you own
  houses or hotels, you must return these to the Bank in exchange for
  money to the extent of one-half the amount paid for them; this cash is
  given to the creditor. If you have mortgaged property you also turn
  this property over to your creditor but the new owner must at once
  pay the Bank the amount of interest on the loan, which is 10% of the
  value of the property. The new owner who does this may then, at
  his/her option, pay the principal or hold the property until some later
  turn, then lift the mortgage. If he/she holds property in this way until
  a later turn, he/she must pay the interest again upon lifting the
  mortgage.
  Should you owe the Bank, instead of another player, more than you
  can pay (because of taxes or penalties) even by selling off buildings
  and mortgaging property, you must turn over all assets to the Bank. In
  this case, the Bank immediately sells by auction all property so taken,
  except buildings. A bankrupt player must immediately retire from the
  game. The last player left in the game wins
"""

titleFont = None
subtitleFont = None
mainTextFont = None
buttonFont = None
