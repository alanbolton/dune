from enum import Enum
import pygame
import socket
import time
import colors
import dune_msg as Msg
from threading import Thread
import dune_game as Dune
import dune_gui as Gui
import character as char
import treachery as TreacheryCard
import battle as Battle

class DuneClientGameState(Enum):
    JOINING = 0
    WAITING_TO_PLAY = 1
    PLAYING = 2

class DuneClient(Dune.DuneGame) :
    def __init__(self, my_ip, port):
        super().__init__(False)
        print("creating the Dune client game object")
        self.state = DuneClientGameState.JOINING

        self.sector_under_storm = 1
        self.treachery = TreacheryCard.Treachery(self)#needed simply so character create will work

        self.characters_playing = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if my_ip != '':
            self.socket.connect((my_ip, port))

        try:
            Thread(target=dune_client_thread_keyboard, args=(self, )).start()
        except:
            print("Error Thread did not start.")

    def __str__(self):
        ret_str = 'Turn: {} sectorUnder_storm: {} gameState: {} \n'.format(self.turn,  \
                                                                           self.sector_under_storm_get(),\
                                                                           self.state)
        ret_str += super().__str__()
        return ret_str

    def format_and_send_message(self, msg):
        msg = self.send_msg_format(msg)
        self.socket.send(msg.encode('utf-8'))

    def next_state(self):
        self.state = DuneClientGameState(self.state.value + 1)

    def sector_under_storm_get(self):
        return self.sector_under_storm

    def process_message(self, connection, data):
        print('RCV: ' + data)
        cmd, *args = data.split(' ')

        character = self.socket_to_character_mapping.get(connection, None)
        if 'create' == cmd:
            my_character = char.create_character(args[0], self, args[1], int(args[2]), connection)
            self.characters[int(args[2])] = my_character
            self.socket_to_character_mapping[my_character.client_socket] = my_character
            self.free_characters.remove(my_character.name)
            self.characters_playing.append(my_character.name)
        elif 'beam' == cmd:
            character.beam(int(args[0]), args[1], args[2], int(args[3]), int(args[4]), int(args[5]))

        elif 'beam_between_request' == cmd:
            character.move_between(args[0], args[1], int(args[2]), int(args[3]))

        elif 'move_request' == cmd:
            move_successful = character.on_planet_move(args[0], args[1], int(args[2]), int(args[3]))
            if True == move_successful:
                msg = 'Success move request was successful'
            else:
                msg = 'Err move_request_failed'

        elif 'movement_notification' == cmd:
            character.myGame.planet.character_movement(args[0], args[1], int(args[2]), int(args[3]), args[4], int(args[5]), int(args[6]))

        elif 'planet_shipment' == cmd:
            character.myGame.planet_shipment(int(args[0]), args[1], args[2], int(args[3]), int(args[4]))

        elif 'planet_ship_reinforcements' == cmd:
            character.myGame.planet_ship_reinforcements(args[0], args[1], int(args[2]), int(args[3]))

        elif 'beam_query' == cmd:
            character.beam_query()

        elif 'opm_query' == cmd:
            character.move_query()

        elif 'predict' == cmd:
            character.predict(data)

        elif 'setup' == cmd:
            character.setup(data)

        elif 'characters_playing' == cmd:
            offset = 0
            for x in range(int(args[0])):
                offset = x * 3 #*3 is because we are extracting two values each loop
                #remove the character from free list
                if args[offset + 1] != character.name:
                    self.free_characters.remove(args[offset + 1])
                    self.characters_playing.append(args[offset + 1])

                self.gui.map.player_dot_set(int(args[offset + 2]), args[offset + 1], args[offset + 3])

            self.state = DuneClientGameState.PLAYING
            self.gui.player.soft_keys_clear_all(800, 770, 6)  # FIXME get rid of the hard coding
            self.gui.player.disable_all_row_entries(770)

        elif 'spy_choice' == cmd:
            offset = 0
            for x in range(int(args[0])):
                offset = x * 2 #*2 is because we are extracting two values each loop
                character.spy_dealt(args[offset + 1], int(args[offset + 2]))

            character.spy_choice()

        elif 'spy_select' == cmd:
            character.spy_select(args[0])

        elif 'spice_payment' == cmd:
            character.spice_payment(args[0], int(args[1]))
            self.gui.player.spice_amount_update(character.spice)

        elif 'storm_movement' == cmd:
            self.turn = int(args[0])
            self.gui.map.set_storm(self.sector_under_storm, colors.BLACK)
            self.sector_under_storm = int(args[1])
            self.gui.map.set_storm(self.sector_under_storm, colors.LIME_GREEN)
            self.gui.player.system_info_box_write('Turn {} Sector_Under_Storm {}'.format(self.turn, self.sector_under_storm_get()))
            character.next_storm_movement_set(int(args[2])) #next storm movement

        elif 'spice_blow' == cmd :
            #first place the spice being blown into the global territory structure
            character.myGame.planet.spice_blow(args[0], int(args[1]))
            character.myGame.gui.map.spice_card_place(args[0], int(args[2]))

        elif 'spice_blow_next' == cmd :
            #first place the spice being blown into the global territory structure
            character.next_spice_blow_cards(args[0], int(args[1]), args[2], int(args[3]))

        elif 'spice_remove' == cmd :
            character.myGame.planet.spice_harvest(args[0], int(args[1]))

        elif 'troops_killed_all' == cmd:
            self.kill_troops_in_territory(args[0], args[1])

        elif 'troops_killed' == cmd:
            if args[0] == 'reserve': #this exist for Fremen placing troops into a strom territory need to move troops from reserve to tank
                character.allocate_troops_from_reserves(float(args[2]), float(args[3]))
                character.troops_killed(float(args[2]), float(args[3]))
            else:
                troops = character.myGame.planet.troops_get(args[0], args[1])
                self.kill_some_troops_in_territory(args[0], troops, float(args[2]), float(args[3]))

        elif 'troops_uploaded' == cmd:
            troops = character.myGame.planet.troops_get(args[0], args[1])
            self.kill_some_troops_in_territory(args[0], troops, float(args[2]), float(args[3]))
            character.self.troops['reserve'].tokens += int(args[2])
            self.gui.player.tokens_update(character.name, character.self.troops['reserve'].tokens)
            if character.name == 'Emperor' or character.name == 'Fremen':
                character.self.troops['reserve'].fedaykins += int(args[3])
                self.gui.player.fedaykins_update(character.name, character.self.troops['reserve'].fedaykins)

        elif 'worm' == cmd :
            character.worm_announcement(args[0], int(args[1]))

        elif 'fremen_fleeing_worm' == cmd : #sent to all characters to up date global DB
            character.worm_flee(args[0], args[1])

        elif 'yes_no_query' == cmd:
            if args[1] == 'consolidate_troops':
                is_yes, msg = Gui.dune_gui_yes_no_query(self, args[0], args[1], False)
                if True == is_yes:
                    self.gui.map.event.reset()
                    self.gui.map.event.msg_init(msg)
                    self.gui.map.event.text_box_init('Choose Territory ', 820, 630)
                    self.gui.map.event.display_text_box()
                    self.gui.map.event_wait(Gui.DuneGuiEventTypes.CLICK, None, Gui.DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
                    character.send(self.gui.map.event.msg, False)
            elif args[1] == 'revive_additional_tokens' or args[1] == 'Weather_Control' or args[1] == 'limit_fedaykins_lost':
                is_yes, msg = Gui.dune_gui_yes_no_query(self, args[0], args[1], True)
                character.send(msg, False)
            else:
                is_yes, msg = Gui.dune_gui_yes_no_query(self, args[0], args[1], False)
                character.send(msg, False)

        elif 'revival' == cmd : #this command is for both free revival and tleilaxu Ghola card. If arg[0] is 0 it is normal revival else it contains the # being revived
            character.revival(int(args[0]))

        elif 'benes_coexistence' == cmd :
            self.update_benes_peacefulness(args)

        elif 'prediction' == cmd :
            character.prediction(args[0], int(args[1]))

        elif 'benes_coexistence_query' == cmd :
            num_of_queries = int(len(args) / 2)
            msg = 'benes_coexistence'
            for x in range(num_of_queries):
                offset = x * 2  # *2 is because we are extracting two values each loop
                territory_name = args[offset + 0]
                question = 'Are you Peaceful in {}'.format(territory_name)
                is_answer_yes, not_used = Gui.dune_gui_yes_no_query(self, character.name, question, False)
                if True == is_answer_yes:
                    msg += ' {} {}'.format(territory_name, 'yes')
                else:
                    msg += ' {} {}'.format(territory_name, 'no')
            character.send(msg, False)

        elif 'benes_voice_query' == cmd:
            Gui.dune_gui_benes_voice_request(self)
            character.send(self.gui.player.event.msg, False)

        elif 'treachery_card' == cmd :
            offset = 0
            for x in range(int(len(args)/2)):
                offset = x * 2 #*2 is because we are extracting two values each loop
                character.treachery_cards_add(args[offset], args[offset + 1])

        elif 'treachery_card_discard' == cmd :
            character.treachery_card_del(args[0])

        elif 'treachery_card_discard_multiple' == cmd :
            character.treachery_card_del_multiple(*args)

        elif 'treachery_card_discard_query' == cmd:
            Gui.post_battle_discard_query(self.gui.player, *args, )
            character.send(self.gui.player.event.msg, False)

        elif 'treachery_card_bidding' == cmd:
            bid_amount = int(args[2])
            self.gui.map.treachery_card_up_for_bid(args[0], bid_amount, args[1], args[3])
            if args[0] != 'TreacheryBack' and args[3] == character.name:
                Gui.player_bidding(self, character, bid_amount)

        elif 'choose_next_battle' == cmd:
            Gui.choose_next_battle(self.gui.player, *args, )
            character.send(self.gui.player.event.msg, False)

        elif 'submit_battle_plan_query' == cmd:
            Gui.dune_gui_battle_plan_set(self, character, args[0], args[4], args[8], args[10])
            character.send(self.gui.player.event.msg, False)

        elif 'battle' == cmd:
            self.gui.player.clear()
            plan = Battle.BattlePlan()
            plan.general_set(args[1], 0)
            plan.weapon_set(args[2], 'none')
            plan.defense_set(args[3],'none')
            plan.troops_bid_set(float(args[4]))
            plan.spice_payment_set(int(args[5]))
            Gui.display_current_battle_plan_selections(self.gui.player, args[0], plan, 1)

            plan.general_set(args[7], 0)
            plan.weapon_set(args[8], 'none')
            plan.defense_set(args[9],'none')
            plan.troops_bid_set(float(args[10]))
            plan.spice_payment_set(int(args[11]))
            Gui.display_current_battle_plan_selections(self.gui.player, args[6], plan, 0)

        elif 'battle_results' == cmd:
            Gui.display_battle_results(self.gui.player, args[0], args[1], float(args[2]), float(args[3]))

        elif 'atreides_vision_query' == cmd:
            is_blocked = False
            if args[0] == 'True':
                is_blocked = True

            if True == character.is_card_of_type_available('Karama'):
                karama_card = character.get_first_card_of_type('Karama')
            else:
                karama_card = None
            if False == is_blocked or (True == is_blocked and None != karama_card):
                Gui.dune_gui_atreides_battle_vison_request(self, is_blocked, karama_card)
            else:
                self.gui.player.event.msg_init('atreides_vision_response none')
            character.send(self.gui.player.event.msg, False)

        elif 'atreides_vision' == cmd:
            character.myGame.gui.player.system_info_box_write(data)

        elif 'treachery_bidding_vision:' == cmd:
            display_msg = 'Cards ({}) for Bid This Round'.format(len(args))
            self.gui.player.text_box(display_msg, 15, colors.GOLD, colors.BLACK, 820, 575, 560, 20)
            count = 1
            for x in range(len(args)):
                self.gui.player.treachery_card_choice_place(args[x], count, 820, 600, Gui.CARD_SMALL_X)
                count += 1

        elif 'general_used' == cmd:
            character.general_used(args[0])

        elif 'general_killed' == cmd:
            character.general_killed(args[0])

        elif 'general_captured' == cmd:
            character.general_captured(args[0], args[1])

        elif 'general_freed' == cmd:
            character.general_freed(args[0])

        elif 'general_revived' == cmd:
            character.general_revived(args[0])

        elif 'generals_used_clear' == cmd:
            character.clear_general_used_list()

        elif 'kwisatz_haderach_update' == cmd:
            character.kwisatz_haderach_update(float(args[0]))

        elif 'truth_trance_query' == cmd:
            if character.name == args[1]:
                is_yes, msg = Gui.dune_gui_yes_no_query(self, args[1], args[2], False)
                if True == is_yes:
                    msg = 'truth_trance_response {} {} {} yes'
                else:
                    msg = 'truth_trance_response {} {} {} yes'
                character.send(self.gui.map.event.msg, False)
            else:
                msg = '{} is asking {}  the following: {}'.format(args[0], args[1], args[2])
                character.myGame.gui.system_info_box_write(msg)

        elif 'clear_player_display' == cmd:
            self.gui.player.clear()

        elif 'Error' == cmd or 'Msg' == cmd or 'Info' == cmd:
            character.myGame.gui.player.system_info_box_write(data)

        else :
             print('invalid command ( {} ) recieved from server'.format(cmd))

def dune_client_thread(this_game):
    is_active = True

    this_game.my_messaging = Msg.DuneMsg(this_game.socket, this_game)
    while is_active:
        func = client_state_machine(this_game.state)
        func(this_game)

def dune_client_thread_keyboard(this_game):
    cmd = ''
    request = ''

    request = input("request -> ")
    while cmd != "quit":
        cmd, *args = request.split(' ')
        if 'showLocal' == cmd :
            if 0 != len(args):
                if 'char' == args[0]:
                    for dot, character in this_game.characters.items():
                        print(character)
                elif 'planet' == args[0]:
                    print(this_game.planet)
                elif 'territory' == args[0]:
                    this_territory = this_game.planet.find_territory(args[1])
                    print(this_territory)
                else:
                    print(this_game)
            else:
                print('Error not enough parameters to the show command')
        else:
            new_msg = this_game.send_msg_format(request)
            this_game.socket.send(new_msg.encode('utf-8'))
        request = input("request -> ")

    this_game.socket.close()

def join(this_game):
    this_event = this_game.gui.player.event

    this_event.msg_init('join')
    this_event.text_box_init('Enter Name', 820, 630)

    this_game.gui.player.soft_key_create_with_handler(800, 770, 1, 'JOIN', join_selected, this_game)
    this_game.gui.player.soft_key_create_with_handler(800, 770, 2, 'JOIN AS', join_as_selected, this_game)
    this_game.gui.player.enable_row(770)
    pygame.event.clear()

    this_game.gui.player.event_wait(Gui.DuneGuiEventTypes.CLICK, None, Gui.DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
    this_game.gui.player.disable_all_row_entries(770) #disable the rows from enabling any more processing
    join_as_select = this_event.more_data_required

    #both join and join_as require the user to input a their name prompt them to do so and gather the info
    this_event.reset_dynamic_fields()
    this_event.display_text_box()
    this_game.gui.player.event_wait(Gui.DuneGuiEventTypes.TEXT, None, 0)
    this_event.msg_add_to(this_event.text)

    if True == join_as_select:  # join_as requires the user to select the character they want via soft keys
        this_event.reset_dynamic_fields()  # re-arm for new event
        this_game.gui.player.soft_key_create(800, 770, 1, 'Atreides', this_event, 'Atreides')
        this_game.gui.player.soft_key_create(800, 770, 2, 'Bene_Gesserit', this_event, 'Bene_Gesserit')
        this_game.gui.player.soft_key_create(800, 770, 3, 'Emperor', this_event, 'Emperor')
        this_game.gui.player.soft_key_create(800, 770, 4, 'Fremen', this_event, 'Fremen')
        this_game.gui.player.soft_key_create(800, 770, 5, 'Guild', this_event, 'Guild')
        this_game.gui.player.soft_key_create(800, 770, 6, 'Harkonnen', this_event, 'Harkonnen')
        this_game.gui.player.enable_row(770)
        this_game.gui.player.event_wait(Gui.DuneGuiEventTypes.CLICK, None, Gui.DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)

    this_game.format_and_send_message(this_event.msg)
    this_game.next_state()

    this_game.gui.player.clear()
    this_game.gui.player.disable_row(770)
    this_game.gui.player.disable_all_row_entries(770)

def join_selected(*args, ):
    this_game = args[0]
    this_event = this_game.gui.player.event

    this_game.gui.player.text_box(this_event.text_box_label, 12, colors.BLUE, colors.WHITE, this_event.text_box_x, \
                           this_event.text_box_y, 150, 15)
    this_event.clr_more_data_required()

def join_as_selected(*args,):
    this_game = args[0]
    this_event = this_game.gui.player.event

    this_game.gui.player.text_box(this_event.text_box_label, 12, colors.BLUE, colors.WHITE, this_event.text_box_x, \
                           this_event.text_box_y, 150, 15)
    this_event.set_more_data_required()

def waiting_to_play(this_game):
    this_event = this_game.gui.player.event
    this_event.reset()
    this_event.msg_init('')

    this_event.text_box_init('', 820, 630)

    this_game.gui.player.soft_keys_clear_all(800, 770, 6)
    this_game.gui.player.soft_key_create(800, 770, 1, 'PLAY', this_event, 'play')
    this_game.gui.player.enable_row(770)

    while this_game.state == DuneClientGameState.WAITING_TO_PLAY:
        this_game.gui.player.poll_event(Gui.DuneGuiEventTypes.CLICK, this_game.my_messaging.rcv_input, 0)
        if True == this_game.gui.player.event.is_event_of_type(Gui.DuneGuiEventHandling.CLICK):
            this_game.format_and_send_message(this_event.msg)
            this_game.state == DuneClientGameState.PLAYING
        else:
            time.sleep(.5)

    this_game.gui.player.clear()
    this_game.gui.player.disable_row(770)
    this_game.gui.player.disable_all_row_entries(770)

def playing(this_game):
    this_event = this_game.gui.player.event
    this_event.reset()

    while this_game.state == DuneClientGameState.PLAYING:
        this_game.my_messaging.rcv_input()
    time.sleep(.5)

def client_state_machine(state):
    game_management = {
        DuneClientGameState.JOINING: join,
        DuneClientGameState.WAITING_TO_PLAY: waiting_to_play,
        DuneClientGameState.PLAYING: playing,
      }
    func = game_management.get(state, playing)
    return func

def main():
    this_game = DuneClient('127.0.0.1', 5000)

    dune_client_thread(this_game)

if __name__ == '__main__':
    main()
