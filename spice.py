import deck
import treachery
import time


spice_deck = { 'Broken_Land_12':8, 'Cielago_North_3':8,'Cielago_South_2':12,'Shai_Hulud_1':-1,'Funeral_Plain_15':6,'Habbanya_Erg_16':8, \
               'Habbanya_Ridge_Flat_18':10,'Shai_Hulud_2':-1,'Hagga_Basin_13':6,'OH_Gap_10':6,  'Shai_Hulud_3':-1,'Red_Chasm_7':8, \
               'Rock_Outcroppings_14':6,'Shai_Hulud_4':-1,'The_Great_Flat_15':10,'The_Minor_Erg_8':8,'Shai_Hulud_5':-1, \
               'Sihaya_Ridge_9':6,'South_Mesa_5':10,'Shai_Hulud_6':-1,'Wind_Pass_North_17':6,}

worm_cards = ['Shai_Hulud_1', 'Shai_Hulud_2' ,'Shai_Hulud_3' ,'Shai_Hulud_4' ,'Shai_Hulud_5' ,'Shai_Hulud_6']

class Spice(deck.Deck):
    def __init__(self, thisGame):
        self.myGame = thisGame
        super().__init__('Spice Deck', spice_deck)

        self.blow_number = 0 #during the blow round this variable determines which blow pile is being performed.
        self.consecutive_worms = 0
        self.blow_pile1 = dict()
        self.add_pile_to_cards_in_play(self.blow_pile1)
        self.blow_pile2 = dict()
        self.add_pile_to_cards_in_play(self.blow_pile2)
        self.next_blow = dict()
        self.add_pile_to_cards_in_play(self.next_blow)

    def __str__(self):
        ret_str = 'Spice Blow 1: {}   Spice blow_pile2: {}\n'.format(self.blow_pile1, self.blow_pile2)
        ret_str += super().__str__()
        return ret_str

    def is_card_a_worm(self, card):
        is_a_worm_card = False
        if card in worm_cards:
            is_a_worm_card = True
        return is_a_worm_card

    def blow(self):
        self.consecutive_worms = 0
        self.blow_number = 0
        if self.myGame.turn == 1:
            while self.blow_number < 2:
                territory_name, amount = self.deal_card()
                if amount == -1:
                    self.place_in_deck(territory_name, amount)
                else:
                    blow_to_territory(self, territory_name, amount)
        else:
            use_next_blow_pile = True
            while self.blow_number < 2:
                if True == use_next_blow_pile:
                    territory_name, amount = next(iter(self.next_blow.items()))
                    self.next_blow.pop(territory_name)
                else:
                    territory_name, amount = self.deal_card()

                if amount == -1:
                    self.consecutive_worms += 1
                    if 1 == self.consecutive_worms:
                        if self.blow_number == 0:
                            territory_name, amount = next(iter(self.blow_pile1.items()))
                        else:
                            territory_name, amount = next(iter(self.blow_pile2.items()))

                    is_fremen_reacting, next_territory = worm(self, territory_name, False)

                    while is_fremen_reacting == True:
                        is_fremen_reacting, next_territory = worm(self, next_territory, True)

                    if len(self.next_blow) != 0:
                        use_next_blow_pile = True
                    else:
                        use_next_blow_pile = False
                else:
                    blow_to_territory(self, territory_name, amount)
                    if len(self.next_blow) != 0:
                        use_next_blow_pile = True
                    else:
                        use_next_blow_pile = False

        territory_name, amount = self.deal_card()
        self.next_blow[territory_name] = amount
        territory_name, amount = self.deal_card()
        self.next_blow[territory_name] = amount

        atreides = self.myGame.is_character_playing('Atreides')
        if None != atreides:
            msg = 'spice_blow_next '
            for territory_name, amount in self.next_blow.items():
                msg += '{} {} '.format(territory_name, str(amount))
            atreides.send(msg, False)


def blow_to_territory(self, territory_name, amount):
    *args, = territory_name.split('_')
    #after the split the last args value will contain the sector # of the territory if == to turn don't blow the spice
    if self.myGame.sector_under_storm_get() == int(args[len(args) - 1]):
        amount = 0

    self.myGame.planet.spice_blow(territory_name, amount)

    if self.blow_number == 0:
        self.discard(self.blow_pile1, territory_name, amount)
    else:
        self.discard(self.blow_pile2, territory_name, amount)
    self.blow_number += 1
    self.consecutive_worms = 0

    msg = 'spice_blow {} {} {}'.format(territory_name, amount, self.blow_number)
    self.myGame.broadcast(msg, False, '')


def worm(self, territory, attack_by_fremen):
    fremen_is_reacting = False
    rsp_needed = False
    fremen_next_territory = ''

    msg = 'worm {} {}'.format(territory, int(self.consecutive_worms))
    #Broadcast to all. Ommiting the Fremen. A msg will be sent to Fremen if he is playing but we need a response him
    self.myGame.broadcast(msg, False, 'Fremen')

    #now let the worm do it's damage on the territory
    if False == self.is_card_a_worm(territory):
        self.myGame.planet.worm_attack(territory)

    #now see if Fremen is playing and how they would like to handle this worm
    fremen = self.myGame.is_character_playing('Fremen')
    if None != fremen:
        #if the fremen is occupying the territory or it is the 2nd or more worm we need Fremen to respond with an action
        if (True == fremen.is_occupying_territory(territory) or 1 < self.consecutive_worms) and attack_by_fremen == False:
            rsp_needed = True

        fremen.send(msg, rsp_needed)

        #FIXME can we use the treachery logic for waiting???
        if True == rsp_needed:
            while 0 == self.myGame.all_characters_ready():
                time.sleep(.5)
            if True == fremen.worm_request:
                fremen_is_reacting = True
                fremen_next_territory = fremen.worm_request_territory
                if 1 == self.consecutive_worms:
                    fremen.worm_flee(territory, fremen.worm_request_territory)
        fremen.worm_request = False

    return fremen_is_reacting, fremen_next_territory


