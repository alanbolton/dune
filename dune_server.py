import generals as Generals
import socket
from enum import Enum
import random
import threading as Threading
import time
import dune_game as Dune
import dune_msg as Msg
import battle as Battle
import character as char
import spice
import storm
import treachery as TreacheryCard
import pygame

class TurnRound(Enum):
    STORM = 0
    SPICE_BLOW = 1
    BIDDING = 2
    REVIVAL_AND_MOVEMENT = 3
    BATTLE = 4
    COLLECTION = 5

class DuneServerGameState(Enum):
    JOINING = 0
    PLAYER_SETUP = 1
    SPIES = 2
    PLAYING = 3
    WINNER = 4

class DuneServer(Dune.DuneGame) :
    def __init__(self, max_num_of_turns, my_ip, port):
        super().__init__(True)
        print("creating the dune game object")
        self.state = DuneServerGameState.JOINING
        self.max_num_of_turns = max_num_of_turns
        self.round = TurnRound.STORM
        self.num_of_rounds = 6

        self.character_turn_order = dict() #at the start of every turn this dict is re-ordered based on storm location
        self.player_dot_sectors = [2, 5, 8, 11, 14, 17]

        self.storm_tracker = storm.Storm(self)
        self.spice = spice.Spice(self)
        self.treachery = TreacheryCard.Treachery(self)

        self.battle_mgmt = Battle.Battle(self)

        #the following elements handle yes_no reponses from characters When the question is asked all the following are cleared
        #if the character being asked responds "pass" then yes_rcvd is False and implies a "no" was issued. if "yes" is
        #rcvd then yes_rcvd = True answering_character is the one who repsoneded (for informaitonal purposes) string and
        #value rcvd element are used for responses like bidding (that is the only current use)
        self.yes_rcvd = False
        self.answering_character = ''
        self.string_rcvd = ''
        self.value_rcvd = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((my_ip, port))
        self.socket.listen(6)

        try:
            Threading.Thread(target=game, args=(self, )).start()
        except:
            print("Game thread did not start.")

    def __str__(self):
        ret_str = 'Turn: {}/{} {} sectorUnder_storm: {} gameState: {} \n'.format(self.turn, \
                                                                                 self.max_num_of_turns, \
                                                                                 self.round, \
                                                                                 self.sector_under_storm_get(),\
                                                                                 self.state)
        ret_str += '   Free Characters: '
        for character_name in self.free_characters:
            ret_str += ' {}, '.format(character_name)
        ret_str += '\n'

        ret_str += super().__str__()

        ret_str += self.spice.__str__()
        return ret_str

    def next_state(self):
        self.state = DuneServerGameState(self.state.value + 1)

    def next_round(self):
        next_round = (self.round.value + 1) % self.num_of_rounds
        self.round = TurnRound(next_round)
        if self.round == TurnRound.STORM:
            self.turn += 1
            print('TURN {} ' + str(self.turn) + ' *************************************************')

    def sector_under_storm_get(self):
        return self.storm_tracker.sector_under_storm_get()

    def planet_shipment(self, round, territory_name, owner, tokens, fedaykins):
        super().planet_shipment(round, territory_name, owner, tokens, fedaykins)
        msg = 'planet_shipment {} {} {} {} {}'.format(self.turn, territory_name, owner, tokens, fedaykins)
        self.broadcast(msg, False, owner)

    def planet_shipment_local(self, territory_name, troops):
        super().planet_shipment_local(territory_name, troops)
        msg = 'planet_shipment {} {} {} {} {}'.format(self.turn, territory_name, troops.owner, troops.tokens, troops.fedaykins)
        self.broadcast(msg, False, troops.owner)

    def planet_ship_reinforcements(self, territory_name, owner, tokens, fedaykins):
        super().planet_ship_reinforcements(territory_name, owner, tokens, fedaykins)
        msg = 'planet_ship_reinforcements {} {} {} {}'.format(territory_name, owner, tokens, fedaykins)
        self.broadcast(msg, False, owner)

    def kill_some_troops_in_territory(self, territory, troops, tokens_killed, fedaykins_killed):
        super().kill_some_troops_in_territory(territory, troops, tokens_killed, fedaykins_killed)

        msg = 'troops_killed {} {} {} {}'.format(territory, troops.owner, tokens_killed, fedaykins_killed)
        self.broadcast(msg, False, '')

    def kill_troops_in_territory(self, territory_name, owner):
        super().kill_troops_in_territory(territory_name, owner)
        msg = 'troops_killed_all {} {}'.format(territory_name, owner)
        self.broadcast(msg, False, '')

    def player_join_request(self, player_name, connection, character_requested):
        player_dot = random.choice(self.player_dot_sectors)
        self.player_dot_sectors.remove(player_dot)

        if len(self.characters) >= 6:
            resp_str = 'err maxcharactersExceeded'
            connection.send(resp_str.encode('utf-8'))
        else:
            if character_requested in self.free_characters:
                character_name = character_requested
            else:  # character already taken so no you get a random character assigned
                character_name = random.choice(list(self.free_characters))
            self.free_characters.remove(character_name)

            this_character = char.create_character(character_name, self, player_name, player_dot, connection)
            self.characters[player_dot] = this_character
            self.socket_to_character_mapping[this_character.client_socket] = this_character

            msg = 'create {} {} {}'.format(this_character.name, this_character.player_name, this_character.player_dot_sector)
            this_character.send(msg, False)

    def all_characters_ready(self):
        num_characters = 0
        num_ready = 0
        for key, character in self.characters.items():
            num_characters += 1
            if character.state == char.CharacterState.READY:
                num_ready += 1

        return num_characters == num_ready

    def prep_for_yes_no_query(self):
        self.yes_rcvd = False
        self.answering_character = ''
        self.string_rcvd = ''
        self.value_rcvd = 0

    def process_message(self, connection, data):
        ret = 0
        err = 0
        cmd, *args = data.split(' ')
        print('RCV: {}'.format(data))
        if 'show' == cmd:
            if 0 != len(args):
                resp_str = 'success showing game status on sever console for {}'.format(args[0])
                connection.send(resp_str.encode('utf-8'))
                if 'char' == args[0]:
                    for dot, character in self.characters.items():
                        print(character)
                elif 'planet' == args[0]:
                    print(self.planet)
                else:
                    print(self)

        elif 'quit' == cmd:
            ret = -1000

        if self.state == DuneServerGameState.JOINING:
            if 'join' == cmd:
                if len(args) == 0 :
                    print('Error invalid join request {}'.format(connection))
                elif len(args) == 1:
                    self.player_join_request(args[0], connection, '') #let a random character be assigned
                else:
                    self.player_join_request(args[0], connection, args[1]) #pass the characters name requested

            elif 'play' == cmd:
                self.next_state()
                #Setup the playing sequence based on playerdot
                self.characters = {k: self.characters[k] for k in sorted(self.characters)}
                # inform all players of characters playing and their player dots
                msg = 'characters_playing {}'.format(len(self.characters))
                for key, character in self.characters.items():
                    msg += ' {} {} {}'.format(character.name, key, character.player_name)
                self.broadcast(msg, False, '')

                #first have characters with fixed config do their auto placement
                for key, character in self.characters.items():
                    if character.name != 'Fremen' and character.name != 'Bene_Gesserit':
                        character.setup_request('setup')

                # next handle the setup sequencing between Fremen and Bene if they are playing
                fremen = self.is_character_playing('Fremen')
                if None != fremen:
                    fremen.setup_request('setup')
                else:
                    bene = self.is_character_playing('Bene_Gesserit')
                    if None != bene:
                        bene.setup_request('setup')

            elif 'stack' == cmd:
                self.treachery.stack_the_deck()

            else:
                err = -1

        elif self.state == DuneServerGameState.PLAYER_SETUP:
            character = self.socket_to_character_mapping[connection]
            if 'place' == cmd:
                character.place(args[0], int(args[1]), int(args[2]))

            elif 'prediction' == cmd:
                if 2 == len(args):
                    character.prediction(args[0], int(args[1]))
                    character.client_send(data)
                else:
                    print('Error invalid prediction by Bene not info information provided\n')


            elif 'setup_request' == cmd:
                character.setup_request('setup')

            else:
                err = -1

        elif self.state == DuneServerGameState.SPIES:
            character = self.socket_to_character_mapping[connection]
            if 'spy_select' == cmd and len(args) >= 1:
                character.spy_select(args[0])
                character.send(data, False)
            else:
                err = -1

        elif self.state == DuneServerGameState.PLAYING:
            guild_is_blocking_beam = False

            character = self.socket_to_character_mapping[connection]
            if 'worm_flee' == cmd or 'worm_attack' == cmd:
                character.worm_response(args[0])
            elif 'beam_request' == cmd:
                guild = self.is_character_playing('Guild')
                if guild != None and character.name != 'Guild' and True == guild.is_card_of_type_available('Karama'):
                    the_card = guild.get_card_name_from_type('Karama')
                    msg = 'yes_no_query {} block_thier_shipment?'.format(character.name)
                    guild_is_blocking_beam = guild.send_query_and_wait(msg)

                if False == guild_is_blocking_beam:
                    if len(args) > 3:
                        using_karama = args[3]
                    else:
                        using_karama = 'no'
                    character.move_to_planet(args[0], int(args[1]), int(args[2]), using_karama)
                else:
                    msg = 'Info Guild blocked shipment'
                    character.send(msg, False)
                    guild.treachery_card_del(the_card)
                    character.ready()  # it is a valid move so mark character as ready


            elif 'beam_between_request' == cmd:
                move_allowed = character.move_between(args[0], args[1], int(args[2]), int(args[3]))
                if True == move_allowed:
                    msg = data
                    character.send(msg, False)
                    #now provide an update to all others
                    if 'reserve' != args[1]:
                        self.planet.announce_character_movement(character.name, args[0],args[1])
                    else:
                        msg = 'troops_killed {} {} {} {}'.format('reserve', character.name, int(args[2]), int(args[3]))
                        self.broadcast(msg, False, character.name)
                else:
                    msg = 'beam_query'
                    character.send(msg, False)
                    msg = 'move from {} to {} denied'.format(args[0], args[1])
                    print(msg)

            elif 'move_request' == cmd:
                move_successful = character.on_planet_move(args[0],args[1],int(args[2]), int(args[3]))
                if True == move_successful:
                    #echo the command back to the client
                    msg = data
                    character.send(msg, False)
                    # now provide an update to all others
                    self.planet.announce_character_movement(character.name, args[0], args[1])
                else:
                    print('Err OPM failed re-issuing opm_query')
                    msg = 'opm_query'
                    character.send(msg, False)

            elif 'pass' == cmd:
                #indicates the character responded but passed on the last request made to it
                character.ready()
                print('Info {} passed'.format(character.name))

            elif 'yes_no_response' == cmd:
                #the character has responeded
                self.yes_rcvd = True
                self.answering_character = character.name
                if 0 < len(args):
                    if args[0].isdecimal():
                        self.value_rcvd = int(args[0])
                    else:
                        self.string_rcvd = args[0]
                character.ready()

            elif 'treachery_card_bid' == cmd:
                if len(args) >= 1:
                    if args[0].isdecimal():
                        character.myGame.yes_rcvd = True
                        character.myGame.value_rcvd = int(args[0])
                        if len(args) > 1:
                            character.myGame.string_rcvd = args[1] #this covers player requesting to use a karama to pay
                    elif args[0] == 'pass':
                        character.myGame.yes_rcvd = False
                        character.myGame.prep_for_yes_no_query()
                    else:
                        character.myGame.yes_rcvd = False
                        print('FIXME received garbage {}'.format(args[0]))
                    character.ready()

            elif 'treachery_card_discard_multiple' == cmd:
                if args[0] != 'none' and args[0] != 'pass':
                    msg = 'Info {} discarding these {}'.format(character.name, args)
                    self.broadcast(msg, False, character.name)
                    character.treachery_card_del_multiple(*args)

                character.ready()

            elif 'benes_coexistence' == cmd:
                self.update_benes_peacefulness(args)
                character.ready()
                #now send the selections to all clients to update their status

                self.broadcast(data, False, '')
            elif 'next_battle' == cmd:
                character.current_battle = [args[0], args[1]]
                character.ready() #indicate we got the reponse as the code is blocking waiting for it

            elif 'benes_voice' == cmd or 'atreides_vision_response' == cmd:
                self.string_rcvd = args[0]
                character.ready()

            elif 'submit_battle_plan' == cmd: # arg0< general | cheap_hero | none >  1 < bid_amount > 2 < offense_card_name >> 3< defense_card_name > 4<spice>
                if len(args) <= 5:
                    is_plan_valid = character.battle_plan_set(args[0], float(args[1]), args[2], args[3], int(args[4]), 'False')
                else:
                    is_plan_valid = character.battle_plan_set(args[0], float(args[1]), args[2], args[3], int(args[4]), args[5])

                if True == is_plan_valid:
                    character.ready()
                else:
                    msg = 'Plan was invalid please try again\n'
                    print(msg)
                    character.send(msg, False)

            elif 'play_card' == cmd:
                if args[0] == 'Ghola':
                    if args[1] == 'Tokens':
                        character.revival(5)
                    elif len(character.dead_generals) != 0:
                        general = character.dead_generals[0]
                        character.general_revived(general)
                elif args[0] == 'Karama_1' or args[0] == 'Karama_2':
                    character.play_karama_card(*args)
                elif args[0] == 'Truth_Trance_1' or args[0] == 'Truth_Trance_2':
                    who = self.is_character_playing(args[1])
                    msg = 'truth_trance_query {} {} {}'.format(character.name, who.name, args[2])
                    character.myGame.broadcast(msg, False, character.name)

                character.treachery_card_del(args[0])

            elif 'truth_trance_response' == cmd:
                msg = 'Info {} asked {} {} : {}'.format(args[1], args[0], args[2], args[3])
                character.myGame.broadcast(msg, False, character.name)

            else:
                err = -1

            if err == -1:
                resp_str = 'err invalidCmd'
                connection.send(resp_str.encode('utf-8'))
                print('Error invalid command {} recieved from {} '.format(cmd, connection))

        return ret

def handle_discard_treachery_card_msg(character, data):
    cmd, *args = data.split(' ')
    offset = 0
    for x in range(len(args)):
        character.treachery_card_del(args[x])

def game(thisGame):
    while True:
        func = game_state_machine(thisGame.state)
        func(thisGame)

def join_waiting(thisGame):
    count = 0
    msg = 'Info Waiting for everyone to join'
    while thisGame.state == DuneServerGameState.JOINING:
        count += 1
        if count % 10 == 0:
            print(msg)
        time.sleep(.5)

def setup_waiting(thisGame):
    count = 0
    msg = 'Info Waiting for everyone to join and get setup'
    while thisGame.state == DuneServerGameState.PLAYER_SETUP:
        if True == thisGame.all_characters_ready():
            thisGame.next_state()

        count += 1
        if count % 10 == 0:
            print(msg)
        time.sleep(.5)

def game_selecting_spies(thisGame):
    print('Info Spy time. Shuffling generals and dealing 4 to each character to make a selection')
    my_deck_of_generals = Generals.Generals()

    for key, character in thisGame.characters.items():
        my_deck_of_generals.deal_spies(character)

    while thisGame.state == DuneServerGameState.SPIES:
        time.sleep(.5)
        if thisGame.all_characters_ready():
            thisGame.next_state()
            thisGame.turn = 1


def game_play(thisGame):
    print('The Game is ON!')
    print('TURN {} ' + str(thisGame.turn) + ' *************************************************')
    while thisGame.state == DuneServerGameState.PLAYING:
        print('====== {} ' + str(thisGame.round) + ' ==============================================')
        func = round_state_machine(thisGame)
        func(thisGame)
        thisGame.next_round()

        if thisGame.max_num_of_turns < thisGame.turn:
            thisGame.next_state()

def game_winner(thisGame):
    msg = 'FIXME add logic to figure out who won by default'
    while thisGame.state == DuneServerGameState.WINNER:
        print(msg)
        time.sleep(20)

def game_bad_state(thisGame):
    msg = 'Critical Error invalid game state {}'.format(thisGame.state)
    while True:
        print(msg)
        time.sleep(20)

def game_state_machine(state):
    game_management = {
        DuneServerGameState.JOINING: join_waiting,
        DuneServerGameState.PLAYER_SETUP : setup_waiting,
        DuneServerGameState.SPIES : game_selecting_spies,
        DuneServerGameState.PLAYING : game_play,
        DuneServerGameState.WINNER : game_winner
    }
    func = game_management.get(state, lambda: game_bad_state)
    return func

def bad_round():
    msg = 'FIXME some how the turn phase got messed up'

def round_state_machine(thisGame):
    round_management = {
        # TurnRound.STORM: storm_round,
        # TurnRound.SPICE_BLOW : spice_blow,
        # TurnRound.BIDDING : deal_4_to_all_playing,
        #TurnRound.BIDDING: bidding_round,
        # TurnRound.REVIVAL_AND_MOVEMENT : revival_and_movement_round,
        # TurnRound.BATTLE : battle_round,
        # TurnRound.COLLECTION : collection_round

        TurnRound.STORM: storm_round,
        TurnRound.SPICE_BLOW: spice_blow,
        TurnRound.BIDDING: bidding_round,
        TurnRound.REVIVAL_AND_MOVEMENT: revival_and_movement_round,
        TurnRound.BATTLE: battle_round,
        TurnRound.COLLECTION: collection_round
    }
    func = round_management.get(thisGame.round, lambda: bad_round)
    return func

def deal_4_to_all_playing(thisGame):
    for x in range(4):
        thisGame.treachery.dealing_round()

def no_op_round(thisGame):
    print('FIXME used for debugging and eleminating round actions\n')

def storm_round(thisGame):
    thisGame.storm_tracker.movement()

def spice_blow(thisGame):
    thisGame.spice.blow()

def bidding_round(thisGame):
    if 0 != (thisGame.turn % 2):
        print('Info this is a dealing Round\n')
        thisGame.treachery.dealing_round()
    else:
        print('Info this is a NON dealing Round\n')

    print('Starting the Bidding process\n')
    thisGame.treachery.bidding_round()

def revival_and_movement_round(thisGame):
    guild_moves_in_seq = False
    guild_played = False #set indicating the Guild played this turn already

    #First if bene character is playing we need them to delcare where they are peaceful or not to start the movement phase
    bene = thisGame.is_character_playing('Bene_Gesserit')
    if bene is not None:
        added, msg = bene.create_peacefulness_declaration('benes_coexistence_query')
        if added != 0:
            bene.send_query_and_wait(msg) #we need to wait for Bene to respond with her updated declarations

        added, msg = bene.create_peacefulness_declaration('benes_coexistence')
        if added != 0:
            thisGame.broadcast(msg, False, '')

    #guild moves in seq controls whether Guild decides when to move or if a karama card has been played preventing him to choose when he moves
    guild = thisGame.is_character_playing('Guild')
    if None == guild:
        guild_moves_in_seq = True

    for key, character in thisGame.characters.items():
        character.revival(0) #reclaims troops ... 0 indicates it is free revival and will use the revival rate of the character
        character.revive_additional_tokens_or_generals()

        if None != guild and False == guild_moves_in_seq:
            guild_moves_in_seq = thisGame.ask_character_to_block_another_characters_advantage(character, 'Guild', 'move_in_normal_sequence?')

    for key, character in thisGame.character_turn_order.items():
        msg = 'yes_no_query Guild ready_to_move?'
        if False == guild_moves_in_seq and False == guild_played and guild != None:
            character_response = guild.send_query_and_wait(msg)
            if True == character_response:
                movement_round_handler(guild)
                guild_played = True

        if character.name != 'Guild' or guild_moves_in_seq == True:
            movement_round_handler(character)

    if guild_played == False and None != guild:
        movement_round_handler(guild)

def movement_round_handler(character):
    msg = 'beam_query'
    character.send_query_and_wait(msg) #we wait for the response but take no action we just need to wait until it is complete

    msg = 'opm_query' #opm = on planet move
    character.send_query_and_wait(msg) #we wait for the response but take no action we just need to wait until it is complete

    play_it = character.treachery_card_play_query('Hajr')
    if True == play_it:
        msg = 'opm_query'  # opm = on planet move
        character.send_query_and_wait( msg)  # we wait for the response but take no action we just need to wait until it is complete

    character.territory_troop_consolidation()#if a player has tokens in a territory but they span multiple sectors this is their chance to consolidate them before moving

def battle_round(thisGame):
    thisGame.battle_mgmt.battle_round()

def collection_round(thisGame):
    for key, character in thisGame.characters.items():
        character.collection()

def dune_server_thread(thisGame, connection):
    is_active = True

    my_messaging = Msg.DuneMsg(connection, thisGame)
    while is_active:
        status = my_messaging.rcv_input()
        if -2 == status:
            print('close received')
            connection.close()


def main():
    thisGame = DuneServer(15, '127.0.0.1', 5000) #FIXME change this or find a way to take it as an arguement when you start the game

    while thisGame.state != DuneServerGameState.SPIES:
        c, addr = thisGame.socket.accept()
        print("connection rcvd from" + str(addr))
        ip, port = str(addr[0]), str(addr[1])
        print("Connected with " + ip + ":" + port)

        try:
            Threading.Thread(target=dune_server_thread, args=(thisGame, c)).start()
        except:
            print("Thread did not start.")

    c.close()


if __name__ == '__main__':
    main()

