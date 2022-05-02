from card import Card
from random import shuffle, randint
class Deck:
    suits = ('Hearts', 'Clubs', 'Diamonds', 'Spades')
    card_values = (2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace')
    def __init__(self,deck_count=1) -> None:     
        self.cards = []
        self.discards = []
        self.shuffleFlag = True
        for count in range(deck_count):
            for suit in self.suits:
                for value in self.card_values:
                    self.cards.append(Card(value,suit))
        
    
    def shuffle(self):
        self.cards = self.cards + self.discards
        shuffle(self.cards)
        self.shuffleFlag = False
        
    def insertBlank(self):
        insertPoint = randint(len(self.cards), len(self.cards)*1.5)
        self.cards.insert(len(self.cards)-insertPoint, Card('BLANK', ' '))       
    
    def deal(self):
        card = self.cards.pop(0)
        if card.name_value == "BLANK":
            self.shuffleFlag = True
            card = self.cards.pop(0)
        return card