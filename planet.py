from enum import Enum
import planetDune as map
import character
import territory as Territory
import troops as trps
import treachery
import time

class Planet :
    def __init__(self, myGame):
        self.myGame = myGame
        self.territories = dict() #this is <name_sector>: *Territory Class
        self.territories_occupied = set()
        self.territories_with_spice = set()

    def __str__(self):
        ret_str = 'Number of Created Territories: {}\n'.format(len(self.territories))
        ret_str += '  TerritoriesOccupied: {} \n'.format(self.territories_occupied)
        ret_str += '  TerritoriesWithSpice: {} \n'.format(self.territories_with_spice)
        ret_str += '  Territories: \n'
        for key, value in self.territories.items():
            if key in self.territories_occupied or key in self.territories_with_spice:
                ret_str += '     {}'.format(value)

        return ret_str

    def build_map(self, full_map):
        for sector in range(19):
            territory_list =  map.territories_by_sector_get(sector)
            for entry in territory_list:
                if entry[1] == 1:
                    this_territory = Territory.Desert(entry[0])
                    self.territories[entry[0]] = this_territory
                elif entry[1] == 2:
                    this_territory = Territory.Rock(entry[0])
                    self.territories[entry[0]] = this_territory
                else:
                    this_territory = Territory.City(entry[0])
                    self.territories[entry[0]] = this_territory

                if True == full_map:
                    neighbor_list = map.territories_neighbors_get(entry[0])
                    for neighbor in neighbor_list:
                        this_territory.add_neighbor(neighbor[0], neighbor[1])

                    alias_list = map.territories_aliases_get(entry[0])
                    for alias in alias_list:
                        if alias != this_territory.name:
                            this_territory.add_alias(alias)

                    self.spice_update_gui(this_territory)
                    self.troops_update_gui(this_territory)

        self.myGame.gui.map.place_troop_markers()
        self.myGame.gui.map.enable()

    def find_territory(self, name):
        return self.territories[name]

    def spice_blow(self, name, amount):
        if 0 != amount:
            territory = self.find_territory(name)
            territory.spice_blow(amount)
            self.territories_with_spice.add(name)
            self.spice_update_gui(territory)
        else:
            print('Info spice not blown to {} due to sector being under storm'.format(name))

    def spice_avaliable_get(self, name):
        territory = self.find_territory(name)
        return territory.spice_avaliable_get()

    def spice_harvest(self, name, amount):
        territory = self.find_territory(name)
        amount_harvested = territory.spice_harvest(amount)
        if 0 == territory.spice_avaliable_get():
            if name in self.territories_with_spice:
                self.territories_with_spice.remove(name)

        self.spice_update_gui(territory)
        return amount_harvested

    def spice_update_gui(self, territory):
        spice_markers = map.territories_spice_marker_get(territory.name)
        for x, y in spice_markers:
            if x != 0 and y != 0:
                self.myGame.gui.map.spice_territory_update(territory.spice, x, y)

    def troops_enter(self, name, troops):
        territory = self.find_territory(name)
        territory.place_troops(troops)
        if name not in self.territories_occupied:
            self.territories_occupied.add(name)
        self.troops_update_gui(territory)

    def troops_remove(self, name, owner):
        territory = self.find_territory(name)
        territory.remove_troops(owner)
        if 0 == self.get_number_of_occupants(name):
            self.territories_occupied.remove(name)
        self.troops_update_gui(territory)

    def troops_get(self, name, owner):
        territory = self.find_territory(name)
        return territory.get_troops_by_owner(owner)

    def troops_update(self, name, owner, tokens, fedaykins):
        territory = self.find_territory(name)
        troops = self.troops_get(name, owner)
        troops.tokens = tokens
        troops.fedaykins = fedaykins
        self.troops_update_gui(territory)

    def troops_increase(self, name, owner, tokens, fedaykins):
        territory = self.find_territory(name)
        territory.increase_troops(owner, tokens, fedaykins)
        self.troops_update_gui(territory)

    def troops_reduce(self, name, owner, tokens, fedaykins):
        territory = self.find_territory(name)
        territory.reduce_troops(owner, tokens, fedaykins)
        self.troops_update_gui(territory)

    def troops_remove_some(self, name, owner, tokens, fedaykins):
        territory = self.find_territory(name)
        troops = territory.get_troops_by_owner(owner)
        troops.tokens -= tokens
        troops.fedaykins -= fedaykins
        if troops.tokens == 0 and troops.fedaykins == 0:
            self.territories_occupied.remove(name)
        self.troops_update_gui(territory)

    def troops_update_gui(self, territory):
        troop_marker = map.territories_troop_markers_get(territory.name)
        x, y, territory_name = troop_marker[0]
        if territory_name != territory.name:
            print('Err mismatch in internal data structures')
        for offset in range(3):
            self.myGame.gui.map.troops_place('', 0, 0, False, x, y, offset, len(territory.occupied.values()))

        offset = 0
        for troops in territory.occupied.values():
            self.myGame.gui.map.troops_place(troops.owner, int(troops.tokens), int(troops.fedaykins), \
                                             troops.include_fedaykins,  x, y, offset, len(territory.occupied.values()))
            offset += 1

    def can_troops_enter(self, name, who_is_entering):
        territory = self.find_territory(name)
        num_of_occupants = territory.get_number_of_occupants()
        if num_of_occupants <= 1:
            entrance_allowed = True
        elif num_of_occupants > 1 and 'Bene_Gesserit' == who_is_entering:
            entrance_allowed = True
        elif num_of_occupants > 1:
            entrance_allowed = False
            if territory.type != Territory.TerritoryType.CITY:
                entrance_allowed = True  #no limit to how many characters can occupy Rocks and desert territories
            else: #if it is a city and one occupant is bene and she is peaceful or one occupant is the character entering it is allowed
                for owner, troops in territory.occupied.items():
                    if (owner == 'Bene_Gesserit' and troops.peaceful == True) or  (owner == who_is_entering):
                        entrance_allowed = True
        else:
            entrance_allowed = False
        return entrance_allowed

    def get_number_of_occupants(self, territory_name):
        territory = self.find_territory(territory_name)
        return territory.get_number_of_occupants()

    def does_character_occupy(self, name, owner):
        territory = self.find_territory(name)
        does_character_occupy = territory.does_character_occupy(owner)
        return does_character_occupy

    def territories_in_a_sector_get(self, sector):
        return map.territories_by_sector_get(sector)

    def storm_impact(self, first_sector, num_of_sectors_impacted):
        for x in range(num_of_sectors_impacted):
            territory_list = map.territories_by_sector_get(first_sector)
            first_sector = next_sector(first_sector)
            for entry in territory_list:
                territory = self.find_territory(entry[0])
                inflict_damage_on_territory(self, territory, False)

    def worm_attack(self, territory_attacked):
        this_territory = self.find_territory(territory_attacked)
        if this_territory.type != Territory.TerritoryType.CITY and this_territory.type != Territory.TerritoryType.ROCK:
            inflict_damage_on_territory(self, this_territory, True)

    def is_territory_under_storm(self, territory_name):
        under_storm = False
        *args, = territory_name.split('_')
        #the last args value represents the sector # contained in the territory name
        if int(args[(len(args) - 1)]) == self.myGame.sector_under_storm_get():
            under_storm = True

        return under_storm

    def is_territory_shield_wall_or_adjacent(self, territory_name):
        result = False

        neighbor_list = map.territories_neighbors_get('Sheild_Wall_8')
        for neighbor in neighbor_list:
            if territory_name == neighbor[0]:
                result = True
                break
        if False == result:
            neighbor_list = map.territories_neighbors_get('Sheild_Wall_9')
            for neighbor in neighbor_list:
                if territory_name == neighbor[0]:
                    result = True
                    break
        return result

    def sheild_wall_blown(self):
        # destroy everything on sheild_wall
        territory = self.find_territory('Sheild_Wall_8')
        inflict_damage_on_territory(self.myGame.planet, territory, False)
        territory = self.find_territory('Sheild_Wall_9')
        inflict_damage_on_territory(self.myGame.planet, territory, False)
        territory = self.find_territory('Arrakeen_10')
        territory.set_protection(False)
        territory = self.find_territory('Carthag_11')
        territory.set_protection(False)
        territory = self.find_territory('Imperial_Basin_9')
        territory.set_protection(False)
        territory = self.find_territory('Imperial_Basin_10')
        territory.set_protection(False)
        territory = self.find_territory('Imperial_Basin_11')
        territory.set_protection(False)

    def validate_on_planet_move(self, start, end, max_distance, who):
        path = []
        path.append(start)
        allowed = opm_verify(self, start, end, max_distance, 0, path, False, who)
        return allowed

    def validate_on_planet_move_through_storm(self, start, end, max_distance, who):
        path = []
        path.append(start)
        allowed = opm_verify(self, start, end, max_distance, 0, path, True, who)
        return allowed

    def announce_character_movement(self, who, start, end):
        start_troops = self.troops_get(start, who)
        end_troops = self.troops_get(end, who)
        msg = 'movement_notification {} '.format(who)
        if None == start_troops:
            tokens = 0
            fedaykins = 0
        else:
            tokens = start_troops.tokens
            fedaykins = start_troops.fedaykins
        msg += '{} {} {} '.format(start, int(tokens), int(fedaykins))
        msg += '{} {} {} '.format(end, int(end_troops.tokens), int(end_troops.fedaykins))
        self.myGame.broadcast(msg, False, who)

    def character_movement(self, who, start, s_tokens, s_fedaykins, end, e_tokens, e_fedaykins):
        end_troops = self.troops_get(end, who)

        if s_tokens == 0 and s_fedaykins == 0:
            self.troops_remove(start, who)
        else:
            self.troops_update(start, who, s_tokens, s_fedaykins)
        if None == end_troops:
            landing_party = trps.Troops(self.myGame.turn, who, e_tokens, e_fedaykins)
            self.troops_enter(end, landing_party)
        else:
            self.troops_update(end, who, e_tokens, e_fedaykins)

    def movment_between_two_territories(self, character, start, end, tokens, fedaykins):
        start_troops = self.troops_get(start, character.name)

        if start_troops.tokens == tokens and start_troops.fedaykins == fedaykins:  # are we moving all tokens
            self.troops_remove(start, character.name)  # remove troops from start area
            character.troops_removed(start)

            if True == self.does_character_occupy(end, character.name):
                self.troops_increase(end, character.name,  start_troops.tokens, start_troops.fedaykins)
            else:
                character.troops_placed(end, start_troops)
                self.troops_enter(end, start_troops)
        else:
            self.troops_remove_some(start, character.name, tokens, fedaykins)
            if True == self.does_character_occupy(end, character.name):
                self.troops_increase(end, character.name,  tokens, fedaykins)
            else:
                new_troops = trps.Troops(self.myGame.turn, character.name, tokens, fedaykins)
                character.troops_placed(end, new_troops)
                self.troops_enter(end, new_troops)

def next_sector(sector):
    next_sector = (sector + 1) % 18
    if next_sector == 0:
        next_sector = 18
    return next_sector

def inflict_damage_on_territory(myPlanet, territory, is_worm_attack):
    occupied_list = dict()
    if False == territory.is_protected_from_storm() or True == is_worm_attack:
        if territory.name in myPlanet.territories_with_spice:
            msg = 'spice_remove {} {}'.format(territory.name, territory.spice)
            territory.spice_remove()
            myPlanet.territories_with_spice.remove(territory.name)
            myPlanet.myGame.broadcast(msg, False, '')

        if territory.name in myPlanet.territories_occupied:
            for owner, troops in territory.occupied.items():
                occupied_list[owner] = troops   #create this duplicate list as the logic below will modify myPlanet.territories_occupied
            for owner, troops in occupied_list.items():
                if 'Fremen' == owner and False == is_worm_attack:  # fremen only looses half his troops during storm nothing to a worm
                    tmp_tokens = troops.tokens
                    tmp_fedaykins = troops.fedaykins
                    #need to use the "tmp"values because if you pass troops.x into "reduce_troops_in_half" it updates
                    #troops.x then the call to "kill_some_troops" causes a double decrement
                    tokens_lost, fedaykins_lost = character.reduce_troops_in_half(tmp_tokens, tmp_fedaykins)
                    myPlanet.myGame.kill_some_troops_in_territory(territory.name, troops, tokens_lost, fedaykins_lost)
                elif 'Fremen' == owner and True == is_worm_attack:  # fremen only looses half his troops during storm nothing to a worm
                    block = myPlanet.myGame.block_characters_advantage('Fremen', 'worm_surfing')
                    if True == block:
                        myPlanet.myGame.kill_troops_in_territory(territory.name, troops.owner)
                    else:
                        print('Info Fremen occupies territory but and can ride the WORM!!!')
                else: #for any other player but the Fremen they are destroyed
                    myPlanet.myGame.kill_troops_in_territory(territory.name, troops.owner)

def opm_verify(myPlanet, start_name, end_name, max_distance, current_distance, path, through_storm_allowed, who):
    allowed = False

    # print('Start:{} end:{} distance {}:{} path {} throughStrom:{}'.format(start_name, end_name, current_distance, max_distance, path, through_storm_allowed))

    destination_allowed = myPlanet.can_troops_enter(end_name, who) #if there are already 2 troops in the desitnation it is not allowed
    if (True == destination_allowed) and \
        (False == is_territories_sector_under_storm(myPlanet, end_name) or True == through_storm_allowed) and \
        (False == is_territories_sector_under_storm(myPlanet, start_name) or True == through_storm_allowed):
        
        start = myPlanet.find_territory(start_name)
        # print('    Neighbors:{}'.format(start.neighbors))

        for neighbor, cost in start.neighbors.items():
            storm_encountered = is_territories_sector_under_storm(myPlanet, neighbor)
            if False == storm_encountered or True == through_storm_allowed:  # make sure adjacent neighbor isn't under storm if it is ignore and loop to next
                test_territory = myPlanet.find_territory(neighbor)
                # print('    Aliases For:{}  {}'.format(neighbor, test_territory.aliases))
                if end_name == neighbor or end_name in test_territory.aliases:
                    allowed = True
                elif (neighbor not in path):  # if it is in path it means it has been used in this analysis
                    if cost != 0:
                        current_distance += cost

                    if max_distance > current_distance:
                        path.append(neighbor)
                        allowed = opm_verify(myPlanet, neighbor, end_name, max_distance, current_distance, path, through_storm_allowed, who)
                        path.remove(neighbor)

                    if cost != 0:
                         current_distance -= 1

                if True == allowed:
                    break;
    return allowed

def is_territories_sector_under_storm(myPlanet, name):
    under_storm = False
    *args, = name.split('_')
    sector = int(args[(len(args) - 1)])
    if sector == myPlanet.myGame.sector_under_storm_get():
        under_storm = True
    return under_storm
