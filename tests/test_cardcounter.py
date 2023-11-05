from unittest import TestCase
from card import Card, Suit, Deck
from rules import Round
from utils import Hand, Action
from player import Player
from player import CardCounter


class TestCardCounter(TestCase):
    def test_observe_new_deck(self):
        player = CardCounter(1, 1)
        deck = Deck(n=6, observers=[player])

        self.assertEqual(player.num_decks, 6)

    def test_shuffle(self):
        player = CardCounter(1, 1)
        deck = Deck(n=6, observers=[player])
        deck.deal()
        deck.deal()

        self.assertEqual(player.cards_dealt, 2)

        deck.shuffle()
        self.assertEqual(player.cards_dealt, 0)

    def test_true_count(self):
        player = CardCounter(1, 1)
        player.num_decks = 6
        player.cards_dealt = 64
        player.running_count = 5
        self.assertEqual(player.true_count(), 1)

    def test_true_count_6deck_running_11(self):
        player = CardCounter(1, 1)
        player.num_decks = 6
        player.cards_dealt = 10
        player.running_count = 15
        self.assertEqual(player.true_count(), 2)

    def test_particular_sequence(self):
        player = CardCounter(1, 1)
        deck = Deck(6, observers=[player])

        deck.cards[:6] = [
            Card(Suit.clovers, 7),
            Card(Suit.spades, 13),
            Card(Suit.hearts, 2),
            Card(Suit.diamonds, 4),
            Card(Suit.hearts, 9),
            Card(Suit.hearts, 3),
        ]

        for _, expected in zip(range(7), [0, -1, 0, 1, 1, 2]):
            deck.deal()
            self.assertEqual(player.running_count, expected )
