from card import Card, Deck, ProbabilityDeck, Suit
from rules import Hand, Action

from probability_utils import build_dealer_hands, build_hands, calculate_prob, deepcopy
from probability_node import Node

class GameState(Node):
    def __init__(self, hand: Hand,
                 dealer_hand: Hand,
                 deck: ProbabilityDeck, probability):
        self.hand = hand
        self.dealer_hand = dealer_hand
        self.deck = deck

        super().__init__(probability=probability)

    def __repr__(self):
        return f'hand: {self.hand}| dealer_hand: {self.dealer_hand} | probabiltiy: {self.probability} | children: {len(self.children)}| busted:{self.value == -1}'

    def get_hands(self):
        hand = self.hand
        if (hand.value < 17) | ((hand.aces > 0) & (hand.value == 17)):
            for card in [Card(Suit.spades, value) for value in range(1, 14)]:
                new_hand = Hand(hand.cards + [card])
                prob = self.probability * self.deck.probability(card.value)
                deck = deepcopy(self.deck)
                deck.pull_card_value(card)
                node = GameState(hand=new_hand,
                                 dealer_hand=self.dealer_hand,
                                 deck=deck,
                                 probability=prob
                                 )

                node.get_hands()
                self.add_child(node)
        else:
            return


if __name__ == "__main__":
    deck = ProbabilityDeck(n=6)
    deck.pull_card_value(Card.from_desc('10 spades'))
    deck.pull_card_value(Card.from_desc('2 spades'))
    deck.pull_card_value(Card.from_desc('2 spades'))

    state = GameState(hand=Hand([Card.from_desc('10 spades'),
                                 Card.from_desc('2 spades')]),
                      dealer_hand=Hand([Card.from_desc('2 spades')]),
                      deck=deck,
                      probability=1)

    state.get_hands()
    print('hold')