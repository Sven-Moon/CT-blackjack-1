from deck import Deck

class BlackjackPlayerBase:
    def __init__(self) -> None:
        self.hand = [] 
            
    def discard(self, deck):
        deck.discards = deck.discards + self.hand
        self.hand = []        
    
    def takeTopCard(self, deck):        
        self.hand.append(deck.deal())