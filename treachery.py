import deck
import character as char
import random
import time

treachery_deck = { 'Defense_1': 'Projectile', 'Defense_2': 'Projectile', 'Defense_3': 'Projectile', 'Defense_4': 'Projectile', \
                   'Defense_5': 'Poison', 'Defense_6': 'Poison', 'Defense_7': 'Poison', 'Defense_8': 'Poison',
                   'Weapon_1': 'Projectile', 'Weapon_2': 'Projectile', 'Weapon_3': 'Projectile', 'Weapon_4': 'Projectile', 
                   'Weapon_5': 'Poison', 'Weapon_6': 'Poison', 'Weapon_7': 'Poison', 'Weapon_8': 'Poison', \
                   'Weapon_9': 'Lasegun', 'Cheap_Hero_1': 'played_once', 'Cheap_Hero_2': 'played_once', \
                   'Cheap_Hero_3': 'played_once', 'Worthless_1': 'Kulon', 'Worthless_2': 'Trip_to_Gamont', \
                   'Worthless_3': 'La_La_La', 'Worthless_4': 'Baliset', 'Worthless_5': 'Jubba_Cloak', \
                   'Truth_Trance_1': '1_yes_no_question', 'Truth_Trance_2': '1_yes_no_question', 'Weather_Control': 'move_0_to_10_sectors',\
                   'Hajr': '1_extra_OPM',  'Ghola': 'revive_1_general_or_5_tokens', 'Karama_1': 'stop_or_use_powers' ,\
                   'Karama_2': 'stop_or_use_powers', 'Family_Atomics': 'blow_up_Sheild_Wall'}

#STACKED DECK is for testing only and allows us to dictate the order cards are dealt used for testing specific card handling
stacked_deck = { 'Karama_2': 'stop_or_use_powers', 'Karama_1': 'stop_or_use_powers', 'Weapon_4': 'Projectile','Worthless_3': 'La_La_La',\
                 'Defense_5': 'Poison', 'Defense_6': 'Poison', 'Cheap_Hero_2': 'played_once', 'Weapon_2': 'Projectile', \
                 'Weapon_1': 'Projectile', 'Weapon_2': 'Projectile', 'Weapon_3': 'Projectile', 'Weapon_4': 'Projectile', \
                 'Weather_Control': 'move_0_to_10_sectors',   'Hajr': '1_extra_OPM', 'Truth_Trance_2': '1_yes_no_question',\
                 'Defense_1': 'Projectile', 'Defense_2': 'Projectile', 'Defense_3': 'Projectile', 'Defense_4': 'Projectile', \
                 'Defense_6': 'Poison', 'Defense_7': 'Poison', 'Defense_8': 'Poison', 'Defense_5': 'Poison', \
                 'Weapon_5': 'Poison', 'Weapon_6': 'Poison', 'Weapon_7': 'Poison', 'Weapon_8': 'Poison', \
                 'Weapon_9': 'Lasegun',  'Family_Atomics': 'blow_up_Sheild_Wall' }

karama_cards = ['Karama_1', 'Karama_2']
worthless_cards = ['Worthless_1', 'Worthless_2', 'Worthless_3', 'Worthless_4', 'Worthless_5']
truth_trance_cards = ['Truth_Trance_1', 'Truth_Trance_2']
cheap_hero_cards = ['Cheap_Hero_1', 'Cheap_Hero_2','Cheap_Hero_3']
weapon_cards = ['Weapon_1', 'Weapon_2', 'Weapon_3', 'Weapon_4', 'Weapon_5', 'Weapon_6', 'Weapon_7', 'Weapon_8', 'Weapon_9']
defense_cards = ['Defense_1', 'Defense_2', 'Defense_3', 'Defense_4', 'Defense_5', 'Defense_6', 'Defense_7', 'Defense_8']
all_others = ['Weather_Control', 'Hajr', 'Ghola', 'Family_Atomics']

class Treachery(deck.Deck) :
    def __init__(self, thisGame):
        self.myGame = thisGame

        super().__init__('Treachery Deck', treachery_deck)

    def __str__(self):
        ret_str = 'Nothing Yet to display \n'
        ret_str += super().__str__()
        return ret_str

    def stack_the_deck(self):
        self.deck = stacked_deck

    def is_card_of_type(self, type, card):
        is_card_of_type = False
        list_of_cards_of_a_type = get_list_of_card_type(type)
        if card in list_of_cards_of_a_type:
            is_card_of_type = True
        return is_card_of_type

    def dealing_round(self):
        for key, character in self.myGame.character_turn_order.items():
            deal_card_to_character(self.myGame, character)

    def bidding_round(self):
        bidding(self.myGame)

def get_list_of_card_type(type):
    card_of_type = {
        'Karama':karama_cards,
        'Worthless': worthless_cards,
        'Truth_Trance': truth_trance_cards,
        'Cheap_Hero': cheap_hero_cards,
        'Weapons': weapon_cards,
        'Defense': defense_cards,
    }
    list_of_type = card_of_type.get(type, all_others)
    return list_of_type

def deal_card_to_character(thisGame, character):
    cards_needed = character.treachery_cards_needed()
    cards_per_deal = character.treachery_cards_per_deal_get()
    msg = 'treachery_card '
    cards_dealt = 0
    while 0 != cards_needed and 0 != cards_per_deal:
        card, details = thisGame.treachery.deal_card()
        cards_dealt += 1
        msg += '{} {} '.format(card, details)
        cards_per_deal -= 1
        cards_needed -= 1
        character.treachery_cards_add(card, details)

    if 0 != cards_dealt:
        character.send(msg, False)

def bidding(thisGame):
    bid_order_list = dict()
    card_list = dict()
    #need to construct a modifiable character list based initially on the game.character_turn_order
    for key, this_character in thisGame.character_turn_order.items():
        bid_order_list[this_character.name] = this_character
        this_character.chaom()

    #create a list of cards to bid on based on the number of characters not "full"
    for key, this_character in thisGame.characters.items():
        if 0 != this_character.treachery_cards_needed():
            card, detail = thisGame.treachery.deal_card()
            card_list[card] = detail
        #if the character is full he can still bid on cards but must pay for the card using a Karama card
        elif False == this_character.is_card_of_type_available('Karama'):
            del bid_order_list[this_character.name]

    atreides = thisGame.is_character_playing('Atreides')
    if None is not atreides and 0 != len(card_list): #send the card list to Atreides as he has vision to see the future
        msg = 'treachery_bidding_vision:'
        for card in card_list.keys():
            msg += ' {}'.format(card)
        atreides.send(msg, False)

    while 0 != len(card_list):
        # get the first card up for bid from the list
        card, detail = next(iter(card_list.items()))
        del card_list[card] #remove card from bidding list

        #initialize local variables that control the bidding sequence
        first_bidder_name, first_bidding_character = next(iter(bid_order_list.items()))
        forces_one_bid = True #needed when there is only one player bidding on cards to force the while loop below to execute
        passes_to_win_bid = (len(bid_order_list) - 1)
        passes_rcvd = 0
        bid = 0
        paying_with_karama = False
        paying_with_karama_card_name = ''
        bidding_character = None
        bidding_character_name = ''
        #if only one player is bidding because everyone else is full then passess to win will be 0 and = to passes_rcvd which is init to 0
        #force_one_bid  insures the while loop is executed once and the card for bid is offered to the sole player
        while ((passes_to_win_bid != passes_rcvd) or (True == forces_one_bid)):
            forces_one_bid = False
            # keep track of the number of characters the card is offered to ... a the end of this while loop a test will be
            #made for offers_this_loop == num_of_bidders and the bid == 0 will cause the while loop to terminate as no one wants the card
            offers_this_loop = 0
            for character_name, this_character in bid_order_list.items():
                offers_this_loop += 1
                msg = 'treachery_card_bidding {} {} {} {}'.format(card, bidding_character_name, bid, this_character.name)
                thisGame.broadcast(msg, False, this_character.name)
                character_made_bid = this_character.send_query_and_wait(msg)

                if True == character_made_bid:
                    if thisGame.value_rcvd > bid:
                        bid = thisGame.value_rcvd
                        if '' != thisGame.string_rcvd:
                            if this_character.is_card_of_type_available('Karama') and \
                                    thisGame.treachery.is_card_of_type('Karama', thisGame.string_rcvd):
                                paying_with_karama = True
                                paying_with_karama_card_name = thisGame.string_rcvd
                            else:
                                paying_with_karama = False
                                paying_with_karama_card_name = ''
                        else:
                            paying_with_karama = False
                            paying_with_karama_card_name = ''

                        passes_rcvd = 0
                        bidding_character = this_character
                        bidding_character_name = this_character.name
                    else:
                        passes_rcvd += 1
                        print('Err illegal bid. Value too low treating as a pass')
                else:
                    passes_rcvd += 1
                #when more than 1 in the bidding rcvd must equal passes to win ... if only one player rcvd > needed means
                #the one player bidding passed.
                if (passes_rcvd == passes_to_win_bid and bid != 0) or (passes_rcvd > passes_to_win_bid) or \
                        ((offers_this_loop == len(bid_order_list)) and (bid == 0))    :
                    #set rcvd == to_win so the while loop will terminate.
                    passes_rcvd = passes_to_win_bid
                    break

        if bid != 0:
            #inform everyone else of the results
            msg = 'Info {} bought {} for {}'.format(bidding_character.name, card, bid)
            bidding_character.myGame.broadcast(msg, False, bidding_character.name)

            #add the card to the winning characters hand
            bidding_character.treachery_cards_add(card, detail)
            msg = 'treachery_card {} {} '.format(card, detail)

            #if the winning player is Harkonnen see if anyone wants to prevent him from getting an extra card
            if bidding_character.name == 'Harkonnen':
                block = thisGame.block_characters_advantage('Harkonnen', 'extra_card')
                if False == block:
                    cards_needed = bidding_character.treachery_cards_needed()  # helps determine if they are full
                    cards_per_deal = (bidding_character.treachery_cards_per_deal_get() - 1)  # minus 1 becaue they just won 1 card
                    while 0 != cards_needed and 0 != cards_per_deal:
                        card, details = thisGame.treachery.deal_card()
                        msg += '{} {} '.format(card, details)
                        cards_per_deal -= 1
                        cards_needed -= 1
                        bidding_character.treachery_cards_add(card, details)
            #send the cards to the winning bidder
            bidding_character.send(msg, False)

            cards_needed = bidding_character.treachery_cards_needed() #lets see if the winning player is not full
            if 0 == cards_needed:
                print('{} is full and being removed from the bidding sequence'.format(bidding_character.name))
                bid_order_list.pop(bidding_character.name)

        #update the bidding order list by popping the first one in the sequence and moving it to the back of the list. First
        #get the first player on the list if it equal the first_bidding_character variable pop the entry and place it last.
        try:
            character_name, this_character = next(iter(bid_order_list.items()))
            if character_name == first_bidder_name:
                bid_order_list.pop(character_name)
                bid_order_list[character_name] = this_character
        except StopIteration:
            pass

        if 0 != bid: #the card was bid on and bought
            #if bene is the winner and is using a Karama card to pay and it is a worthless card see if anyone wants to stop her
            if bidding_character.name == 'Bene_Gesserit' and True == paying_with_karama and \
                    thisGame.treachery.is_card_of_type('Worthless', paying_with_karama_card_name):
                block = thisGame.block_characters_advantage('Bene_Gesserit', 'using_worthless_card_as_karama')
                if True == block:
                    paying_with_karama = False

            if True == paying_with_karama: #the bidder is paying using a karama so simply discard the Karama card
                bidding_character.treachery_card_del(paying_with_karama_card_name)

            elif bidding_character.name != 'Emperor':
                bidding_character.spice_payment('del', bid)

                #if emperor is playing pay the man
                emperor = thisGame.is_character_playing('Emperor')
                if None != emperor  and bidding_character.name != 'Emperor':
                    emperor.spice_payment('add', bid)

    msg = 'treachery_card_bidding {} {} {} {}'.format('TreacheryBack', '', 0, '')
    thisGame.broadcast(msg, False, '')

    if None is not atreides:
        msg = 'clear_player_display'
        atreides.send(msg, False)
