from utils import Hand, Action
from card import Card, Deck
from math import floor, ceil


class Player:
    def __init__(self, bankroll: float, min_bet: float):
        super().__init__()
        self.bankroll = bankroll
        self.min_bet = min_bet

    def bet(self):
        pass

    def action(self, player_hand, dealer_hand):
        pass

    def observe(self, *args, **kwargs):
        pass

    def bet(self):
        # self.bankroll -= self.min_bet
        return self.min_bet


class BasicStrategyPlayer(Player):
    def action(self, player_hand, dealer_hand):
        # surrenders
        if len(player_hand.cards) == 2:
            if (player_hand.value == 16) & (
                dealer_hand.cards[0].value in (1, 9, 10, 11, 12, 13)) & (player_hand.cards[0] != 8):
                return Action.surrender

            elif (player_hand.value == 15) & (
                dealer_hand.cards[0].value in (10, 11, 12, 13)
            ):
                return Action.surrender

            # splits
            elif player_hand.cards[0].value == player_hand.cards[1].value:
                return self.split(player_hand, dealer_hand)

            # soft
            elif player_hand.aces > 0:
                return self.soft_totals(player_hand, dealer_hand)

        return self.hard_totals(player_hand, dealer_hand)

    def split(self, player_hand: Hand, dealer_hand: Hand):
        # splits
        if (player_hand.cards[0].value == 1) & (player_hand.cards[1].value == 1):
            return Action.split

        if (player_hand.cards[0].value == 9) & (player_hand.cards[1].value == 9):
            if dealer_hand.cards[0].value in (2, 3, 4, 5, 6, 8, 9):
                return Action.split
            else:
                return Action.stay

        if player_hand.cards[0].value in (10, 11, 12, 13):
            return Action.stay

        if (player_hand.cards[0].value == 8) & (player_hand.cards[1].value == 8):
            return Action.split

        if (
            (player_hand.cards[0].value == 7)
            & (player_hand.cards[1].value == 7)
            & (dealer_hand.cards[0].value in (2, 3, 4, 5, 6, 7))
        ):
            return Action.split

        elif (
            (player_hand.cards[0].value == 6)
            & (player_hand.cards[1].value == 6)
            & (dealer_hand.cards[0].value in (2, 3, 4, 5, 6))
        ):
            return Action.split

        elif (
            (player_hand.cards[0].value == 5)
            & (player_hand.cards[1].value == 5)
            & (dealer_hand.cards[0].value in (2, 3, 4, 5, 6, 7, 8, 9))
        ):
            return Action.split

        elif (
            (player_hand.cards[0].value == 4)
            & (player_hand.cards[1].value == 4)
            & (dealer_hand.cards[0].value in (5, 6))
        ):
            return Action.split

        elif (
            (player_hand.cards[0].value == 3)
            & (player_hand.cards[1].value == 3)
            & (dealer_hand.cards[0].value in (2, 3, 4, 5, 6, 7))
        ):
            return Action.split

        elif (
            (player_hand.cards[0].value == 2)
            & (player_hand.cards[1].value == 2)
            & (dealer_hand.cards[0].value in (2, 3, 4, 5, 6, 7))
        ):
            return Action.split

        else:
            return Action.hit

    def soft_totals(self, player_hand, dealer_hand):
        if player_hand.value >= 20:
            return Action.stay

        if player_hand.value == 19:
            if dealer_hand.cards[0].value == 6:
                return Action.double
            else:
                return Action.stay

        if player_hand.value == 18:
            if dealer_hand.cards[0].value in (2, 3, 4, 5, 6):
                return Action.double
            elif dealer_hand.cards[0].value in (9, 10, 11, 12, 13):
                return Action.hit
            else:
                return Action.stay

        if player_hand.value == 17:
            if dealer_hand.cards[0].value in (3, 4, 5, 6):
                return Action.double
            else:
                return Action.hit

        if player_hand.value in (16, 15):
            if dealer_hand.cards[0].value in (4, 5, 6):
                return Action.double
            else:
                return Action.hit

        if player_hand.value in (14, 13):
            if dealer_hand.cards[0].value in (5, 6):
                return Action.double
            else:
                return Action.hit

    def hard_totals(self, player_hand, dealer_hand):
        if player_hand.value >= 17:
            return Action.stay

        elif player_hand.value in (16, 15, 14, 13):
            if dealer_hand.cards[0].value in (2, 3, 4, 5, 6):
                return Action.stay
            else:
                return Action.hit

        elif player_hand.value == 12:
            if dealer_hand.cards[0].value in (4, 5, 6):
                return Action.stay
            else:
                return Action.hit

        elif player_hand.value == 11:
            return Action.double if len(player_hand.cards) == 2 else Action.hit

        elif player_hand.value == 10:
            if dealer_hand.cards[0].value in (2, 3, 4, 5, 6, 7, 8, 9):
                return Action.double if len(player_hand.cards) == 2 else Action.hit
            else:
                return Action.hit

        elif dealer_hand.value == 9:
            if dealer_hand.cards[0].value in (3, 4, 5, 6):
                return Action.double if len(player_hand.cards) == 2 else Action.hit
            else:
                return Action.hit
        else:
            return Action.hit


class CardCounter(BasicStrategyPlayer):
    def __init__(self, bankroll: float, min_bet: float):
        super().__init__(bankroll, min_bet)
        self.running_count = 0
        self.cards_dealt = 0
        self.num_decks = None

    def observe(self, *args, **kwargs):
        if type(args[0]) == Card:
            card = args[0]
            if card.face_up and (card.value in (2, 3, 4, 5, 6)):
                self.running_count += 1
                self.cards_dealt += 1

            elif card.face_up and (card.value in (1, 10, 11, 12, 13)):
                self.running_count -= 1
                self.cards_dealt += 1

        elif args[0] == "shuffled":
            self.running_count = 0
            self.cards_dealt = 0

        elif type(args[0]) == Deck:
            self.num_decks = args[0].n

    def true_count(self):
        remaining_decks = (self.num_decks * 52 - self.cards_dealt) / 52
        if self.running_count > 0:
            return floor(self.running_count / remaining_decks)
        elif self.running_count < 0:
            return ceil(self.running_count / remaining_decks)
        else:
            return 0

    def bet(self):
        true_count = self.true_count()
        if true_count <= 3:
            return self.min_bet

        else:
            print(f'raising bet: {true_count * self.min_bet}')
            return (true_count) * self.min_bet
