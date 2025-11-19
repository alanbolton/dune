from enum import Enum
import planet
import dune_gui as Gui
import troops as trps
import dune_msg as Msg

class DuneGame(Msg.DuneMsg):
    def __init__(self, is_server):
        print("creating the base Dune Class object\n")
        self.turn = 0
        self.is_server = is_server
        if True is self.is_server:
            self.gui = Gui.DuneNoGui(self)
        else:
            self.gui = Gui.DuneGui(self)

        self.planet = planet.Planet(self)
        self.planet.build_map(True)

        self.characters = dict()
        self.socket_to_character_mapping = dict()
        self.free_characters = ['Harkonnen', 'Atreides', 'Guild', 'Bene_Gesserit', 'Fremen', 'Emperor']

    def __str__(self):
        ret_str = '   characters:\n'
        for key, value in self.characters.items():
            ret_str += '      {} {} \n'.format(key, value)

        ret_str += '   planet: {}'.format(self.planet.__str__())

        return ret_str

    def find_character_by_name(self, search_name):
        the_character = None
        for key, character in self.characters.items():
            if character.name == search_name:
                the_character = character
                break
        return the_character

    def is_character_playing(self, character_name):
        char = None
        for dot, character in self.characters.items():
            if character.name == character_name:
                char = character
        return char

    def does_house_exist(self, house_name):
        if house_name not in self.free_characters:
            house_exist = True
        else:
            house_exist = False
        return house_exist

    def broadcast(self, data, is_response_needed, exclude_character):
        if True == self.is_server:
            for key, character in self.characters.items():
                if character.name != exclude_character:
                    character.send(data, is_response_needed)

    def planet_shipment(self, round, territory_name, owner, tokens, fedaykins):
        landing_party = trps.Troops(round, owner, tokens, fedaykins)
        self.planet.troops_enter(territory_name, landing_party)

    def planet_shipment_local(self, territory_name, troops):
        self.planet.troops_enter(territory_name, troops)

    def planet_ship_reinforcements(self, territory_name, owner, tokens, fedaykins):
        self.planet.troops_increase(territory_name, owner, tokens, fedaykins)

    def kill_some_troops_in_territory(self, territory, troops, tokens_killed, fedaykins_killed):
        character = self.find_character_by_name(troops.owner)
        if None != character:
            character.kill_some_troops(territory, troops, tokens_killed, fedaykins_killed)
        else:
            self.planet.troops_remove_some(territory, troops.owner, tokens_killed, fedaykins_killed)

    def kill_troops_in_territory(self, territory_name, owner):
        character = self.find_character_by_name(owner)
        if None != character:
            character.kill_all_troops(territory_name)
        else:
            self.planet.troops_remove(territory_name, owner)

    def update_benes_peacefulness(self, args):
        my_range = int(len(args) / 2)
        for x in range(my_range):
            offset = x * 2  # *2 is because we are extracting two values each loop
            territory_name = args[offset + 0]
            if args[offset + 1] == 'yes':
                im_peaceful = True
            else:
                im_peaceful = False

            benes_troops = self.planet.troops_get(territory_name, 'Bene_Gesserit')
            if benes_troops is not None:
                benes_troops.troops_peaceful_set(im_peaceful)
                msg = 'Bene {} peaceful {}'.format(territory_name, args[offset + 1])
                self.gui.player.system_info_box_write(msg)

    def block_characters_advantage(self, character_name, advantage):
        blocking = False
        for player_dot, this_character in self.characters.items():
            blocking = self.ask_character_to_block_another_characters_advantage(this_character, character_name, advantage)
            if True == blocking:
                break
        return blocking

    def ask_character_to_block_another_characters_advantage(self, ask_who, about_who, advantage):
        blocking = False
        if ask_who.name != about_who and ask_who.is_card_of_type_available('Karama'):
            msg = 'yes_no_query {} {} '.format(about_who, advantage)
            blocking = ask_who.send_query_and_wait(msg)
            if True == blocking:
                card = ask_who.get_first_card_of_type('Karama')
                msg = '{} answered yes to blocking {}  {}'.format(ask_who.name, about_who, advantage)
                ask_who.myGame.broadcast(msg, False, ask_who.name)
                ask_who.treachery_card_del(card)
        return blocking

    def find_player_with_card_and_ask_to_play(self, card_name):
        play_it = False
        for player_dot, this_character in self.characters.items():
            play_it = this_character.treachery_card_play_query(card_name)
            if True == play_it:
                break
        return play_it


