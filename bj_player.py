from bj_player_base import BlackjackPlayerBase 
class BlackjackPlayer(BlackjackPlayerBase):
    def __init__(self, user):
        super().__init__()
        self.money = user.money
        self.name = user.name
        self.split_hand = [] 
        self.bet = 0
        self.split_bet = 0
    
    
    def wager(self, bet):
        self.money -= bet
        return bet
    
    def double_down(self):
        self.money -= self.bet
        self.bet *=2
    
    def split(self):
        pass    
    
    def settle(self, winnings):
        self.money += winnings