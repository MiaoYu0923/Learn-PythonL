import random
class Card:
    def __init__(self, suit, rank):
        self.rank = rank
        self.suit = suit
    def getStr(self):
        return self.rank + "of" + self.suit

class Deck:
    def __init__(self):
        self.__deck = []
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        for rank in ranks:
            for suit in suits:
                self.__deck.append(Card(rank, suit))
    def shuffle(self):
        random.shuffle(self.__deck)
    def dealCard(self):
        return self.__deck.pop()
    def count(self):
        return len(self.__deck)

def main():
    print("Card Dealer")
    print()

    deck = Deck()
    deck.shuffle()

    print("I have shuffled a deck of", str(deck.count()), "cards" )
    print()

    count = int(input("How many cards would you like? "))
    print()

    print("Here are your cards:")
    cards = []
    for i in range(count):
        card = deck.dealCard()
        print(card.getStr())
        cards.append(card)
    print()

    print("There are", str(deck.count()), "cards left in the deck")
    print()

    print("Good luck")

if __name__ == "__main__":
    main()