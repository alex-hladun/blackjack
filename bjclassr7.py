import collections
import random
import time

class Deck: 
    def __init__(self):
        suit = ['spades', 'clubs', 'hearts', 'diamonds']
        rank = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']
        faceval = [1,2,3,4,5,6,7,8,9,10,10,10,10]
        Card = collections.namedtuple('Card', ['rank','suit','faceval'])
        self.deck = []
        for suit in suit:
            i=0
            for x in rank:
                self.deck.append(Card(x, suit, faceval[i]))
                i = i+1

    def shuffle(self):
        print("Shuffling Deck...")
        random.shuffle(self.deck)

class Hand:
    def __init__(self):
        self.handtotal = [[]]
        self.handarray = [[]]
        self.betarray = [[]]
        self.movecount = [0]


    def initialize(self,hn):
        """Takes the initial hand (player or dealer) and calculates the hand value(s), 
        dependent on the presence of aces or not"""

        #resets the count for split cards
        self.handtotal[hn] = []

        if self.handarray[hn][0].faceval == 1 and self.handarray[hn][1].faceval == 1:
            self.handtotal[hn].append(2)
            self.handtotal[hn].append(12)
        elif self.handarray[hn][0].faceval == 1:
            self.handtotal[hn].append(1 + self.handarray[hn][1].faceval)
            self.handtotal[hn].append(11 + self.handarray[hn][1].faceval)
        elif self.handarray[hn][1].faceval == 1:
            self.handtotal[hn].append(1 + self.handarray[hn][0].faceval)
            self.handtotal[hn].append(11 + self.handarray[hn][0].faceval)
        else: 
            self.handtotal[hn].append(self.handarray[hn][0].faceval+self.handarray[hn][1].faceval)

    def checkmove(self,player,hn):
        """checks what moves are possible based on the current hand and asks the player.
        Returns the move. hn denotes hand number."""
        while True:
            #check if split move possible
            if len(self.handarray[hn]) == 2:
                if self.handarray[hn][0].rank == self.handarray[hn][1].rank:
                    try:
                        self.move = input("Press h to hit, s to stand, sp to split, or d to double:")
                    except: 
                        print("Unrecognized command")
                        continue
                    if self.move == 'h' or self.move=='s':
                        break
                    elif self.move == 'd' or self.move=='sp':
                        betcheck = sum(self.betarray)+self.betarray[hn]
                        if betcheck > player.balance:
                            print("You don't have enough $$$")
                            time.sleep(0.5)
                            continue
                        else:
                            break
                else:
                    try:
                        self.move = input("Press h to hit, s to stand, or d to double:")
                    except: 
                        print("Unrecognized command")
                        continue
                    if self.move == "h" or self.move=="s":
                        break
                    if self.move == "d" or self.move=="sp":
                        betcheck = sum(self.betarray)+self.betarray[hn]
                        if betcheck > player.balance:
                            print("You don't have enough $$$")
                            time.sleep(0.5)
                            continue
                        else:
                            break

            else: 
                try:
                    self.move = input("Press h to hit, or s to stand:")
                except: 
                    print("Unrecognized command")
                    continue
                if self.move == 'h' or 's':
                    break
                    
    def blackjack_check(self,hn):
        self.blackjack = False
        for x in self.handtotal[hn]:
            if x == 21:
                print("BLACKJACK!!!!")
                self.movecount[hn] = 21
                time.sleep(0.5)
                player.balance = player.balance + 1.5 * player.bet
                self.blackjack = True
                player.dealing = False
    
   
    def hit(self,deck,hn):
        self.handarray[hn].append(deck.deck.pop())

    def double(self,deck,hn):
        """This function is called when the player chooses to double their hand"""
        self.betarray[hn] = 2 * self.betarray[hn]
        ###Be cautious of this for later
        self.hit(deck,hn)
    
    def callout(self,hn):
        '''reads out the most recent card drawn'''
        print(self.handarray[hn][-1].rank,"of ",self.handarray[hn][-1].suit)
        time.sleep(0.5)

    def movetick(self,hn):
        self.movecount[hn]=self.movecount[hn]+1

    def full_callout(self,hn):
        '''reads out the latest hand and hand total'''
        print("Hand number", hn+1,"of",len(self.handarray),":")
        print(self.handarray[hn][-2].rank,"of ",self.handarray[hn][-2].suit)
        time.sleep(0.5)
        print(self.handarray[hn][-1].rank,"of ",self.handarray[hn][-1].suit)
        time.sleep(0.5)

    def score_callout(self,hn):
        '''reads out your hand total'''
        print("Your hand total is ", self.handtotal[hn])
        time.sleep(0.5)

    def checkhand(self,player,hn):
        """Calculates the hand score. 
        Determine handtotal if it has ace
        add 1 to existing values and then append an 11.
        Also checks for bust condition"""
        if self.handarray[hn][-1].faceval == 1:
            for i in range(0,len(self.handarray[hn])-1):
                self.handtotal[hn].append(self.handtotal[hn][i] + 10)
            for i in range(0,len(self.handarray[hn])-1):
                self.handtotal[hn][i] = self.handtotal[hn][i] + 1
        else:           
            for i in range(0,len(self.handtotal[hn])):
                self.handtotal[hn][i]=self.handtotal[hn][i]+self.handarray[hn][-1].faceval

        #removes hands that are bust
        for x in list(self.handtotal[hn]):
            if x > 21:
                self.handtotal[hn].remove(x)

        if len(self.handtotal[hn]) == 0:
            # print("Your hand total is" handtotal)
            print("You Busted!!!")
            time.sleep(0.5)
            player.balance = player.balance - self.betarray[hn]
            player.dealing = False
            self.splitting = False
            return
        # else:
        #     #only putting this in here due to a glitch?
        #     for x in self.handtotal[hn]:
        #         if x > 21:
        #             self.handtotal[hn].remove(x)
            
        #     for x in self.handtotal[hn]:
        #         if x > 21:
        #             self.handtotal[hn].remove(x)

        print("Your new hand total is ", self.handtotal[hn])
        player.dealing = True
        return

    def dealerhit(self,player,deck):
        '''Makes dealer hit until she busts, or is 17 and higher'''
        print("Dealer draws ",self.handarray[0][-1].rank, "of",self.handarray[0][-1].suit)
        time.sleep(0.5)
        self.initialize(0)
        print("Dealer hand total is: ", self.handtotal[0])
        time.sleep(0.5) 
        self.dealing = True
        #Checks to see if dealer has soft 17 or hard 17. Stops dealing if they have hard 17.
        while self.dealing:
            for x in self.handtotal[0]:  
                if x == 17:
                    for y in self.handtotal[0]:
                        if y < 17:
                            break
                        else:
                            self.dealerbust = False
                            return
                elif x > 16:
                    self.dealerbust = False
                    return
            
            self.hit(deck,0)
            self.movetick(0)
            print("Dealer draws ",self.handarray[0][-1].rank, "of",self.handarray[0][-1].suit)
            time.sleep(0.5)

            self.check_dealer_bust()
            time.sleep(0.5)

        return

    def check_dealer_bust(self):
        '''This function is called to see if the dealer busts. 
        It REMOVES any cards over 21'''
        
        if self.handarray[0][-1].faceval == 1:
            for i in range(len(self.handtotal[0])):
                self.handtotal[0].append(self.handtotal[0][i] + 11)
                self.handtotal[0][i] = self.handtotal[0][i] + 1
        else:           
            for i in range(len(self.handtotal[0])):
                self.handtotal[0][i]=self.handtotal[0][i]+self.handarray[0][-1].faceval

        #removes hands that are bust
        for x in self.handtotal[0]:
            if x > 21:
                self.handtotal[0].remove(x)
        
        if len(self.handtotal[0]) == 0:
            self.dealing = False
            self.dealerbust = True
        else:
            print("Dealer hand total is: ", self.handtotal[0])   
            time.sleep(0.5)
            self.dealing = True
            self.dealerbust = False
        return 

    def split(self,deck,hn):
        '''sets up the hand array with the new split cards'''
        self.handarray.append([])
        self.handtotal.append([])
        self.movecount.append(0)
        self.betarray.append(self.betarray[hn])
        print("You have chosen to split!")
        time.sleep(0.5)
        self.handarray[-1].append(self.handarray[hn].pop())
        self.hit(deck,hn)
        self.hit(deck,len(self.handarray)-1)

class Table:
    def __init__(self, balance):
        self.balance = int(balance)

    def play(self):
        """The main play function for the blackjack game"""
        while self.balance > 0:
            print('\n')
            print("Welcome to BlackJack")   
            # bet = 5
            # only in here to speed things up
            self.prompt_bet()

            #honestly forget why this is here.
            if self.balance < 0:
                break

            deck = Deck()
            deck.shuffle()
            playerhand = Hand()
            playerhand.betarray[0] = self.bet
            dealerhand = Hand()
            playerhand.hit(deck,0)
            dealerhand.hit(deck,0)
            playerhand.hit(deck,0)
            dealerhand.hit(deck,0)
            playerhand.initialize(0)

            print('\n')
            print("Your cards are:")
            time.sleep(0.5)
            print(playerhand.handarray[0][0].rank, "of", playerhand.handarray[0][0].suit)
            time.sleep(0.5)
            print(playerhand.handarray[0][1].rank, "of", playerhand.handarray[0][1].suit)
            time.sleep(0.5)
            print("Your hand total is ", playerhand.handtotal[0])
            time.sleep(0.5)
            
            playerhand.blackjack_check(0)
            
            if playerhand.blackjack == False:
                print('\n')
                print("Dealer is showing:")
                time.sleep(0.5)
                print(dealerhand.handarray[0][0].rank, "of", dealerhand.handarray[0][0].suit)
                self.dealing = True

            while self.dealing:
                '''calls for initial move'''
                #SPLIT TESTING BELOW:
                # balance, bet, dealing, dealtotal, handtotal, dealerbust = playersplit(hand, deck, handtotal[0], balance, bet, dealing, dealerhand)
                # balance, bet, dealing = comparetable(handtotal, dealtotal[0], balance, bet, dealing, dealerbust)
                # print("TEST COMPLETE")

                playerhand.checkmove(player,0)

                if playerhand.move == 'h':
                    playerhand.hit(deck,0)
                    playerhand.callout(0)
                    playerhand.checkhand(player,0)

                elif playerhand.move == 's':
                    dealerhand.dealerhit(player,deck)
                    self.compare_table(playerhand,dealerhand)
                
                elif playerhand.move == 'd':
                    playerhand.double(deck,0)
                    playerhand.callout(0)
                    playerhand.checkhand(player,0)
                    if self.dealing == False:
                        break
                    dealerhand.dealerhit(player,deck)
                    self.compare_table(playerhand,dealerhand)
                elif playerhand.move == 'sp':
                    playerhand.split(deck,0)
                    self.split_betting(playerhand,deck)
                    dealerhand.dealerhit(player,deck)
                    self.compare_table(playerhand,dealerhand)

        if self.balance == 0:
            print("Out of money. Thanks for playing loser")
        else: 
            print("Thanks for playing")

    def split_betting(self,playerhand,deck):
        
        for x in range(0,len(playerhand.handarray)):
            #calculate initial score
            
            if playerhand.movecount[x] > 0:
                continue
            else:
                playerhand.initialize(x)
                playerhand.full_callout(x)
                playerhand.score_callout(x)
                playerhand.blackjack_check(x)
                
                #Need to put this here in case the player gets a blackjack, then we skip
                if playerhand.movecount[x] > 0:
                    playerhand.splitting = False
                else:
                    playerhand.splitting = True

                while playerhand.splitting:
                    playerhand.checkmove(player,x)
                    if playerhand.move == 'h':
                        playerhand.hit(deck,x)
                        playerhand.movetick(x)
                        playerhand.callout(x)
                        playerhand.checkhand(player,x)
                        if len(playerhand.handarray[x]) == 0:
                            playerhand.splitting = False
                    elif playerhand.move == 's':
                        playerhand.splitting = False
                        playerhand.movetick(x)
                        continue
                    elif playerhand.move == 'd':
                        playerhand.double(deck,x)
                        playerhand.callout(x)
                        playerhand.movetick(x)
                        playerhand.checkhand(player,x)
                        playerhand.splitting = False
                    elif playerhand.move == 'sp':
                        playerhand.split(deck,x)
                        #repeating function in case of multiple splits
                        self.split_betting(playerhand,deck)
                        self.split_betting(playerhand,deck)
                        self.split_betting(playerhand,deck)

    def compare_table(self,playerhand,dealerhand):
        """Compares the 'table', ie the players hand(s) versus the dealers hand"""
        
        for x in range(0,len(playerhand.handtotal)):   
            if len(playerhand.handtotal) > 1:
                print('\n')
                print("Split Hand", x+1,"of",len(playerhand.handarray),":")
                time.sleep(0.5)
                if len(playerhand.handtotal[x]) == 0:
                    print("You busted!")
                    time.sleep(0.5)
                    continue

                if playerhand.movecount[x] == 21:
                    print("You got a Blackjack!!") 
                    time.sleep(0.5)
                    continue

            if dealerhand.dealerbust == True:
                print("You have",max(playerhand.handtotal[x]),"and Dealer busted!!!")
                time.sleep(0.5)
                self.balance = self.balance + playerhand.betarray[x]
                continue
            if max(playerhand.handtotal[x]) > max(dealerhand.handtotal[0]):
                print("You have",max(playerhand.handtotal[x]),", dealer has",max(dealerhand.handtotal[0]))
                time.sleep(0.5)
                print("Player wins hand!")
                time.sleep(0.5)
                self.balance = self.balance + playerhand.betarray[x]
                continue
            elif max(playerhand.handtotal[x]) == max(dealerhand.handtotal[0]):
                print("You have",max(playerhand.handtotal[x]),", dealer also has",max(dealerhand.handtotal[0]),". Tie!")
                time.sleep(0.5)
                continue
            else: 
                print("You have",max(playerhand.handtotal[x]), ", dealer has",max(dealerhand.handtotal[0]))
                time.sleep(0.5)
                print("Dealer Wins hand!")
                time.sleep(0.5)
                self.balance = self.balance - playerhand.betarray[x]
                continue
        
        self.dealing = False
        return

    def prompt_bet(self):
        """Asks player for a bet and ensures it is within the balance range"""
        while self.balance > 0:
            print("You have $",int(self.balance))
            self.bet = input("Enter bet amount to play, or type 'q' to quit: ").lower()
            if self.bet == 'q':
                print("You leave the table with $", int(self.balance))
                self.balance = -1
                return
            try: 
                self.bet= float(self.bet)
                if 0 < self.bet <= self.balance:
                    return self
                raise ValueError
            except ValueError:
                print(f"You do not have enough money! Or invalid answer")

            
if __name__ == '__main__':
    player = Table(1000)
    player.play()
    player.play()
