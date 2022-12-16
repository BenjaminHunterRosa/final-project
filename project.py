import random
import DisplayManager

# Properties for cards in UNO
colours      = ["red", "blue", "green", "yellow"]
specialCards = ["S", "R", "+2"]
wildCards    = ["+4", "W"]

class Card:
    def __init__(self, colour, number, special):
        self.colour  = colour
        self.number  = number
        self.special = special

    def displayCard(self):
        ''' This function displays the card (Colour, Number) to the terminal '''
        # If the card is a non-coloured special card (i.e. 'Wildcard')
        if self.special == wildCards[0] or self.special == wildCards[1]:
            print(self.special, end = " ")

        # If the card is a coloured special card (i.e. Skip, Reverse, +2)
        elif self.special == specialCards[0] or self.special == specialCards[1] or self.special == specialCards[2]:
            print(self.colour + self.special, end = " ")

        # If the card is 'normal' (has a colour and a number)
        else:
            print(self.colour + str(self.number), end = " ")

class Player:
    def __init__(self, id, hand, numCards):
        self.id       = id
        self.hand     = hand
        self.numCards = numCards

    def addCard(self, card):
        ''' This function adds a new card to the player's hand '''
        self.hand.append(card)
        self.numCards += 1

    def displayHand(self):
        ''' This function displays the player's hand to the terminal '''
        print("Player " + str(self.id) + "'s hand: ", end = " ")
        for card in self.hand:
            card.displayCard()
        print("")

def initPlayers(players):
    ''' This function initializes a player of the game '''
    for i in range(4):
        hand = []
        players.append(Player(i + 1, hand, 0))

def initDeck(deck):
    ''' This function initializes a deck of 108 UNO cards '''

    # Create one 0 Card for each colour
    for col in colours:
        deck.append(Card(col, 0, None))

    # Create two cards for numbers 1 - 9 for each colour
    for col in colours:
        for i in range(1, 10):
            deck.append(Card(col, i, None))
            deck.append(Card(col, i, None))

    # Create two Skip, Reverse, and +2 cards for each colour
    for col in colours:
        for s in specialCards:
            deck.append(Card(col, None, s))
            deck.append(Card(col, None, s))

    # Create four +4Wildcard and Wildcard cards
    for w in wildCards:
        for i in range(4):
            deck.append(Card(None, None, w))

    # Shuffle the deck
    random.shuffle(deck)

def displayDeck(deck):
    '''This function displays all the cards in the deck [for debugging] '''
    for card in deck:
        card.displayCard()
        print("")

def setMiddle(deck, middle):
    ''' This function will check if the middle at the start of the game is valid
    (i.e. The middle can't be a 'special' card)
    If the middle is invalid, then continue to draw cards from the deck until valid '''
    # If the card is a non-coloured special card (i.e. 'Wildcard')
    if middle.special ==wildCards[0] or middle.special == wildCards[1]:
        # The middle card is put at the back of the deck and a new middle card is drawn
        deck.append(middle)
        middle = deck.pop(0)

        setMiddle(deck, middle)

    # If the card is a coloured special card (i.e. Skip, Reverse, +2)
    elif middle.special == specialCards[0] or middle.special == specialCards[1] or middle.special == specialCards[2]:
        deck.append(middle)
        middle = deck.pop(0)

        setMiddle(deck, middle)

def drawACard(deck, player):
    ''' This function will allow the player to draw a card from the top of the deck '''
    player.addCard(deck.pop(0))

def isSkip(middle):
    ''' This function returns True if the middle card is a Skip card '''
    if middle.special == specialCards[0]:
        return True

def isReverse(middle):
    ''' This function returns True if the middle card is a Reverse card '''
    if middle.special == specialCards[1]:
        return True

def isPlus2(middle):
    ''' This function returns True if the middle card is a +2 card '''
    if middle.special == specialCards[2]:
        return True

def isWildcard4(middle):
    ''' This function returns True if it the middle card is a +4Wildcard '''
    if middle.special == wildCards[0]:
        return True

def playCards(currentPlayer, middle, deck):
   ''' This function will allow the player to play cards from their hand
   while making sure the player does not break any rules of the game'''
   valid = False
   wildcard = False

   """Checking for special cards (reverse and skip cards will be checked outside of this function, in the main()"""
   if middle.special in wildCards:
       middleColour = middle.colour
       middle.colour = None # reset
       wildcard = True

   """Ask user to play a card"""
   while True:
       print("Enter index of card you want to play (first card is 1, second card is 2, etc.):", end=" ")
       playerCard = int(input()) - 1
       # print("you entered: {}".format(playerCard+1))
       if playerCard < 0 or playerCard >= currentPlayer.numCards:
           print("Invalid card. Please try again.")
       else:
           break

   # If card is completely invalid, and player cannot play
   # currentPlayer.hand[playerCard].displayCard()
   # middle.displayCard()

   if currentPlayer.hand[playerCard].colour != middle.colour and currentPlayer.hand[playerCard].number != middle.number and currentPlayer.hand[playerCard].special not in wildCards and currentPlayer.hand[playerCard].special != middle.special:
       print("CAN'T PLAY, draw card.")
       pass
   else:
       if currentPlayer.hand[playerCard].special is None:
           print("CAN'T PLAY, draw card.")
           pass
       print("VALID CARD!! Wildcard = {}".format(wildcard))
       """If card is valid, play card, and remove from player's hand"""
       if wildcard is True:  # if true, we can only play a colour
         wildcard = False
         if currentPlayer.hand[playerCard].colour == middleColour:
             deck.append(middle)
             middle = currentPlayer.hand.pop(playerCard)
             valid = True
             currentPlayer.numCards -= 1
       else:
          if currentPlayer.hand[playerCard].colour == middle.colour or currentPlayer.hand[playerCard].number == middle.number or currentPlayer.hand[playerCard].special == middle.special:
              deck.append(middle)
              middle = currentPlayer.hand.pop(playerCard)

              currentPlayer.numCards -= 1
              valid = True  # a valid card was played
          if currentPlayer.hand[playerCard].special in wildCards:
              deck.append(middle)
              middle = currentPlayer.hand.pop(playerCard)

              print("Choose the colour to change to (1=red, 2=blue, 3=green, 4=yellow): ", end="")
              newColour = int(input())-1
              middle.colour = colours[newColour]
              currentPlayer.numCards -= 1
              valid = True  # a valid card was played

   return valid, middle



def main():
    ''' This function manages the UNO card game loop '''
    # Initialize display manager
    displayManager = DisplayManager.DisplayManager(800,800)
    # Initialize deck of 108 cards and randomly shuffle them into a queue
    deck = []
    initDeck(deck)

    # Initialize the 4 players
    players = []
    initPlayers(players)

    # Set the middle card to start the game by drawing from the top of the deck
    middle = deck.pop(0)
    setMiddle(deck, middle)

    # Deal 7 cards to each player's hand
    for i in range(4):
        for j in range(7):
            drawACard(deck, players[i])

    # The game is over when a player's number of cards reaches 0
    # Continue the game loop until game over
    direction = "clockwise" # Initially, order of play is P1 -> P2 -> P3 -> P4 -> P1 -> ...
    currentPlayer = -1       # P1's turn will start first

    while True:
        # The direction of play determines the order
        if direction == "clockwise":
            # Determine which player's turn it is
            currentPlayer = (currentPlayer + 1) % 4

            # Check the middle card and apply any special card effects
            if isReverse(middle):
                currentPlayer = (currentPlayer - 1) % 4
                direction == "counterClockwise"
                continue

            if isSkip(middle):
                continue

            if isPlus2(middle):
                for i in range(2):
                    drawACard(deck, players[currentPlayer])

            if isWildcard4(middle):
                for i in range(4):
                    drawACard(deck, players[currentPlayer])

            # Display the middle card to the current player
            print("Here is the middle card: ", end = " ")
            middle.displayCard()
            print("")

            # Display the current player's hand to the terminal
            players[currentPlayer].displayHand()
            # Display current scene
            displayManager.drawScene(players[currentPlayer], middle)
            displayManager.updateScene()
            # The current player may play a card/cards from their hand
                # If no card is played, the current player must draw a card from the deck


            # If the current player has no cards remaining, they win!
            if players[currentPlayer].numCards == 0:
                break

        # The game order has been reversed and is COUNTERClockwise
        else:
            # Determine which player's turn it is
            currentPlayer = (currentPlayer - 1) % 4

            # Check the middle card and apply any special card effects
            if isReverse(middle):
                currentPlayer = (currentPlayer - 1) % 4
                direction == "clockwise"
                continue

            if isSkip(middle):
                continue

            if isPlus2(middle):
                for i in range(2):
                    drawACard(deck, players[currentPlayer])

            if isWildcard4(middle):
                for i in range(4):
                    drawACard(deck, players[currentPlayer])

            # Display the middle card to the current player
            print("Here is the middle card: ", end = " ")
            middle.displayCard()
            print("")

            # Display the current player's hand to the terminal
            players[currentPlayer].displayHand()

            # The current player may play a card/cards from their hand
                # If no card is played, the current player must draw a card from the deck

            # If the current player has no cards remaining, they win!
            if players[currentPlayer].numCards == 0:
                break

        # Remove this later
        if currentPlayer == 3:
            break
        displayManager.quit()

main()
