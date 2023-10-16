from typing import List

from card import Deck
from player import Player
from utils import Hand, Action


class Round:
    def __init__(
        self, player: Player, deck: Deck, dealer_must_hit_at_soft_17: bool = True
    ):
        self.player = player
        self.dealer_must_hit_at_soft_17 = dealer_must_hit_at_soft_17
        self.deck = deck
        self.black_pays = 3 / 2

    def play_round(self):
        player_hand, dealer_hand = self.deal()
        if (dealer_hand.value == 21) & (player_hand.value != 21):
            return -1

        elif (dealer_hand.value < 21) & (player_hand.value == 21):
            return self.black_pays

        elif (dealer_hand.value == 21) & (player_hand.value == 21):
            return 0.0

        else:
            hands = self.play_hand(player_hand, dealer_hand)

        dealer_hand = self.dealer_turn(dealer_hand, hands)

        payout = 0
        for hand in hands:
            hand_pay_out = self.resolve(hand, dealer_hand)

            payout += hand_pay_out

        del player_hand
        del dealer_hand
        return payout

    def deal(self):
        deck = self.deck
        dealer_hand = Hand()
        player_hand = Hand()
        player_hand.new_card(deck.deal(face_up=True))
        dealer_hand.new_card(deck.deal(face_up=True))
        player_hand.new_card(deck.deal(face_up=True))
        dealer_hand.new_card(deck.deal(face_up=False))
        return player_hand, dealer_hand

    def dealer_turn(self, dealer_hand: Hand, hands: List[Hand]):
        if all(hand.is_busted() for hand in hands) if len(hands)> 0 else False:
            return dealer_hand

        while dealer_hand.value < 17:
            dealer_hand.new_card(self.deck.deal(face_up=True))

        if (
            (dealer_hand.value == 17)
            & dealer_hand.is_soft()
            & (self.dealer_must_hit_at_soft_17)
        ):
            dealer_hand.new_card(self.deck.deal(face_up=True))

        return dealer_hand

    def play_hand(
        self, player_hand: Hand, dealer_hand: Hand) -> List[Hand]:
        action = self.player.action(player_hand, dealer_hand)

        if action == Action.hit:
            player_hand.new_card(self.deck.deal(face_up=True))
            if not player_hand.is_busted():
                return self.play_hand(player_hand, dealer_hand)
            else:
                return [player_hand]

        if action == Action.stay:
            return [player_hand]

        if action == Action.double:
            player_hand.new_card(self.deck.deal(face_up=True))
            player_hand.doubled = True
            return [player_hand]

        if action == Action.surrender:
            player_hand.surrendered = True
            return [player_hand]

        if action == Action.split:
            hand1 = Hand(
                [player_hand.cards[0], self.deck.deal(face_up=True)])
            hand2 = Hand(
                [player_hand.cards[1], self.deck.deal(face_up=True)])
            res = self.play_hand(hand1, dealer_hand) + self.play_hand(hand2, dealer_hand)

            return res

    def resolve(self, hand: Hand, dealer_hand: Hand) -> float:
        bet = 2 if hand.doubled else 1

        if hand.surrendered:
            return -0.5

        elif hand.is_busted():  # bust
            return -bet

        elif hand.value == dealer_hand.value:  # push
            return 0

        elif (hand.value <= 21) & (dealer_hand.is_busted()):  # dealer bust but player not
            return bet

        elif (hand.value > dealer_hand.value) & (not dealer_hand.is_busted()):  # higher value
            return bet

        else:
            return -bet