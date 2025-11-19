import colors
import pygame
from enum import Enum
import generals as Generals
import planetDune as Map
import battle as Battle
import time

TOTAL_AREA_X = 1400
TOTAL_AREA_Y = 800

ROW_HEIGHT = 100

MAP_SIZE_X = 800
MAP_SIZE_Y = 800

CARD_X = 105
CARD_Y = 150
CARD_SMALL_X = 70
CARD_SMALL_Y = 100

GENERAL_X = 115
GENERAL_Y = 115
GENERAL_SMALL_X = 85
GENERAL_SMALL_Y = 85

GENERAL_SELECTION_SPACING = 90 #used for general selectino spy, battle etc

PI = 3.141592653
TIME_EVENT = pygame.USEREVENT+1

SOFT_KEY_HEIGHT = 30
SOFT_KEY_WIDTH = 90
SOFT_KEY_SPACING = 10
SOFT_KEY_FONT_SIZE = 10
SOFT_KEY_FONT_COLOR = colors.BLACK
SOFT_KEY_BORDER_COLOR = colors.DARK_GRAY
SOFT_KEY_COLOR = colors.BEIGE
SOFT_KEY_NUMBER_OF_KEYS = 6

class DuneGuiEventTypes(Enum):
    ALL = 0
    CLICK = 1
    TEXT = 2
    TIMER = 4
class DuneGuiEventTypesControl(Enum):
    EVENT_TYPE_CTRL_NONE = 0
    EVENT_TYPE_CTRL_NUMBERS_ONLY = 1
    EVENT_TYPE_CTRL_ALPHA_ONLY = 2

class DuneGui():
    def __init__(self, my_game):
        pygame.init()
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        self.my_game = my_game
        self.clock = pygame.time.Clock()
        self.clock.tick(100)
        # pygame.time.set_timer(TIME_EVENT, 10000) this creates a pygame event not currently needed

        # Create a board
        self.game_board = pygame.display.set_mode([TOTAL_AREA_X, TOTAL_AREA_Y])

        # This sets the name of the window
        pygame.display.set_caption('DUNE... Don\'t be Harkonnen\'s Bitch!')

        # Set positions of graphics
        background_position = [0, 0]
        background_image = pygame.image.load("./DuneGameImages/duneBoard1.jpg").convert()
        background_image = pygame.transform.scale(background_image, (MAP_SIZE_X, MAP_SIZE_Y))
        pygame.draw.rect(self.game_board, colors.WHITE, [800, 315, 600, 205], 0) #spy area and spice tokens etc
        self.game_board.blit(background_image, background_position)

        self.map = GuiMap(self, 0, MAP_SIZE_X, 0, MAP_SIZE_Y)
        self.player = GuiPlayer(self, MAP_SIZE_X, TOTAL_AREA_X, 0, MAP_SIZE_Y)
        self.player.define_row_keys(SOFT_KEY_NUMBER_OF_KEYS, 800, 770, SOFT_KEY_WIDTH, SOFT_KEY_HEIGHT)

        self.map.set_storm(1, colors.LIME_GREEN)
        self.map.treachery_card_up_for_bid('TreacheryBack', 0, '', '')
        self.map.spice_card_place('SpiceBack', 1)
        self.map.spice_card_place('SpiceBack', 2)

        self.player.system_info_box_empty()

        self.player.clear()

class DuneNoGui():
    def __init__(self, my_game):
        self.my_game = my_game
        self.map = GuiAreaMapNone(self)
        self.player = GuiAreaPlayerNone(self)

#AREA objects
class GuiArea():
    def __init__(self, my_gui, x_lo, x_hi, y_lo, y_hi):
        self.my_gui = my_gui
        self.x_lo = x_lo
        self.x_hi = x_hi
        self.y_lo = y_lo
        self.y_hi = y_hi
        self.row_table = dict()  # this is row_number:ROW_OBJ

        self.event = GuiEvent(self) #for now afix an event to the GUI Area

    def process_click_event(self, event):
        click_valid = False
        search_rows = []

        row_id = self.get_row_id(event.y)
        if row_id in self.row_table:
            search_rows.append(row_id)
        # it is possible the "key" spans rows and the click isn't in the base row so we search the row prior just in case
        if event.y > ROW_HEIGHT:
            row_id = self.get_row_id((event.y - ROW_HEIGHT))
            if row_id in self.row_table:
                search_rows.append(row_id)

        for row_id in search_rows:
            row = self.row_table[row_id]
            if row.is_row_enabled == True and event.y <= row.y_hi and event.y >= row.y_lo:
                for entry in row.entry_table.values():
                    if entry.is_entry_enabled == True and event.x <= entry.x_hi and event.x >= entry.x_lo and \
                       event.y <= entry.y_hi and event.y >= entry.y_lo:
                        entry.func(*entry.args, )
                        click_valid = True
                        break
        return click_valid

    def get_row_id(self, y_lo):
        return int(y_lo / ROW_HEIGHT)

    def find_or_add_row(self, y_lo, y_hi):
        row_id = self.get_row_id(y_lo)
        if row_id not in self.row_table.keys():
            this_row = GuiRow(row_id, y_lo, y_hi)
            self.row_table[row_id] = this_row
        else:
            this_row = self.row_table[row_id]
            this_row.set_lo_hi(y_lo, y_hi)
        return this_row

    def define_row_keys(self, num_keys, key_anchor_x, key_anchor_y, key_width, key_height):
        my_row = self.find_or_add_row(key_anchor_y, (key_anchor_y + key_height))
        for key_number in range(num_keys):
            key_x = key_anchor_x + (key_number * (key_width + SOFT_KEY_SPACING))
            my_row.entry_add(key_number, key_x, (key_x + key_width), key_anchor_y, (key_anchor_y + key_height), False, no_action)

    def destroy_row(self, y_lo):
        row_id = self.get_row_id(y_lo)
        del self.row_table[row_id]

    def set_row_key_info(self, key_anchor_y, key_number, func, *args, ):
        row_id = self.get_row_id(key_anchor_y)
        my_row = self.row_table[row_id]
        my_row.entry_update(key_number, True, func, *args, )

    def enable_row(self, y_lo):  # this enables the rows if the individual entries are disabled the will remain so
        row_id = self.get_row_id(y_lo)
        this_row = self.row_table[row_id]
        this_row.is_row_enabled = True

    def enable_row_all(self):
        for row_id in range(int(TOTAL_AREA_Y / ROW_HEIGHT)):
            this_row = self.row_table[row_id]
            this_row.is_row_enabled = True

    def disable_row(self, y_lo):  # only disables the row the individual entries in the row retain their current setting
        row_id = self.get_row_id(y_lo)
        this_row = self.row_table[row_id]
        this_row.is_row_enabled = False

    def disable_row_entry(self, y_lo, key_number):
        row_id = self.get_row_id(y_lo)
        this_row = self.row_table[row_id]
        this_row.entry_disable(key_number)

    def disable_all_row_entries(self, y_lo):
        row_id = self.get_row_id(y_lo)
        this_row = self.row_table[row_id]
        for key_number in range(len(this_row.entry_table)):
            this_row.entry_disable(key_number)

    def enable_all_row_entries(self, y_lo):
        row_id = self.get_row_id(y_lo)
        this_row = self.row_table[row_id]
        for key_number in range(len(this_row.entry_table)):
            this_row.entry_enable(key_number)

    def enable_row_entry(self, y_lo, key_number):
        row_id = self.get_row_id(y_lo)
        this_row = self.row_table[row_id]
        this_row.entry_enable(key_number)

    def text_box(self, text, font_size, color, font_color, x, y, width, height):
        myText = pygame.font.Font('freesansbold.ttf', font_size)
        mySurf, myRect = text_box_object(text, font_color, myText)
        myRect.center = ((x + int((width/2))), (y + int((height/2))))
        pygame.draw.rect(self.my_gui.game_board, color, [x, y, width, height], 0)
        self.my_gui.game_board.blit(mySurf, myRect)

        pygame.display.flip()

    def text_circle(self, text, font_size, color, font_color, x, y, radius):
        myText = pygame.font.Font('freesansbold.ttf', font_size)
        mySurf, myRect = text_circle_object(text, font_color, myText)
        myRect.center = (x, y)
        pygame.draw.circle(self.my_gui.game_board, color, [x, y], radius)
        self.my_gui.game_board.blit(mySurf, myRect)

    def event_wait(self, requested_event, client_poll_func, event_control):
        while self.event.type == DuneGuiEventHandling.NO_EVENT or self.event.type == DuneGuiEventHandling.IN_PROGRESS:
            self.poll_event(requested_event, client_poll_func, event_control)

    def poll_event(self, requested_event, client_poll_func, event_control):
        poll_for_event(self, requested_event, event_control)
        if None != client_poll_func:
            client_poll_func()

class GuiMap(GuiArea):
    def __init__(self, my_gui, x_lo, x_hi, y_lo, y_hi):
        super().__init__(my_gui, x_lo, x_hi, y_lo, y_hi)

    def player_dot_set(self, player_dot, character, player_name):
        b, t = character_colors_get(character)
        if 2 == player_dot:
            x = 400
            y = 775
            name_x = 420
            name_y = 765
        elif 5 == player_dot:
            x = 725
            y = 580
            name_x = 735
            name_y = 570
        elif 8 == player_dot:
            x = 725
            y = 210
            name_x = 735
            name_y = 200
        elif 11 == player_dot:
            x = 400
            y = 20
            name_x = 420
            name_y = 10
        elif 14 == player_dot:
            x = 75
            y = 210
            name_x = 0
            name_y = 200
        elif 17 == player_dot:
            x = 75
            y = 585
            name_x = 0
            name_y = 575
        self.text_circle('', 10, b, t, x, y, 10)
        self.text_box(player_name, 10, b, t, name_x, name_y, 60, 10)

    def set_storm(self, sector, color):
        num = 11 + sector
        if num >= 18:
            num -= 18
        start_point = (num * 20 * PI) / 180
        stop_point = (((num * 20) + 22) * PI) / 180

        pygame.draw.arc(self.my_gui.game_board, color, [40, 30, 725, 735], start_point, stop_point, 5)

    def troops_place(self, who, tokens, fedaykins, fedaykins_valid, box_x, box_y, offset, num_occupants):
        y = box_y + 10
        x = (box_x + 10) + (offset * 20)

        if False is fedaykins_valid:
            troops = '{}'.format(tokens)
        else:
            troops = '{}/{}'.format(tokens, fedaykins)

        if who != '':
            b, t = character_colors_get(who)
            self.text_circle(troops, 12, b, t, x, y, 10)

        x = (box_x + 10) + (num_occupants * 20)
        self.text_circle('', 12, colors.SILVER, colors.SILVER, x, y, 10)

        pygame.display.update()

    def spice_card_place(self, card, deck):
        image = pygame.image.load(r'./DuneGameImages/SpiceCards/{}.gif'.format(card))
        image = pygame.transform.scale(image, (CARD_X, CARD_Y))

        if 1 == deck:
            x = 20
        else:
            x = 690
        y = 650
        self.my_gui.game_board.blit(image, (x, y))

        pygame.display.update()

    def spice_territory_update(self, amount, x, y):
        if amount == 0:
            self.text_box('*', 12, colors.LIGHT_BLUE, colors.BLACK, x, y, 15, 15)
        else:
            self.text_box('{}'.format(amount), 12, colors.LIGHT_BLUE, colors.BLACK, x, y, 15, 15)
        pygame.display.update()

    def treachery_card_up_for_bid(self, card, amount, who, next_bidder):
        image = pygame.image.load(r'./DuneGameImages/TreacheryCards/{}.gif'.format(card))
        image = pygame.transform.scale(image, (CARD_X, CARD_Y))
        self.my_gui.game_board.blit(image, (10, 10))
        if card != 'TreacheryBack':
            b, t = character_colors_get(who)
            self.text_box('{}'.format(amount), 20, colors.LIGHT_BLUE, b, 115, 10, 20, 20)
            b1, t1 = character_colors_get(next_bidder)
            self.text_circle('', 12, b1, t1, 125, 40, 10)
        else:
            self.text_box(''.format(amount), 20, colors.LIGHT_BLUE, colors.LIGHT_BLUE, 115, 10, 20, 20)
            self.text_circle('', 12, colors.SILVER, colors.SILVER, 125, 40, 10)

        pygame.display.update()

    def place_troop_markers(self):
        for row_id in range(int(TOTAL_AREA_Y/ROW_HEIGHT)):
            marker_list = Map.troop_markers_by_row(row_id)
            row_y_lo = row_id * 100
            row_y_hi = (row_id * 100) + (ROW_HEIGHT - 1)
            this_row = self.find_or_add_row(row_y_lo, row_y_hi)

            entry_id = 0
            for marker in marker_list:
                for x, y, name in marker:
                    this_row.entry_add(entry_id, x, x+60, y, y+20, True, append_args_to_msg_and_click_info, self.event, name)
                    entry_id += 1

    def enable(self):
        self.enable_row_all()

class GuiPlayer(GuiArea):
    def __init__(self, my_gui, x_lo, x_hi, y_lo, y_hi):
        super().__init__(my_gui, x_lo, x_hi, y_lo, y_hi)

    def soft_key_create(self, key_base_x, key_base_y, key_number, text, *args, ):
        self.soft_key_create_with_colors(key_base_x, key_base_y, key_number, text, SOFT_KEY_COLOR, SOFT_KEY_FONT_COLOR, *args, )

    def soft_key_create_with_handler(self, key_base_x, key_base_y, key_number, text, func, *args, ):
        self.soft_key_create_with_colors_and_handler(key_base_x, key_base_y, key_number, text, SOFT_KEY_COLOR, SOFT_KEY_FONT_COLOR, func, *args, )

    def soft_key_create_with_colors(self, key_base_x, key_base_y, key_number, text, key_color, font_color, *args, ):
        self.soft_key_create_with_colors_and_handler(key_base_x, key_base_y, key_number, text, key_color, font_color, append_args_to_event_msg, *args, )

    def soft_key_create_with_colors_and_handler(self, key_base_x, key_base_y, key_number, text, key_color, font_color, func, *args, ):
        self.soft_key(key_number, text, key_base_x, key_base_y, key_color, font_color)
        self.set_row_key_info(key_base_y, (key_number - 1), func, *args, )

    def soft_key(self, key_number, text, key_base_x, key_base_y, key_color, font_color):
        y_co = key_base_y
        x_co = key_base_x + ((key_number - 1) * 100) #key_number is 1 based needs to be 0 based for this calculation
        self.text_box(text, SOFT_KEY_FONT_SIZE, key_color, font_color, x_co, y_co, SOFT_KEY_WIDTH, SOFT_KEY_HEIGHT)
        pygame.draw.rect(self.my_gui.game_board, SOFT_KEY_BORDER_COLOR, [x_co, y_co, SOFT_KEY_WIDTH, SOFT_KEY_HEIGHT], 5)

    def soft_keys_clear_all(self, key_base_x, key_base_y, num_keys):
        self.disable_all_row_entries(key_base_y)
        pygame.draw.rect(self.my_gui.game_board, colors.WHITE, [key_base_x, key_base_y, (num_keys * 100), SOFT_KEY_HEIGHT], 0)

    def treachery_card_place(self, card, position):
        if position <= 4:
            y = 5
            offset = position - 1  # need this to be zero based
        else:
            y = 160
            offset = position - 5  # need this to be zero based for positions 5 - 8

        x = 800 + (150 * offset)
        image = pygame.image.load(r'./DuneGameImages/TreacheryCards/{}.gif'.format(card))
        image = pygame.transform.scale(image, (CARD_X, CARD_Y))
        self.my_gui.game_board.blit(image, (x, y))

        pygame.display.update()

    def treachery_card_choice_place(self, card, position, x, y, spacing):
        offset = position - 1  # need this to be zero based

        x = x + (spacing * offset)
        image = pygame.image.load(r'./DuneGameImages/TreacheryCards/{}.gif'.format(card))
        image = pygame.transform.scale(image, (CARD_SMALL_X, CARD_SMALL_Y))
        self.my_gui.game_board.blit(image, (x, y))

        pygame.display.update()

    def general_place(self, house, general, position):
        offset = position - 1 #we need this to be 0 based.
        x_coordinate = 800 + (offset * 120)
        image = pygame.image.load(r'./DuneGameImages/Generals/{}/{}.png'.format(house, general))
        image = pygame.transform.scale(image, (GENERAL_X, GENERAL_Y))
        self.my_gui.game_board.blit(image, (x_coordinate, 315))

        pygame.display.update()

    def general_attriute_add(self, attribute, color, position):
        offset = position - 1 #we need this to be 0 based.
        x_coordinate = 820 + (offset * 120)
        new_font = pygame.font.Font(None, 30)
        text = new_font.render(attribute, True, color)
        self.my_gui.game_board.blit(text, [x_coordinate, 365])

        pygame.display.update()

    def spy_suspects_place(self, general, position, base_x, base_y):
        offset = position - 1 #we need this to be 0 based.
        x_coordinate = base_x + (offset * GENERAL_SELECTION_SPACING)
        house = Generals.get_house_by_general(general)
        image = pygame.image.load(r'./DuneGameImages/Generals/{}/{}.png'.format(house, general))
        image = pygame.transform.scale(image, (GENERAL_SMALL_X, GENERAL_SMALL_Y))
        self.my_gui.game_board.blit(image, (x_coordinate, base_y))

        pygame.display.update()

    def spy_declare(self, position):
        offset = position - 1 #we need this to be 0 based.
        x_coordinate = 1065 + (offset * 90)
        new_font = pygame.font.Font(None, 25)
        text = new_font.render('SPY', True, colors.RED)
        self.my_gui.game_board.blit(text, [x_coordinate, 460])

        pygame.display.update()

    def system_info_box_empty(self):
        self.sys_info_line = 0
        self.sys_previous_info_line = 0
        self.text_box('System Updates:', 10, colors.WHITE, colors.DEEP_SKY_BLUE, 800, 460, 240, 10)
        self.text_box('', 10, colors.WHITE, colors.BLACK, 800, 470, 240, 10)
        self.text_box('', 10, colors.WHITE, colors.BLACK, 800, 480, 240, 10)
        self.text_box('', 10, colors.WHITE, colors.BLACK, 800, 490, 240, 10)
        self.text_box('', 10, colors.WHITE, colors.BLACK, 800, 500, 240, 10)
        self.text_box('', 10, colors.WHITE, colors.BLACK, 800, 510, 240, 10)
        pygame.draw.rect(self.my_gui.game_board, colors.BLACK, [800, 460, 240, 60], 1)

    def system_info_box_write(self, text):
        if self.sys_info_line != self.sys_previous_info_line:
            offset = 470 + (self.sys_previous_info_line * 10)
            pygame.draw.rect(self.my_gui.game_board, colors.WHITE, [800, offset, 10, 5], 0)

        offset = 470 + (self.sys_info_line * 10)
        pygame.draw.rect(self.my_gui.game_board, colors.RED, [800, offset, 10, 5], 0)
        self.text_box(text, 10, colors.WHITE, colors.BLACK, 805, offset, 240, 10)
        self.sys_previous_info_line = self.sys_info_line
        self.sys_info_line = (self.sys_info_line + 1) % 5
        pygame.draw.rect(self.my_gui.game_board, colors.BLACK, [800, 460, 240, 60], 1)

    def clear(self):
        pygame.draw.rect(self.my_gui.game_board, colors.WHITE, [800, 520, 600, 280], 0)
        pygame.display.update()

    def spice_amount_update(self, spice):
        self.text_box('{}'.format(spice), 20, colors.LIGHT_BLUE, colors.BLACK, 800, 435, 20, 20)
        pygame.display.update()

    def tokens_update(self, who, how_many):
        b, t = character_colors_get(who)
        self.text_circle('{}'.format(int(how_many)), 15, b, t, 835, 445, 10)

    def fedaykins_update(self, who, how_many):
        b, t = character_colors_get(who)
        self.text_circle('*{}'.format(int(how_many)), 15, b, t, 860, 445, 10)

    def kwisatz_haderach_update(self, how_many):
        self.text_circle('{}'.format(how_many), 15, colors.GREEN, colors.RED, 860, 445, 10)

    def next_spice_blow_vision(self, where1, amount1, where2, amount2):
        b, t = character_colors_get('Atreides')
        self.text_box('{} {}'.format(where1, amount1), 8, b, t, 875, 435, 130, 10)
        self.text_box('{} {}'.format(where2, amount2), 8, b, t, 875, 445, 130, 10)

    def next_storm_movement(self, how_much):
        b, t = character_colors_get('Fremen')
        self.text_box('Next Strom: {}'.format(how_much), 12, b, t, 875, 435, 130, 20)

    def benes_prediction_update(self, who, when):
        b, t = character_colors_get('Bene_Gesserit')
        self.text_box('{} {}'.format(who, when), 12, b, t, 875, 435, 130, 20)

    def captured_general_place(self, house, general, position, any_spies_in_display):
        offset = position - 1  # we need this to be 0 based.
        if 0 == any_spies_in_display:
            x_coordinate = 1045 + (offset * 90)
            y_coordinate = 435
        else:
            x_coordinate = 1045 + (offset * 90)
            y_coordinate = 525

        image = pygame.image.load(r'./DuneGameImages/Generals/{}/{}.png'.format(house, general))
        image = pygame.transform.scale(image, (GENERAL_SMALL_X, GENERAL_SMALL_Y))
        self.my_gui.game_board.blit(image, (x_coordinate, y_coordinate))
        new_font = pygame.font.Font(None, 20)
        text = new_font.render('Captured', True, colors.RED)
        self.my_gui.game_board.blit(text, [x_coordinate, (y_coordinate + 30)])
        pygame.display.update()

    def captured_general_clear(self, number_to_clear, any_spies_in_display):
        hieght = GENERAL_SMALL_Y
        width = (GENERAL_SMALL_X + 5) * number_to_clear
        x_coordinate = 1045
        if 0 != any_spies_in_display:
            y_coordinate = 435
        else:
            y_coordinate = 525
        pygame.draw.rect(self.my_gui.game_board, colors.WHITE, [x_coordinate, y_coordinate, width, hieght], 0)
        pygame.display.update()

#For Servers with no GUI
class GuiAreaNone():
    def __init__(self, my_gui):
        self.my_gui = my_gui

    def process_click_event(self, event):
        pass

    def get_row_id(self, y_lo):
        pass

    def find_or_add_row(self, y_lo, y_hi):
        pass

    def define_row_keys(self, num_keys, key_anchor_x, key_anchor_y, key_width, key_height):
        pass

    def destroy_row(self, y_lo):
        pass

    def set_row_key_info(self, key_anchor_y, key_number, func, *args, ):
        pass

    def enable_row(self, y_lo):  # this enables the rows if the individual entries are disabled the will remain so
        pass

    def enable_row_all(self):
        pass

    def disable_row(self, y_lo):  # only disables the row the individual entries in the row retain their current setting
        pass

    def disable_row_entry(self, y_lo, key_number):
        pass

    def disable_all_row_entries(self, y_lo):
        pass

    def enable_all_row_entries(self, y_lo):
        pass

    def enable_row_entry(self, y_lo, key_number):
        pass

    def text_box(self, text, font_size, color, font_color, x, y, width, height):
        pass

    def text_circle(self, text, font_size, color, font_color, x, y, radius):
        pass

    def event_wait(self, requested_event, client_poll_func, event_control):
        pass

    def poll_event(self, requested_event, client_poll_func, event_control):
        pass

class GuiAreaMapNone(GuiAreaNone):
    def __init__(self, my_gui):
        super().__init__(my_gui)

    def player_dot_set(self, player_dot, character, player_name):
        pass

    def set_storm(self, sector, color):
        pass

    def troops_place(self, who, tokens, fedaykins, fedaykins_valid, box_x, box_y, offset, num_occupants):
        pass

    def spice_card_place(self, card, deck):
        pass

    def spice_territory_update(self, amount, x, y):
        pass

    def place_troop_markers(self):
        pass

    def enable(self):
        pass

class GuiAreaPlayerNone(GuiAreaNone):
    def __init__(self, my_gui):
        super().__init__(my_gui)

    def soft_key(self, key_number, text, key_base_x, key_base_y, key_color, font_color):
        pass

    def soft_keys_clear_all(self, key_base_x, key_base_y, num_keys):
        pass

    def treachery_card_place(self, card, position):
        pass

    def treachery_card_choice_place(self, card, position, x, y, spacing):
        pass

    def treachery_card_up_for_bid(self, card, amount, who, next_bidder):
        pass

    def general_place(self, house, general, position):
        pass

    def general_attriute_add(self, attribute, color, position):
        pass

    def spy_suspects_place(self, general, position, base_x, base_y):
        pass

    def spy_declare(self, position):
        pass

    def system_info_box_empty(self):
        pass

    def system_info_box_write(self, text):
        pass

    def clear(self):
        pass

    def spice_amount_update(self, spice):
        pass

    def tokens_update(self, who, how_many):
        pass

    def fedaykins_update(self, who, how_many):
        pass

    def kwisatz_haderach_update(self, how_many):
        pass

    def next_spice_blow_vision(self, where1, amount1, where2, amount2):
        pass

    def next_storm_movement(self, how_much):
        pass

    def benes_prediction_update(self, who, when):
        pass

    def captured_general_place(self, house, general, position, any_spies_in_display):
        pass

    def captured_general_clear(self, number_to_clear, any_spies_in_display):
        pass

#ROW, ROW_ENTRIES and EVENTs
class GuiRow():
    def __init__(self, id, y_lo, y_hi):
        self.is_row_enabled = False
        self.id = id
        self.y_lo = y_lo
        self.y_hi = y_hi
        self.entry_table = dict()  # this is entry_id:GuiRowEntry

    def set_lo_hi(self, lo, hi):
        self.y_lo = lo
        self.y_hi = hi

    def row_delete(self, row_id):
        self.entry_table = dict()  # this is entry_id:GuiRowEntry

    def row_enable(self, row_id):
        self.is_row_enabled = True

    def row_disable(self, row_id):
        self.is_row_enabled = False

    def entry_add(self, id, x_lo, x_hi, y_lo, y_hi, enable_entry, func, *args, ):
        if len(args):
            new_entry = GuiRowEntry(x_lo, x_hi, y_lo, y_hi, enable_entry, func, *args)
        else:
            new_entry = GuiRowEntry(x_lo, x_hi, y_lo, y_hi, enable_entry, func)
        self.entry_table[id] = new_entry

    def entry_enable(self, key_number):
        this_entry = self.entry_table[key_number]
        this_entry.enable()

    def entry_disable(self, key_number):
        this_entry = self.entry_table[key_number]
        this_entry.disable()

    def entry_disable_all(self):
        for this_entry in self.entry_table.vaues():
            this_entry.disable()

    def entry_update(self, key_number, is_enabled, func, *args, ):
        this_entry = self.entry_table[key_number]
        this_entry.update(is_enabled, func, *args, )


class GuiRowEntry():
    def __init__(self, x_lo, x_hi, y_lo, y_hi, enable_entry, func, *args):
        self.is_entry_enabled = enable_entry
        self.x_lo = x_lo
        self.x_hi = x_hi
        self.y_lo = y_lo
        self.y_hi = y_hi
        self.func = func
        self.args = args

    def enable(self):
        self.is_entry_enabled = True

    def disable(self):
        self.is_entry_enabled = False

    def update(self, enable_entry, func, *args, ):
        self.is_entry_enabled = enable_entry
        self.func = func
        self.args = args

    def is_a_match(self, x, y):
        if x >= self.x_lo and x <= self.x_hi and y >= y_lo and y <= y_hi:
            match = True
        else:
            match = False
        return match

class DuneGuiEventHandling(Enum):
    NO_EVENT = 0
    IN_PROGRESS = 1
    TEXT = 2
    CLICK = 3
    TIMER = 4

class GuiEvent():
    def __init__(self, my_area):
        self.type = DuneGuiEventHandling.NO_EVENT
        self.my_area = my_area
        self.x = 0
        self.y = 0
        self.click_info = None
        self.text = ''
        self.text_box_label = ''
        self.text_box_x = 0
        self.text_box_y = 0
        self.more_data_required = False
        self.msg = None
        self.value = None

    def __str__(self):
        ret_str = '{} x: {} y: {} text{}'.format(self.type, self.x, self.y, self.text)
        return ret_str

    def set_type(self, this_type):
        self.type = this_type

    def reset_type(self):
        self.type = DuneGuiEventHandling.NO_EVENT

    def is_event_of_type(self, this_type):
        return (self.type == this_type)

    def reset(self):
        self.reset_dynamic_fields()
        self.text_box_label = ''
        self.text_box_x = 0
        self.text_box_y = 0
        self.msg = None

    def reset_dynamic_fields(self):
        self.type = DuneGuiEventHandling.NO_EVENT
        self.x = 0
        self.y = 0
        self.click_info = None
        self.text = ''
        self.value = None
        self.more_data_required = False

    def add_char(self, char):
        self.text += char

    def del_char(self):
        self.text = self.text[:-1]

    def set_click_coordinates(self, x, y):
        self.type = DuneGuiEventHandling.CLICK
        self.x = x
        self.y = y

    def text_box_init(self, new_label, x, y):
        self.text_box_label = new_label
        self.text_box_x = x
        self.text_box_y = y

    def set_text_box_label(self, new_label):
        self.text_box_label = new_label

    def msg_init(self, msg):
        self.msg = msg

    def msg_add_to(self, data):
        if len(self.msg) == 0:
            self.msg = data
        else:
            self.msg = '{} {}'.format(self.msg, data)

    def set_more_data_required(self):
        self.more_data_required = True

    def clr_more_data_required(self):
        self.more_data_required = False

    def display_text_box(self):
        if self.text_box_label != '':
            string = '{}: {}'.format(self.text_box_label, self.text)
            pygame.draw.rect(self.my_area.my_gui.game_board, colors.WHITE, [self.text_box_x, self.text_box_y, 150, 15], 0)
            self.my_area.text_box(string, 12, colors.BLUE, colors.WHITE, self.text_box_x, self.text_box_y, 150, 15)
        pygame.display.update()

#GUI command wrappers for handling interaction with user
def dune_gui_benes_prediction(this_game):
    this_event = this_game.gui.player.event

    num_of_choices = (len(this_game.characters_playing) - 1) #don't include self in num of choices

    this_game.gui.player.text_box('Prediction Player/Round', 15, colors.GOLD, colors.BLACK, 820, 600, 560, 20)
    this_game.gui.player.define_row_keys(num_of_choices, 820, 630, SOFT_KEY_WIDTH, SOFT_KEY_HEIGHT)

    key_number = 1
    this_event.reset()
    for player in this_game.characters_playing:
        if player != 'Bene_Gesserit':
            b, t = character_colors_get(player)
            this_game.gui.player.soft_key_create_with_colors(820, 630, key_number, player, b, t, this_event, player)
            key_number += 1

    this_event.msg_init('prediction')
    pygame.event.clear()
    this_game.gui.player.enable_row(630)

    this_game.gui.player.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
    this_game.gui.player.disable_all_row_entries(630)
    this_game.gui.player.disable_row(630)

    this_event.reset_dynamic_fields()
    this_event.text_box_init('Round: ', 820, 630)
    this_event.display_text_box()
    this_game.gui.player.event_wait(DuneGuiEventTypes.TEXT, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NUMBERS_ONLY)
    this_event.msg_add_to(this_event.text)

    this_game.format_and_send_message(this_event.msg)
    this_game.gui.player.clear()
    this_game.gui.player.disable_row(770)
    this_game.gui.player.disable_all_row_entries(770)

    return True

def dune_gui_spy_selection(this_game, suspect_list):
    processed = False
    this_event = this_game.gui.player.event

    count = 1
    for suspect in suspect_list:
        house = Generals.get_house_by_general(suspect)
        this_game.gui.player.spy_suspects_place(suspect, count, 820, 630)
        count += 1

    this_game.gui.player.text_box('Choose SPY', 15, colors.BLUE, colors.WHITE, 820, 600, (len(suspect_list) * 90), 30)
    this_game.gui.player.define_row_keys(count, 820, 630, GENERAL_SMALL_X, GENERAL_SMALL_Y)
    count = 0
    for suspect in suspect_list:
        this_game.gui.player.set_row_key_info(630, count, append_args_to_event_msg, this_event, suspect)
        count += 1

    this_event.reset()
    this_event.msg_init('spy_select')
    this_game.gui.player.enable_row(630)
    this_game.gui.player.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
    this_game.format_and_send_message(this_event.msg)

    this_game.gui.player.clear()
    this_game.gui.player.disable_row(630)
    this_game.gui.player.disable_all_row_entries(630)

def append_args_to_event_msg(*args):
    this_event = args[0]
    num_to_append = len(args) - 1

    for x in range(num_to_append):
        this_event.msg_add_to(args[1 + x])

def append_args_to_msg_and_click_info(*args):
    this_event = args[0]
    this_event.msg_add_to(args[1])
    this_event.click_info = args[1]

def place_args_to_click_info(*args):
    this_event = args[0]
    this_event.click_info = args[1]

def player_bidding(this_game, character, bid_amount):
    gui = this_game.gui
    this_event = gui.player.event

    this_event.reset()

    if bid_amount >= character.spice:
        # This player doesn't have enough spice so auto generate a 'pass' response
        msg = 'Info you have {} spice and the bid is {}'.format(character.spice, bid_amount)
        gui.player.system_info_box_write(msg)
        msg = 'pass'
        character.send(msg, False)
    else:
        this_event.reset()
        pay_buttons = 4  # max soft keys with descreate values is 4 (6 - pass/other) if karma available this is reduced

        gui.player.soft_key_create(800, 770, 1, 'PASS', this_event, 'pass')

        if True == character.is_card_of_type_available('Karama') and character.name != 'Emperor':
            pay_buttons -= 1
            gui.player.soft_key_create_with_handler(800, 770, 6, 'Pay w/ Karama', bid_with_karama, this_event, character)

        soft_key_base = 2  # this is soft key number subtract 1 to get index for "set_row_key_info"
        spice_value = bid_amount + 1
        for loop in range(pay_buttons):
            key_number = soft_key_base + loop
            if character.spice >= spice_value:
                gui.player.soft_key_create(800, 770, key_number, '{}'.format(spice_value), this_event, spice_value)
                spice_value += 1

        if spice_value <= character.spice:
            gui.player.soft_key_create_with_handler(800, 770, (pay_buttons + 2), 'Other Value', bid_with_value, this_event)

        this_event.msg_init('treachery_card_bid')
        pygame.event.clear()
        gui.player.enable_row(770)

        this_game.gui.player.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
        if True == this_event.more_data_required:
            this_event.reset_dynamic_fields()
            this_game.gui.player.disable_all_row_entries(770)
            this_event.text_box_init('Bid Amount: ', 820, 630)
            this_event.display_text_box()
            this_game.gui.player.event_wait(DuneGuiEventTypes.TEXT, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NUMBERS_ONLY)
            this_event.msg_add_to(this_event.text)
            if None != this_event.value:
                this_event.msg_add_to(this_event.value)
        if this_event.click_info == 'pass':
            this_event.msg_init('pass')
        this_game.format_and_send_message(this_event.msg)

    pygame.draw.rect(this_game.gui.game_board, colors.WHITE, [800, 770, 600, 30], 0) #remove the yes/no keys
    this_game.gui.player.disable_row(770)
    this_game.gui.player.disable_all_row_entries(770)

def bid_with_karama(*args,):
    this_event = args[0]
    who = args[1]

    this_event.value = who.get_first_card_of_type('Karama')
    this_event.set_more_data_required()

def bid_with_value(*args,):
    this_event = args[0]
    this_event.set_more_data_required()

def dune_gui_play_karama(this_game, character, reason):
    card = None
    play_karama = False
    karama_card_list = []
    this_event = this_game.gui.player.event

    this_game.gui.player.clear()

    count = 1
    for card in character.treachery_cards.keys():
        if character.is_card_type_karama(card):
            karama_card_list.append(card)
            this_game.gui.player.treachery_card_choice_place(card, count, 820, 600, CARD_SMALL_X)
            count += 1

    this_game.gui.player.soft_key_create_with_handler(800, 770, 1, 'PASS', place_args_to_click_info, this_event, 'pass')

    this_game.gui.player.text_box(reason, 12, colors.BLUE, colors.WHITE, 820, 570, 200, 30)
    this_game.gui.player.define_row_keys(count, 820, 600, CARD_SMALL_X, CARD_SMALL_Y)
    count = 0
    for card in karama_card_list:
        this_game.gui.player.set_row_key_info(630, count, place_args_to_click_info, this_event, card)
        count += 1

    this_event.reset()
    this_game.gui.player.enable_row(600)
    this_game.gui.player.enable_row(770)

    this_game.gui.player.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
    if 'pass' != this_event.click_info:
        card = this_event.click_info
        play_karama = True

    this_game.gui.player.clear()
    this_game.gui.player.disable_row(600)
    this_game.gui.player.disable_all_row_entries(600)
    this_game.gui.player.disable_row(770)
    this_game.gui.player.disable_all_row_entries(770)

    pygame.display.update()

    return play_karama, card

def dune_gui_place_or_beam_reqeust(this_game, cmd, tokens, fedaykins):
    processed = False
    beam_requested = False

    player_gui = this_game.gui.player
    map_gui = this_game.gui.map

    if cmd == 'place':
        key_text = 'PLACE'
    else:
        key_text = 'BEAM'
    map_gui.event = this_game.gui.map.event
    player_gui.soft_key_create_with_handler(800, 770, 1, 'PASS', place_args_to_click_info, player_gui.event, 'pass')
    player_gui.soft_key_create_with_handler(800, 770, 2, key_text, place_args_to_click_info, player_gui.event, 'beam')
    player_gui.event.reset()
    player_gui.enable_row(770)

    player_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)

    if player_gui.event.click_info == 'beam':
        map_gui.event.reset()
        map_gui.event.msg_init('')
        processed = dune_gui_beam_info_get(map_gui, tokens, fedaykins)
        if True == processed:
            map_gui.event.msg_init('{} {}'.format(cmd, map_gui.event.msg))
            beam_requested = True

    elif player_gui.event.click_info == 'pass':
        map_gui.event.msg_init('pass')
        processed = True

    return processed, beam_requested

def  dune_gui_move_between_territories(this_game, cmd, who):
    processed = False
    player_gui = this_game.gui.player
    map_gui = this_game.gui.map

    player_event = player_gui.event
    player_event.reset()
    map_event = map_gui.event
    map_event.reset()

    player_gui.soft_key_create_with_handler(800, 770, 1, 'PASS', place_args_to_click_info, player_gui.event, 'pass')
    player_gui.soft_key_create_with_handler(800, 770, 2, 'MOVE', place_args_to_click_info, player_gui.event, 'move')
    player_gui.event.reset()
    player_gui.enable_row(770)
    player_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)

    if player_event.click_info == 'move':
        processed = beam_between(this_game.gui, cmd, who)

    elif player_event.click_info == 'pass':
        map_event.msg_init('pass')
        processed = True

    return processed

def dune_gui_guild_beaming(this_game, tokens, fedaykins):
    processed = False

    player_gui = this_game.gui.player
    map_gui = this_game.gui.map

    player_event = player_gui.event
    map_event = map_gui.event

    player_event.reset()
    player_gui.soft_key_create_with_handler(800, 770, 1, 'PASS', place_args_to_click_info, player_gui.event, 'pass')
    player_gui.soft_key_create_with_handler(800, 770, 2, 'From Resreves', place_args_to_click_info, player_gui.event, 'from')
    player_gui.soft_key_create_with_handler(800, 770, 3, 'To Resreves', place_args_to_click_info, player_gui.event, 'to')
    player_gui.soft_key_create_with_handler(800, 770, 4, 'Between Sites', place_args_to_click_info, player_gui.event, 'between')
    player_gui.event.reset()
    player_gui.enable_row(770)

    map_event.msg_init('beam_between_request')
    player_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
    if player_event.click_info == 'from': #from reserves is a normal beam for other characters use that logic
        map_gui.event.reset()
        map_gui.event.msg_init('')
        processed = dune_gui_beam_info_get(map_gui, tokens, fedaykins)
        if True == processed:
            map_gui.event.msg_init('{} {}'.format('beam_request', map_gui.event.msg))
    elif player_event.click_info == 'to':
        map_gui.event.reset()
        map_gui.event.msg_init('')
        processed = dune_gui_beam_info_get(map_gui, tokens, fedaykins)
        if True == processed:
            from_territory, tokens, fedaykins = map_gui.event.msg.split(' ')
            msg = 'beam_between_request {} reserve {} {}'.format(from_territory, tokens, fedaykins)
            map_gui.event.msg_init(msg)
    elif player_event.click_info == 'between':
        processed = beam_between(this_game.gui, 'beam_between_request', 'Guild')
    else:
        map_event.msg_init('pass')
        processed = True
    return processed


def beam_between(gui, cmd, who):
    map_gui = gui.map

    map_event = map_gui.event

    map_event.msg_init(cmd)
    map_event.text_box_init('Choose Start', 820, 630)
    map_event.display_text_box()

    map_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)

    if map_event.click_info != None:
        territory = gui.my_game.planet.find_territory(map_event.click_info)
        troops = territory.get_troops_by_owner(who)
        if None != troops:
            processed = dune_gui_beam_info_get(map_gui, troops.tokens, troops.fedaykins)
        else:
            processed = False
            gui.player.system_info_box_write('Err Movement no Troops to move')
    else:
        processed = False
        print('Err not check beam between in gui')
    return processed


# in this_game.gui.map.event.msge we'll store <territory><Tokens><Fedaykins>
def dune_gui_beam_info_get(map_gui, tokens, fedaykins):
    tokens_entered = 0
    fedaykins_entered = 0

    map_gui.event.text_box_init('Choose Territory', 820, 630)
    map_gui.event.display_text_box()

    map_gui.event.reset_dynamic_fields()

    map_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)

    map_gui.event.reset_dynamic_fields()
    map_gui.event.set_text_box_label('Enter Troops:')
    map_gui.event.display_text_box()
    map_gui.event_wait(DuneGuiEventTypes.TEXT, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NUMBERS_ONLY)
    map_gui.event.msg_add_to(map_gui.event.text)
    tokens_entered = int(map_gui.event.text)

    if 0 != fedaykins:
        map_gui.event.reset_dynamic_fields()
        map_gui.event.set_text_box_label('Enter Fedaykins:')
        map_gui.event.display_text_box()
        map_gui.event_wait(DuneGuiEventTypes.TEXT, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NUMBERS_ONLY)
        map_gui.event.msg_add_to(map_gui.event.text)
        fedaykins_entered = int(map_gui.event.text)
    else:
        map_gui.event.msg_add_to('0')

    if tokens_entered > tokens or fedaykins_entered > fedaykins:
        processed = False
    else:
        processed = True

    return processed

def dune_gui_yes_no_query(this_game, who, question, prompt_for_value):
    is_answer_yes = True
    this_event = this_game.gui.player.event
    player_gui = this_game.gui.player

    the_query = '{} {}'.format(who, question)
    this_game.gui.player.text_box(the_query, 15, colors.GOLD, colors.BLACK, 820, 750, 560, 20)

    player_gui.soft_key_create_with_colors_and_handler(800, 770, 1, 'YES', colors.GREEN, colors.WHITE, \
                                                       place_args_to_click_info, this_event, 'yes')
    player_gui.soft_key_create_with_colors_and_handler(800, 770, 2, 'NO', colors.RED, colors.WHITE, \
                                                       place_args_to_click_info, this_event, 'no')

    this_event.reset_dynamic_fields()
    this_event.msg_init('yes_no_response')
    pygame.event.clear()
    this_game.gui.player.enable_row(770)

    this_game.gui.player.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
    this_game.gui.player.disable_all_row_entries(770)
    this_game.gui.player.disable_row(770)
    pygame.draw.rect(this_game.gui.game_board, colors.WHITE, [800, 750, 580, 50], 0) #remove the yes/no keys

    if 'yes' == this_event.click_info and True == prompt_for_value:
        this_event.reset_dynamic_fields()
        this_event.text_box_init('Enter Number: ', 820, 630)
        this_event.display_text_box()
        this_game.gui.player.event_wait(DuneGuiEventTypes.TEXT, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NUMBERS_ONLY)
        this_event.msg_add_to(this_event.text)
    elif 'yes' == this_event.click_info and False == prompt_for_value:
        this_event.msg_add_to(question)
    else:
        is_answer_yes = False
        this_event.msg_init('pass')

    pygame.display.update()

    return is_answer_yes, this_event.msg

def dune_gui_atreides_battle_vison_request(this_game, is_blocked, karama_card):
    is_choice_needed = False
    player_gui = this_game.gui.player
    player_event = player_gui.event

    this_game.gui.player.text_box('Select Opponents Battle Element to See', 15, colors.GOLD, colors.BLACK, 820, 750, 560, 20)
    soft_key_number = 1
    if None != karama_card:
        player_gui.soft_key_create(800, 770, soft_key_number, 'Entire Plan', player_gui.event, karama_card)
        soft_key_number += 1
        is_choice_needed = True
    if False == is_blocked:
        player_gui.soft_key_create(800, 770, soft_key_number, 'Bid Amount', player_gui.event, 'bid')
        soft_key_number += 1
        player_gui.soft_key_create(800, 770, soft_key_number, 'General', player_gui.event, 'general')
        soft_key_number += 1
        player_gui.soft_key_create(800, 770, soft_key_number, 'Offense', player_gui.event, 'offense')
        soft_key_number += 1
        player_gui.soft_key_create(800, 770, soft_key_number, 'Defense', player_gui.event, 'defense')
        soft_key_number += 1
        is_choice_needed = True
    if True == is_choice_needed:
        player_event.reset()
        player_event.msg_init('atreides_vision_response')
        player_gui.enable_row(770)
        player_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
        player_gui.disable_all_row_entries(770)
        player_gui.disable_row(770)
    else:
        player_gui.system_info_box_write('Your vision was blocked')

    player_gui.clear()

BID_SET = 1
GEN_SET = 2
OFF_SET = 4
DEF_SET = 8
MAX_SET_VALUE = BID_SET + GEN_SET + OFF_SET + DEF_SET

def dune_gui_battle_plan_set(this_game, character, territory_name, benes_voice, tokens_full_strength, kwisatz_haderach_blocked):
    player_gui = this_game.gui.player
    player_event = player_gui.event
    battle_plan = Battle.BattlePlan()

    display_msg = 'Bene\'s voice: {}: '.format(benes_voice)
    player_gui.system_info_box_write(display_msg)

    the_query = 'The Battle is in {}'.format(territory_name)
    this_game.gui.player.text_box(the_query, 15, colors.GOLD, colors.BLACK, 820, 750, 560, 20)

    player_event.reset()
    elements_set = 0
    finished = False
    while False == finished:
        gen_list, o_list, d_list, prep_elements_set = setup_battle_plan_prep(character, battle_plan, benes_voice)
        elements_set |= prep_elements_set

        setup_battle_plan_selection_keys(player_gui, player_event, len(gen_list), len(o_list), len(d_list), elements_set)
        player_gui.enable_row(770)
        player_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)

        player_gui.soft_keys_clear_all(800, 770, 6)
        player_gui.disable_row(770)

        if 'general' == player_event.click_info:
            player_gui.define_row_keys(len(gen_list), 820, 540, CARD_SMALL_X, CARD_SMALL_Y)
            count = 1
            for general in gen_list:
                #FIXME this count being 0 sometimes and 1 in other APIs sucks and needs fixed
                player_gui.set_row_key_info(540, (count -1), set_battle_plan_general, battle_plan, general)
                if False == player_gui.my_gui.my_game.treachery.is_card_of_type('Cheap_Hero', general):
                    house = Generals.get_house_by_general(general)
                    player_gui.spy_suspects_place(general, count, 820, 540)
                else:
                    player_gui.treachery_card_choice_place(general, count, 820, 540, GENERAL_SELECTION_SPACING)

                count += 1

            player_event.reset_dynamic_fields()
            player_gui.enable_row(540)
            player_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
            elements_set |= GEN_SET
            player_gui.disable_row(540)
        elif 'bid' == player_event.click_info:
            battle_territory = character.myGame.planet.find_territory(territory_name)
            troops = battle_territory.get_troops_by_owner(character.name)
            player_gui.event.reset_dynamic_fields()
            player_event.text_box_init('Enter # of Troops:', 820, 525)
            player_event.display_text_box()
            player_gui.event_wait(DuneGuiEventTypes.TEXT, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NUMBERS_ONLY)
            battle_plan.troops_bid_set(player_gui.event.text)

            player_event.reset_dynamic_fields()
            player_event.set_text_box_label('Enter Spice Payment:')
            player_event.display_text_box()
            player_gui.event_wait(DuneGuiEventTypes.TEXT, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NUMBERS_ONLY)
            battle_plan.spice_payment_set(player_gui.event.text)

            num_troops = float(battle_plan.troops_bid_get())
            spice_paid = int(battle_plan.spice_payment_get())

            if True == tokens_full_strength:
                max_bid_possible = (troops.tokens + (troops.fedaykins * 2))
            else:
                display_msg = 'Fedaykins/Sedarkars counted at half strength'
                player_gui.system_info_box_write(display_msg)
                max_bid_possible = (troops.tokens + troops.fedaykins)

            if num_troops > max_bid_possible:
                num_troops = max_bid_possible
                battle_plan.troops_bid_set(str(num_troops))

            if spice_paid >= num_troops:
                pass
            elif (((num_troops - spice_paid)*2) + spice_paid) <= max_bid_possible:
                pass
            else:
                display_msg = 'INFO troops bid is changed based on spice paid'
                player_gui.system_info_box_write(display_msg)
                num_troops = spice_paid + (float((max_bid_possible - spice_paid)/2))
                battle_plan.troops_bid_set(num_troops)
                display_msg = 'INFO Now Bid: {} Paid: {}'.format(num_troops, spice_paid)
                player_gui.system_info_box_write(display_msg)

            elements_set |= BID_SET

        elif 'offense' == player_event.click_info:
            player_gui.define_row_keys(len(o_list), 820, 540, CARD_SMALL_X, CARD_SMALL_Y)
            count = 1
            for card in o_list:
                #FIXME this count being 0 sometimes and 1 in other APIs sucks and needs fixed
                player_gui.set_row_key_info(540, count-1, set_battle_plan_offense, battle_plan, card)
                player_gui.treachery_card_choice_place(card, count, 820, 540, CARD_SMALL_X)
                count += 1
            player_event.reset_dynamic_fields()
            player_gui.enable_row(540)
            player_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
            elements_set |= OFF_SET
            player_gui.disable_row(540)
        elif 'defense' == player_event.click_info:
            player_gui.define_row_keys(len(d_list), 820, 540, CARD_SMALL_X, CARD_SMALL_Y)
            count = 1
            for card in d_list:
                #FIXME this count being 0 sometimes and 1 in other APIs sucks and needs fixed
                player_gui.set_row_key_info(540, count-1, set_battle_plan_defense, battle_plan, card)
                player_gui.treachery_card_choice_place(card, count, 820, 540, CARD_SMALL_X)
                count += 1
            player_event.reset_dynamic_fields()
            player_gui.enable_row(540)
            player_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
            elements_set |= DEF_SET
            player_gui.disable_row(540)
        elif 'finish' == player_event.click_info:
            if BID_SET != (elements_set & BID_SET):
                battle_plan.troops_bid_set(0)
                battle_plan.spice_payment_set(0)
                elements_set |= BID_SET
            if GEN_SET != (elements_set & GEN_SET):
                battle_plan.general_set('none', 0)
                elements_set |= GEN_SET
            if OFF_SET != (elements_set & OFF_SET):
                battle_plan.weapon_set('none', 0)
                elements_set |= OFF_SET
            if DEF_SET != (elements_set & DEF_SET):
                battle_plan.defense_set('none', 0)
                elements_set |= DEF_SET
            finished = True

        player_event.reset_dynamic_fields()

        pygame.draw.rect(this_game.gui.game_board, colors.WHITE, [800, 520, 600, 120], 0)
        display_current_battle_plan_selections(player_gui, character.name, battle_plan, 0)

    player_event.msg_init('submit_battle_plan')
    general, not_used = battle_plan.general_get()
    player_event.msg_add_to(general)
    player_event.msg_add_to(battle_plan.troops_bid_get())
    card, not_used = battle_plan.weapon_get()
    player_event.msg_add_to(card)
    card, not_used = battle_plan.defense_get()
    player_event.msg_add_to(card)
    player_event.msg_add_to(battle_plan.spice_payment_get())

    player_gui.clear()

def set_battle_plan_general(*args, ):
    battle_plan = args[0]
    general = args[1]
    battle_plan.general_set(general, 0)

def set_battle_plan_offense(*args, ):
    battle_plan = args[0]
    card = args[1]
    battle_plan.weapon_set(card, 0)

def set_battle_plan_defense(*args, ):
    battle_plan = args[0]
    card = args[1]
    battle_plan.defense_set(card, 0)

def setup_battle_plan_prep(character, battle_plan, benes_voice):
    offense_card_list = []
    defense_card_list = []
    elements_set = 0

    if 0 != len(benes_voice) and character.name != 'Bene_Gesserit':
        cant_or_must, o_or_d, o_or_d_type = benes_voice.split('_')
    else:
        cant_or_must = 'neither'
        o_or_d = 'none'
        o_or_d_type = 'none'
    weapon, not_used = battle_plan.weapon_get()
    defense, not_used = battle_plan.defense_get()
    general_list = character.generals_available_for_battle()

    if True == character.is_card_of_type_available('Weapons') or True == character.is_card_of_type_available('Worthless'):
        if cant_or_must == 'must' and o_or_d == 'offense':
            for card, detail in character.treachery_cards.items():
                if (character.myGame.treachery.is_card_of_type('Weapons', card) and detail == o_or_d_type) or\
                   (o_or_d_type == 'Worthless' and True == character.is_card_of_type_available('Worthless')):
                    battle_plan.weapon_set(card, 'not_set')
                    elements_set |= OFF_SET
                    offense_card_list = []
                    break
                elif (character.myGame.treachery.is_card_of_type('Weapons', card) or \
                      character.myGame.treachery.is_card_of_type('Worthless', card)) and card != defense:
                        offense_card_list.append(card)

        elif cant_or_must == 'cant' and o_or_d == 'offense':
            for card, detail in character.treachery_cards.items():
                if (character.myGame.treachery.is_card_of_type('Weapons', card) and o_or_d_type != detail) or \
                    (character.myGame.treachery.is_card_of_type('Worthless', card) and  o_or_d_type != 'Worthless'):
                    offense_card_list.append(card)
        else:
            for card, detail in character.treachery_cards.items():
                if (character.myGame.treachery.is_card_of_type('Weapons', card) or \
                   character.myGame.treachery.is_card_of_type('Worthless', card)) and card != defense:
                    offense_card_list.append(card)

    if True == character.is_card_of_type_available('Defense') or True == character.is_card_of_type_available('Worthless'):
        if cant_or_must == 'must' and o_or_d == 'defense':
            for card, detail in character.treachery_cards.items():
                if (character.myGame.treachery.is_card_of_type('Defense', card) and detail == o_or_d_type) or\
                   (o_or_d_type == 'Worthless' and True == character.is_card_of_type_available('Worthless')):
                    battle_plan.defense_set(card, 'not_set')
                    elements_set |= DEF_SET
                    defense_card_list = []
                    break
                elif (character.myGame.treachery.is_card_of_type('Defense', card) or \
                      character.myGame.treachery.is_card_of_type('Worthless', card)) and card != defense:
                        defense_card_list.append(card)

        elif cant_or_must == 'cant' and o_or_d == 'defense':
            for card, detail in character.treachery_cards.items():
                if ((character.myGame.treachery.is_card_of_type('Defense', card) and o_or_d_type != detail) or \
                    (character.myGame.treachery.is_card_of_type('Worthless', card) and  o_or_d_type != 'Worthless')) and \
                    card != weapon:
                    defense_card_list.append(card)
        else:
            for card, detail in character.treachery_cards.items():
                if (character.myGame.treachery.is_card_of_type('Defense', card) or \
                    character.myGame.treachery.is_card_of_type('Worthless', card)) and card != weapon:
                    defense_card_list.append(card)

    return general_list, offense_card_list, defense_card_list, elements_set

def setup_battle_plan_selection_keys(gui, event, general_list_size, o_list_size, d_list_size, elements_set):
    gui.soft_key_create_with_handler(800, 770, 6, 'Finished', place_args_to_click_info, event, 'finish')
    if 0 != general_list_size:
        if elements_set & GEN_SET:
            gui.soft_key_create_with_colors_and_handler(800, 770, 2, 'General', SOFT_KEY_COLOR, SOFT_KEY_FONT_COLOR, \
                                                        place_args_to_click_info, event, 'general')
        else:
            gui.soft_key_create_with_colors_and_handler(800, 770, 2, 'General', SOFT_KEY_COLOR, colors.GREEN, \
                                                        place_args_to_click_info, event, 'general')

        if elements_set & BID_SET:
            gui.soft_key_create_with_colors_and_handler(800, 770, 1, 'Bid', SOFT_KEY_COLOR, SOFT_KEY_FONT_COLOR, \
                                                        place_args_to_click_info, event, 'bid')
        else:
            gui.soft_key_create_with_colors_and_handler(800, 770, 1, 'Bid', SOFT_KEY_COLOR, colors.GREEN, \
                                                        place_args_to_click_info, event, 'bid')

        if 0 != d_list_size:
            if elements_set & DEF_SET:
                gui.soft_key_create_with_colors_and_handler(800, 770, 4, 'Defense', SOFT_KEY_COLOR, SOFT_KEY_FONT_COLOR,\
                                                            place_args_to_click_info, event, 'defense')
            else:
                gui.soft_key_create_with_colors_and_handler(800, 770, 4, 'Defense', SOFT_KEY_COLOR, colors.GREEN,\
                                                            place_args_to_click_info, event, 'defense')

        if 0 != o_list_size:
            if elements_set & OFF_SET:
                gui.soft_key_create_with_colors_and_handler(800, 770, 3, 'Offense', SOFT_KEY_COLOR, SOFT_KEY_FONT_COLOR,\
                                                            place_args_to_click_info, event, 'offense')
            else:
                gui.soft_key_create_with_colors_and_handler(800, 770, 3, 'Offense', SOFT_KEY_COLOR, colors.GREEN,\
                                                            place_args_to_click_info, event, 'offense')
    else:
        if elements_set & BID_SET:
            gui.soft_key_create_with_colors_and_handler(800, 770, 1, 'Bid', SOFT_KEY_COLOR, SOFT_KEY_FONT_COLOR, \
                                                        place_args_to_click_info, event, 'bid')
        else:
            gui.soft_key_create_with_colors_and_handler(800, 770, 1, 'Bid', SOFT_KEY_COLOR, colors.GREEN, \
                                                        place_args_to_click_info, event, 'bid')

def display_current_battle_plan_selections(player_gui, who, battle_plan, display_area):
    if display_area == 0:
        bid_x = 825
        bid_y = 685
        generals_and_cards_x = 900
        generals_and_cards_y = 655
    else:
        bid_x = 825
        bid_y = 560
        generals_and_cards_x = 900
        generals_and_cards_y = 530

    b, t = character_colors_get(who)
    player_gui.text_circle('{}'.format(float(battle_plan.troops_bid_get())), 15, b, t, bid_x, bid_y, 10)
    player_gui.text_box('{}'.format(battle_plan.spice_payment_get()), 20, colors.LIGHT_BLUE, colors.BLACK, (bid_x+20), bid_y, 20, 20)

    general, not_used = battle_plan.general_get()
    if False == player_gui.my_gui.my_game.treachery.is_card_of_type('Cheap_Hero', general) and general != 'none':
        player_gui.spy_suspects_place(general, 1, generals_and_cards_x, generals_and_cards_y)
    elif general != 'none':
        player_gui.treachery_card_choice_place(general, 1, generals_and_cards_x, generals_and_cards_y, CARD_SMALL_X)

    card, not_used = battle_plan.weapon_get()
    if card != 'none':
        player_gui.treachery_card_choice_place(card, 1, generals_and_cards_x +100, generals_and_cards_y, CARD_SMALL_X)
    else:
        player_gui.treachery_card_choice_place('TreacheryBack', 1, generals_and_cards_x +100, generals_and_cards_y, CARD_SMALL_X)

    card, not_used = battle_plan.defense_get()
    if card != 'none':
        player_gui.treachery_card_choice_place(card, 1, generals_and_cards_x +200, generals_and_cards_y, CARD_SMALL_X)
    else:
        player_gui.treachery_card_choice_place('TreacheryBack', 1, generals_and_cards_x +200, generals_and_cards_y, CARD_SMALL_X)

def display_battle_results(player_gui, result_type, who_won, winner_total, loser_total):
    if result_type == 'battle':
        final_results = '{} wins! {} to {}'.format(who_won, winner_total, loser_total)
    elif result_type == 'treachery':
        final_results = '{} Calls Treachery!'.format(who_won)
    elif result_type == 'treachery_double':
        final_results = 'Double Treachery! Everything Lost'
    elif result_type == 'kaboom':
        final_results = 'KABOOM!!! Lasegun + sheild = mushroom cloud'

    player_gui.text_box(final_results, 15, colors.GOLD, colors.BLACK, 820, 630, 560, 20)

def post_battle_discard_query(player_gui, *args, ):
    player_event = player_gui.event
    discard_list = []
    discard_choice_list = []

    for card in args:
        discard_choice_list.append(card)

    player_gui.text_box('Discard?', 15, colors.GOLD, colors.BLACK, 1180, 520, 320, 20)
    player_gui.define_row_keys(len(args), 1180, 540, CARD_SMALL_X, CARD_SMALL_Y)

    player_gui.soft_key_create_with_handler(800, 770, 6, 'Finished', place_args_to_click_info, player_event, 'finished')

    finished = False
    player_event.msg_init('treachery_card_discard_multiple')
    while False == finished:
        count = 1
        for card in discard_choice_list:
            # FIXME this count being 0 sometimes and 1 in other APIs sucks and needs fixed
            player_gui.set_row_key_info(540, count - 1, append_args_to_msg_and_click_info, player_gui.event, card)
            player_gui.treachery_card_choice_place(card, count, 1180, 540, CARD_SMALL_X)
            count += 1

        player_event.reset_dynamic_fields()
        player_gui.enable_row(540)
        player_gui.enable_row(770)
        player_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
        player_gui.disable_row(540)
        player_gui.disable_row(770)
        if 'finished' == player_event.click_info:
            cmd, *cards = player_event.msg.split(' ')
            if 0 == len(cards):
                player_event.msg_init('pass')
            finished = True
        else:
            discard_list.append(player_event.click_info)
            discard_choice_list.remove(player_event.click_info)

        pygame.draw.rect(player_gui.my_gui.game_board, colors.WHITE, [1180, 540, 420, 100], 0)

        count = 1
        for card in discard_list:
            if card != None:
                player_gui.treachery_card_choice_place(card, count, 1180, 665, CARD_SMALL_X)
            count += 1

def choose_next_battle(player_gui, *args, ):
    player_event = player_gui.event

    num_of_choices = int(len(args)/2)#args contains territory:who combo or 2 values per entry

    player_gui.text_box('Choose the Next Battle location and opponent', 15, colors.GOLD, colors.BLACK, 810, 600, 560, 20)
    player_gui.define_row_keys(num_of_choices, 820, 630, SOFT_KEY_WIDTH, SOFT_KEY_HEIGHT)

    key_number = 1
    player_event.reset()
    for x in range(num_of_choices):
        where = args[2 * x]
        who = args[(2 * x) + 1]
        b, t = character_colors_get(who)
        player_gui.soft_key_create_with_colors(820, 630, key_number, where, b, t, player_event, where, who)
        key_number += 1

    player_event.msg_init('next_battle')
    pygame.event.clear()
    player_gui.enable_row(630)

    player_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
    player_gui.disable_all_row_entries(630)
    player_gui.disable_row(630)

VOICE_CMD_SET = 1
VOICE_O_OR_D_SET = 2
VOICE_TYPE_SET = 4
VOICE_SET_MAX = VOICE_CMD_SET + VOICE_O_OR_D_SET + VOICE_TYPE_SET

def dune_gui_benes_voice_request(this_game):
    player_gui = this_game.gui.player
    player_event = player_gui.event

    this_game.gui.player.text_box('Select Benes Voice Command', 15, colors.GOLD, colors.BLACK, 820, 750, 560, 20)

    finished = False
    elements_set = 0
    cmd = ''
    o_or_d = ''
    element_type = ''

    player_event.reset()
    while False == finished:
        player_event.reset_dynamic_fields()
        create_benes_voice_selection_keys(player_gui, player_event, elements_set)
        player_gui.enable_row(770)
        player_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
        player_gui.soft_keys_clear_all(800, 770, 6)
        player_gui.disable_row(770)

        if 'command' == player_event.click_info:
            player_gui.define_row_keys(2, 820, 540, SOFT_KEY_WIDTH, SOFT_KEY_HEIGHT)
            player_gui.soft_key_create_with_colors_and_handler(820, 540, 1, 'Must Play', colors.GREEN, colors.WHITE, \
                                                               place_args_to_click_info, player_event, 'must')
            player_gui.soft_key_create_with_colors_and_handler(820, 540, 2, 'Cant Play', colors.RED, colors.WHITE, \
                                                               place_args_to_click_info, player_event, 'cant')

            player_event.reset_dynamic_fields()
            player_gui.enable_row(540)
            player_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
            player_gui.destroy_row(540)
            pygame.draw.rect(this_game.gui.game_board, colors.WHITE, [820, 540, 580, SOFT_KEY_HEIGHT], 0)
            cmd = player_event.click_info
            elements_set |= VOICE_CMD_SET

        elif 'o_or_d' == player_event.click_info:
            player_gui.define_row_keys(2, 820, 540, SOFT_KEY_WIDTH, SOFT_KEY_HEIGHT)
            player_gui.soft_key_create_with_colors_and_handler(820, 540, 1, 'Offense', colors.GREEN, colors.WHITE, \
                                                               place_args_to_click_info, player_event, 'offense')
            player_gui.soft_key_create_with_colors_and_handler(820, 540, 2, 'Defense', colors.RED, colors.WHITE, \
                                                               place_args_to_click_info, player_event, 'defense')

            player_event.reset_dynamic_fields()
            player_gui.enable_row(540)
            player_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
            player_gui.destroy_row(540)
            pygame.draw.rect(this_game.gui.game_board, colors.WHITE, [820, 540, 580, SOFT_KEY_HEIGHT], 0)
            o_or_d = player_event.click_info
            elements_set |= VOICE_O_OR_D_SET

        elif 'element' == player_event.click_info:
            player_gui.define_row_keys(4, 820, 540, SOFT_KEY_WIDTH, SOFT_KEY_HEIGHT)
            player_gui.soft_key_create_with_colors_and_handler(820, 540, 1, 'Projectile', colors.BLUE, colors.WHITE, \
                                                               place_args_to_click_info, player_event, 'Projectile')
            player_gui.soft_key_create_with_colors_and_handler(820, 540, 2, 'Poison', colors.DEEP_SKY_BLUE, colors.WHITE, \
                                                               place_args_to_click_info, player_event, 'Poison')
            player_gui.soft_key_create_with_colors_and_handler(820, 540, 3, 'Worthless', colors.LIGHT_BLUE, colors.WHITE, \
                                                               place_args_to_click_info, player_event, 'Worthless')

            if elements_set & VOICE_O_OR_D_SET and (o_or_d == 'offense' or o_or_d == ''):
                player_gui.soft_key_create_with_colors_and_handler(820, 540, 4, 'Lase Gun', colors.DARK_BLUE, colors.WHITE, \
                                                                   place_args_to_click_info, player_event, 'Lasegun')

            player_event.reset_dynamic_fields()
            player_gui.enable_row(540)
            player_gui.event_wait(DuneGuiEventTypes.CLICK, None, DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NONE)
            player_gui.destroy_row(540)
            pygame.draw.rect(this_game.gui.game_board, colors.WHITE, [820, 540, 580, SOFT_KEY_HEIGHT], 0)
            element_type = player_event.click_info
            elements_set |= VOICE_TYPE_SET

        elif 'finish' == player_event.click_info:
            benes_voice = 'benes_voice {}_{}_{}'.format(cmd, o_or_d, element_type)
            player_event.msg_init(benes_voice)
            finished = True

        current_voice = 'Current Voice: {} play {} {}'.format(cmd, element_type, o_or_d)
        this_game.gui.player.text_box(current_voice, 15, colors.GOLD, colors.BLACK, 820, 650, 560, 20)

    player_gui.soft_keys_clear_all(800, 770, 6)
    player_gui.disable_row(770)
    player_gui.clear()

def create_benes_voice_selection_keys(gui, event, elements_set):
    if elements_set == VOICE_SET_MAX:
        gui.soft_key_create_with_handler(800, 770, 6, 'Finished', place_args_to_click_info, event, 'finish')

    if elements_set & VOICE_CMD_SET:
        gui.soft_key_create_with_colors_and_handler(800, 770, 1, 'Command', SOFT_KEY_COLOR, SOFT_KEY_FONT_COLOR, \
                                                    place_args_to_click_info, event, 'command')
    else:
        gui.soft_key_create_with_colors_and_handler(800, 770, 1, 'Command', SOFT_KEY_COLOR, colors.GREEN, \
                                                    place_args_to_click_info, event, 'command')

    if elements_set & VOICE_O_OR_D_SET:
        gui.soft_key_create_with_colors_and_handler(800, 770, 2, 'offense/defense', SOFT_KEY_COLOR, SOFT_KEY_FONT_COLOR, \
                                                    place_args_to_click_info, event, 'o_or_d')
    else:
        gui.soft_key_create_with_colors_and_handler(800, 770, 2, 'offense/defense', SOFT_KEY_COLOR, colors.GREEN, \
                                                    place_args_to_click_info, event, 'o_or_d')

    if elements_set & VOICE_TYPE_SET:
        gui.soft_key_create_with_colors_and_handler(800, 770, 3, 'Element', SOFT_KEY_COLOR, SOFT_KEY_FONT_COLOR, \
                                                    place_args_to_click_info, event, 'element')
    else:
        gui.soft_key_create_with_colors_and_handler(800, 770, 3, 'Element', SOFT_KEY_COLOR, colors.GREEN, \
                                                    place_args_to_click_info, event, 'element')

# Support Routines
def text_box_object(text, color, font):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def text_circle_object(text, color, font):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def character_colors_get(who):
    back_ground_color = colors.BLACK
    text_color = colors.BLACK

    if 'Atreides' == who:
        back_ground_color = colors.GREEN
        text_color = colors.BLACK
    elif 'Bene_Gesserit' == who:
        back_ground_color = colors.DEEP_SKY_BLUE
        text_color = colors.BLACK
    elif 'Emperor' == who:
        back_ground_color = colors.RED
        text_color = colors.BLACK
    elif 'Fremen' == who:
        back_ground_color = colors.YELLOW
        text_color = colors.BLACK
    elif 'Guild' == who:
        back_ground_color = colors.ORANGE
        text_color = colors.BLACK
    elif 'Harkonnen' == who:
        back_ground_color = colors.BLACK
        text_color = colors.WHITE

    return back_ground_color, text_color

def poll_for_event(area, event_types, event_control):
    gui = area.my_gui
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and ((event_types == DuneGuiEventTypes.CLICK) or event_types == 0):
            player_position = pygame.mouse.get_pos()
            area.event.set_click_coordinates(player_position[0], player_position[1])
            processed = area.process_click_event(area.event)
            if True == processed:
                area.event.type = DuneGuiEventHandling.CLICK
            else:
                area.event.type = DuneGuiEventHandling.NO_EVENT

        elif event.type == pygame.KEYDOWN and ((event_types == DuneGuiEventTypes.TEXT) or event_types == 0):
            pygame.draw.rect(gui.game_board, colors.WHITE, [area.event.text_box_x, area.event.text_box_y, 150, 15], 0)
            area.event.display_text_box()

            key_value = event.unicode
            # gui.system_info_box_write(key_name)
            if event.key is pygame.K_RETURN:
                if DuneGuiEventTypesControl.EVENT_TYPE_CTRL_NUMBERS_ONLY == event_control:
                    if True == is_number(area.event.text):
                        area.event.type = DuneGuiEventHandling.TEXT
                    else:
                        area.event.text = ''
                elif DuneGuiEventTypesControl.EVENT_TYPE_CTRL_ALPHA_ONLY == event_control:
                    if True == area.event.text.isalpha():
                        area.event.type = DuneGuiEventHandling.TEXT
                    else:
                        area.event.text = ''
                else:
                    area.event.type = DuneGuiEventHandling.TEXT

                pygame.draw.rect(gui.game_board, colors.WHITE, [area.event.text_box_x, area.event.text_box_y, 150, 15], 0)

            elif event.key is pygame.K_BACKSPACE:
                area.event.type = DuneGuiEventHandling.IN_PROGRESS
                area.event.del_char()
                area.event.display_text_box()
            else:
                area.event.type = DuneGuiEventHandling.IN_PROGRESS
                area.event.add_char(key_value)
                area.event.display_text_box()
        elif event.type == TIME_EVENT and ((event_types == DuneGuiEventTypes.TIMER) or event_types == 0):
            area.event.type = DuneGuiEventHandling.TIMER
            gui.system_info_box_write('time event {}'.format(gui.debug_counter))
        else:
            print(event)

    pygame.display.update()
    pygame.display.flip()

def no_action(*args,):
    pass

def is_number(n):
    try:
        float(n) #If string is not a valid `float`, it'll raise `ValueError` exception
    except ValueError:
        return False
    return True
