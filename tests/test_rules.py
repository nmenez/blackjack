from unittest import TestCase
from card import Card, Suit, Deck
from rules import Round
from utils import Hand, Action
from player import Player


class TestRound(TestCase):
    def test_dealer_blackjack(self):
        class MockDeck(Deck):
            def __init__(self, n=1):
                super().__init__(n)
                self.cards = [
                    Card(Suit.spades, 2),
                    Card(Suit.spades, 10),
                    Card(Suit.spades, 3),
                    Card(Suit.spades, 1),
                ]
        deck = MockDeck()
        round = Round(Player(1, 1), deck)
        res = round.play_round()
        self.assertEqual(-1, res)
        self.assertEqual(deck.index, 4)

    def test_player_blackjack(self):
        class MockDeck(Deck):
            def __init__(self, n=1):
                super().__init__(n)
                self.cards = [
                    Card.from_desc('ace of spades'),
                    Card.from_desc('2 diamonds'),
                    Card.from_desc('jack of hearts'),
                    Card.from_desc('3 clovers'),
                ]

        deck = MockDeck()
        round = Round(Player(1, 1), deck)
        res = round.play_round()
        self.assertEqual(round.black_pays, res)

    def test_blackjack_push(self):
        class MockDeck(Deck):
            def __init__(self, n=1):
                super().__init__(n)
                self.cards = [
                    Card.from_desc('ace of spades'),
                    Card.from_desc('king of diamonds'),
                    Card.from_desc('jack of hearts'),
                    Card.from_desc('ace of clovers'),
                ]

        deck = MockDeck()
        round = Round(Player(1, 1), deck)
        res = round.play_round()
        self.assertEqual(0, res)


    def test_hit_stay(self):
        class MockDeck(Deck):
            def __init__(self, n=1):
                super().__init__(n)
                self.cards = [
                    Card(Suit.spades, 2),
                    Card(Suit.spades, 10),
                    Card(Suit.spades, 3),
                    Card(Suit.spades, 1),
                ]

        class MockPlayer(Player):
            def __init__(self, bankroll):
                super().__init__(bankroll, 1)
                self.actions = [Action.hit, Action.stay]

            def action(self, player_hand, dealer_hand):
                return self.actions.pop(0)

        round = Round(MockPlayer(1), MockDeck())
        hand = Hand([Card(Suit.hearts, 2), Card(Suit.hearts, 3)])

        res = round.play_hand(hand, Hand())

        self.assertEqual(len(res), 1)
        hand = res[0]
        self.assertEqual("[2 hearts, 3 hearts, 2 spades]", str(hand.cards))

    def test_hit_bust(self):
        class MockDeck(Deck):
            def __init__(self, n=1):
                super().__init__(n)
                self.cards = [
                    Card(Suit.spades, 10),
                    Card(Suit.spades, 10),
                    Card(Suit.spades, 3),
                    Card(Suit.spades, 1),
                ]

        class MockPlayer(Player):
            def __init__(self, bankroll):
                super().__init__(bankroll, 1)

            def action(self, player_hand, dealer_hand):
                return Action.hit

        round = Round(MockPlayer(1), MockDeck())
        hand = Hand([Card(Suit.hearts, 10), Card(Suit.hearts, 6)])

        res = round.play_hand(hand, Hand())
        hand = res[0]
        self.assertTrue(hand.is_busted())

    def test_double(self):
        class MockDeck(Deck):
            def __init__(self, n=1):
                super().__init__(n)
                self.cards = [
                    Card(Suit.spades, 10),
                    Card(Suit.spades, 10),
                    Card(Suit.spades, 3),
                    Card(Suit.spades, 1),
                ]

        class MockPlayer(Player):
            def __init__(self, bankroll):
                super().__init__(bankroll, 1)

            def action(self, player_hand, dealer_hand):
                return Action.double

        round = Round(MockPlayer(1), MockDeck())
        hand = Hand(
            [Card(Suit.hearts, 10, face_up=True), Card(Suit.hearts, 6, face_up=True)]
        )

        res = round.play_hand(hand, Hand())

        self.assertEqual(len(res), 1)
        hand = res[0]
        self.assertEqual("[10 hearts, 6 hearts, 10 spades]", str(hand.cards))
        self.assertEqual(hand.value, 26)

    def test_surrender(self):
        class MockDeck(Deck):
            def __init__(self, n=1):
                super().__init__(n)
                self.cards = [
                    Card(Suit.spades, 10),
                    Card(Suit.spades, 10),
                    Card(Suit.spades, 3),
                    Card(Suit.spades, 1),
                ]

        class MockPlayer(Player):
            def __init__(self, bankroll):
                super().__init__(bankroll, 1)

            def action(self, player_hand, dealer_hand):
                return Action.surrender

        round = Round(MockPlayer(1), MockDeck())
        hand = Hand([Card(Suit.hearts, 10), Card(Suit.hearts, 6)])

        res = round.play_hand(hand, Hand())

        hand = res[0]
        bet = res[0]
        self.assertTrue(hand.surrendered)

    def test_split_once(self):
        class MockDeck(Deck):
            def __init__(self, n=1):
                super().__init__(n)
                self.cards = [
                    Card(Suit.spades, 10),
                    Card(Suit.spades, 9),
                    Card(Suit.spades, 3),
                    Card(Suit.spades, 1),
                ]

        class MockPlayer(Player):
            def __init__(self, bankroll):
                super().__init__(bankroll, 1)

                self.actions = [Action.split, Action.stay, Action.stay]

            def action(self, player_hand, dealer_hand):
                return self.actions.pop(0)

        round = Round(MockPlayer(1), MockDeck())
        hand = Hand([Card(Suit.spades, 8), Card(Suit.hearts, 8)])

        res = round.play_hand(hand, Hand())

        self.assertEqual(len(res), 2)
        for hand in res:
            self.assertEqual(len(hand.cards), 2)

    def test_split_twice(self):
        class MockDeck(Deck):
            def __init__(self, n=1):
                super().__init__(n)
                self.cards = [
                    Card(Suit.spades, 8),
                    Card(Suit.spades, 9),
                    Card(Suit.spades, 3),
                    Card(Suit.spades, 4),
                    Card(Suit.hearts, 2),
                    Card(Suit.hearts, 3),
                ]

        class MockPlayer(Player):
            def __init__(self, bankroll):
                super().__init__(bankroll, 1)

                self.actions = [
                    Action.split,
                    Action.split,
                    Action.hit,
                    Action.stay,
                    Action.stay,
                    Action.stay,
                    Action.stay,
                    Action.stay,
                ]

            def action(self, player_hand, dealer_hand):
                return self.actions.pop(0)

        round = Round(MockPlayer(1), MockDeck())
        hand = Hand([Card(Suit.spades, 8), Card(Suit.hearts, 8)])

        res = round.play_hand(hand, Hand())

        self.assertEqual(len(res), 3)
        hand1 = res[0]
        self.assertEqual(len(hand1.cards), 3)
        hand2 = res[1]
        self.assertEqual(len(hand2.cards), 2)
        hand3 = res[2]
        self.assertEqual(len(hand3.cards), 2)

    def test_split_aces(self):
        class MockDeck(Deck):
            def __init__(self, n=1):
                super().__init__(n)
                self.cards = [
                    Card(Suit.spades, 10),
                    Card(Suit.spades, 10),
                    Card(Suit.spades, 3),
                    Card(Suit.spades, 4),
                    Card(Suit.hearts, 2),
                    Card(Suit.hearts, 3),
                ]

        class MockPlayer(Player):
            def __init__(self, bankroll):
                super().__init__(bankroll, 1)

                self.actions = [
                    Action.split,
                    Action.stay,
                    Action.stay,
                    Action.stay,
                    Action.stay,
                    Action.stay,
                    Action.stay,
                ]

            def action(self, player_hand, dealer_hand):
                return self.actions.pop(0)

        round = Round(MockPlayer(1), MockDeck())
        hand = Hand([Card(Suit.spades, 1), Card(Suit.hearts, 1)])

        res = round.play_hand(hand, Hand())

        self.assertEqual(len(res), 2)
        hand1 = res[0]
        self.assertEqual(len(hand1.cards), 2)

        hand2 = res[1]
        self.assertEqual(len(hand2.cards), 2)


class TestDealerTurn(TestCase):
    def test_dealer_turn_must_hit(self):
        dealer_hand = Hand([Card.from_desc('2 spades'),
                            Card.from_desc('3 spades')])

        class MockDeck(Deck):
            def __init__(self, n=1):
                super().__init__(n)
                self.cards = [
                    Card(Suit.spades, 10),
                    Card(Suit.diamonds, 10),
                    Card(Suit.spades, 3),
                    Card(Suit.spades, 4),
                    Card(Suit.hearts, 2),
                    Card(Suit.hearts, 3),
                ]

        round = Round(None, MockDeck())
        dealer_hand = round.dealer_turn(dealer_hand, [])
        self.assertEqual(len(dealer_hand), 4)
        self.assertEqual(str(dealer_hand.cards[2]), '10 spades')
        self.assertEqual(str(dealer_hand.cards[3]), '10 diamonds')
        self.assertEqual(str(dealer_hand.cards[3]), '10 diamonds')



    def test_dealer_soft_17(self):
        dealer_hand = Hand([Card.from_desc('ace of spades'),
                            Card.from_desc('6 hearts')])

        class MockDeck(Deck):
            def __init__(self, n=1):
                super().__init__(n)
                self.cards = [
                    Card(Suit.spades, 10),
                    Card(Suit.diamonds, 10),
                ]


        round = Round(None, MockDeck(), dealer_must_hit_at_soft_17=True)

        dealer_hand = round.dealer_turn(dealer_hand, [])

        self.assertEqual(len(dealer_hand), 3)
        self.assertEqual(dealer_hand.value, 17)

    def test_dealer_turn_all_hands_busted(self):
        hand1 = Hand([Card.from_desc('jack of hearts'),
                      Card.from_desc('5 diamonds'),
                      Card.from_desc('8 clovers')])

        hand2 = Hand([Card.from_desc('9 hearts'),
                      Card.from_desc('5 diamonds'),
                      Card.from_desc('8 clovers')])

        dealer_hand = Hand([Card.from_desc('5 hearts'),
                            Card.from_desc('9 clovers')])
        deck = Deck(n=1)
        round = Round(None, deck, dealer_must_hit_at_soft_17=True)
        round.dealer_turn(dealer_hand, [hand1, hand2])
        self.assertEqual(len(dealer_hand), 2)
        self.assertEqual(dealer_hand.value, 14)
        self.assertEqual(deck.index, 0)

    def test_dealer_turn_one_hand_busted(self):
        hand1 = Hand([Card.from_desc('jack of hearts'),
                      Card.from_desc('5 diamonds'),
                      Card.from_desc('8 clovers')])



        dealer_hand = Hand([Card.from_desc('5 hearts'),
                            Card.from_desc('9 clovers')])
        deck = Deck(n=1)
        round = Round(None, deck, dealer_must_hit_at_soft_17=True)
        round.dealer_turn(dealer_hand, [hand1])
        self.assertEqual(len(dealer_hand), 2)
        self.assertEqual(dealer_hand.value, 14)
        self.assertEqual(deck.index, 0)


    def test_dealer_turn_one_hand_busted_other_in_play(self):
        hand1 = Hand([Card.from_desc('jack of hearts'),
                      Card.from_desc('5 diamonds'),
                      Card.from_desc('8 clovers')])

        hand2 = Hand([Card.from_desc('9 hearts'),
                      Card.from_desc('5 diamonds'),
                      Card.from_desc('5 clovers')])

        dealer_hand = Hand([Card.from_desc('5 hearts'),
                            Card.from_desc('9 clovers')])
        class MockDeck(Deck):
            def __init__(self, n=1):
                super().__init__(n)
                self.cards = [
                    Card(Suit.spades, 10),
                    Card(Suit.diamonds, 10),
                    Card(Suit.spades, 3),
                    Card(Suit.spades, 4),
                    Card(Suit.hearts, 2),
                    Card(Suit.hearts, 3),
                ]
        deck = MockDeck()
        round = Round(None, deck, dealer_must_hit_at_soft_17=True)

        round.dealer_turn(dealer_hand, [hand1, hand2])
        self.assertEqual(len(dealer_hand), 3)
        self.assertEqual(dealer_hand.value, 24)
        self.assertEqual(deck.index, 1)




class TestResolve(TestCase):
    def test_dealer_bust(self):
        hand = Hand([Card(Suit.spades, 10), Card(Suit.spades, 6)])
        dealer_hand = Hand(
            [Card(Suit.hearts, 9), Card(Suit.hearts, 10), Card(Suit.spades, 8)]
        )
        round = Round(None, None, True)
        payout = round.resolve(hand, dealer_hand)
        self.assertEqual(payout, 1)

    def test_21_not_blackjack(self):
        hand = Hand(
            [Card(Suit.spades, 10), Card(Suit.spades, 1)]
        )
        dealer_hand = Hand([Card(Suit.hearts, 9), Card(Suit.hearts, 10)])
        round = Round(None, None, True)
        payout = round.resolve(hand, dealer_hand)

        self.assertEqual(1, payout)

    def test_21_push(self):

        hand = Hand([Card(Suit.spades, 10), Card(Suit.spades, 1)])
        dealer_hand = Hand([Card(Suit.hearts, 1), Card(Suit.hearts, 10)])
        round = Round(None, None, True)
        payout = round.resolve(hand, dealer_hand)
        self.assertEqual(payout, 0)

    def test_higher_value(self):
        hand = Hand([Card(Suit.spades, 10), Card(Suit.spades, 8)])
        dealer_hand = Hand([Card(Suit.hearts, 2), Card(Suit.hearts, 10)])
        round = Round(None, None, True)
        payout = round.resolve(hand, dealer_hand)
        self.assertEqual(payout, 1)

    def test_lower_value(self):
        hand = Hand([Card(Suit.spades, 10), Card(Suit.spades, 8)])
        dealer_hand = Hand([Card(Suit.hearts, 10), Card(Suit.hearts, 10)])
        round = Round(None, None, True)
        payout = round.resolve(hand, dealer_hand)
        self.assertEqual(payout, -1)

    def test_player_bust(self):
        hand = Hand([Card.from_desc('8 spades'),
                     Card.from_desc('8 spades'),
                     Card.from_desc(('6 hearts'))])

        dealer_hand = Hand()

        round = Round(None, None, True)
        res = round.resolve(hand, dealer_hand)
        self.assertEqual(res, -1)

    def test_player_surrendered(self):
        hand = Hand([Card.from_desc('10 spades'),
                     Card.from_desc('6 spades'),
                     Card.from_desc(('6 hearts'))])
        hand.surrendered = True

        dealer_hand = Hand([Card.from_desc('ace of spades'),
                            Card.from_desc('2 hearts')])

        round = Round(None, None, True)
        res = round.resolve(hand, dealer_hand)
        self.assertEqual(res, -0.5)

    def test_doubled_win(self):
        hand = Hand([Card.from_desc('7 spades'),
                     Card.from_desc('4 spades'),
                     Card.from_desc(('10 hearts'))])
        hand.doubled = True

        dealer_hand = Hand([Card.from_desc('10 spades'),
                            Card.from_desc('9 hearts')])

        round = Round(None, None, True)
        res = round.resolve(hand, dealer_hand)
        self.assertEqual(res, 2)

    def test_doubled_loss(self):
        hand = Hand([Card.from_desc('7 spades'),
                     Card.from_desc('4 spades'),
                     Card.from_desc(('4 hearts'))])
        hand.doubled = True

        dealer_hand = Hand([Card.from_desc('10 spades'),
                            Card.from_desc('9 hearts')])

        round = Round(None, None, True)
        res = round.resolve(hand, dealer_hand)
        self.assertEqual(res, -2)

