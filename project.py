import random
import sys

class card:
    '''represents a card'''

    def __init__(self, rank, color=None):
        '''Card(rank,color) -> Card
        creates a card with the given rank and color'''
        self.rank = rank
        self.color = color

    def __str__(self):
        '''str(card) -> str'''
        card = ''
        if self.color != None:
            card += str(self.color) + ' '
        card += str(self.rank)
        return(card)

    def match(self, other):
        '''card.match(card) -> boolean
        this function will return True if the cards match in rank or color, False if not'''
        return (self.color == other.color) or (self.rank == other.rank) \
            or self.rank in ['WILD', 'WILD DRAW FOUR']


class Deck:
    '''represents a deck/list of typically 108 Uno cards'''

    def __init__(self):
        '''Deck() -> Deck
        creates a new full Uno deck'''
        self.deck = []
        for color in ['red', 'blue', 'green', 'yellow']:
            self.deck.append(card(0, color))  # one 0 of each color
            for i in range(2):
                for n in range(1, 10):  # two of each of 1-9 of each color
                    self.deck.append(card(n, color))
            for i in range(2):
                # add two action cards for every color
                for action in ['SKIP', 'REVERSE', 'DRAW TWO']:
                    self.deck.append(card(action, color))
        for i in range(4):
            self.deck.append(card('WILD'))
            self.deck.append(card('WILD DRAW FOUR'))
        random.shuffle(self.deck)  # shuffle the deck

    def __str__(self):
        '''str(deck) -> str'''
        return 'An Uno deck with ' + str(len(self.deck)) + ' cards remaining.'

    def empty(self):
        '''Deck.empty() -> boolean
        this function will return True if the deck is empty, and False if it is not'''
        return len(self.deck) == 0

    def remove_card(self):
        '''Deck.remove_card() -> Card
        this function deals a card from the deck and returns it (the dealt card is removed from the deck)'''
        return self.deck.pop()

    def reset_deck(self, pile):
        '''Deck.reset(pile)
        this function resets the deck from the pile'''
        self.deck = pile.reset_pile()  # get cards from the pile
        random.shuffle(self.deck)  # shuffle the deck


class Pile:
    '''represents the discard pile in Uno
    attribute:
      pile: list of UnoCards'''

    def __init__(self, deck):
        '''Pile(deck) -> Pile
        creates a new pile by drawing a card from the deck'''
        card = deck.remove_card()
        self.pile = [card]  # all the cards in the pile

    def __str__(self):
        '''str(Pile) -> str'''
        return 'The pile has ' + str(self.pile[-1]) + ' on top.\n'

    def top_card(self):
        '''Pile.top_card() -> Card
        returns the top card in the pile'''
        return self.pile[-1]

    def add_card(self, card):
        '''Pile.add_card(card)
        adds the card to the top of the pile'''
        self.pile.append(card)

    def reset_pile(self):
        '''Pile.reset_pile() -> list
        removes all but the top card from the pile and
          returns the rest of the cards as a list of Cards'''
        newdeck = self.pile[:-1]
        self.pile = [self.pile[-1]]
        return newdeck


class Player:
    '''represents a player with a name and a hand'''

    def __init__(self, name, deck):
        '''Player(name,deck) -> Player
        creates a new player with a new 7-card hand'''
        self.name = name
        self.hand = [deck.remove_card() for i in range(7)]

    def __str__(self):
        '''str(Player) -> Player'''
        return str(self.name) + ' has ' + str(len(self.hand)) + ' cards.'

    def get_hand(self):
        '''get_hand(self) -> str
        returns a string representation of the hand, one card per line'''
        output = ''
        for card in self.hand:
            output += str(card) + '\n'
        return output

    def has_won(self):
        '''Player.has_won() -> boolean
        returns True if the player's hand is empty (player has won)'''
        return len(self.hand) == 0

    def draw_card(self, deck):
        '''Player.draw_card(deck) -> Card
        draws a card, adds to the player's hand and returns the card drawn'''
        card = deck.remove_card()  # get card from the deck
        self.hand.append(card)   # add this card to the hand
        return card

    def play_card(self, card, pile):
        '''Player.play_card(card,pile)
        plays a card from the player's hand to the pile'''
        self.hand.remove(card)
        pile.add_card(card)

    def take_turn(self, deck, pile):
        '''Player.take_turn(deck,pile)
        takes the player's turn in the game'''
        # print player info
        print(self.name + ", it's your turn.")
        print(pile)
        print("Your hand: ")
        print(self.get_hand())
        # get a list of cards that can be played
        topcard = pile.top_card()
        matches = [card for card in self.hand if card.match(topcard)]
        if len(matches) > 0:  # can play
            for index in range(len(matches)):
                # print the playable cards with their number
                print(str(index + 1) + ": " + str(matches[index]))
            # get player's choice of which card to play
            choice = 0
            while choice < 1 or choice > len(matches):
                choicestr = input("Which do you want to play? ")
                if choicestr.isdigit():
                    choice = int(choicestr)
            # play the chosen card from hand, add it to the pile
            self.play_card(matches[choice - 1], pile)
            # default to if not wild card
            global newColor
            newColor = ''
            # if card is wild
            if matches[choice - 1].rank == 'WILD' or matches[choice - 1].rank == 'WILD DRAW FOUR':
                while newColor not in ['red', 'blue', 'green', 'yellow']:
                    # ask for new color
                    newColor = input('What is the new color? ')
            return matches[choice - 1].rank, newColor
        else:  # can't play
            print("You can't play, so you have to draw.")
            input("Press enter to draw. ")
            # check if deck is empty -- if so, reset it
            if deck.empty():
                deck.reset_deck(pile)
            # draw a new card from the deck
            newcard = self.draw_card(deck)
            print("You drew: " + str(newcard))
            if newcard.match(topcard):  # can be played
                print("Good -- you can play that!")
                self.play_card(newcard, pile)
                # default to if not wild card
                newColor = ''
                # if card is wild
                if newcard.rank == 'WILD' or newcard.rank == 'WILD DRAW FOUR':
                    while newColor not in ['red', 'blue', 'green', 'yellow']:
                        # ask for new color
                        newColor = input('What is the new color? ')
                return newcard.rank, newColor
            else:   # still can't play
                print("Sorry, you still can't play.")
                input("Press enter to continue. ")
                return topcard.rank, None


class Bot:
    '''represents a computer player'''

    def __init__(self, name, deck):
        '''Bot(name,deck) -> Bot
        creates a new computer player with a new 7-card hand'''
        self.name = name
        self.hand = [deck.remove_card() for i in range(7)]

    def __str__(self):
        '''str(UnoBot) -> UnoBot'''
        return str(self.name) + ' has ' + str(len(self.hand)) + ' cards.'

def findnum(strval):
    try:
        x = int(strval)
        return x
    except:
        sys.exit()



def shufflenames(names):
    for namePos in range(len(names)):
        randPos = random.randint(0, (len(names)-1))
        names[namePos], names[randPos] = names[randPos], names[namePos]
    return names

def main():
    '''main(numPlayers)
    plays a game of Uno with a number of Players'''
    # set up full deck and initial discard pile
    global deck
    deck = Deck()
    global pile
    pile = Pile(deck)
    # set up game modifier (aka action cards)
    powers = ['SKIP', 'REVERSE', 'DRAW TWO']
    # bot names for fun :D
    botNames  = ['Apple', 'Orange', 'Banana', 'Coconut', 'Watermelon', 'Orange',
                'Cherry', 'Pear', 'Mango', 'Strawberry', 'Kiwi', 'Cantaloupe'
                'Pineapple', 'Grapefruit', 'Peach', 'Grape', 'Lemon']
    shufflenames(botNames)
    # set up player changer
    playerChange = 1
    global numPlayers
    numPlayers = findnum(input("how many players?" ))
    numBots = findnum(input("how many cpus?" ))
    # set up the players
    global playerList
    playerList = []
    for n in range(numPlayers):
        # get each player's name, then create an UnoPlayer
        name = input('Player #' + str(n + 1) + ', enter your name: ')
        playerList.append(Player(name, deck))
    for n in range(numBots):
        name = botNames[n] + ' Bot'
        playerList.append(Bot(name, deck))
    # randomly assign who goes first
    global currentPlayerNum
    currentPlayerNum = random.randrange(numPlayers)
    # play the game
    while True:
        # print the game status
        print('\n' * 1)
        print('-------')
        for player in playerList:
            print(player)
        print('-------')
        # take a turn]
        move, colorl = playerList[currentPlayerNum].take_turn(deck, pile)
        # check for a winner
        if playerList[currentPlayerNum].has_won():
            print(playerList[currentPlayerNum].name + " wins!")
            print("Thanks for playing!")
            break
        # normalize playerChange
        playerChange = int(abs(playerChange) / playerChange)

        # go to the next player and acknowledge game modifier
        checkmove(move)
        # change the player appropriately
        currentPlayerNum = (currentPlayerNum + playerChange) % numPlayers

def checkmove(move):
    playerChange = 1
            # if the card just played is SKIP
    if move == 'SKIP':
        playerChange *= 2
        # if the card just played is REVERSE
    elif move == 'REVERSE':
        playerChange *= -1
        # if the card just played is DRAW TWO
    elif move == 'DRAW TWO':
        # draw two cards
        for i in range(2):
            global playerList
            global currentPlayerNum
            global numPlayers
            global deck
            global playerList
            playerList[(currentPlayerNum + playerChange) %numPlayers].draw_card(deck)
        # skip that player
        playerChange *= 2
    elif move == 'WILD' or move == 'WILD DRAW FOUR':
        # set new color
        pile.top_card().color = newColor
        # draw four cards
    if move == 'WILD DRAW FOUR':
        for i in range(4):
            playerList[(currentPlayerNum + playerChange) %
                           numPlayers].draw_card(deck)
            # skip that player
            playerChange *= 2
    return True

if __name__ == "__main__":
    main()
