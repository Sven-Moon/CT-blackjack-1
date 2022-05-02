from bj_dealer import BlackjackDealer as Dealer
from bj_player import BlackjackPlayer as Player
from deck import Deck
from user import User
import msvcrt as m
import os
from time import sleep

clear = lambda: os.system('cls')


class Blackjack:
    """ Blackjack accepts a user with money. Blackjack does not return a value, only modifies the money attribute of the User. A User with $0 is unable to play."""
    def __init__(self, user) -> None:
        self.dealer = Dealer()
        self.player = Player(user)
        self.deck = Deck(6)
        
        self.runGame()
        
    def runGame(self):
        # display player name & money
        print(f"Welcome {self.player.name}!")
        # ask (while True)
        while True:
            clear()
            
            print(f"Your cash: ${self.player.money}")
            ans = input(f"\nShall I deal you in or are you a quitter? \n\n[D]eal me in! [Q]uittin' time: ").lower()
            #  Quit: write to user file, break
            if ans in ['q', "quit"]:
                print("\nNice seein' ya, partner!")
                sleep(2)
                break
            elif ans == 'd':
            # Play: runRound()   
                self.runRound() 
            else:
                print(f"You said \"{ans}\"... I don't get it.")     
                sleep(2)       
        
    def runRound(self):
        # If shuffle, Dealer shuffles deck
        if self.deck.shuffleFlag:
            self.deck.shuffle()
            # insert clear card between 60 - 75 from end of deck
            self.deck.insertBlank()
        self.betting()    
        
        self.initialDeal()
        
        if not self.evalForBlackjack():
            return
        
        if not self.playerDraw():
            return
        
        self.dealerDraw() 
        
        self.resolveRound()       

    # runRound methods    
    def betting(self):
        while True:
            clear()
            try:
                bet = int(input(f"\nWhat's your bet there, partner? (you have ${self.player.money}) \n\nYour bet: $"))
                if bet > self.player.money:
                    print(f"I won't take your ugly daughter if you lose. You only have ${self.player.money}, so you can't bet ${bet}. Try again")
                elif bet == 0:
                    print("Ya can't just watch. Put some money down or scram!")
                elif bet < 0:
                    print(f"You can't bet negative amounts. What does that even mean here? Bet more than $0, ya igit")
                else:
                    self.player.bet = self.player.wager(bet)
                    break
            except:
                print("\nThat's not a denomination I'm familiar with. Try again.")
            sleep(2)
    
    def initialDeal(self):
        self.player.takeTopCard(self.deck)
        self.dealer.takeTopCard(self.deck)
        self.player.takeTopCard(self.deck)
        self.dealer.takeTopCard(self.deck)
        self.displayHands()  
        sleep(1)
    
    def evalForBlackjack(self):
        # if Player cards are 21, 
        if self.cardTotal(self.player.hand) == 21:  
            # if Dealer cards != 21:          
            if self.cardTotal(self.dealer.hand) != 21:
                 # round ends and Player gains bet + 1.5x bet
                print('Natural Blackjack!')
                print(f"Here, take your winnings: ${self.player.bet*2.5}")
                self.player.settle(int(self.player.bet*2.5))
                self.cleanup()
                self.wait()
                return False
            else: # else Player receives bet back                
                print('Draw')
                self.player.settle(self.player.bet)            
                self.cleanup() 
                return False # round ends
        return True
        
    def playerDraw(self):
        while True:
            choice = self.displayOptions()
            # player chooses to stand or hit
                # Hit: Player is dealt a card
            if choice == 'h':
                self.player.takeTopCard(self.deck)
                self.displayHands()
                    # if Player card total is > 21
                if self.cardTotal(self.player.hand) > 21:
                    print(f"\n{self.cardTotal(self.player.hand)} ... You busted.")
                    self.cleanup()
                    self.wait()
                    return False
                    # hand is bust - end round
                # Stand: Player turn (for hand) ends                    
            elif choice == 'd':
                self.player.double_down()
                self.player.takeTopCard(self.deck)
                self.displayHands()
                sleep(2)
                break
            elif choice == 's':
                break
            elif choice == 'p':
                pass
                    # Yes Split: 
                        # Player now has two hands, each played separately
                        # hand 2 is played after hand 1 
                        # 21 receives 1x bet rather than 1.5x 
        return True
    
    def cardTotal(self, hand):
        """
        Input: array of card names
        Output: hand total
        Ace counts as 1 if total would be over 21 otherwise
        """
        total = 0
        aces = 0
        for card in hand:
            if isinstance(card.name_value, int):
                total += card.name_value
            elif card.name_value == 'Ace':
                total += 11
                aces +=1
            else:
                total += 10
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total
    
    def displayHands(self, show=False):
        clear()
        playerCards = " ".join([card.name for card in self.player.hand])
        if not show:
            dealerCards = " ".join([card.name if i == 0 else "?" for i, card in enumerate(self.dealer.hand)])
        else: 
            dealerCards = " ".join([card.name for card in self.dealer.hand])
        
        print(f"At Stake: ${self.player.bet} \tRemaining cash: ${self.player.money}")
        # Player shows both cards, dealer shows 1
        print("")
        print("Dealer".center(10," ") + f"{self.player.name}".center(20," "))
        print(f"{dealerCards}".center(10," "), f"{playerCards}".center(20," "))
        
    def displayOptions(self):
        # if Player shows pairs (2 Jacks, 2 8s, etc.),
            # Player has option to split
        # if Player shows 9 - 11, Player may double down
            # double down: bet is doubled, receives 1 card face down, turn ends
        split = self.player.hand[0].name_value == self.player.hand[1].name_value 
        double = self.cardTotal(self.player.hand) in range(9,12) and self.player.money >= self.player.bet
        initial_round = len(self.player.hand) == 2
        
        # if split and double and initial_round:
        #     ans = input('\n[H]it   [S]tand   [D]ouble down  S[p]lit\n').lower()
        if double and initial_round:
            ans = input('\n[H]it   [S]tand   [D]ouble down\n').lower()
        # elif split and initial_round:
        #     ans = input('\n[H]it   [S]tand   S[p]lit\n').lower()
        else:
            ans = input('\n[H]it   [S]tand\n').lower()
        return ans
        
    def dealerDraw(self):
        clear()
        self.displayHands(True)
        # Dealer 
            # If hand total < 17, Hit, else Stand (if A makes >= 17, stand)
        while self.cardTotal(self.dealer.hand) < 17:
            print('\nDealer takes a card')            
            self.dealer.takeTopCard(self.deck)
            sleep(1)
            self.displayHands(True)
            sleep(1)      
        if self.cardTotal(self.dealer.hand) > 21:
            print('\nUh oh...')             
        else:
            print('\nDealer stands')      
        sleep(2)
            
    def resolveRound(self):
        clear()
        # Settlement
        dealerTotal = self.cardTotal(self.dealer.hand)
        playerTotal = self.cardTotal(self.player.hand)
        # Dealer busts OR Player total > Dealer total: Player receives 2x bet
        
        print(f"\nDealer --- Player")
        print(f"{dealerTotal}".center(6," ", ) + " "*5 + f"{playerTotal}".center(6, " "))
        print('')
        if dealerTotal > 21:
            print("Dealer busts! You win!")
            print(f"\nWinnings: ${self.player.bet}")
            self.player.settle(2*self.player.bet)
        elif dealerTotal < playerTotal:
            print("Great! You won!")
            print(f"\nWinnings: ${self.player.bet}")
            self.player.settle(2*self.player.bet)
        # Player total = Dealer total: Player receives bet
        elif dealerTotal == playerTotal:
            print('\nYou got your money back.')
            self.player.settle(self.player.bet)
        # Dealer total > Player total: round end
        else:
            print('Better luck next time!')        
        
        print(f"\nYour cash: ${self.player.money}")
        self.wait()
        self.cleanup()
    
    def cleanup(self):
        self.player.discard(self.deck)
        self.dealer.discard(self.deck)
        
    def wait(self):
        print("\nPress any key to continue...")
        m.getch()
        
        
      
user = User('Sven') 
bj_game = Blackjack(user)