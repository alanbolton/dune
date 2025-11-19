from enum import Enum
import troops


class TerritoryType(Enum):
    UNKNOWN = 0
    DESERT = 1
    ROCK = 2
    CITY = 3

class Territory :
    def __init__(self, name):
        self.name = name
        self.type = TerritoryType.UNKNOWN
        self.spice = 0
        self.beam_cost = 2
        self.is_protected = False
        self.neighbors = dict()  #this maintains a mapping of <territory_name>:cost the cost is used to keep track of the number of territories traversed either 0 or 1
        self.aliases = [] #this a list of other names for the territory ..when territories span multiple sectors they have names like name_x name_y name_z etc all
        self.occupied = dict()  #this is a list of <character_name>:Troop Class that occupy the territory
        self.dirty = False
    def __str__(self):
        ret_str = '{} {} protectFromStorm:{} spice: {} \n'.format(self.name, self.type, self.is_protected, self.spice)
        ret_str += '       OccupiedBy: \n'
        for key, value in self.occupied.items():
            ret_str += '          {}'.format(value)
        return ret_str

    def add_neighbor(self, territory_name, traverse_cost):
        self.neighbors[territory_name] = traverse_cost

    def add_alias(self, alias):
        self.aliases.append(alias)

    def get_first_troops(self):
        owner = next(iter(self.occupied))
        return self.occupied[owner]

    def get_number_of_occupants(self):
        return len(self.occupied)

    def get_troops_by_owner(self, owner):
        troops = None
        if True == self.does_character_occupy(owner):
            troops = self.occupied[owner]
        return troops

    def increase_troops(self, owner, tokens, fedaykins):
        troops = self.get_troops_by_owner(owner)
        troops.tokens += tokens
        troops.fedaykins += fedaykins

    def reduce_troops(self, owner, tokens, fedaykins):
        troops = self.get_troops_by_owner(owner)
        if troops.tokens >= tokens:
            troops.tokens -= tokens
        else:
            print('Error illegal troop reduction tokens exist {} requested {}'.format(troops.tokens,tokens))
        if troops.fedaykins >= fedaykins:
            troops.fedaykins -= fedaykins
        else:
            print('Error illegal troop reduction fedaykins exist {} requested {}'.format(troops.fedaykins, fedaykins))

    def remove_troops(self, owner):
        self.occupied.pop(owner)

    def place_troops(self, troops):
        self.occupied[troops.owner] = troops

    def does_character_occupy(self, owner):
        does_character_occupy = False
        for character in self.occupied.keys():
            if character == owner:
                does_character_occupy = True
        return does_character_occupy

    def spice_blow(self, amount):
        self.spice += amount

    def spice_remove(self):
        self.spice = 0

    def spice_harvest(self, amount):
        if amount > self.spice:
            amount = self.spice
        self.spice -= amount
        return amount

    def spice_avaliable_get(self):
        return self.spice

    def beam_cost_get(self):
        return self.beam_cost

    def is_occupied(self):
        if 0 != len(self.occupied):
            return True
        else:
            return False

    def set_protection(self, setting):
        self.is_protected = setting

    def is_protected_from_storm(self):
        return self.is_protected

    def is_territory_dirty(self):
        return self.dirty

    def dirty_set(self, is_dirty):
        self.dirty = is_dirty

class City(Territory):
    def __init__(self, name):
        super().__init__(name)
        self.type = TerritoryType.CITY
        self.beam_cost = 1

        if 'Arrakeen_10' == name or 'Carthag_11' == name:
            self.is_protected = True

class Rock(Territory):
    def __init__(self, name):
        super().__init__(name)
        self.type = TerritoryType.ROCK
        self.is_protected = True

class Desert(Territory):
    def __init__(self, name):
        super().__init__(name)
        self.type = TerritoryType.DESERT

        if 'Imperial_Basin_9' == name or 'Imperial_Basin_10' == name or 'Imperial_Basin_11' == name:
            self.is_protected = True
