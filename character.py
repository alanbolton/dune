from enum import Enum
import colors
import dune_gui as Gui
import battle as Battle
import generals as Generals
import planetDune as map
import planet
import random
import troops
import time


class CharacterState(Enum):
    IDLE = 0
    READY = 1
    JOIN = 2
    ACTION_NEEDED = 3


class Character :
    def __init__(self, name, myGame, player_name, player_dot, connection):
        self.name = name
        self.state = CharacterState.ACTION_NEEDED

        self.myGame = myGame #this is the game object we are associated with

        self.player_name = player_name
        self.player_dot_sector = player_dot
        self.client_socket = connection

        self.revival_rate = 1
        self.spice = 0
        self.movement = 1
        self.max_num_of_treachery_cards = 4
        self.treachery_cards = dict()
        self.myGame.treachery.add_pile_to_cards_in_play(self.treachery_cards) #this is needed when a treachery shuffle is needed

        self.battle_plan = Battle.BattlePlan()
        self.current_battle = []
        self.used_generals = dict()
        self.dead_generals = dict()
        self.captured_generals = dict() #general:characterObj For Hark this is a list of all generals he's captured everyone else is the generasl captured by Hark
        self.spies_delt = dict()
        self.spy = dict()
        self.troops = dict() #territory_name:troops object
        self.troops['reserve'] = troops.Troops(0, self.name, 20, 0)
        self.troops['tank'] = troops.Troops(0, self.name, 0, 0)

    def __str__(self):
        ret_str = '{} ({} playerDot: {} ) connection: {} \n'.format(self.name, self.player_name, self.player_dot_sector, self.client_socket)
        ret_str += '   {} {} spice: {} movement: {} revivalRate: {} \n'.format(self.name, self.state, self.spice, self.movement,  self.revival_rate)
        ret_str += '      Treachery Cards:\n'
        for key, value in self.treachery_cards.items():
            ret_str += '         {} {} \n'.format(key, value)
        ret_str += '      Generals:\n'
        for key, value in self.generals.items():
            ret_str += '         {} {} \n'.format(key, value)
        ret_str += '      Dead Generals:\n'
        for value in self.dead_generals:
            ret_str += '         {}\n'.format(value)
        ret_str += '      Captured Generals:\n'
        for value in self.captured_generals:
            ret_str += '         {}\n'.format(value)
        ret_str += '      Used Generals:\n'
        for value in self.used_generals:
            ret_str += '         {}\n'.format(value)
        ret_str += '      Troop Location: \n'
        for key, value in self.troops.items():
            ret_str += '         {} {}'.format(key, value)
        ret_str += '      Spy:\n'
        for key, value in self.spy.items():
            ret_str += '         {} {} \n'.format(key, value)
        ret_str += '      Safe Generals:\n'
        for key, value in self.spies_delt.items():
            ret_str += '         {} {} \n'.format(key, value)
        return ret_str

    def initial_display(self):
        x = 1
        for general in self.generals:
            self.myGame.gui.player.general_place(self.name, general, x)
            x += 1
        self.myGame.gui.player.spice_amount_update(self.spice)
        self.myGame.gui.player.tokens_update(self.name, self.troops['reserve'].tokens)

    def reserve_troops_gui_update(self):
        self.myGame.gui.player.tokens_update(self.name, self.troops['reserve'].tokens)

    def allocate_troops_from_reserves(self, tokens, fedaykins):
        if self.troops['reserve'].tokens >= tokens and self.troops['reserve'].fedaykins >= fedaykins:
            self.troops['reserve'].tokens -= tokens
            self.troops['reserve'].fedaykins -= fedaykins

    def place(self, territory_name, tokens, fedaykins):
        if territory_name != '':
            self.beam(self.myGame.turn, territory_name, self.name, tokens, fedaykins, 0)
        self.state = CharacterState.READY

    def ask_yes_no(self, name, action):
        msg = 'yes_no_query {} {} '.format(name, action)
        answer = self.send_query_and_wait(msg)
        return answer

    def pre_battle_setup(self, blocked):
        return ''  #this should never be called but return an empty string for consistency

    def battle_plan_set(self, general, bid, offense, defense, spice_allocated, kwisatz_haderach_played):
        valid_plan = True
        self.battle_plan.plan_reset()
        if general not in self.dead_generals and general not in self.used_generals and general in self.generals:
            value = self.generals_value_get(general)
            self.battle_plan.general_set(general, value)

            msg = 'general_used {}'.format(general)
            self.client_send(msg)

        elif general not in self.generals and general in self.captured_generals:
            owner = self.captured_generals.get(general, 0)
            value = owner.generals_value_get(general)
            self.battle_plan.general_set(general, value)
        elif True == self.myGame.treachery.is_card_of_type('Cheap_Hero', general) or 'none' == general:
            self.battle_plan.general_set(general, 0)
        else:
            valid_plan = False

        if spice_allocated > self.spice:
            valid_plan = False
        else:
            territory_name = self.myGame.battle_mgmt.battle_territory_get()
            my_troops = self.myGame.planet.troops_get(territory_name, self.name)
            if True == self.myGame.battle_mgmt.are_troops_full_strength(self.name):
                max_bid = (my_troops.tokens + (my_troops.fedaykins * 2))
            else:
                max_bid = (my_troops.tokens + (my_troops.fedaykins))
            if spice_allocated == 0:
                max_bid = max_bid/2 #can only bid at half strength
            elif spice_allocated < max_bid:
                max_bid = spice_allocated + ((max_bid - spice_allocated)/2)
            if bid > max_bid:
                valid_plan = False
            else:
                self.battle_plan.troops_bid_set(bid)

        if general != 'none':  # cards can only be played if a general or cheap hero are being played
            if self.myGame.treachery.is_card_of_type('Weapons', offense) or \
               self.myGame.treachery.is_card_of_type('Worthless', offense) or \
               offense == 'none':
                card_details = self.treachery_cards.get(offense, 0)
                self.battle_plan.weapon_set(offense, card_details)
            else:
                valid_plan = False

            if self.myGame.treachery.is_card_of_type('Defense', defense) or \
               self.myGame.treachery.is_card_of_type('Worthless', defense) or \
               defense == 'none':
                card_details = self.treachery_cards.get(defense, 0)
                self.battle_plan.defense_set(defense, card_details)
            else:
                valid_plan = False
        self.battle_plan.spice_payment_set(spice_allocated)
        return valid_plan

    def battle_won(self, battle_territory, spice_won, was_general_killed, opponent, won_by_treachery):
        general, value  = self.battle_plan.general_get()
        if general != 'none' and False == self.myGame.treachery.is_card_of_type('Cheap_Hero', general) and  \
           general in self.generals.keys():
            if True == was_general_killed:
                self.general_killed(general)
            else:
                self.general_used(general)

        if False == won_by_treachery: #if treachery is called the player looses no tokens or pays any spice
            troops = self.myGame.planet.troops_get(battle_territory, self.name)

            # adjust tokens used
            troops_bid = self.battle_plan.troops_bid_get()
            spice_spent = self.battle_plan.spice_payment_get() #need this to determine  how many are at full strength
            #now determine the actual number of Troops needed to settle the battle spice paid troops at 1 all other count .5
            troops_bid = ((troops_bid - spice_spent) * 2) + spice_spent
            if troops_bid % 1 != 0:
                troops_bid = int(troops_bid) + 1

            # no fedaykins involved no need to query player or if the bid is only 1 and there are "tokens" avaliable take the token
            if troops.fedaykins == 0 or (troops_bid == 1 and troops.tokens != 0):
                tokens = troops_bid
                fedaykins = 0
            #if no tokens are available everything needs taken from Fedaykins
            elif troops.fedaykins != 0 and troops.tokens == 0:
                tokens = 0
                fedaykins = troops_bid/2
                if fedaykins % 1 != 0:
                    fedaykins = int(fedaykins) + 1
            else:
                #let the player either limit the number of fedaykins lost to a specified value or
                limit_fedaykins = self.ask_yes_no(self.name, 'limit_fedaykins_lost')
                if True == limit_fedaykins:
                    fedaykins = self.myGame.value_rcvd
                    while (troops_bid - (fedaykins * 2)) > troops.tokens:
                        fedaykins += 1
                else:
                    fedaykins = troops.fedaykins
                if (fedaykins * 2) > troops_bid:
                    fedaykins = int(troops_bid/2)

                tokens = troops_bid - (fedaykins * 2)

            self.myGame.kill_some_troops_in_territory(battle_territory, troops, tokens, fedaykins)

            if spice_won >= spice_spent:
                spice_won -= spice_spent
                collect_or_spend = 'add'
            else:
                spice_won = spice_spent - spice_won
                collect_or_spend = 'del'
            if 0 != spice_won:
                self.spice_payment(collect_or_spend, spice_won)

        self.treachery_discard_query()

    def battle_lost(self, territory_name, was_general_killed):
        card_list = []

        self.spice_payment('del', self.battle_plan.spice_payment_get())

        general, value = self.battle_plan.general_get()
        cheap_hero_played = self.myGame.treachery.is_card_of_type('Cheap_Hero', general)
        if True == cheap_hero_played:  # it needs to be discarded
            card_list.append(general)
        elif True == was_general_killed and general != 'none' and general in self.generals.keys():
            self.general_killed(general)
        elif general != 'none':
            self.general_used(general)

        key, value = self.battle_plan.defense_get()
        if key != 'none':
            card_list.append(key)
        key, value = self.battle_plan.weapon_get()
        if key != 'none':
            card_list.append(key)

        self.myGame.kill_troops_in_territory(territory_name, self.name)
        self.treachery_card_del_multiple(*card_list)

    def beam(self, round, territory_name, owner, tokens, fedaykins, cost):
        if self.spice >= cost:
            if territory_name in self.troops:
                if True == self.myGame.planet.does_character_occupy(territory_name, owner):
                    self.allocate_troops_from_reserves(tokens, fedaykins)
                    self.myGame.planet_ship_reinforcements(territory_name, self.name, tokens, fedaykins)
            else:
                landing_party = troops.beam_troops(self.troops['reserve'], round, owner, tokens, fedaykins)
                self.troops[territory_name] = landing_party
                self.myGame.planet_shipment_local(territory_name, landing_party)

            msg = 'beam {} {} {} {} {} {}'.format(self.myGame.turn, territory_name, owner, tokens, fedaykins, cost)
            self.client_send(msg)
            self.spice -= cost

            self.reserve_troops_gui_update()
            self.myGame.gui.player.spice_amount_update(self.spice)

        else:
            print('Error player can not afford shipment send error to client')

    def beam_query(self):
        processed = False

        while False == processed:
            processed, beam_requested = Gui.dune_gui_place_or_beam_reqeust(self.myGame, 'beam_request',\
                                                                           self.troops['reserve'].tokens,\
                                                                           self.troops['reserve'].fedaykins)

            if True == beam_requested and self.is_card_of_type_available('Karama'):
                play_karama, karama_card = Gui.dune_gui_play_karama(self.myGame, self, 'Select Karama to ship at Guild Rate')
                if True == play_karama:
                    self.myGame.gui.map.event.msg_add_to(karama_card)

            if True == processed:
                self.send(self.myGame.gui.map.event.msg, False)
                self.myGame.gui.player.clear()

    def move_query(self):
        processed = False
        while False == processed:

            processed = Gui.dune_gui_move_between_territories(self.myGame, 'move_request', self.name)
            if True == processed:
                self.send(self.myGame.gui.map.event.msg, False)
                self.myGame.gui.player.clear()

    def move_to_planet(self, territory_name, tokens, fedaykins, using_karama):
        if False == self.myGame.planet.is_territory_under_storm(territory_name) or \
           False == self.myGame.planet.can_troops_enter(territory_name, self.name):
            bene = self.myGame.is_character_playing('Bene_Gesserit')  # we need to know if bene is playing to query on peacefulness or piggybacking
            territory = self.myGame.planet.find_territory(territory_name)
            beam_cost = territory.beam_cost_get()
            shipment_cost = beam_cost * (tokens + fedaykins)

            if 'no' != using_karama:
                shipment_cost = int((shipment_cost + 1)/2) #paying at Guild Rate add 1 so cost is rounded up if a half
                self.treachery_card_del(using_karama)

            if 'Guild' == self.name:
                shipment_cost = int((shipment_cost + 1)/2)

            if self.spice >= shipment_cost:
                # self.name == 'Bene_Gesserit':
                    # yes = self.ask_yes_no(territory_name, 'piggy_backing')
                    # if True == yes:
                    #     tokens += 1 #increase as Bene is piggybacking 1 token with her shipment

                self.beam(self.myGame.turn, territory_name, self.name, tokens, fedaykins, shipment_cost)

                # if bene is not None and self.name != 'Bene_Gesserit': #only ask bene the following if she is NOT the one making the move
                #     block = self.myGame.block_characters_advantage('Bene_Gesserit', 'block_piggybacking')
                #     if False == block:
                #         yes = bene.ask_yes_no(territory_name, 'piggy_backing?')
                #         if True == yes:
                #             bene.beam(self.myGame.turn, territory_name, bene.name, 1, 0, 0)
                #
                if bene is not None and self.myGame.planet.does_character_occupy(territory_name, 'Bene_Gesserit'):
                    bene.query_peacefulness_if_necessary(bene.myGame, territory_name)

                guild = self.myGame.is_character_playing('Guild')
                #only pay the guild if he is playing and its not him making shipments
                if None != guild and 'no' == using_karama and 'Guild' != self.name:
                    guild.spice_payment('add', shipment_cost)
            self.ready()  # it is a valid move so mark character as ready incase we need to ask a follow up question
        else:
            msg = 'beam_query'
            self.send(msg, False)

    def on_planet_move(self, start, end, tokens, fedaykins):
        move_allowed = False
        end_troops = None
        if start in self.troops:
            max_distance = self.movement
            if self.ornothopters_available():
                max_distance = 3

            print('max distance is {}'.format(max_distance))
            move_allowed = self.myGame.planet.validate_on_planet_move(start, end, max_distance, self.name)
            if True == move_allowed:
                self.myGame.planet.movment_between_two_territories(self, start, end, tokens, fedaykins)

                bene = self.myGame.is_character_playing('Bene_Gesserit')  # we need to know if bene is playing to query on peacefulness
                if bene is not None and self.myGame.planet.does_character_occupy(end, 'Bene_Gesserit'):
                    bene.query_peacefulness_if_necessary(bene.myGame, end)

                self.ready()
        else:
            print('Error {} is trying to move tokens from {} which they do not occupy'.format(self.name, start))

        return move_allowed

    def territory_troop_consolidation(self):
        territory_list = []
        for territory_name in self.troops.keys():
            if territory_name != 'reserve' and territory_name != 'tank':
                territory = self.myGame.planet.find_territory(territory_name)
                territory.dirty_set(False)
                territory_list.append(territory_name)

        storm_sector = self.myGame.sector_under_storm_get()

        for territory_name in territory_list:
            if territory_name in self.troops:
                merge_candidates = []
                territory = self.myGame.planet.find_territory(territory_name)
                if False == territory.is_territory_dirty():
                    merge_candidates.append(territory_name)
                    territory.dirty_set(True)
                    alias_list = map.territories_aliases_get(territory_name)
                    for alias in alias_list:
                        if alias in self.troops and alias != territory_name:
                            merge_candidates.append(alias)
                            alias_territory = self.myGame.planet.find_territory(alias)
                            alias_territory.dirty_set(True)

                    consolidate = False
                    if len(merge_candidates) > 1:
                        consolidate = self.ask_yes_no(territory_name, 'consolidate_troops')

                    if True == consolidate:
                        final_territory = self.myGame.string_rcvd
                        for candidate in merge_candidates:
                            if candidate != final_territory:
                                move_allowed = self.myGame.planet.validate_on_planet_move(candidate, final_territory, 1, self.name)
                                if True == move_allowed:
                                    troops = self.myGame.planet.troops_get(candidate, self.name)
                                    self.myGame.planet.movment_between_two_territories(self, candidate, final_territory, troops.tokens, troops.fedaykins)

                                    msg = 'move_request {} {} {} {}'.format(candidate, final_territory, troops.tokens, troops.fedaykins)
                                    self.client_send(msg)

                                    self.myGame.planet.announce_character_movement(self.name, candidate, final_territory)


    def setup_request(self, cmd):
        request = '{} '.format(cmd)
        self.send(request, True)

    def ready(self):
        self.state = CharacterState.READY

    def next_storm_movement_set(self, distance):
        #only the Fremen acts on this everyone else ignores the announcement
        pass

    def revival(self, number):
        revival_count = 0

        if 0 == number:
            x = self.revival_rate
        else:
            x = number

        while x and  self.troops['tank'].fedaykins != 0:
            self.troops['reserve'].fedaykins += 1
            self.troops['tank'].fedaykins -= 1
            x -= 1
            revival_count += 1
            if 0 == number: #if number == 0 this is free revival and we are limited to one fedaykin during free revival
                break

        while x and self.troops['tank'].tokens != 0:
            self.troops['reserve'].tokens += 1
            self.troops['tank'].tokens -= 1
            x -= 1
            revival_count += 1

        if 0 != revival_count:
            msg = 'revival {}'.format(number)
            self.client_send(msg)

        self.reserve_troops_gui_update()

    def revive_additional_tokens_or_generals(self):
        num_to_revive = 0
        if self.troops['tank'].tokens != 0 or self.troops['tank'].fedaykins != 0:
            character_response = self.ask_yes_no(self.name, 'revive_additional_tokens')
            if True == character_response:
                num_to_revive = self.myGame.value_rcvd
                if num_to_revive > 3 - self.revival_rate:
                    num_to_revive = 3 - self.revival_rate
                    msg = 'Info revival request too high limited to {}'.format(num_to_revive)
                    self.send(msg, False)
                if self.spice < (num_to_revive * 2):   #it cost 2 spice per token to revirve
                    num_to_revive = int(self.spice/2)
                    msg = 'Info not enough spcie request limited to {}'.format(num_to_revive)
                    self.send(msg, False)

                self.revival(num_to_revive)
                self.spice_payment('del', (num_to_revive * 2))

        if len(self.dead_generals) != 0:
            general = next(iter(self.dead_generals.keys()))
            value = self.generals_value_get(general)
            if self.spice >= value:
                character_response = self.ask_yes_no('self', 'revive_dead_general')
                if True == character_response:
                        self.general_revived(general)
                        self.spice_payment('del', value)
            else:
                msg = 'Info general revival needs {} spice'.format(value)
                self.send(msg, False)

    def chaom(self):
        if 0 == self.spice:
            self.spice_payment('add', 2)

    def collection(self):
        collection_list = set()
        collection_amount = 0
        if 'Arrakeen_10' in self.troops:
            if False == self.troops['Arrakeen_10'].peaceful:
                collection_amount += 2
        if 'Carthag_11' in self.troops:
            if False == self.troops['Carthag_11'].peaceful:
                collection_amount += 2
        if 'Tueks_Sietch_5' in self.troops:
            if False == self.troops['Tueks_Sietch_5'].peaceful:
                collection_amount += 1

        if self.ornothopters_available():
            spice_per_token = 3
        else:
            spice_per_token = 2

        for territory_name in self.myGame.planet.territories_with_spice:
            collection_list.add(territory_name)

        for territory_name in collection_list:
            if territory_name in self.troops:
                myTroops = self.troops[territory_name]
                max_amount = spice_per_token * (myTroops.tokens + myTroops.fedaykins)
                this_amount = self.myGame.planet.spice_harvest(territory_name, max_amount)
                collection_amount += this_amount
                #inform all clients that spice is being removed from a territory
                msg = 'spice_remove {} {}'.format(territory_name, this_amount)
                self.myGame.broadcast(msg, False, '')

        self.spice += collection_amount
        if 0 != collection_amount:
            self.spice_payment('add', collection_amount)

    def spy_dealt(self, general, value):
        house = Generals.get_house_by_general(general)
        house_exist = self.myGame.does_house_exist(house)
        if house_exist is True:
            self.spies_delt[general] = value
            self.myGame.gui.player.spy_suspects_place(general, len(self.spies_delt), 1045, 435)

    def spy_select(self, general):
        x = 1
        for suspect in self.spies_delt:
            if suspect == general and (general not in self.generals):
                self.myGame.gui.player.spy_declare(x)
            x += 1

        if general != 'none' and general != '' and (general not in self.generals):
            value = self.spies_delt.pop(general)
            self.spy[general] = value
            self.state = CharacterState.READY

        elif general == 'none':
            self.state = CharacterState.READY

    def spy_choice(self):
        count = 0
        for suspect in self.spies_delt:
            if suspect in self.generals:
                count += 1

        if count == len(self.spies_delt) or 0 == len(self.spies_delt):
            msg = 'spy_select none'
            self.send(msg, False)
        elif (len(self.spies_delt) - count) == 1:
            for suspect in self.spies_delt:
                if suspect not in self.generals:
                    msg = 'spy_select {}'.format(suspect)
                    self.send(msg, False)
        else:
            suspect_list = []
            for suspect in self.spies_delt.keys():
                if suspect not in self.generals:
                    suspect_list.append(suspect)
            Gui.dune_gui_spy_selection(self.myGame, suspect_list)

    def want_to_call_treachery(self, opponent, general):
        calling_treachery = False
        if general in self.spy or general in opponent.captured_generals:
            calling_treachery = self.ask_yes_no(general, 'call_treachery')
        return calling_treachery

    def generals_available_for_battle(self):
        general_list = {}
        for general, value in self.generals.items():
            if general not in self.dead_generals and general not in self.used_generals and general not in self.captured_generals:
                general_list[general] = value

        if True == self.is_card_of_type_available('Cheap_Hero'):
            card = self.get_first_card_of_type('Cheap_Hero')
            general_list[card] = 0

        return general_list

    def general_used(self, who):
        position = 1
        for general in self.generals.keys():
            print('Used who {} thisGeneral {}'.format(who, general))
            if who == general:
                self.myGame.gui.player.general_attriute_add('Used', colors.VIOLET, position)
                self.used_generals[who] = position
            position += 1

        msg = 'general_used {}'.format(who)
        self.client_send(msg)

    def general_remove_from_used_list(self, who):
        position = self.used_generals.pop(who)
        self.myGame.gui.player.general_place(self.name, who, position)

    def clear_general_used_list(self):
        for general, position in self.used_generals.items():
            self.myGame.gui.player.general_place(self.name, general, position)

        self.used_generals = dict()
        msg = 'generals_used_clear'
        self.client_send(msg)

    def general_killed(self, who):
        if who in self.used_generals:
            self.used_generals.pop(who)

        position = 1
        for general in self.generals.keys():
            print('killed who {} thisGeneral {}'.format(who, general))
            if who == general:
                self.myGame.gui.player.general_place(self.name, who, position)
                self.myGame.gui.player.general_attriute_add('DEAD', colors.RED, position)
                self.dead_generals[who] = position
            position += 1

        msg = 'general_killed {}'.format(who)
        self.client_send(msg)

    def general_captured(self, name, who):
        position = 1
        for general in self.generals.keys():
            print('captured who {} thisGeneral {}'.format(name, general))
            if name == general:
                self.myGame.gui.player.general_place(self.name, name, position)
                self.myGame.gui.player.general_attriute_add('Captured', colors.PINK, position)
                self.captured_generals[name] = who
            position += 1

        if self.myGame.is_server == True: #on the server "who" is a character object on a client it is the character's_name
            msg = 'general_captured {} {}'.format(name, who.name)
            self.client_send(msg)

    def general_freed(self, who):
        position = 1
        for general in self.generals.keys():
            if who == general:
                self.myGame.gui.player.general_place(self.name, who, position)
                self.captured_generals.pop(who)
            position += 1

        msg = 'general_freed {}'.format(who)
        self.client_send(msg)

    def general_revived(self, who):
        position = self.dead_generals.pop(who)
        self.myGame.gui.player.general_place(self.name, who, position)

        msg = 'general_revived {}'.format(who)
        self.client_send(msg)

    def generals_value_get(self, who):
        return self.generals[who]

    def spice_payment(self, transaction_type, amount):
        if 'add' == transaction_type:
            self.spice += amount
        else:
            self.spice -= amount
        msg = 'spice_payment {} {}'.format(transaction_type, amount)
        self.client_send(msg)

    def worm_announcement(self, territory, attack_number):
        print('Info WORM is ATTACKING {}\n'.format(str(territory)))
        if attack_number == 1:
            print('Info if Fremen is in this territory they can ride the WORM to another territory')
        else:
            print('Info if Fremen is playing they can send this WORM to attack another territory ... Is he Comming for you?')

    def worm_flee(self, old_territory, new_territory):
        old_troops = self.myGame.planet.troops_get(old_territory, 'Fremen')
        if None == old_troops:
            print('FIXME something is fucked up ... could not find Fremen Troops in territory {}'.format(old_territory))
        if self.myGame.planet.does_character_occupy(new_territory, 'Fremen'):
            new_troops = self.myGame.planet.troops_get(new_territory, 'Fremen')
            new_troops.tokens += old_troops.tokens
            new_troops.fedaykins += old_troops.fedaykins
            self.myGame.planet.troops_remove(old_territory, old_troops.owner)
            update = True
        else:
            self.myGame.planet.troops_remove(old_territory, old_troops.owner)
            self.myGame.planet.troops_enter(new_territory, old_troops)
            update = False

        return update

    def ornothopters_available(self):
        available = False
        for territory_name, my_troops in self.troops.items():
            print('{} placed {} this round{}'.format(territory_name, my_troops.round_placed, self.myGame.turn))
            if territory_name == "Carthag_11" or territory_name == 'Arrakeen_10':
                if my_troops.round_placed < self.myGame.turn:
                    available = True
        return available

    def worm_response(self, territory):
        print('FIXME The wrong character {} is providing a response to a worm attack in {}\n'.format(str(self.name),str(territory)))

    def kill_all_troops(self, territory_name):
        self.troops_killed(self.troops[territory_name].tokens, self.troops[territory_name].fedaykins)
        self.troops[territory_name].tokens = 0
        self.troops[territory_name].fedaykins = 0
        self.myGame.planet.troops_remove(territory_name, self.name)
        self.troops.pop(territory_name)

    def kill_some_troops(self, territory, troops, num_tokens, num_fedaykins):
        if num_tokens == troops.tokens and num_fedaykins == troops.fedaykins:
            self.kill_all_troops(territory)
        else:
            self.troops_killed(num_tokens, num_fedaykins)
            self.myGame.planet.troops_reduce(territory, self.name, num_tokens, num_fedaykins)

    def troops_killed(self, tokens, fedaykins):
        self.troops['tank'].tokens += tokens
        self.troops['tank'].fedaykins += fedaykins

    def troops_placed(self, where, troops):
        self.troops[where] = troops

    def troops_removed(self, where):
        del self.troops[where]

    def is_occupying_territory(self, territory_name):
        is_occupying = False
        if territory_name in self.troops:
            is_occupying = True
        return is_occupying

    def treachery_cards_display_update(self):
        x = 1
        for card in self.treachery_cards.keys():
            self.myGame.gui.player.treachery_card_place(card,x)
            x += 1
        while x <= 4:
            self.myGame.gui.player.treachery_card_place('TreacheryBack', x)
            x += 1

    def treachery_cards_per_deal_get(self):
        return 1

    def treachery_cards_needed(self):
        return (4 - len(self.treachery_cards))

    def treachery_cards_add(self, card, detail):
        self.treachery_cards[card] = detail
        self.treachery_cards_display_update()

    def treachery_card_del(self, card):
        msg = 'treachery_card_discard {}'.format(card)
        self.client_send(msg)
        del self.treachery_cards[card]
        self.treachery_cards_display_update()

    def treachery_card_del_multiple(self, *cards):
        if len(cards) != 0:
            msg = 'treachery_card_discard_multiple '
            offset = 0
            for x in range(len(cards)):
                if cards[x] != '' and cards[x] != ' ':
                    msg += '{} '.format(cards[x])
                    del self.treachery_cards[cards[x]]
            self.treachery_cards_display_update()
            self.client_send(msg)

    def treachery_card_play_query(self, card_name):
        play_it = False
        if self.is_card_available(card_name):
            if card_name != 'Family_Atomics':
                play_it = self.ask_yes_no(self.name, card_name)
            elif card_name == 'Family_Atomics' and True == self.in_or_adjacent_to_shield_wall():
                play_it = self.ask_yes_no(self.name, card_name)

            if True == play_it:
                self.myGame.answering_character = self.name
                self.treachery_card_del(card_name)

        return play_it

    def treachery_discard_query(self):
        card_added = 0
        # Form a message with all cards they played to ask them which to discard
        msg = 'treachery_card_discard_query'
        general, value = self.battle_plan.general_get()
        if True == self.myGame.treachery.is_card_of_type('Cheap_Hero', general):  # it needs to be discarded
            msg += ' {}'.format(general)
            card_added += 1

        key, value = self.battle_plan.defense_get()
        if key != 'none':
            msg += ' {}'.format(key)
            card_added += 1

        key, value = self.battle_plan.weapon_get()
        if key != 'none':
            msg += ' {}'.format(key)
            card_added += 1

        if 0 != card_added:
            self.send_query_and_wait(msg)

    def is_card_of_type_available(self, card_type):
        is_available = False
        for card in self.treachery_cards.keys():
            if True == self.myGame.treachery.is_card_of_type(card_type, card):
                is_available = True
                break
        return is_available

    def get_first_card_of_type(self, card_type):
        the_card = None
        for card in self.treachery_cards.keys():
            if True == self.myGame.treachery.is_card_of_type(card_type, card):
                the_card = card
                break
        return the_card

    def get_first_card_of_type_with_details(self, card_type, card_details):
        the_card = None
        for card, details in self.treachery_cards.items():
            if True == self.myGame.treachery.is_card_of_type(card_type, card) and details == card_details:
                the_card = card
                break
        return the_card

    def is_card_type_karama(self, card):
        is_karama = self.myGame.treachery.is_card_of_type('Karama', card)
        return is_karama

    def is_card_available(self, card_name):
        is_available = False
        if card_name in self.treachery_cards.keys():
            is_available = True
        return is_available

    def get_card_name_from_type(self, card_type):
        the_card = 'Not_Found'
        for card, detail in self.treachery_cards.items():
            if True == self.myGame.treachery.is_card_of_type(card_type, card):
                the_card = card
        return the_card

    def play_karama_card(self):
        print('Err why is {} trying to play a Karama Card'.format(self.name))

    def treachery_cards_replace(self, num, **cards):
        replacements = dict()

        msg = 'treachery_card_discard_multiple'
        for x in range(num):
            card, value = random.choice(list(self.treachery_cards.items()))
            self.treachery_cards.pop(card)
            replacements[card] = value
            msg += ' {}'.format(card)
        self.client_send(msg)

        msg = 'treachery_card'
        for card, value in cards.items():
            self.treachery_cards[card] = value
            msg += ' {} {}'.format(card, value)
        self.client_send(msg)

        return replacements

    #methods for sending information to the clients
    def client_send(self, msg):
        if self.myGame.is_server:
            self.send(msg, False)

    def send(self, data, is_response_needed):
        new_msg = self.myGame.send_msg_format(data)
        print('SEND: ' + new_msg)
        if True == is_response_needed:
            self.state = CharacterState.ACTION_NEEDED
        if None != self.client_socket:
            self.client_socket.send(new_msg.encode('utf-8'))
            time.sleep(.25)

    def send_query_and_wait(self, data):
        self.myGame.prep_for_yes_no_query()
        self.send(data, True)
        while self.state != CharacterState.READY:
            time.sleep(.5)
        return self.myGame.yes_rcvd

    def in_or_adjacent_to_shield_wall(self):
        is_adjacent = False
        for key in self.troops.keys():
            if key != 'reserve' and key != 'tank':
                is_adjacent = self.myGame.planet.is_territory_shield_wall_or_adjacent(key)
                if True == is_adjacent:
                    break
        return is_adjacent

class Harkonnen(Character):
    def __init__(self, myGame, player_name, player_dot, connection, spice, revival_rate):
        super().__init__('Harkonnen', myGame, player_name, player_dot, connection)
        self.spice = spice
        self.revival_rate = revival_rate
        self.generals = Generals.get_generals_by_house('Harkonnen')
        self.state = CharacterState.IDLE
        self.max_num_of_treachery_cards = 8

    def setup(self, data):
        response = 'place Carthag_11 10 0'
        self.send(response, False)

    def spy_select(self, general):
        x = 1
        for suspect in self.spies_delt:
            if suspect not in self.generals:
                self.myGame.gui.player.spy_declare(x)
            x += 1

        suspect_list = self.spies_delt.copy()
        for general in suspect_list:
            if general not in self.generals:
                value = self.spies_delt.pop(general)
                self.spy[general] = value

        self.state = CharacterState.READY

    def spy_choice(self):
        msg = 'spy_select none'
        self.send(msg, False)

    def treachery_cards_display_update(self):
        x = 1
        for card in self.treachery_cards.keys():
            self.myGame.gui.player.treachery_card_place(card,x)
            x += 1
        while x <= 8:
            self.myGame.gui.player.treachery_card_place('TreacheryBack', x)
            x += 1

    def treachery_cards_per_deal_get(self):
        return 2

    def treachery_cards_needed(self):
        return (8 - len(self.treachery_cards))

    def play_karama_card(self, *args):
        cards = dict()
        new_cards = dict()
        if args[1] == 'Swap':
            msg = 'Info Harkonnen is swapping {} cards with {}'.format(int(args[3]), args[2])
            self.myGame.broadcast(msg, False, self.name)

            msg = 'treachery_card_discard_multiple'
            for x in range(int(args[3])):
                value = self.treachery_cards.pop(args[x+4])
                cards[args[x+4]] = value
                msg += ' {}'.format(args[x+4])

            self.send(msg, False) #have the hark client discard the cards they are swapping

            who = self.myGame.is_character_playing(args[2])
            new_cards = who.treachery_cards_replace(int(args[3]), **cards)

            msg = 'treachery_card'
            for card, value in new_cards.items():
                self.treachery_cards[card] = value
                msg += ' {} {}'.format(card, value)

            self.send(msg, False) #have the hark client discard the cards they are swapping

    def generals_available_for_battle(self):
        general_list = {}
        general_list = super().generals_available_for_battle()

        for general in self.captured_generals.keys():
            general_list[general] = 0 #hmm FIXME we aren't carrying around the captured generals value
        return general_list

    def battle_won(self, battle_territory, spice_won, was_general_killed, opponent, won_by_treachery):
        #before calling the base class behavior let Hark decide on capturing a general and keeping it or selling for 2 spice
        general_list = []
        block = self.myGame.block_characters_advantage('Harkonnen', 'capturing a general')
        if False == block:
            for general, value in opponent.generals.items():
                if (general not in opponent.dead_generals and general not in opponent.captured_generals and \
                    general not in opponent.used_generals):
                    general_list.append(general)

            if 0 != len(general_list):
                general = random.choice(list(general_list))

            response = self.ask_yes_no(general, 'capture')
            if response == True:
                opponent.general_captured(general, self)
                self.general_captured(general, opponent)
            else:
                opponent.general_killed(general)
                spice_won += 2 #add 2 spice for the captured general
                
        super().battle_won(battle_territory, spice_won, was_general_killed, opponent, won_by_treachery)
        harkonnen_captured_general_resoltion(self, was_general_killed)

    def general_captured(self, name, who):
        self.captured_generals[name] = who
        if self.myGame.is_server == True: #on  a servier who is a character object on a client is the character_name
            msg = 'general_captured {} {}'.format(name, who.name)
            self.client_send(msg)
        else:
            self.myGame.gui.player.captured_general_place(who, name, len(self.captured_generals), len(self.spy))

    def general_freed(self, who):
        spies_displayed = (len(self.spy) + len(self.spies_delt))
        self.myGame.gui.player.captured_general_clear(len(self.captured_generals), spies_displayed)
        self.captured_generals.pop(who)

        position = 1
        for general in self.captured_generals.keys():
            house = Generals.get_house_by_general(who)
            spies_displayed = (len(self.spy) + len(self.spies_delt))
            self.myGame.gui.player.captured_general_place(house, who, position, spies_displayed)
            position += 1

        msg = 'general_freed {}'.format(who)
        self.client_send(msg)

    def battle_lost(self, territory_name, was_general_killed):
        super().battle_lost(territory_name, was_general_killed)
        harkonnen_captured_general_resoltion(self, was_general_killed)

def harkonnen_captured_general_resoltion(harkonnen, was_general_killed):
    #if all of Harkonnens generals are dead then all captured generals must be freed
    if len(harkonnen.dead_generals) == len(harkonnen.generals):
        for general, owner in harkonnen.captured_generals.items():
            owner.general_freed(general)
            harkonnen.general_freed(general)
        harkonnen.captured_generals = dict() #all generals freed clear the list

    #see if this was a captured general if it is and it is dead put it in the tank else return it to the owners active list
    general, value = harkonnen.battle_plan.general_get()
    owner = harkonnen.captured_generals.get(general, None)
    if owner is not None:
        if True == was_general_killed:
            owner.general_freed(general)
            owner.general_killed(general)
            harkonnen.general_freed(general)
        else:
            owner.general_freed(general)
            harkonnen.general_freed(general)

class Atreides(Character):
    def __init__(self, myGame, player_name, player_dot, connection, spice, revival_rate):
        super().__init__('Atreides', myGame, player_name, player_dot, connection)
        self.spice = spice
        self.revival_rate = revival_rate
        self.kwisatz_haderach_count = 0
        self.kwisatz_haderach_killed = False

        self.generals = Generals.get_generals_by_house('Atreides')
        self.state = CharacterState.IDLE

    def __str__(self):
        ret_str = super().__str__()
        ret_str += '    Kwazi Headache Count: {}\n'.format(self.kwisatz_haderach_count)
        return ret_str

    def initial_display(self):
        super().initial_display()
        self.myGame.gui.player.kwisatz_haderach_update(self.kwisatz_haderach_count)

    def setup(self, data):
        msg = 'place Arrakeen_10 10 0'
        self.send(msg, False)

    def next_spice_blow_cards(self, next_territory_name1, next_amount1, next_territory_name2, next_amount2 ):
        self.myGame.gui.player.next_spice_blow_vision(next_territory_name1, next_amount1, next_territory_name2, next_amount2)

    def revive_additional_tokens_or_generals(self):
        super().revive_additional_tokens_or_generals()
        if True == self.kwisatz_haderach_killed and self.spice >= 2:
            character_response = self.ask_yes_no(self.name, 'want_your_headache_back')
            if True == character_response:
                self.kwisatz_haderach_killed = False
                self.spice_payment('del', 2)

    def battle_plan_set(self, general, bid, offense, defense, spice_allocated, kwisatz_haderach_played):
        valid_plan = super().battle_plan_set(general, bid, offense, defense, spice_allocated, kwisatz_haderach_played)
        if True == kwisatz_haderach_played and False == self.kwisatz_haderach_killed:
            self.battle_plan.apply_kwisatz_haderach()
        elif True == kwisatz_haderach_played:
            valid_plan = False

        return valid_plan

    def pre_battle_setup(self, blocked):
        msg = 'atreides_vision_query {}'.format(blocked)
        self.send_query_and_wait(msg)
        msg = "Info Atreides vision request {}".format(self.myGame.string_rcvd)
        self.myGame.broadcast(msg, False, self.name)
        return self.myGame.string_rcvd

    def battle_won(self, battle_territory, spice_won, was_general_killed, opponent, won_by_treachery):
        self.kwisatz_haderach_count += self.battle_plan.troops_bid_get()
        msg = 'kwisatz_haderach_update {}'.format(self.kwisatz_haderach_count)
        self.client_send(msg)

        super().battle_won(battle_territory, spice_won, was_general_killed, opponent, won_by_treachery)

    def battle_lost(self, territory_name, was_general_killed):
        troops = self.troops[territory_name]
        self.kwisatz_haderach_count += troops.tokens #he lost them all
        msg = 'kwisatz_haderach_update {}'.format(self.kwisatz_haderach_count)
        self.client_send(msg)

        super().battle_lost(territory_name, was_general_killed)

    def  kwisatz_haderach_update(self, new_value):
        self.kwisatz_haderach_count = new_value
        self.myGame.gui.player.kwisatz_haderach_update(self.kwisatz_haderach_count)

class Guild(Character):
    def __init__(self, myGame, player_name, player_dot, connection, spice):
        super().__init__('Guild', myGame, player_name, player_dot, connection)
        self.spice = spice
        self.generals = Generals.get_generals_by_house('Guild')
        self.state = CharacterState.IDLE

        self.already_moved_this_turn = False

    def setup(self, data):
        response = 'place Tueks_Sietch_5 5 0'
        self.send(response, False)

    def move_between(self, from_territory_name, to_territory_name, tokens, fedaykins):
        if False == self.myGame.planet.is_territory_under_storm(from_territory_name):
            self.ready() #it is valid so mark the character as ready in case we need to ask them follow up questions
            ret_status = True
            movement_cost = guild_beam_cost_between_territories(self.myGame.planet, \
                                                                from_territory_name, \
                                                                to_territory_name, \
                                                                tokens, \
                                                                fedaykins)
            if 'reserve' == to_territory_name: #doing a territory to territory beam
                from_troops = self.myGame.planet.troops_get(from_territory_name, self.name)
                if from_troops.tokens == tokens and from_troops.fedaykins == fedaykins: #are we moving all tokens
                    self.myGame.planet.troops_remove(from_territory_name, self.name)#remove troops from start area
                    del (self.troops[from_territory_name]) #all troops are moving so clear the characters mapping of territory to troops
                else:
                    self.myGame.planet.troops_reduce(from_territory_name, self.name, tokens, fedaykins)
                self.troops['reserve'].tokens += tokens
                self.myGame.gui.player.tokens_update(self.name, self.troops['reserve'].tokens)

            elif False == self.myGame.planet.is_territory_under_storm(to_territory_name):
                self.myGame.planet.movment_between_two_territories(self, from_territory_name, to_territory_name, tokens, fedaykins)

                bene = self.myGame.is_character_playing('Bene_Gesserit')  # we need to know if bene is playing to query on peacefulness
                if bene is not None and self.myGame.planet.does_character_occupy(to_territory_name, 'Bene_Gesserit'):
                    bene.query_peacefulness_if_necessary(bene.myGame, to_territory_name)
            else:
                ret_status = False

            if True == ret_status:
                self.spice -= movement_cost
                self.myGame.gui.player.spice_amount_update(self.spice)

        else:
            ret_status = False
            print('Error illegal move request territory {} is under storm'.format(from_territory_name))
            msg = 'Msg territory_under_storm_try_again'
            self.send(msg, False)
        return ret_status

    def beam_query(self):
        processed = False
        while False == processed:
            processed = Gui.dune_gui_guild_beaming(self.myGame,  self.troops['reserve'].tokens, self.troops['reserve'].fedaykins)
            if True == processed:
                self.send(self.myGame.gui.map.event.msg, False)
                self.myGame.gui.player.clear()


class BeneGesserit(Character):
    def __init__(self, myGame, player_name, player_dot, connection, spice):
        super().__init__('Bene_Gesserit', myGame, player_name, player_dot, connection)
        self.state = CharacterState.IDLE
        self.spice = spice
        self.generals = Generals.get_generals_by_house('Bene_Gesserit')
        self.my_prediction = ''
        self.my_prediction_round = 0

    def initial_display(self):
        super().initial_display()
        self.myGame.gui.player.benes_prediction_update(self.my_prediction, self.my_prediction_round)

    def setup(self, data):
        processed = False
        response = 'place Polar_Sink_0 1 0'
        self.send(response, False)

        while False == processed:
            processed, beam_requested = Gui.dune_gui_place_or_beam_reqeust(self.myGame, 'place', 1, 0)
            if True == processed:
                self.send(self.myGame.gui.map.event.msg, False)
                self.myGame.gui.player.clear()

    def predict(self, data):
        prediction_made = False
        while False == prediction_made:
            prediction_made = Gui.dune_gui_benes_prediction(self.myGame)

    def pre_battle_setup(self, blocked):
        if False == blocked:
            msg = 'benes_voice_query'
            self.send_query_and_wait(msg)
            msg = 'Info VOICE:\" {} \"'.format(self.myGame.string_rcvd)
            self.myGame.broadcast(msg, False, self.name)
        return self.myGame.string_rcvd

    def create_peacefulness_declaration(self, msg_cmd):
        return_msg = '{} '.format(msg_cmd)
        added = 0
        for territory_name, troops in self.troops.items():
            if territory_name != 'reserve' and territory_name != 'tank':
                if self.myGame.planet.get_number_of_occupants(territory_name) > 1:
                    added += 1
                    if troops.peaceful == True:
                        im_peaceful  =  'yes'
                    else:
                        im_peaceful = 'no'
                    return_msg += '{} {} '.format(territory_name, im_peaceful)
        if 0 == added:
            return added, None
        else:
            return added, return_msg

    def query_peacefulness_if_necessary(self, thisGame, territory_name):
        my_troops = thisGame.planet.troops_get(territory_name, self.name)
        num_occupants = thisGame.planet.get_number_of_occupants(territory_name)
        if num_occupants == 2:
            msg = 'benes_coexistence_query {} {}'.format(territory_name, 'no')
            self.send(msg, False)
        elif num_occupants > 2:#greater than 2 bene must be peaceful
            my_troops.troops_peaceful_set(True)
            msg = 'benes_coexistence {} yes'.format(territory_name)
            self.myGame.broadcast(msg, False, '')

    def prediction(self, character, round):
        self.my_prediction = character
        self.my_prediction_round = round
        self.state = CharacterState.READY
        self.myGame.gui.player.benes_prediction_update(self.my_prediction, self.my_prediction_round)

    def place(self, territory_name, tokens, fedaykins):
        if tokens <= 1 and territory_name != '':
            self.beam(self.myGame.turn, territory_name, self.name, tokens, fedaykins, 0)
            if 'Polar_Sink_0' != territory_name:
                self.setup_request('predict')
        elif tokens > 1:
            print('ERROR Bene player placed too many tokens during setup {}'.format(tokens))
        else:
            print('INFO Bene player decided not to place an additional token during Setup \n')

    def move_to_planet(self, territory_name, tokens, fedaykins, using_karama):
        if 'no' != using_karama: #bene player wants to use karama card
              if self.myGame.treachery.is_card_of_type('Worthless', using_karama):
                block = self.myGame.block_characters_advantage(self.name, 'using_worthless_card_as_karama')
                if True == block:
                    using_karama = 'no'

        super().move_to_planet(territory_name, tokens, fedaykins, using_karama)

    def chaom(self):
        if self.myGame.turn != 1:
            self.spice_payment('add',2)

    def is_card_of_type_available(self, card_type):
        is_available = super().is_card_of_type_available(card_type)
        if False == is_available and 'Karama' == card_type:
            is_available = super().is_card_of_type_available('Worthless')
        return is_available

    def get_first_card_of_type(self, card_type):
        the_card = None
        if 'Karama' == card_type:
            the_card = super().get_first_card_of_type('Worthless')
        if None == the_card:
            the_card = super().get_first_card_of_type(card_type)
        return the_card

    def is_card_type_karama(self, card):
        is_karama = super().is_card_type_karama(card)
        if False == is_karama:
            is_karama = self.myGame.treachery.is_card_of_type('Worthless', card)

        return is_karama

class Fremen(Character):
    def __init__(self, myGame, player_name, player_dot, connection, spice, revival_rate, movement):
        super().__init__('Fremen', myGame, player_name, player_dot, connection)
        self.state = CharacterState.IDLE
        self.spice = spice
        self.revival_rate = revival_rate
        self.movement = movement
        self.next_storm_movement = 0

        self.worm_request = False
        self.worm_request_territory = ''

        self.troops['reserve'].tokens -= 3
        self.troops['reserve'].fedaykins += 3

        self.generals = Generals.get_generals_by_house('Fremen')
        self.num_tokens_to_setup = 10

    def initial_display(self):
        super().initial_display()
        self.myGame.gui.player.fedaykins_update(self.name, self.troops['reserve'].fedaykins)
        self.myGame.gui.player.next_storm_movement(0)

    def reserve_troops_gui_update(self):
        self.myGame.gui.player.tokens_update(self.name, self.troops['reserve'].tokens)
        self.myGame.gui.player.fedaykins_update(self.name, self.troops['reserve'].fedaykins)

    def setup(self, data):
        tokens_to_setup = self.num_tokens_to_setup
        available_tokens = self.troops['reserve'].tokens
        available_fedaykins = self.troops['reserve'].fedaykins
        while 0 != tokens_to_setup:
            msg = '{} tokens across Sietch_Tabr_14, False_Wall_South_(4|5), and or False_Wall_West_(16|17|18)'.format(tokens_to_setup)
            self.myGame.gui.player.text_box(msg, 10, colors.AQUA, colors.BLACK, 820, 550, 560, 15)
            msg = 'Available tokens: {} fedaykins {}'.format(available_tokens, available_fedaykins)
            self.myGame.gui.player.text_box(msg, 10, colors.AQUA, colors.BLACK, 820, 570, 560, 15)

            processed, beam_requested = Gui.dune_gui_place_or_beam_reqeust(self.myGame, 'place',\
                                                                           self.troops['reserve'].tokens,\
                                                                           self.troops['reserve'].fedaykins)
            if True == beam_requested:
                cmd, *args = self.myGame.gui.map.event.msg.split(' ')
                tokens = int(args[1])
                fedaykins = int(args[2])

                if (tokens <= self.troops['reserve'].tokens and fedaykins <= self.troops['reserve'].fedaykins and \
                    tokens_to_setup >= (tokens + fedaykins)) and \
                    ((args[0] == 'Sietch_Tabr_14') or (args[0] == 'False_Wall_South_4') or \
                     (args[0] == 'False_Wall_South_5') or (args[0] == 'False_Wall_West_16') or \
                     (args[0] == 'False_Wall_West_17') or (args[0] == 'False_Wall_West_18')):
                    self.send(self.myGame.gui.map.event.msg, False)
                    tokens_to_setup -= (tokens + fedaykins)
                    available_tokens -= tokens
                    available_fedaykins -= fedaykins

        self.myGame.gui.player.clear()

    def next_storm_movement_set(self, distance):
        self.next_storm_movement = distance
        self.myGame.gui.player.next_storm_movement(distance)

    def worm_announcement(self, territory, attack_number):
        super().worm_announcement(territory, attack_number)
        if 1 == attack_number and True == self.is_occupying_territory(territory):
            #FIXME need a pop dialogue box Asking Fremen if they want to ride the worm
            print('enter \' worm_flee <new_territory> \'')
        elif 1 < attack_number:
            #FIXME need a pop dialogue box Asking Fremen if they want to send the worm to attack a different territory
            print('enter \' worm_attack <territory>\'')
        else:
            print('Info WORM is ATTACKING {}\n'.format(str(territory)))

    def worm_response(self, territory):
        if 'none' != territory:
            self.worm_request_territory = territory
            self.worm_request = True
        self.state = CharacterState.READY

    def play_karama_card(self, *args):
        if args[0] == 'Attack':
            territory = self.myGame.planet.find_territory(args[1])
            planet.inflict_damage_on_territory(self.myGame.planet, territory, True)

    def worm_flee(self, old_territory, new_territory):
        if True == self.myGame.planet.can_troops_enter(new_territory, self.name):
            my_troops = self.myGame.planet.troops_get(old_territory, self.name)
            update = super().worm_flee(old_territory, new_territory)

            del self.troops[old_territory]
            #if it wasnt an update palce the troops into the new territory. If it was an update my_troops were consolidated
            #with the troops that occupied the new territory. hopefully my_troops get garbage collected some how :)
            if False == update:
                my_troops.round_placed = self.myGame.turn
                self.troops[new_territory] = my_troops

            # need to see if Bene occupies this territory to determine peacefulness
            bene = self.myGame.is_character_playing('Bene_Gesserit')
            if bene is not None and self.myGame.planet.does_character_occupy(new_territory, 'Bene_Gesserit'):
                bene.query_peacefulness_if_necessary(bene.myGame, new_territory)

            msg = 'fremen_fleeing_worm {} {}'.format(old_territory, new_territory)
            self.myGame.broadcast(msg, False, '')
        return update

    def place(self, territory_name, tokens, fedaykins):
        if (territory_name != 'Sietch_Tabr_14') and (territory_name != 'False_Wall_South_4') and (territory_name != 'False_Wall_South_5') and \
           (territory_name != 'False_Wall_West_16') and (territory_name != 'False_Wall_West_17') and (territory_name != 'False_Wall_West_18'):
            print('Error Fremen setup placement is in wrong territory_name')
        else:
            if fedaykins > self.troops['reserve'].fedaykins or fedaykins > self.num_tokens_to_setup:
                print('Error Fremen trying to place unavailable fedaykins')
            elif (fedaykins + tokens) > self.num_tokens_to_setup :
                print('Error Fremen trying to place too many tokens')
            else :
                self.beam(self.myGame.turn, territory_name, self.name, tokens, fedaykins, 0)
                self.num_tokens_to_setup -= (tokens + fedaykins)

        if self.num_tokens_to_setup == 0:
            bene = self.myGame.is_character_playing('Bene_Gesserit')
            if None != bene:
                bene.setup_request('setup')

            self.state = CharacterState.READY

    def move_to_planet(self, territory_name, tokens, fedaykins, using_karama):
        # insure Fremen is starting within 2 territories of The Great Flat
        move_allowed = self.myGame.planet.validate_on_planet_move_through_storm('The_Great_Flat_15', territory_name, 2, self.name)
        if True == move_allowed:
            territory_under_storm = self.myGame.planet.is_territory_under_storm(territory_name)
            if True == territory_under_storm:
                tokens_lost, fedaykins_lost = reduce_troops_in_half(tokens, fedaykins)
                #allocate troops lost to storm from reserves
                self.allocate_troops_from_reserves(tokens_lost, fedaykins_lost)
                #place the troops lost to storm into the tank
                self.troops_killed(tokens_lost, fedaykins_lost)

                msg = 'troops_killed {} {} {} {}'.format('reserve', self.name, tokens_lost, fedaykins_lost)
                self.client_send(msg)

                tokens -= tokens_lost
                fedaykins -= fedaykins_lost

            self.beam(self.myGame.turn, territory_name, self.name, tokens, fedaykins, 0)
            self.ready()

            bene = self.myGame.is_character_playing('Bene_Gesserit') #need to see if Bene occupies this territory to determine peacefulness
            if bene is not None and self.myGame.planet.does_character_occupy(territory_name, 'Bene_Gesserit'):
                bene.query_peacefulness_if_necessary(bene.myGame, territory_name)

        else:
            msg = 'Err Fremen is pulling some shit and trying to start in an illegal spot'
            print(msg)
            self.client_send(msg)

    def on_planet_move(self, start, end, tokens, fedaykins):
        move_allowed = super().on_planet_move(start, end, tokens, fedaykins) #see if a path exist no through a storm
        #if the call to super above is false it may have failed due to storm. So the following has the same logic as super
        #but calls a validate that allows movement through a strom. If allowed half of the moving troops are lost to the storm
        if False == move_allowed:
            if start in self.troops:
                max_distance = self.movement
                if self.ornothopters_available():
                    max_distance = 3
                move_allowed = self.myGame.planet.validate_on_planet_move_through_storm(start, end, max_distance, self.name)
                if True == move_allowed:
                    my_troops = self.myGame.planet.troops_get(start, self.name)
                    if my_troops.tokens == tokens and my_troops.fedaykins == fedaykins:
                        self.myGame.planet.troops_remove(start, self.name)
                        del(self.troops[start])
                        #determine the number of tokens lost to the storm
                        tokens_lost, fedaykins_lost = reduce_troops_in_half(my_troops.tokens, my_troops.fedaykins)
                        #move the number troops lost to storm to the tank
                        self.troops_killed(tokens_lost, fedaykins_lost)
                        #up date the troops by reducing the number lost to storm
                        my_troops.tokens -= tokens
                        my_troops.fedaykins -= fedaykins
                        #place the troops into the new territory
                        self.troops[end] = my_troops
                        self.myGame.planet.troops_enter(end, my_troops)
                    else:
                        #first remove the # of tokens specified from the source of the troops (my_troops)
                        my_troops.tokens -= tokens
                        my_troops.fedaykins -= fedaykins
                        #determine how many of the specified tokens are lost due to storm and move them to the tank
                        tokens_lost, fedaykins_lost = reduce_troops_in_half(tokens, fedaykins)
                        self.troops_killed(tokens_lost, fedaykins_lost)
                        #now remove the number of tokens specified from the total requested
                        tokens -= tokens_lost
                        fedaykins -= fedaykins_lost
                        #create a new troop object to place in the new territory
                        new_troops = troops.Troops(self.myGame.turn, self.name, tokens, fedaykins)
                        self.troops[end] = new_troops
                        self.myGame.planet.troops_enter(end, new_troops)

                    bene = self.myGame.is_character_playing( 'Bene_Gesserit')  # need to see if Bene occupies this territory to determine peacefulness
                    if bene is not None and self.myGame.planet.does_character_occupy(end, 'Bene_Gesserit'):
                        bene.query_peacefulness_if_necessary(bene.myGame, end)

                self.ready()

            else:
                print('Error {} is trying to move tokens from {} which they do not occupy'.format(self.name, start))

        return move_allowed

class Emperor(Character):
    def __init__(self, myGame, player_name, player_dot, connection, spice):
        super().__init__('Emperor', myGame, player_name, player_dot, connection)
        self.spice = spice
        self.troops['reserve'].tokens -= 5
        self.troops['reserve'].fedaykins += 5
        self.generals = Generals.get_generals_by_house('Emperor')
        self.state = CharacterState.IDLE

    def initial_display(self):
        super().initial_display()
        self.myGame.gui.player.fedaykins_update(self.name, self.troops['reserve'].fedaykins)
        #the emperor has no setup requirements as he starts all 20 tokens off planet
        self.state = CharacterState.READY

    def reserve_troops_gui_update(self):
        self.myGame.gui.player.tokens_update(self.name, self.troops['reserve'].tokens)
        self.myGame.gui.player.fedaykins_update(self.name, self.troops['reserve'].fedaykins)

    def setup_request(self, cmd): #Emperor has no pre-setup needs
        pass

    def play_karama_card(self, *args):
        if args[0] == 'Tokens':
            self.revival(3)
        elif len(self.dead_generals) != 0:
            general = self.dead_generals[0]
            self.general_revived(general)

def reduce_troops_in_half(tokens, fedaykins):
    tokens_lost = 0
    fedaykins_lost = 0

    reduction = int(((tokens + fedaykins + 1) / 2))
    while reduction != 0 and tokens != 0:
        tokens -= 1
        reduction -= 1
        tokens_lost += 1
    while reduction != 0 and fedaykins != 0:
        fedaykins -= 1
        reduction -= 1
        fedaykins_lost += 1
    return tokens_lost, fedaykins_lost

def create_character(character_name, my_game, player_name, player_dot, connection):
    new_player = None

    if 'Harkonnen' == character_name:
        new_player = Harkonnen(my_game, player_name, player_dot, connection, 10, 2)
    elif 'Atreides' == character_name:
        new_player = Atreides(my_game, player_name, player_dot, connection, 10, 2)
    elif 'Guild' == character_name:
        new_player = Guild(my_game, player_name, player_dot, connection, 5)
    elif 'Bene_Gesserit' == character_name:
        new_player = BeneGesserit(my_game, player_name, player_dot, connection, 5)
    elif 'Fremen' == character_name:
        new_player = Fremen(my_game, player_name, player_dot, connection, 3, 3, 2)
    elif 'Emperor' == character_name:
        new_player = Emperor(my_game, player_name, player_dot, connection, 10)
    else:
        print('FIXME invalid character requested {}'.format(character_name))

    new_player.initial_display()

    return new_player

def guild_beam_cost_between_territories(my_planet, from_territory_name, to_territory_name, tokens, fedaykins):
    from_territory = my_planet.find_territory(from_territory_name)
    beam_cost = from_territory.beam_cost_get()

    if 'reserve' != to_territory_name:
        to_territory = my_planet.find_territory(to_territory_name)
        to_beam_cost = to_territory.beam_cost_get()
        if to_beam_cost > beam_cost:
            beam_cost = to_beam_cost

    shipment_cost = int(((beam_cost * (tokens + fedaykins)) + 1)/2) #add 1 so cost is rounded up ie taking half of 3 1.5 rounds to 2

    return shipment_cost

