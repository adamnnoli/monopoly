"""
  Contains all of the Game Constants
"""
# The amount of money each player starts with
STARTING_CASH = 1500

# Width of the Game Window
GAME_WIDTH = 1050

# Height of the Game Window
GAME_HEIGHT = 700

# Length of the Long Side of a Board TIle
TILE_LONG = 100

# Length of the Short Side of a Board TIle
TILE_SHORT = 50

# Length of one side of a house piece
HOUSE_SIZE = 12

# Color of the Game Board
GAME_BOARD_COLOR = "#c0e2ca"

# Color of a house (Green)
HOUSE_COLOR = "#006b1d"

# Color of a hotel (Dark Red)
HOTEL_COLOR = "#ba2800"

# Color of a General Button (Light Blue)

# Color of the Quit Button (Red)

# Font of Title
TITLE_FONT = ("Comic Sans MS", 16, 'bold')
# Font of a Subtitle
# Font of General Text
GENERAL_TEXT_FONT = ("Comic Sans MS", 10)
# Font of a Button Text
# Font of a Main Label
# Font of a Log

# Message Displayed in the Welcome Window
WELCOME_MESSAGE = (
    "Welcome to Monopoly!\n"
    "The object of the game is to become the last player standing by forcing all other players to become bankrupt.\n"
    "To play the game roll the dice. Your piece will move for you. Depending on where you land you may\n"
    "be able to buy real estate, pay rent, pay taxes, draw a Chance or Community Chest, Go To Jail, etc.\n"
    "If you roll doubles, then after taking your turn you will be able to roll again. But be careful,\n"
    "if you roll three doubles in a row, you will be forced to go to jail.\n"
    "If you land on, or pass, GO then you will get an extra $200.\n"
    "If you land on an unowned property then you can buy it at the stated price. If you do not want to\n"
    "buy the property than it will go up for auction and any player can bid on it.\n"
    "If you land on an owned property, than you will have to pay the owner the rent list on its Title Deed Card.\n"
    "If you land on Income Tax then you will have to pay $200 to the bank.\n"
    "If you land on Luxury Tax,then you will have to pay $100 to the bank.\n"
    "If you land on a Chance or Community Chest Card, you will draw the top card and follow the instructions on it.\n"
    "If the card is a Get Out of Jail Free Card, then you can keep it until you use it, sell it to another player,\n"
    "or use it to Get Out of Jail Free\n"
    "Jail\n"
    "You enter jail if you land on Go To Jail, you draw a Go To Jail Card, or you roll doubles 3x in a row.\n"
    "While in Jail you can still collect rents, trade with other players, and improve properties.\n"
    "Monopolies\n"
    "Building and Selling\n"
    "Mortgages\n"
    "Bankruptcy\n\n"
    "If the property is mortgaged, no rent can be collected. When a\n"
    "property is mortgaged, its Title Deed card is placed face down in front\n"
    "of the owner.\n"
    "It is an advantage to hold all the Title Deed cards in a color-group\n"
    "(e.g., Boardwalk and Park Place; or Connecticut, Vermont and Oriental\n"
    "Avenues) because the owner may then charge double rent for\n"
    "unimproved properties in that color-group. This rule applies to\n"
    "unmortgaged properties even if another property in that color-group\n"
    "is mortgaged.\n"
    "It is even more advantageous to have houses or hotels on properties\n"
    "because rents are much higher than for unimproved properties.\n"
    "The owner may not collect the rent if he/she fails to ask for it before\n"
    "the second player following throws the dice.\n"

    "JAIL”… You land in Jail when… (1) your token lands on the space\n"
    "marked “Go to Jail”; (2) you draw a card marked “Go to Jail”; or\n"
    "(3) you throw doubles three times in succession.\n"
    "When you are sent to Jail you cannot collect your $200 salary in that\n"
    "move since, regardless of where your token is on the board, you must\n"
    "move it directly into Jail. Yours turn ends when you are sent to Jail.\n"
    "If you are not “sent” to Jail but in the ordinary course of play land\n"
    "on that space, you are “Just Visiting,” you incur no penalty, and you\n"
    "move ahead in the usual manner on your next turn.\n"
    "You get out of Jail by… (1) throwing doubles on any of your next\n"
    "three turns; if you succeed in doing this you immediately move\n"
    "forward the number of spaces shown by your doubles throw; even\n"
    "though you had thrown doubles, you do not take another turn;\n"
    "(2) using the “Get Out of Jail Free” card if you have it; (3) purchasing\n"
    "the “Get Out of Jail Free” card from another player and playing it;\n"
    "(4) paying a fine of $50 before you roll the dice on either of your next\n"
    "two turns.\n"
    "If you do not throw doubles by your third turn, you must pay the\n"
    "$50 fine. You then get out of Jail and immediately move forward the\n"
    "number of spaces shown by your throw.\n"
    "Even though you are in Jail, you may buy and sell property, buy\n"
    "and sell houses and hotels and collect rents.\n"

    "HOUSES… When you own all the properties in a color-group you\n"
    "may buy houses from the Bank and erect them on those properties.\n"
    "If you buy one house, you may put it on any one of those\n"
    "properties. The next house you buy must be erected on one of the\n"
    "unimproved properties of this or any other complete color-group you\n"
    "may own.\n"
    "The price you must pay the Bank for each house is shown on your\n"
    "Title Deed card for the property on which you erect the house.\n"
    "The owner still collects double rent from an opponent who lands on\n"
    "the unimproved properties of his/her complete color-group.\n"
    "Following the above rules, you may buy and erect at any time as\n"
    "many houses as your judgement and financial standing will allow. But\n"
    "you must build evenly, i.e., you cannot erect more than one house on\n"
    "any one property of any color-group until you have built one house on\n"
    "every property of that group. You may then begin on the second row\n"
    "of houses, and so on, up to a limit of four houses to a property. For\n"
    "example, you cannot build three houses on one property if you have\n"
    "only one house on another property of that group.\n"
    "As you build evenly, you must also break down evenly if you sell\n"
    "houses back to the Bank (see SELLING PROPERTY).\n"

    "HOTELS… When a player has four houses on each property of a\n"
    "complete color-group, he/she may buy a hotel from the Bank and\n"
    "erect it on any property of the color-group. He/she returns the four\n"
    "houses from that property to the Bank and pays the price for the hotel\n"
    "as shown on the Title Deed card. Only one hotel may be erected on\n"
    "any one property.\n"

    "SELLING PROPERTY… Unimproved properties, railroads and\n"
    "utilities (but not buildings) may be sold to any player as a private\n"
    "transaction for any amount the owner can get; however, no property\n"
    "can be sold to another player if buildings are standing on any\n"
    "properties of that color-group. Any buildings so located must be sold\n"
    "back to the Bank before the owner can sell any property of that color-group.\n"
    "Houses and hotels may be sold back to the Bank at any time for\n"
    "one-half the price paid for them.\n"
    "All houses on one color-group must be sold one by one, evenly, in\n"
    "reverse of the manner in which they were erected.\n"
    "All hotels on one color-group may be sold at once, or they may be\n"
    "sold one house at a time (one hotel equals five houses), evenly, in\n"
    "reverse of the manner in which they were erected.\n"

    "MORTGAGES… Unimproved properties can be mortgaged through\n"
    "the Bank at any time. Before an improved property can be mortgaged,\n"
    "all the buildings on all the properties of its color-group must be sold\n"
    "back to the Bank at half price. The mortgage value is printed on each\n"
    "Title Deed card.\n"
    "No rent can be collected on mortgaged properties or utilities, but\n"
    "rent can be collected on unmortgaged properties in the same group.\n"
    "In order to lift the mortgage, the owner must pay the Bank the\n"
    "amount of the mortgage plus 10% interest. When all the properties of a\n"
    "color-group are no longer mortgaged, the owner may begin to buy\n"
    "back houses at full price.\n"
    "The player who mortgages property retains possession of it and no\n"
    "other player may secure it by lifting the mortgage from the Bank.\n"
    "However, the owner may sell this mortgaged property to another\n"
    "player at any agreed price. If you are the new owner, you may lift the\n"
    "mortgage at once if you wish by paying off the mortgage plus 10%\n"
    "interest to the Bank. If the mortgage is not lifted at once, you must pay\n"
    "the Bank 10% interest when you buy the property and if you lift the\n"
    "mortgage later you must pay the Bank an additional 10% interest as\n"
    "well as the amount of the mortgage.\n"

    "BANKRUPTCY… You are declared bankrupt if you owe more than\n"
    "you can pay either to another player or to the Bank. If your debt is to\n"
    "another player, you must turn over to that player all that you have of\n"
    "value and retire from the game. In making this settlement, if you own\n"
    "houses or hotels, you must return these to the Bank in exchange for\n"
    "money to the extent of one-half the amount paid for them; this cash is\n"
    "given to the creditor. If you have mortgaged property you also turn\n"
    "this property over to your creditor but the new owner must at once\n"
    "pay the Bank the amount of interest on the loan, which is 10% of the\n"
    "value of the property. The new owner who does this may then, at\n"
    "his/her option, pay the principal or hold the property until some later\n"
    "turn, then lift the mortgage. If he/she holds property in this way until\n"
    "a later turn, he/she must pay the interest again upon lifting the\n"
    "mortgage.\n"
    "Should you owe the Bank, instead of another player, more than you\n"
    "can pay (because of taxes or penalties) even by selling off buildings\n"
    "and mortgaging property, you must turn over all assets to the Bank. In\n"
    "this case, the Bank immediately sells by auction all property so taken,\n"
    "except buildings. A bankrupt player must immediately retire from the\n"
    "game. The last player left in the game wins\n"
)
# Message Displayed in the Help Window
HELP_MESSAGE = (

)
