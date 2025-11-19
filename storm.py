import random

class Storm :
    def __init__(self, thisGame):
        self.myGame = thisGame
        self.sector_under_storm = 1
        self.next_movement = 0

    def __str__(self):
        ret_str = 'Current Storm Sector: {} \n'.format(self.sector_under_storm)
        return ret_str

    def sector_under_storm_get(self):
        return self.sector_under_storm

    def movement(self):
        from_sector = self.sector_under_storm

        if self.myGame.turn == 1:
            current_movement = random.randint(0, 18)
        else:
            play_it = self.myGame.find_player_with_card_and_ask_to_play('Weather_Control')
            if True == play_it:
                current_movement = self.myGame.value_rcvd
                msg = 'Info {} played the Weather_Control'.format(self.myGame.answering_character)
                self.myGame.broadcast(msg, False, '')
            else:
                current_movement = self.next_movement

        play_it = self.myGame.find_player_with_card_and_ask_to_play('Family_Atomics')
        if True == play_it:
            self.myGame.planet.sheild_wall_blown()
            msg = 'Info Shield_Wall_blown_by{}'.format(self.myGame.answering_character)
            self.myGame.broadcast(msg, False, '')

        self.next_movement = random.randint(1, 6)
        self.sector_under_storm = new_sector(self.sector_under_storm, current_movement)
        msg = 'storm_movement {} {} {}'.format(self.myGame.turn, self.sector_under_storm, self.next_movement)
        self.myGame.broadcast(msg, False, '')

        if self.myGame.turn != 1:
            sector = new_sector(from_sector, 1)  #the storm impacts sector from 1 beyoned the last sector under storm
            if from_sector > self.sector_under_storm:
                num_of_sectors = ((self.sector_under_storm + 18) - from_sector)
            else:
                num_of_sectors = self.sector_under_storm - from_sector

            self.myGame.planet.storm_impact(sector, num_of_sectors)

        fremen = self.myGame.is_character_playing('Fremen')
        if None != fremen:
            fremen.next_storm_movement = self.next_movement

        create_turn_order(self.myGame)
        print('Info Sector {}  is under storm'.format(self.sector_under_storm))

def new_sector(starting_sector, distance):
    end_sector = (starting_sector + distance) % 18
    if end_sector == 0:
        end_sector = 18
    return end_sector

def sectors_distance_from_storm(storm_sector, this_sector):
    distance = 0
    next_sector = storm_sector
    while this_sector != next_sector:
        next_sector = new_sector(next_sector, 1) #advance one sector
        distance += 1

    if distance == 0:
        distance = 20 #if distance = 0 means the storm is on this dot so it should be last. Set distance to be > 18 to insure it is last
    return distance

def create_turn_order(thisGame):
    #fist empty the current turn order dictionary
    thisGame.character_turn_order = { }

    for player_dot, player in thisGame.characters.items():
        distance = sectors_distance_from_storm(thisGame.storm_tracker.sector_under_storm, player_dot)
        thisGame.character_turn_order[distance] = player
    #now sort based on distance from storm
    thisGame.character_turn_order = {k: thisGame.character_turn_order[k] for k in sorted(thisGame.character_turn_order)}


