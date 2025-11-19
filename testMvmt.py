import planet
import storm
import dune_gui as Gui

class TestGame :
    def __init__(self):
        print("creating the test game object")

        self.storm_tracker = storm.Storm(self)

        self.gui = Gui.DuneNoGui(self)

        self.planet = planet.Planet(self)
        self.planet.build_map(True)

    def sector_under_storm_get(self):
        return self.storm_tracker.sector_under_storm


def main():
    cmd = ''

    thisGame = TestGame()

    request = input("request -> ")
    while cmd != "quit":
        cmd, *args = request.split(' ')

        if 'showLocal' == cmd :
            print(str(thisGame))
        elif 'beam':
            pass
        elif 'move':
            pass


def make_move(start, end, max_moves, through_storm_allowed, who):
    if False == through_storm_allowed:
        valid_move = testGame.planet.validate_on_planet_move(start, end, max_moves, who)
    else:
        valid_move = testGame.planet.validate_on_planet_move_through_storm(start, end, max_moves, who)

    print('{}  Move From {} to {} distance {} is allowed {}'.format(who, start, end, max_moves, valid_move))


# testGame = TestGame()
#
# who = 'Emperor'
# # print('only move distance of 3 should pass')
# make_move('Sietch_Tabr_14', 'Hole_in_the_Rock_9', 3, False, who)
# make_move('Sietch_Tabr_14', 'Hole_in_the_Rock_9', 2, False, who)
# make_move('Sietch_Tabr_14', 'Hole_in_the_Rock_9', 1, False, who)
# make_move('Carthag_11', 'Sietch_Tabr_14', 3, False, who)
# make_move('Carthag_11', 'Sietch_Tabr_14', 2, False, who)
# make_move('Carthag_11', 'Sietch_Tabr_14', 1, False, who)
#
# make_move('Tueks_Sietch_5', 'Imperial_Basin_11', 3, False, who)
# make_move('Tueks_Sietch_5', 'Imperial_Basin_11', 2, False, who)
# make_move('Tueks_Sietch_5', 'Imperial_Basin_11', 1, False, who)
#
# print('with move of 1 only Sietch Tabr should fail')
# make_move('Hagga_Basin_12', 'Plastic_Basin_12', 1, False, who)
# make_move('Hagga_Basin_12', 'Wind_Pass_17', 1, False, who)
# make_move('Hagga_Basin_12', 'Sietch_Tabr_14', 1, False, who)
#
#
# print('Ceilago North is 2 away however sector 1 is under storm so should fail')
# make_move('Tueks_Sietch_5', 'Cielago_North_1', 3, False, who)
# make_move('Tueks_Sietch_5', 'Cielago_North_2', 3, False, who)
# make_move('Tueks_Sietch_5', 'Cielago_North_3', 3, False, who)
#
# print('the current storm sector is 1  any movement to or through Meridian should fail')
# make_move('Habbanya_Ridge_Sietch_17', 'Meridian_1', 3, False, who)
# make_move('Habbanya_Ridge_Sietch_17', 'Meridian_1', 2, False, who)
# make_move('Habbanya_Ridge_Sietch_17', 'Meridian_1', 1, False, who)
# make_move('Habbanya_Ridge_Sietch_17', 'Cielago_South_3', 3, False, who)
# make_move('Habbanya_Ridge_Sietch_17', 'Cielago_South_3', 2, False, who)
# make_move('Habbanya_Ridge_Sietch_17', 'Cielago_South_3', 1, False, who)
#
# print('only move distance of 3 & 2 should pass')
# make_move('Habbanya_Ridge_Sietch_17', 'False_Wall_West_16', 3, False, who)
# make_move('Habbanya_Ridge_Sietch_17', 'False_Wall_West_18', 2, False, who)
# make_move('Habbanya_Ridge_Sietch_17', 'False_Wall_West_17', 1, False, who)
#
# print('sietch is too far')
# make_move('Polar_Sink_0', 'Broken_Land_12', 3, False, who)
# make_move('Polar_Sink_0', 'Sihaya_Ridge_9', 3, False, who)
# make_move('Polar_Sink_0', 'Habbanya_Ridge_Sietch_17', 3, False, who)
#
# print('moving through strom')
# make_move('Cielago_South_3', 'Habbanya_Ridge_Flat_18', 3, False, who)
# make_move('Cielago_South_3', 'Cielago_West_18', 3, False, who)
# make_move('Cielago_South_3', 'Wind_Pass_North_17', 3, False, who)
# make_move('Cielago_South_3', 'Habbanya_Ridge_Flat_18', 3, True, who)
# make_move('Cielago_South_3', 'Cielago_West_18', 3, True, who)
# make_move('Cielago_South_3', 'Wind_Pass_North_17', 3, True, who)
#
# print('generic test for fremen starting position cant make Carthag if distance is 2')
# make_move('The_Great_Flat_15', 'Carthag_11', 3, False, who)
# make_move('The_Great_Flat_15', 'Carthag_11', 2, False, who)
# make_move('The_Great_Flat_15', 'Broken_Land_12', 2, False, who)
# make_move('The_Great_Flat_15', 'Sietch_Tabr_14', 2, False, who)
# make_move('The_Great_Flat_15', 'Imperial_Basin_10', 3, False, who)
#
# print('spice hunting from Sietch Tabr with ornothopters')
# make_move('Sietch_Tabr_14', 'OH_Gap_10', 3, False, who)
# make_move('Sietch_Tabr_14', 'Wind_Pass_North_17', 3, False, who)
# make_move('Sietch_Tabr_14', 'Wind_Pass_North_17', 2, False, who)
#
# print('moving to minor erg to spice hunt')
# make_move('Arrakeen_10', 'The_Minor_Erg_5', 3, False, who)
# make_move('Arrakeen_10', 'The_Minor_Erg_8', 2, False, who)
# make_move('Carthag_11', 'The_Minor_Erg_5', 3, False, who)
#
# print('couple of moves from Tueks Sietch')
# make_move('Tueks_Sietch_5', 'Red_Chasm_7', 2, False, who)
# make_move('Tueks_Sietch_5', 'Gara_Kulon_8', 2, False, who)
# make_move('Tueks_Sietch_5', 'Cielago_North_1', 2, False, who)
# # make_move('Tueks_Sietch_5', 'Cielago_North_3', 2, False, who)

def is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`,
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True

print(is_number('.5'))
print(is_number('.a2'))
print(is_number('3'))
