
def intro():
    #Introduction and invitation to start game:
    print("...***BARE-BONES BLACKJACK ***...")
    print("Welcome, I'm the 'Dealer' entity that handles most of the tasks to run this game.  The current release of this Python-based blackjack game is designed for lightweights:  single-player (plus dealer), no additional options such as 'double-down' or 'insurance', bets ranging from only $5-10, and a starting balance of just $50.")  
    print("We're playing with a single deck, but you'll be able to play a dozen or so rounds without interruption before we have to start a new shuffled deck.  Also, at the end of each round you'll get an option to retrieve a history of all your hands, bets and available betting balances compiled during your current playing session.")

def hand_count(Mem, acevalue, currplayer, player1, dealer):
    #print("executing hand_count for {} with acevalue {}".format(Mem.currplayer, acevalue))
    handvalue = 0
    acecount = 0
    
    for card in eval(currplayer+".currcards"):
        #print("{}'s card: {}".format(currplayer, card))
        #print("here's what card[0] of the card looks like:  ", card[0])
        if card[0] in ['J', 'Q', 'K']:
            #print("Jack, Queen or King valued at 10")
            handvalue += 10
        elif card[0] == 'A':
            #print("Card is an Ace; you now have {} Ace(s)".format(acecount))
            #...increment the Ace-in-hand counter 
            acecount += 1
            #test whether or not this is a recount
            if acevalue == 11:
                #first aggregate handvalue with soft acevalue (this is before possible recound
                handvalue += acevalue
                #then set acevalue to 1 for process_~ to eval in case recount required
                #...(if >1 Ace(s) found have to go to acevalue=1 anyway - even just 2 is bust at 11)
                acevalue = 1
            elif acevalue == 1:
                #this is a recount aggregate w/incoming acevalue=1 (bust when set to 11)
                handvalue += acevalue
                #...then set to 0 so fullcyclecount knows recount already occurred
                acevalue = 0
        #for aggregating with number cards:
        else:
            #print("This is (or should be) number card: ", card)
            try:
                handvalue += int(card[0])
            except TypeError:
                print("there was a type error")
                print("an unexpected exception occurred extracting integer from card string")
            else:
                print()
                #print("{}'s number card successfully aggregated handvalue to {}".format(currplayer, handvalue))

    #print("total handvalue from handcount:", handvalue)
    return handvalue, acevalue 

#process_hand_count function with params Mem, handvalue, acecount; returning handvalue, winningplayer
def process_hand_count(handvalue, acevalue):
    #print("running process_hand_count with handvalue={} and acevalue={}".format(handvalue, acevalue))
    winningplayer = "none"
    #***NEED TO ADD LOGIC HERE - ACTUALLY AFTER - FOR BLACKJACK TIE***
    if handvalue == 21:
        print("***")
        print("***{} wins with Blackjack!***".format(Mem.currplayer))
        print("***")
        winningplayer = Mem.currplayer
    #test for bust:
    #..(already tested for and recounted as needed for >21 with soft-Ace in fullcyclecount)
    elif handvalue > 21:
        if Mem.currplayer == "player1":
            winningplayer = "dealer"
            bustedplayer = "player1"
        else:
            winningplayer = "player1"
            bustedplayer = "dealer"
        print("***")
        print("***{} HAS BUSTED; {} WINS***".format(bustedplayer, winningplayer))
        print("***")
    else:
        print()
        #print("{}'s current handvalue:  {}".format(Mem.currplayer, handvalue))
    #update currplayer's handvalue attribute - WITH eval() CAPTURING Mem.currplayer
    currplayerupdatecallstring = "{}.update_handvalue({})".format(Mem.currplayer, handvalue)
    eval(currplayerupdatecallstring)
    return handvalue, winningplayer

def fullcountingcycle(Mem):
    #HANDCOUNT AND PROCESS-HANDCOUNT - FULL CYCLE, CAN BE CALLED FROM:
    #-1. initial deal-player1
    #-2. initial deal-dealer
    #-3. each of player1's requested hits (if any)
    #-4. each of dealer's requested hits (if any)
    acevalue = 11
    handcount_return = hand_count(Mem, acevalue, Mem.currplayer, player1, dealer)
    #print("handcount_return for {} before soft Ace >21 check: ".format(Mem.currplayer, handcount_return))
    #hand_count returns 2 params: currplayer's handvalue & acevalue
    #check if recount required: if >21 and acevalue changed to 1 by prev handcount (finding Ace)
    if handcount_return[0] > 21 and handcount_return[1] == 1:
        print("handcount would bust with soft-Ace acevalue; re-running handcount") 
        print("*FOLLOWING SCREEN-PRINT IS CONFIDENTIAL INFO!; REMOVE AFTER DEBUGGING*")
        handcount_return = hand_count(Mem, handcount_return[1], Mem.currplayer, player1, dealer)
        print("handvalue after hard-Ace recount: ", handcount_return[0])
    #print("calling process_hand_count with handcount_return", handcount_return)
    return process_hand_count(handcount_return[0], handcount_return[1])
    
#####END OF MAIN FUNCTION DECLARATIONS#####

print("******************")

intro()

print("******************")

go_or_stop = input("Do you want to start playing?  Enter 'G' to go ahead or 'S' to stop.").upper()

if go_or_stop == 'S':
    print("Ok,  maybe another time; please forward any suggestions or requests to  dan.northrup@nltgis.com.")
    #END
else:
    #SETUP FOR SERIES OF ROUNDS (WITH INITIAL SHUFFLING OF DECK):
    #import deck and class declaration modules in the Bare Bones (BB) Blackjack package folder
    import BBBlackjack_deck
    import BBBlackjack_ClassDeclarations

    #init globals:
    #with Steve Ferg's "mem class"
    class Mem:
        deck = BBBlackjack_deck.deck
        deck_list = list(deck.keys())
        currplayer = 'player1'
        next_card_index = 0
        roundcount = 1
        #roundstatuscode legend:  C=continuing, W=end with win, Z=exit whole game with errors
        #roundstatuscode = 'C'  ##DON'T THINK NEEDED
        #print("Mem globals class with deck, deck_list, currplayer, next_card_index initialized")
    
    #init objects
    #print("[initializing player1 and dealer objects]")
    dealer = BBBlackjack_ClassDeclarations.DealerClass('dealer', [], 0, [])
    #dealer.update_name('dealer')
    player1 = BBBlackjack_ClassDeclarations.Player('player1', [], 0, 0, [[]], [[]], [[]])
    #player1.update_name('player1')
    
    print("I am shuffling the deck.")
    dealer.shuffle_deck(Mem)
    print()
    
    winningplayer = 'none'
    
    #LOOP OF ROUNDS
    while go_or_stop == 'G' and winningplayer == 'none':
        Mem.currplayer = 'player1'
        player1.currcards = []
        dealer.currcards = []
        #Start a round:
        player1bet = dealer.collect_bets()
    
        while player1bet > player1.cashavail:
            print("Sorry, the Bank says your available balance isn't sufficient for your bet amount.")
            if input("Do you want to try again with a smaller amount? (Y/N)").upper() == "N":
                #print("Okay, thanks for stopping by.  You can launch the game at any time to start fresh with a $50 balance.")
                #     (don't need to say goodbye here; see very bottom after end of loop-of-rounds)
                #negate the condition for the whole loop-of-rounds...
                go_or_stop = 'S'
                #...and "break" out of the prompting/testing-for-payable-bet loop
                break
                #exit()    #original idea (messy, wd involve exception-handling) 
            else:
                #prompt player for bet again if "Y" (not "N")
                player1bet = dealer.collect_bets()
                #("continue" takes you back to top of test-for-sufficient-cash loop)
                continue
        #test if player chose not to (or couldn't) enter a smaller acceptable amount, thus has to quit the game
        if go_or_stop == 'S':
            #"continue" at this level forces skip all below and back up to top of enclosing loop-of-rounds to test go_or_stop
            continue
        
        print("House matches your bet; winnings for this round are currently ${}".format(player1bet * 2))
        player1.update_cashavail(-player1bet)
        player1.update_bet_history(player1bet)
    
        #initial deal:
        dealer.initial_deal(Mem, player1)
    
        #initial call/run of hand_count() are always with 'soft Ace' or acevalue=11;
        #  ...count is re-run with 'hard Ace' or acevalue=1 if over 21 with Ace(s) present
        #note, initially Mem.currplayer='player1'
        #FULL-CYCLE HANDCOUNT, APPLIED TO:
        #-1. fullcyclecount - initial deal-player1 (Mem.currplayer's initial value)
        print("full-cycle count for initial-player1")
        #fullcountingcycle testing for winner determination
        #...exit round if winner (announced w/in this call of the process_hand_count function)
        #fullcountingcycle NOW HAS 2 RETURNS (acevalue, winningplayer)
        fullcountingcycle_return = fullcountingcycle(Mem)
        print("fullcountingcycle_return in initial deal for currplayer={} is [handvalue={}, winningplayer={}]".format(Mem.currplayer, fullcountingcycle_return[0], fullcountingcycle_return[1]))
        if fullcountingcycle_return[1] != 'none':
            print("exiting round due to blackjack or bust - winner has been determined")
        else:
        #-2. fullcyclecount - initial deal-dealer
            print("full-cycle count for initial-dealer")
            Mem.currplayer = 'dealer'
            fullcountingcycle_return = fullcountingcycle(Mem)
            #print("fullcountingcycle_return in initial deal for currplayer={} is [handvalue={}, winningplayer={}]".format(Mem.currplayer, fullcountingcycle_return[0], fullcountingcycle_return[1]))
        #-3. fullcyclecount - hitloop with player1 (changing back from dealer's initial count
            if fullcountingcycle_return[1] == 'none':
                #print("calling hitloop with currplayer = player1 - calls full-cycle count inside")
                Mem.currplayer = 'player1'
                #ask the current player whether they want to hit or stand
                hit_or_stand = dealer.ask_hit_or_stand(Mem)
                winningplayer = 'none'
                #hitloop for as long as player asks for hit; make winningplayer local:
                while hit_or_stand == 'H' and winningplayer == 'none':
                    hitcard = dealer.deal_hit(Mem, player1)
                    #print("{} gets hit with {}, counting cards again...".format(Mem.currplayer, hitcard))
                    fullcountingcycle_return = fullcountingcycle(Mem)
                    #print("fullcountingcycle_return in hit for currplayer={} is [handvalue={}, winningplayer={}]".format(Mem.currplayer, fullcountingcycle_return[0], fullcountingcycle_return[1]))
                    winningplayer = fullcountingcycle_return[1]
                    #after initial hit, ask again 
                    if winningplayer == 'none':
                        hit_or_stand = dealer.ask_hit_or_stand(Mem)
        #-4. fullcyclecount - hitloop with dealer (if winner not determined yet)
        #...once player1 stands (and winner still not determined), dealer's turn for hits
        #...each hitloop iteration has its own handcount processing and potential busts/wins...
            if winningplayer == 'none':
                print("player1 stands, moving on to dealer hits")
                Mem.currplayer = 'dealer'
                #print("starting hitloop with currplayer = dealer - calls fullcyclecount inside")
                #ask the current player whether they want to hit or stand
                hit_or_stand = dealer.ask_hit_or_stand(Mem)
                #hitloop for as long as player asks for hit; make winningplayer local:
                while hit_or_stand == 'H' and winningplayer == 'none':
                    hitcard = dealer.deal_hit(Mem, player1)
                    #print("{} gets hit with {}, counting cards again...".format(Mem.currplayer, hitcard))
                    fullcountingcycle_return = fullcountingcycle(Mem)
                    winningplayer = fullcountingcycle_return[1]
                    print("fullcountingcycle_return in hit for currplayer={} is [handvalue={}, winningplayer={}]".format(Mem.currplayer, fullcountingcycle_return[0], fullcountingcycle_return[1]))
                    #after initial hit, ask again 
                    if winningplayer == 'none':
                        hit_or_stand = dealer.ask_hit_or_stand(Mem)
            #***
            #IF DEALER STANDS / winningplayer STILL NOT YET DETERMINED... 
            #...DETERMINE WINNER OR TIE FROM TEST FOR HIGHEST OR MATCHING HAND:
            if winningplayer == 'none':
                if player1.handvalue != dealer.handvalue:
                    #players don't have equal-value hands
                    if player1.handvalue > dealer.handvalue:
                        winningplayer = 'player1'
                    elif player1.handvalue < dealer.handvalue:
                        winningplayer = 'dealer'
                    print("**")
                    print("BOTH PLAYER AND DEALER STAND; {} HAS HIGHEST HAND AND WINS THE ROUND".format(winningplayer))
                    print("**")
                else:
                    print("**")
                    print("PLAYER AND DEALER HAVE MATCHING HANDS; THIS ROUND IS A TIE")
                    print("**")
                    #return player1's bet (*FUTURE ADD OPTION TO LEAVE IN POT FOR NEXT ROUND*)
                    tie_refund = player1.bet_history[len(player1.bet_history)-1]
                    player1.cashavail += tie_refund
        
        print("--")
        print("--CHECKS FOR ALL WIN / TIE SCENARIOS COMPLETED, END OF ROUND--")    
        print("--")
        print("===")
        print("===DEALER'S HAND: ", dealer.currcards)
        print("===PLAYER1'S HAND: ", player1.currcards)
        print("===")
        #UPDATE PLAYER1'S HAND, HISTORY ETC. ATTRIBUTES
        player1.update_hand_history()
        #if won, deposit winnings into cashavail & cashavail_history
        if winningplayer == 'player1':
            #retrieve winning amt from the amount bet (*2):
            winnings = player1.bet_history[len(player1.bet_history)-1]*2
            print("test retrieval of last bet from bet_history: ", winnings)
            #add to player1.cashavail 
            print("player1.cashavail before adding these winnings: ", player1.cashavail)
            player1.cashavail += winnings
            print("AFTER adding these winnings: ", player1.cashavail)
        #update player1's cashavail_history here (in case winnings changed):
        player1.update_cashavail_history(player1.cashavail)
        print("player1's cashavail_history (at end of each round) is now ", player1.cashavail_history)

        
        go_or_stop = input("Another round?  (G[o] or S[top])").upper()
        if go_or_stop == 'G':
            winningplayer = 'none'
            Mem.roundcount += 1
            print("finished round {}, starting round {}".format(Mem.roundcount-1, Mem.roundcount))
            print("**checking to see if reaching end of deck...**")
            
            if Mem.next_card_index > 36:
                print("ONLY 15 OR FEWER CARDS LEFT IN SHUFFLED DECK, STARTING WITH A NEW, RESHUFFLED DECK.")
                dealer.shuffle_deck(Mem)
                Mem.next_card_index = 0
        print("**")
        print("**")
        
    print("Okay, thanks for coming over to play.  You can launch the game again at any time to start with a fresh deck and a $50 balance.")

#END OF SET OF ROUNDS; reset all globals [AND INSTANCES? WHOLE KERNEL? - PENDING RESEARCH]
Mem.deck = {}
Mem.deck_list = []
Mem.currplayer = ''
Mem.next_card_index = 0
Mem.roundcount = 1
print("globals reset for new set of rounds")
