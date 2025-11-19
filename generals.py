import deck

generals_harkonnen = {'Umman_Kudu': 1, 'Captain_Nefud': 2, 'Piter_DeVries': 3, 'Beast_Rabban': 4, 'Feyd_Rautha': 6}
generals_atreides = {'Dr_Yueh':1, 'Duncan_Idaho':2, 'Gurney_Halleck':4, 'Thufir_Hawat':5, 'Lady_Jessica':5}
generals_guild = {'Guild_Rep':1, 'SooSoo_Sook':2, 'Esmar_Tuek':3, 'Master_Bewt':3, 'Staban_Tuek':5}
generals_bene_gesserit = {'Alia':5, 'Wanna_Marcus':5, 'Princess_Irulan':5, 'Margot_Lady_Fenring':5, 'Mother_Ramallo':5}
generals_fremen = {'Jamis':2, 'Shadout_Mapes':3, 'Ortheym':5, 'Chani':6, 'Stilgar':7}
generals_emperor = {'Bashar':2, 'Caid':3, 'Burseg':3, 'Captain_Aramsham':5, 'Count_Fenring':6}

generals_house_list = ['Harkonnen',  'Atreides',  'Guild',  'Bene_Gesserit',  'Fremen',  'Emperor']

general_deck = {}

class Generals(deck.Deck):
    def __init__(self):
        for house in generals_house_list:
            general_list = get_generals_by_house(house)
            for general, value in general_list.items():
                general_deck[general] = value

        super().__init__('Spy Deck', general_deck)

    def __str__(self):
        ret_str = super().__str__()
        return ret_str

    def deal_spies(self, character):
        msg = 'spy_choice 4 '
        for x in range(4):
            general, val = self.deal_card()
            msg += '{} {} '.format(general, val)
            character.spy_dealt(general, val)
        character.send(msg, True)

def get_generals_by_house(house_name):
    general_management = {
        'Harkonnen': generals_harkonnen ,
        'Atreides': generals_atreides ,
        'Guild': generals_guild,
        'Bene_Gesserit': generals_bene_gesserit,
        'Fremen': generals_fremen,
        'Emperor': generals_emperor
    }
    return general_management.get(house_name, None)

def get_house_by_general(general):
    house = ''
    if general in generals_harkonnen:
        house = 'Harkonnen'
    elif general in generals_atreides:
        house = 'Atreides'
    elif general in generals_guild:
        house = 'Guild'
    elif general in generals_bene_gesserit:
        house = 'Bene_Gesserit'
    elif general in generals_fremen:
        house = 'Fremen'
    elif general in generals_emperor:
        house = 'Emperor'
    return house