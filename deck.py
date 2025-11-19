import random

class Deck :
    def __init__(self, name, deck):
        self.name = name
        self.original_deck = deck
        self.deck = dict()
        self.cards_in_play = []
        self.shuffle_deck()

    def __str__(self):
        ret_str = '{} \n'.format(str(self.name))
        ret_str += '   original_deck: {} \n'.format(str(self.original_deck))
        ret_str += '   shuffled_deck: {} \n'.format(str(self.deck))
        return ret_str

    def shuffle_deck(self):
        keys = list(self.original_deck.keys())
        random.shuffle(keys)
        random.shuffle(keys)
        random.shuffle(keys)
        for key in keys:
            self.deck.update({key:self.original_deck[key]})

        for list_of_piles_in_play in self.cards_in_play:
            for pile in list_of_piles_in_play:
                for card, value in pile.items():
                    self.deck.pop(card)

    def deal_card(self):
        if 0 == len(self.deck):
            self.shuffle_deck()

        card, value = next(iter(self.deck.items()))
        self.deck.pop(card)
        return card, value

    def place_in_deck(self, card, value): #returns a card to the shuffled deck ie appends it to the existing deck
        self.deck[card] = value

    def add_pile_to_cards_in_play(self, *pile): #when a shuffle occurs the cards in these piles are removed from the deck
        self.cards_in_play.append(pile)

    def discard(self, pile, card, value): #places card on discard pile. A discard pile only contains 1 card at a time.
        for last_card in list(pile):
            del pile[last_card]
        pile[card] = value  #place the new card onto the specified pile


