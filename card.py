from enum import Enum, auto
from itertools import product
from random import shuffle


class Suit(Enum):
    spades = auto()
    hearts = auto()
    diamonds = auto()
    clovers = auto()


class Card:
    face = {
        11: "jack",
        12: "queen",
        13: "king",
        1: 'ace'
    }

    def __init__(self, suit: Suit, value: float, face_up=True, observers=[]):
        self.suit = suit
        self.value = value
        self._face_up = face_up
        self.observers = observers

    @classmethod
    def from_desc(cls, desc: str):
        if 'of' in desc:
            face, suit = desc.split(' of ')
            value = {item: key for key, item in Card.face.items()}[face]
            suit = Suit[suit]
            return Card(suit, value)
        else:
            value, suit = desc.split(' ')
            suit = Suit[suit]
            return Card(suit, int(value))

    def __repr__(self):
        if not self.face_up:
            return "face_down"
        elif self.value in self.face.keys():
            return f"{self.face[self.value]} of {self.suit.name}"
        elif self.value == 1:
            return f"ace of {self.suit.name}"
        else:
            return f"{self.value} {self.suit.name}"

    @property
    def face_up(self):
        return self._face_up

    @face_up.setter
    def face_up(self, value):
        self._face_up = value
        for observer in self.observers:
            observer.observe(self)


class Deck:
    def __init__(self, n=1, observers=[]):
        self.n = n
        self.cards = [
            Card(suit, value) for (suit, value) in product(list(Suit), range(1, 14))
        ] * n
        self.index = 0

        self.observers = observers
        for observer in observers:
            observer.observe(self)

    def shuffle(self):
        self.index = 0
        self.cards = [
            Card(suit, value) for (suit, value) in product(list(Suit), range(1, 14))
        ] * self.n
        shuffle(self.cards)
        for observer in self.observers:
            observer.observe("shuffled")

    def deal(self, face_up=True) -> Card:
        if self.index < len(self.cards):
            card = self.cards[self.index]
            card.face_up = face_up
            self.index += 1

            for observer in self.observers:
                observer.observe(card)

            return card
        else:
            raise Exception("empty deck")

    def burn(self):
        self.index += 1

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, item):
        return self.cards[item]

    def pull_card(self, card: Card):
        for index, card_in_deck in enumerate(self.cards):
            if (card.suit == card_in_deck.suit) & (card.value==card_in_deck.value):
                self.cards.pop(index)
                return

class ProbabilityDeck(Deck):
    def __init__(self, n=1, observers=[]):
        super().__init__(n, observers)

        self.card_counts = {value: 4 * self.n for value in range(1, 14)}

    def shuffle(self):
        super().shuffle()
        self.card_counts = {value: 4*self.n for value in range(1, 14)}
    def deal(self, face_up=True) -> Card:
        card = super().deal()
        self.card_counts[card.value] -= 1
        return card

    def pull_card(self, card: Card):
        super().pull_card(card)
        self.card_counts[card.value] -= 1

    def probability(self, value):
        return max(0, self.card_counts[value]/ len(self))

    def pull_card_value(self, card: Card):
        self.card_counts[card.value] -= 1
        for index, card_in_deck in enumerate(self.cards):
            if (card.value==card_in_deck.value):
                self.cards.pop(index)
                return

if __name__ == "__main__":

    deck = ProbabilityDeck(n=1)
    res = deck.probability(1)
    print(res)
    deck.pull_card(Card.from_desc('ace of spades'))


    res = deck.probability(10)
    print(res)