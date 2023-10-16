from card import Deck, Card, Suit
from unittest import TestCase

class TestCard(TestCase):
    def test_face_value_jack(self):
        card = Card(Suit.spades, 11)

        self.assertEqual(str(card), 'jack of spades')

    def test_face_value_queen(self):
        card = Card(Suit.spades, 12)

        self.assertEqual(str(card), 'queen of spades')

    def test_face_value_king(self):
        card = Card(Suit.spades, 13)

        self.assertEqual(str(card), 'king of spades')

    def test_desc_face(self):
        card = Card.from_desc('ace of spades')
        self.assertEqual(card.value, 1)
        self.assertEqual(card.suit, Suit.spades)

        card = Card.from_desc('jack of spades')
        self.assertEqual(card.value, 11)
        self.assertEqual(card.suit, Suit.spades)

        card = Card.from_desc('queen of spades')
        self.assertEqual(card.value, 12)
        self.assertEqual(card.suit, Suit.spades)

        card = Card.from_desc('king of spades')
        self.assertEqual(card.value, 13)
        self.assertEqual(card.suit, Suit.spades)

    def test_desc_number(self):
        for num in ['2','3', '4','5', '6','7','8', '9']:
            card = Card.from_desc(f'{num} spades')
            self.assertEqual(card.value, int(num))
            self.assertEqual(card.suit, Suit.spades)


class TestDeck(TestCase):
    def test_init(self):
        deck = Deck(n=1)
        self.assertEqual(len(deck), 52)
        self.assertEqual(deck.index, 0)
        card = deck.deal()
        self.assertEqual(str(card), 'ace of spades')

    def test_init_multideck(self):
        deck = Deck(n=2)
        self.assertEqual(len(deck), 104)
        self.assertEqual(deck.index, 0)

    def test_shuffle(self):
        deck = Deck(n=1)
        self.assertEqual(len(deck), 52)
        self.assertEqual(deck.index, 0)
        card = deck.deal(face_up=False)

        deck.shuffle()
        for _ in range(52):
            deck.deal()