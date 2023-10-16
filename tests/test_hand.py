from unittest import TestCase

from card import Card, Suit
from utils import Hand


class TestHand(TestCase):
    def test_simple(self):
        hand = Hand([Card(Suit.spades, 2), Card(Suit.clovers, 3)])
        self.assertEqual(hand.value, 5)

    def test_blackjack(self):
        hand = Hand([Card(Suit.spades, 11), Card(Suit.spades, 1)])
        self.assertEqual(hand.value, 21)

    def test_three_aces(self):
        hand = Hand([Card(Suit.spades, 1), Card(Suit.hearts, 1), Card(Suit.clovers, 1)])
        self.assertEqual(hand.value, 13)

    def test_10_and_2_aces(self):
        hand = Hand(
            [Card(Suit.spades, 10), Card(Suit.hearts, 1), Card(Suit.clovers, 1)]
        )
        self.assertEqual(hand.value, 12)

    def test_2_10s_and_an_ace(self):
        hand = Hand(
            [Card(Suit.spades, 10), Card(Suit.hearts, 10), Card(Suit.clovers, 1)]
        )
        self.assertEqual(21, hand.value)

    def test_7_8_ace(self):
        hand = Hand([Card(Suit.spades, 7), Card(Suit.hearts, 8), Card(Suit.clovers, 1)])
        self.assertEqual(hand.value, 16)

    def test_8_7_ace_8(self):
        hand = Hand(
            [
                Card(Suit.spades, 8),
                Card(Suit.hearts, 7),
                Card(Suit.clovers, 1),
                Card(Suit.diamonds, 8),
            ]
        )
        self.assertEqual(hand.value, 24)

    def test_sequence(self):
        hand = Hand([Card(Suit.diamonds, 5), Card(Suit.hearts, 9)])
        self.assertEqual(hand.value, 14)

        hand.new_card(Card(Suit.spades, 1))
        self.assertEqual(hand.value, 15)

        hand.new_card(Card(Suit.spades, 7))
        self.assertEqual(hand.value, 22)
        self.assertEqual(hand.aces, 1)