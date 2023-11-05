from enum import Enum, auto
from typing import List

from card import Card
from copy import deepcopy

class Hand:
    def __init__(self, cards: List[Card] = None):
        self.cards = cards if cards else []
        self.aces = sum([1 for card in self.cards if card.value == 1])
        self.surrendered = False
        self.doubled = False
        self.value = self.calc_value()

    def calc_value(self):
        out = 0

        for card in self.cards:
            if (card.value in Card.face.keys()) and (card.value > 10):
                out += 10
            elif card.value == 1:
                out += 11

            else:
                out += card.value

        for ace in range(self.aces):
            if out > 21:
                out -= 10

        return out

    def new_card(self, card: Card):
        self.cards.append(card)
        if card.value == 1:
            self.aces += 1

        self.value = self.calc_value()

    def is_busted(self):
        return self.value > 21

    def is_soft(self):
        return self.aces > 0

    def __repr__(self):
        return str(self.cards)

    def __len__(self):
        return len(self.cards)


    def __getitem__(self, item):
        return self.cards[item]

    def __deepcopy__(self, memodict={}):
        return Hand(cards=deepcopy(self.cards))

class Action(Enum):
    hit = auto()
    stay = auto()
    double = auto()
    surrender = auto()
    split = auto()
