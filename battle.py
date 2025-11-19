
class Battle:
    def __init__(self, myGame):
        self.myGame = myGame
        self.battle_territory = ''

        self.aggressor = None
        self.aggressor_plan_requested = False
        self.aggressor_calls_treachery = False
        self.defender = None
        self.defender_plan_requested = False
        self.defender_calls_treachery = False

        self.fedaykins_at_full_power = True
        self.sardaukars_at_full_power = True
        self.kwisatz_haderach_blocked = False

        self.atreides_vision_request = '' #either general, bid, weapon, defense, or all
        self.benes_voice = '' # <must | cant> <offense | defense> <poison | projectile | lazegun>

    def battle_prep(self):
        self.__init__(self.myGame)

    def benes_voice_get(self):
        return self.benes_voice

    def battle_territory_get(self):
        return self.battle_territory

    def are_troops_full_strength(self, character):
        full_power = True
        if character == 'Emperor':
            full_power =  self.sardaukars_at_full_power
        elif character == 'Fremen':
            full_power =  self.fedaykins_at_full_power
        return full_power

    def battle_round(self):
        battle_participants = []
        # for each character in order of their turn generate a list of territories the character must battle in
        for key, this_character in self.myGame.character_turn_order.items():
            battle_list = []  # this will be a list of list bol = [[territory, who],[territory, who] ....]
            for territory_name, troops in this_character.troops.items():
                if territory_name != 'reserve' and territory_name != 'tank' and \
                        self.myGame.planet.get_number_of_occupants(territory_name) >= 2:
                    territory = self.myGame.planet.find_territory(territory_name)
                    my_troops = territory.get_troops_by_owner(this_character.name)
                    if False == my_troops.peaceful:
                        for who, opponent_troops in territory.occupied.items():
                            this_battle = [territory_name, who]
                            if who != this_character.name and opponent_troops.peaceful == False:
                                battle_list.append(this_battle)

            while 0 != len(battle_list):
                self.battle_prep()  # initialize the elements used to track the battle setup and resolution
                self.aggressor = this_character

                # build a message to query the character of whom they'd like to battle first. This is based on the content of the battle order list
                if len(battle_list) > 1:
                    msg = 'choose_next_battle '
                    for battle in battle_list:
                        msg += '{} {} '.format(battle[0], battle[1])
                    self.aggressor.send_query_and_wait(msg)
                else:
                    self.aggressor.current_battle = battle_list[0]

                self.battle_territory = self.aggressor.current_battle[0]
                who_is_being_attacked = self.aggressor.current_battle[1]
                self.defender = self.myGame.is_character_playing(who_is_being_attacked)
                battle_list.remove(self.aggressor.current_battle)

                msg = 'Info {} v {} in {}'.format(self.aggressor.name, self.defender.name, self.battle_territory)
                self.myGame.broadcast(msg, False, '')

                if self.aggressor.name == 'Emperor' or self.defender.name == 'Emperor':
                    block = self.myGame.block_characters_advantage('Emperor', 'Sedaurkars_half_strength')
                    if True == block:
                        self.sardaukars_at_full_power = False
                    else:
                        self.sardaukars_at_full_power = True

                if self.aggressor.name == 'Fremen' or self.defender.name == 'Fremen':
                    block = self.myGame.block_characters_advantage('Fremen', 'Fedaykins_half_strength')
                    if True == block:
                        self.fedaykins_at_full_power = False
                    else:
                        self.fedaykins_at_full_power = True

                bidding_only = can_cards_be_played(self)
                #if it is bidding only no need for Bene to user her voice ... atreides can still ask to see the bid amount
                if False == bidding_only:
                    if self.aggressor.name == 'Bene_Gesserit' or self.defender.name == 'Bene_Gesserit':
                        block = self.myGame.block_characters_advantage('Bene_Gesserit', 'stop_her_voice?')
                    if self.aggressor.name == 'Bene_Gesserit':
                        self.benes_voice = self.aggressor.pre_battle_setup(block)
                    elif self.defender.name == 'Bene_Gesserit':
                        self.benes_voice = self.defender.pre_battle_setup(block)

                else:
                    msg = 'Info 1 house has no general cannot play cards'
                    self.myGame.broadcast(msg, False, '')

                if self.aggressor.name == 'Atreides' or self.defender.name == 'Atreides':
                    block = self.myGame.block_characters_advantage('Atreides', 'block_his_vision?')
                    self.kwisatz_haderach_blocked = self.myGame.block_characters_advantage('Atreides', 'block_use_of_kwisatz_haderach?')

                if self.aggressor.name == 'Atreides':
                    self.atreides_vision_request = self.aggressor.pre_battle_setup(block)
                    # if no vision request atreides was blocked or he doesnt want to play a karama  so we'll query his opponent later
                    if self.atreides_vision_request != '':
                        self.send_battle_plan_request('defender', True)
                        self.send_atreides_his_vision()

                elif self.defender.name == 'Atreides':
                    self.atreides_vision_request = self.defender.pre_battle_setup(block)
                    # if no vision request atreides was blocked or he doesnt want to play a karama  so we'll query his opponent later
                    if self.atreides_vision_request != '':
                        self.send_battle_plan_request('aggressor', True)
                        self.send_atreides_his_vision()

                if False == self.aggressor_plan_requested:
                    self.send_battle_plan_request('aggressor', False)

                if False == self.defender_plan_requested:
                    self.send_battle_plan_request('defender', False)

                while False == self.myGame.all_characters_ready():
                    pass

                if self.aggressor not in battle_participants:
                    battle_participants.append(self.aggressor)
                if self.defender not in battle_participants:
                    battle_participants.append(self.defender)

                self.battle_resolution()

        print('number of battle participants {}'.format(len(battle_participants)))
        for this_character in battle_participants:
            this_character.clear_general_used_list()


    def send_battle_plan_request(self, aggressor_or_defender, wait_for_response):

        if 'Emperor' == self.aggressor.name or 'Emperor' == self.defender.name:
            tokens_full_strength = self.sardaukars_at_full_power
        elif 'Fremen' == self.aggressor.name or 'Fremen' == self.defender.name:
            tokens_full_strength = self.fedaykins_at_full_power
        else:
            tokens_full_strength = 'True'

        msg = 'submit_battle_plan_query {} {} {} benes_voice {} atreides_vision {} tokens_full_strength {} kwazi_headache_blocked {}'.format( \
                                                                                          self.battle_territory, \
                                                                                          self.aggressor.name, \
                                                                                          self.defender.name, \
                                                                                          self.benes_voice, \
                                                                                          self.atreides_vision_request,
                                                                                          tokens_full_strength,
                                                                                          self.kwisatz_haderach_blocked)

        if True == wait_for_response:
            if aggressor_or_defender == 'aggressor':
                self.aggressor.send_query_and_wait(msg)
                self.aggressor_plan_requested = True
            else:
                self.defender.send_query_and_wait(msg)
                self.defender_plan_requested = True

        else:
            if aggressor_or_defender == 'aggressor':
                self.aggressor.send(msg, True) #we still want a response we just won't wait for it here
                self.aggressor_plan_requested = True
            else:
                self.defender.send(msg, True) #we still want a response we just won't wait for it here
                self.defender_plan_requested = True

    def send_atreides_his_vision(self):
        if self.aggressor.name == 'Atreides':
            atreides = self.aggressor
            opponent = self.defender
        else:
            atreides = self.defender
            opponent = self.aggressor

        if self.atreides_vision_request == 'Karama_1' or self.atreides_vision_request == 'Karama_2':
            atreides.treachery_card_del(self.atreides_vision_request)
            atreides_requested_entire_plan = True
        else:
            atreides_requested_entire_plan = False

        msg = 'atreides_vision '
        if self.atreides_vision_request == 'general' or atreides_requested_entire_plan == True:
            general, value = opponent.battle_plan.general_get()
            msg += '{}:{} '.format(general, value)
        if self.atreides_vision_request == 'bid' or atreides_requested_entire_plan == True:
            bid = opponent.battle_plan.troops_bid_get()
            msg += 'bid:{} '.format(bid)
        if self.atreides_vision_request == 'offense' or atreides_requested_entire_plan == True:
            card, details = opponent.battle_plan.weapon_get()
            msg += 'O:{} '.format(details)
        if self.atreides_vision_request == 'defense' or atreides_requested_entire_plan == True:
            card, details = opponent.battle_plan.defense_get()
            msg += 'D:{} '.format(details)

        atreides.send(msg, False) #send atredies his vision so we can send him his battle plan request

    def battle_resolution(self):
        print('FIXME time to see who won the battle\n')
        msg = 'battle'
        msg += ' {} {} {} {} {} {}'.format(self.aggressor.name, self.aggressor.battle_plan.general[0], \
                                        self.aggressor.battle_plan.weapon[0], self.aggressor.battle_plan.defense[0],\
                                        self.aggressor.battle_plan.troops_bid, self.aggressor.battle_plan.spice_for_troops_bid)

        msg += ' {} {} {} {} {} {}'.format(self.defender.name, self.defender.battle_plan.general[0], \
                                        self.defender.battle_plan.weapon[0], self.defender.battle_plan.defense[0],\
                                        self.defender.battle_plan.troops_bid, self.defender.battle_plan.spice_for_troops_bid)
        self.myGame.broadcast(msg, False, '')

        if (self.aggressor.battle_plan.weapon_type_get() == 'Lasegun' or self.defender.battle_plan.weapon_type_get() == 'Lasegun') and \
           (self.aggressor.battle_plan.defense_type_get() == 'Projectile' or self.defender.battle_plan.defense_type_get() == 'Projectile'):

            msg = 'battle_results kaboom nonone 0 0'
            self.myGame.broadcast(msg, False, '')

            self.aggressor.battle_lost(self.battle_territory, True)
            self.defender.battle_lost(self.battle_territory, True)

            #there is collateral damage all spice and any troops in the territory are destroyed as well
            spice = self.myGame.planet.spice_avaliable_get(self.battle_territory)
            self.myGame.planet.spice_harvest(self.battle_territory, spice)
            msg = 'spice_remove {} {}'.format(self.battle_territory, spice)
            self.myGame.broadcast(msg, False, '') #Irm all clients to remove the spice from this nuked territory

            territory = self.myGame.planet.find_territory(self.battle_territory)
            for owner, troops in territory.occupied.items():
                self.myGame.kill_troops_in_territory(self.battle_territory, owner)

        else:
            aggressors_total = self.aggressor.battle_plan.troops_bid_get()
            defenders_total = self.defender.battle_plan.troops_bid_get()

            is_general_dead, defender_general, defender_value = self.is_general_killed(self.aggressor, self.defender)
            if False == is_general_dead:
                defenders_total += defender_value

            is_general_dead, aggressor_general, aggressor_value = self.is_general_killed(self.defender, self.aggressor)
            if False == is_general_dead:
                aggressors_total += aggressor_value

            self.defender_calls_treachery = self.defender.want_to_call_treachery(self.aggressor, aggressor_general)
            self.aggressor_calls_treachery = self.aggressor.want_to_call_treachery(self.defender, defender_general)

            if True == self.defender_calls_treachery and True == self.aggressor_calls_treachery:
                msg = 'battle_results treachery_double none {} {}'.format(aggressors_total, defenders_total)
                self.myGame.broadcast(msg, False, '')
                self.aggressor.battle_lost(self.battle_territory, True)
                self.defender.battle_lost(self.battle_territory, True)
            elif True == self.defender_calls_treachery:
                msg = 'battle_results treachery {} {} {}'.format(self.defender.name, defenders_total, aggressors_total)
                self.myGame.broadcast(msg, False, '')
                self.aggressor.battle_lost(self.battle_territory, True)
                self.defender.battle_won(self.battle_territory, aggressor_value, False, self.aggressor, True)
            elif True == self.aggressor_calls_treachery:
                msg = 'battle_results treachery {} {} {}'.format(self.aggressor.name, aggressors_total, defenders_total)
                self.myGame.broadcast(msg, False, '')
                self.defender.battle_lost(self.battle_territory, True)
                self.aggressor.battle_won(self.battle_territory, defender_value, False, self.defender, True)
            elif aggressors_total >= defenders_total:
                msg = 'battle_results battle {} {} {}'.format(self.aggressor.name, aggressors_total, defenders_total)
                self.myGame.broadcast(msg, False, '')
                self.settle_battle_results(self.aggressor, self.defender, self.battle_territory)
            else:
                msg = 'battle_results battle {} {} {}'.format(self.defender.name, defenders_total, aggressors_total)
                self.myGame.broadcast(msg, False, '')
                self.settle_battle_results(self.defender, self.aggressor, self.battle_territory)
        msg = 'clear_player_display'
        self.myGame.broadcast(msg, False, '')

    def settle_battle_results(self, winner, loser, battle_territory):
        winners_purse = 0
        # clean up the loser's Info.
        is_general_dead, general, value = self.is_general_killed(winner, loser)
        if True == is_general_dead:
            winners_purse += value

        loser.battle_lost(battle_territory, is_general_dead)

        # winner gets his generals value in spice if killed
        is_general_dead, general, value = self.is_general_killed(loser, winner)
        if True == is_general_dead:
            winners_purse += value

        winner.battle_won(battle_territory, winners_purse, is_general_dead, loser, False)

    def is_general_killed(self, attacker, victim):
        aW, aWT = attacker.battle_plan.weapon_get()  # W=weapon WT = weaponType
        vG, vGV = victim.battle_plan.general_get()
        vD, vDT = victim.battle_plan.defense_get()

        if vDT != aWT and aW != 'none' and False == self.myGame.treachery.is_card_of_type('Worthless', aW):
            general_killed = True
        else:
            general_killed = False
        return general_killed, vG, vGV

class BattlePlan :
    def __init__(self):
        self.general = [] # simple list [[general:value]] general could be 'none' or 'cheap_hero' as well
        self.troops_bid = 0 #amount of troops tokens + fedaykins bid
        self.weapon = [] #simple list[card_name, detail] can be 'worthless' card as well
        self.defense = [] #simple list [card_name, detail] can be 'worthless' card as well
        self.spice_for_troops_bid = 0

    def __str__(self):
        ret_str = '   General: {0[0]} value: {0[1]}\n'.format(self.general_get())
        ret_str += '   Troops Bid: {}\n'.format(self.troops_bid_get())
        ret_str += '   Weapon: {0[0]} type: {0[1]}\n'.format(self.weapon_get())
        ret_str += '   Defense: {0[0]} type: {0[1]}\n'.format(self.defense_get())
        ret_str += '   Spice Payment: {}\n'.format(self.spice_payment_get())
        return ret_str

    def plan_reset(self):
        self.__init__()

    def spice_payment_set(self, spice):
        self.spice_for_troops_bid = spice

    def spice_payment_get(self):
        return self.spice_for_troops_bid

    def troops_bid_set(self, num_of_troops):
        self.troops_bid = num_of_troops

    def troops_bid_get(self):
        return self.troops_bid

    def general_set(self, general_name, value):
        self.general = [general_name, value]

    def general_get(self):
        if 0 != len(self.general):
            return self.general[0], self.general[1]
        else:
            return 'none', 'none'

    def generals_value_get(self):
        if 0 == len(self.general):
            return 'none'
        else:
            return self.general[1]

    def apply_kwisatz_haderach(self):
        self.general[1] += 2

    def weapon_set(self, card, detail):
        self.weapon = [card, detail]

    def weapon_get(self):
        if 0 != len(self.weapon):
            return self.weapon[0], self.weapon[1]
        else:
            return 'none', 'none'

    def weapon_type_get(self):
        if 0 != len(self.weapon):
            return self.weapon[1]
        else:
            return 'none'

    def defense_set(self, card, detail):
        self.defense = [card, detail]

    def defense_get(self):
        if 0 != len(self.defense):
            return self.defense[0], self.defense[1]
        else:
            return 'none', 'none'

    def defense_type_get(self):
        if 0 != len(self.defense):
            return self.defense[1]
        else:
            return 'none'


def can_cards_be_played(battle):
    bidding_only = False

    num_unavailable_generals = len(battle.aggressor.dead_generals) + len(battle.aggressor.used_generals) + len(battle.aggressor.captured_generals)
    if num_unavailable_generals == len(battle.aggressor.generals) and False == battle.aggressor.is_card_of_type_available('Cheap_Hero'):
        bidding_only = True

    num_unavailable_generals = len(battle.defender.dead_generals) + len(battle.defender.used_generals) + len(battle.defender.captured_generals)
    if num_unavailable_generals == len(battle.defender.generals) and False == battle.defender.is_card_of_type_available('Cheap_Hero'):
        bidding_only = True

    return bidding_only

