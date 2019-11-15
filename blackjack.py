import random
import time

def builddeck():
    suit = ['spades', 'clubs', 'hearts', 'diamonds']
    card = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']
    faceval = [1,2,3,4,5,6,7,8,9,10,10,10,10]
    j=0
    k=0
    cards = []
    suits = []
    facevals = []
    for i in range(52):
        cards.append(card[k])
        suits.append(suit[j])
        facevals.append(faceval[k])
        j=j+1
        if j == 4:
            j = 0
        k=k+1
        if k == 13:
            k = 0
    randlist = random.sample(range(52), 52)
    cardshuf = []
    suitshuf = []
    facevshuf = []
    for i in range(52):
        x = randlist[i]
        cardshuf.append(cards[x])
        suitshuf.append(suits[x])
        facevshuf.append(facevals[x])
    return cardshuf, suitshuf, facevshuf
def playerhit(card, face, suit, cardcount, handtotal, balance, bet, dealing):
    print(card[cardcount], "of",suit[cardcount])
    time.sleep(0.5)
    #determine handtotal if it has ace
    #add 1 to existing values and then append an 11
    if face[cardcount] == 1:
        for i in range(len(handtotal)):
            handtotal[i] = handtotal[i] + 1
            handtotal.append(handtotal[i] + 11)
    else:           
        for i in range(len(handtotal)):
            handtotal[i]=handtotal[i]+face[cardcount]
    #removes hands that are bust
    for x in handtotal[:]:
        if x > 21:
            handtotal.remove(x)

    #checks for bust condition        
    if len(handtotal) == 0:
            # print("Your hand total is" handtotal)
            print("You busted!!!")
            time.sleep(0.5)
            balance = balance - bet
            playing = False
            dealing = False
    else:
        print("Your new hand total is ", handtotal)
        cardcount = cardcount + 1
    return card, face, suit, cardcount, handtotal, balance, bet, dealing
def dealerhit(card, face, suit, cardcount, handtotal, balance, bet, dealing, dealtotal):
    print("Dealer draws ",card[3], "of",suit[3])
    time.sleep(0.5)
    if face[2] == 1 and face[3] == 1:
        dealtotal.append(2)
        dealtotal.append(12)
    elif face[2] == 1:
        dealtotal.append(1 + face[3])
        dealtotal.append(11 + face[3])
    elif face[3] == 1:
        dealtotal.append(1 + face[2])
        dealtotal.append(11 + face[2])
    else: 
        dealtotal.append(face[2]+face[3])
    print("Dealer hand total is: ", dealtotal)
    time.sleep(0.5)
    dealcount = cardcount + 1
    dealercards = True
    while dealercards:
        for x in dealtotal[:]:
            if x > 21:
                dealtotal.remove(x)

        #check dealer total vs player (dealer can't bust on hand)
        for x in dealtotal[:]:
            if x > 16:
                if max(handtotal) > max(dealtotal):
                    print("You have", max(handtotal),", dealer has ", max(dealtotal))
                    time.sleep(1.0)
                    print("Player win!")
                    time.sleep(1.0)
                    balance = balance + bet
                    dealing = False
                    dealercards = False
                    break
                elif max(handtotal) == max(dealtotal):
                    print("You have", max(handtotal),", dealer has ", max(dealtotal))
                    time.sleep(1.0)
                    print("Tie!")
                    time.sleep(1.0)
                    dealing = False
                    dealercards = False
                    break
                else: 
                    print("You have", max(handtotal), ", dealer has", max(dealtotal))
                    time.sleep(1.0)
                    print("Dealer Win!")
                    time.sleep(1)
                    balance = balance - bet
                    dealing = False
                    dealercards = False
                    break

    ##continuous dealer dealing, copied from player deal
        if dealing == False:
            break

        if face[dealcount] == 1:
            for i in range(len(dealtotal)):
                dealtotal.append(dealtotal[i] + 11)
                dealtotal[i] = dealtotal[i] + 1
        else:           
            for i in range(len(dealtotal)):
                dealtotal[i]=dealtotal[i]+face[dealcount]

        print("Dealer draws ",card[dealcount], "of",suit[dealcount])
        time.sleep(1)
        print("Dealer hand total is: ", dealtotal)            
        time.sleep(1)
        
        for x in dealtotal[:]:
            if x > 21:
                dealtotal.remove(x)
        #checks for bust condition        
        if dealing == False:
            break
        elif len(dealtotal) == 0:
            # print("Your hand total is" handtotal)
                print("Dealer busted!!")
                time.sleep(1.5)
                balance = balance + bet
                dealing = False
                dealercards = False
                break
        dealcount = dealcount + 1
    return card, face, suit, cardcount, handtotal, balance, bet, dealing, dealtotal
def play():
    playing = True
    i = 0
    balance = int(50)
    while playing:
        print('\n')
        print("Welcome to BlackJack")   
        print("You have $",int(balance))
        if balance < 1:
            print("You are out of money! Thanks for playing")
            break
        bet = []
        bet = input("Enter bet amount to play, or type 'q' to quit: ")
        if bet == 'q':
            break
        try:
            bet = int(bet)
        except:
            print("Must enter a number!")
            continue
        if bet < 1:
            print("Invalid Bet")
            continue
        elif bet > balance:
            print("You don't have enough money")
            continue
        cardcount = 4
        dealtotal=[]
        handtotal=[]
        card, suit, face = builddeck()
        #calculate your initial card value
        if face[0] == 1 and face[1] == 1:
            handtotal.append(2)
            handtotal.append(12)
        elif face[0] == 1:
            handtotal.append(1 + face[1])
            handtotal.append(11 + face[1])
        elif face[1] == 1:
            handtotal.append(1 + face[0])
            handtotal.append(11 + face[0])
        else: 
            handtotal.append(face[0]+face[1])
        print('\n')
        print("Your cards are:")
        time.sleep(0.5)
        print(card[0], "of", suit[0])
        time.sleep(0.5)
        print(card[1], "of", suit[1])
        time.sleep(0.5)
        print("Your hand total is ", handtotal)
        time.sleep(0.5)
        blackjack = False
        for x in handtotal:
            if x == 21:
                print("BLACKJACK!!!!")
                time.sleep(1.5)
                balance = balance + 1.5*bet
                blackjack = True

        if blackjack == True:
            dealing = False
        else:
            print('\n')
            print("Dealer is showing:")
            time.sleep(0.5)
            print(card[2], "of", suit[2])
            dealing = True

        while dealing:
            try:
                move = input("Press h to hit, s to stand, or d to double: ")
            except: 
                print("Unrecognized command")
                print()
                continue
            if move == 'h':
                card, face, suit, cardcount, handtotal, balance, bet, dealing = playerhit(card, face, suit, cardcount, handtotal, balance, bet, dealing)
            elif move == 's':
                card, face, suit, cardcount, handtotal, balance, bet, dealing, dealtotal = dealerhit(card, face, suit, cardcount, handtotal, balance, bet, dealing, dealtotal)
            elif move == 'd':
                bet = 2*bet
                print(card[cardcount], "of",suit[cardcount])
                time.sleep(0.5)
                #determine handtotal if it has ace
                #add 1 to existing values and then append an 11
                if face[cardcount] == 1:
                    for i in range(len(handtotal)):
                        handtotal[i] = handtotal[i] + 1
                        handtotal.append(handtotal[i] + 11)
                else:           
                    for i in range(len(handtotal)):
                        handtotal[i]=handtotal[i]+face[cardcount]
                #removes hands that are bust
                for x in handtotal[:]:
                    if x > 21:
                        handtotal.remove(x)

                #checks for bust condition        
                if len(handtotal) == 0:
                        print("You busted!!!")
                        time.sleep(0.5)
                        balance = balance - bet
                        dealing = False
                else:
                    print("Your new hand total is ", handtotal)
                    time.sleep(0.5)
                    card, face, suit, cardcount, handtotal, balance, bet, dealing, dealtotal = dealerhit(card, face, suit, cardcount, handtotal, balance, bet, dealing, dealtotal)              
play()
    
 
