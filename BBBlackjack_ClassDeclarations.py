class Player():
    def __init__(self, name, currcards, handvalue, cashavail, cashavail_history, bet_history, hand_history):
        #PER StackOverflow explanation, if you set up a subclass __init__,
        #...Python doesn't assume you still want the parent class's attributes
        self.name = name
        print("Initializing '{}' Player class instance & attributes".format(self.name))
        self.currcards = []
        self.handvalue = 0
        self.cashavail = 50
        self.cashavail_history = []
        self.bet_history = []
        self.hand_history = [[]]
        print("instance of Player being created for a set of rounds.")

    #methods from old BasicPlayer for updating each instance's current cards and current hand value attributes
    def update_currcards(self, currcards):
        self.handvalue = currcards
        #print("player instance's currcards attribute has been updated to: ", self.handvalue)
    def update_handvalue(self, curramount):
        self.handvalue = curramount
        #print("player instance's handvalue attribute has been updated to: ", self.handvalue)

    #update player's available cash when 1) inputting bets to dealer (-) or 2) with winning amounts (+)
    def update_cashavail(self, amount):
        self.cashavail += amount
        print("player1's available cash has been updated to: ", self.cashavail)
        
    #update self's bet history when submitting bets to dealer
    def update_bet_history(self, betamt):
        #if self.bet_history == []:
        #    self.bet_history = betamt
        #else:
        self.bet_history.append(betamt)
        print("player1's bet_history in this set of rounds has been updated to", self.bet_history)
        
    #update self's available-cash history at the end of each round
    def update_cashavail_history(self, amount):
        self.cashavail_history.append(amount)
        #print("player1's available-cash history (at end of each round) has been updated to", self.cashavail_history)
        
    #update self's hand history at end of each round
    def update_hand_history(self):
        self.hand_history.append(self.currcards)
        #print("player1's hand_history in this set of rounds has been updated to", self.hand_history)

class DealerClass():
    def __init__(self, name, currcards, handvalue, shuffled_deck):
        self.name = name
        #print("Initializing '{}' instance & attributes of Dealer class".format(self.name))
        self.currcards = []
        self.handvalue = 0
        self.shuffled_deck = []
        print("instance of Dealer being created for a set of rounds.")

    #methods from old BasicPlayer for updating each instance's current cards and current hand value attributes
    def update_currcards(self, currcards):
        self.handvalue = currcards
        #print("player instance's handvalue attribute has been updated to: ", self.handvalue)
    def update_handvalue(self, curramount):
        self.handvalue = curramount
        #print("player instance's handvalue attribute has been updated to: ", self.handvalue)

    def shuffle_deck(self, Mem):
        import random
        from random import shuffle
        self.shuffled_deck = random.sample(Mem.deck_list, len(Mem.deck_list))
        print("deck has been (re)shuffled")

    def collect_bets(self):
        while True:
            player1bet = input("How much are you betting?  (Enter integer $5-$20)")
            try:
                player1bet = int(player1bet)
            except:
                print("Please try again with a whole number.")
                continue
            if player1bet < 5 or player1bet > 20:
                print("Please try again with a bet in the $5-$20 range.")
            else:
                return player1bet

    def initial_deal(self, Mem, player1):
        #dealer deals to player1 (assigning 'player1' to location/owner of the drawn card):
        Mem.deck[self.shuffled_deck[Mem.next_card_index]] = 'player1'
        #append 1st card to player1's currcards attribute (currplayer known, eval() not req'd here)
        player1.currcards.append(self.shuffled_deck[Mem.next_card_index])
        #move next_card_index to next card 
        Mem.next_card_index += 1
        Mem.deck[self.shuffled_deck[Mem.next_card_index]] = 'player1'
        #append 2nd card to player1's currcards attribute (currplayer known, eval() not req'd here)
        player1.currcards.append(self.shuffled_deck[Mem.next_card_index])
        Mem.next_card_index += 1
        print()
        print("initial 2 cards have been dealt; player1's hand is now: ", player1.currcards)

        #dealer deals to self:
        Mem.deck[self.shuffled_deck[Mem.next_card_index]] = 'dealer'
        #print("(dealer's first card is face-down)")
        #append 1st card to dealer's currcards attribute (currplayer known, eval() not req'd here)
        self.currcards.append(self.shuffled_deck[Mem.next_card_index])
        Mem.next_card_index += 1
        Mem.deck[self.shuffled_deck[Mem.next_card_index]] = 'dealer'
        #append 2nd card to dealer's currcards attribute (currplayer known, eval() not req'd here)
        self.currcards.append(self.shuffled_deck[Mem.next_card_index])
        #print("dealer's second (face-up) card: ", self.shuffled_deck[Mem.next_card_index])
        Mem.next_card_index += 1

    def ask_hit_or_stand(self, Mem):
        if Mem.currplayer == 'dealer':
            if self.handvalue < 17:
                print('dealer asks for a hit')
                return 'H'
            else:
                print('dealer stands')
                return 'S'
        else:
            hit_or_stand = input("Do you want another hit, or stand (H or S)?").upper()
            print("hit_or_stand:", hit_or_stand)
            while hit_or_stand not in ['H','S']:
                input("Please enter either 'H' or 'S'").upper()
            print("player1 chooses {}".format(hit_or_stand))
            return hit_or_stand

    def deal_hit(self, Mem, player1):
        Mem.deck[self.shuffled_deck[Mem.next_card_index]] = Mem.currplayer
        #print("{}'s hit card is: {}".format(Mem.currplayer, self.shuffled_deck[Mem.next_card_index]))
        #append card to currplayer's currcards attribute (1st building the string for eval())
        if Mem.currplayer == 'dealer':
            player = 'self'
        else:
            player = Mem.currplayer
        currcard_update_string = player + ".currcards.append(self.shuffled_deck[Mem.next_card_index])"
        eval(currcard_update_string)
        if Mem.currplayer == 'player1':
            print("player1's hand is now: ", player1.currcards)
        
        Mem.next_card_index += 1
        return self.shuffled_deck[Mem.next_card_index-1]
