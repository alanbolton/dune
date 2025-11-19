import treachery
import storm
import dune_server as DuneServer

from threading import Thread

# class TestGame :
#     def __init__(self):
#         print("creating the test game object")
#
#         self.treachery = treachery.Treachery(self)

def main():
    cmd = ''

    # thisGame = TestGame()

    request = input("request -> ")
    while cmd != "quit":
        cmd, *args = request.split(' ')

        if 'deal' == cmd :
            card, details = testGame.treachery.deal_card()
            this_card(testGame, card, details)

        elif 'shuffle':
            testGame.treachery.shuffle_deck()


def this_card(myGame, card, details, display_type_info):
    print('{}   {}'.format(card, details))
    if display_type_info == True:
        print('   card is type Karama {} '.format(myGame.treachery.is_card_of_type('Karama', card)))
        print('   card is type Worthless {} '.format(myGame.treachery.is_card_of_type('Worthless', card)))
        print('   card is type Truth_Trance {} '.format(myGame.treachery.is_card_of_type('Truth_Trance', card)))
        print('   card is type Cheap_Hero {} '.format(myGame.treachery.is_card_of_type('Cheap_Hero', card)))
        print('   card is type Weapons {} '.format(myGame.treachery.is_card_of_type('Weapons', card)))
        print('   card is type Defense {} '.format(myGame.treachery.is_card_of_type('Defense', card)))
        print('   card is a unique card {} '.format(myGame.treachery.is_card_of_type(card, card)))


# testGame = TestGame()
# for x in range(33):
#     card, details = testGame.treachery.deal_card()
#     this_card(testGame, card, details, True)


testGame = DuneServer.DuneServer(15)

testGame.treachery.stack_the_deck()

testGame.player_join_request('alan', None, 'Harkonnen')
hark = testGame.is_character_playing('Harkonnen')
# testGame.player_join_request('alan', None, 'Fremen')
# fremen = testGame.is_character_playing('Fremen')
testGame.player_join_request('b', None, 'Emperor')
emp = testGame.is_character_playing('Emperor')

storm.create_turn_order(testGame)

testGame.treachery.dealing_round()
testGame.treachery.dealing_round()
testGame.treachery.dealing_round()

print(hark)

string = []
string.append('Karama_1')
string.append('Swap')
string.append('Emperor')
string.append('2')
string.append('Ghola')
string.append('Hajr')

hark.play_karama_card(*string)

# string = []
# string.append('Attack')
# string.append('Imperial_Basin_9')
#
# fremen.play_karama_card(*string)

print(testGame)