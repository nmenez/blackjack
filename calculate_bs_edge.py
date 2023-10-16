from rules import Round
from card import Deck, Card
from player import BasicStrategyPlayer, CardCounter
import matplotlib.pyplot as plt
from numpy import average
import pandas as pd
import numpy as np

class SuperEfficient(Deck):
    def __init__(self, n=1, deals=100, observers=[]):
        super().__init__(n, observers)
        self.rand_int = np.random.randint(0, 52*n, deals)
        self.index = 0

    def shuffle(self):
        for observer in self.observers:
            observer.observe("shuffled")

    def deal(self, face_up=True) -> Card:
        card_place = self.rand_int[self.index]
        card = self.cards[card_place]
        self.index += 1
        return card


payout_history = []
true_count_history = []

player = BasicStrategyPlayer(100, 1.)
n = int(100*1e6)
deck = SuperEfficient(6, n*10, observers=[player])
deck.shuffle()
deck.burn()
round = Round(player, deck, dealer_must_hit_at_soft_17=True)


for i  in range(int(n)):
    if i % 100000 == 0:
        print(i)
    payout_history.append(round.play_round())
    # true_count_history.append(player.true_count())

    deck.shuffle()
    deck.burn()

print(f'{average(payout_history)* 100}%')
#
# data = pd.DataFrame({'true_count': true_count_history, 'payout': payout_history})
# print(data.groupby('true_count').mean())


#
#
# n = 1e3
# player = CardCounter(1, 1)
# deck = Deck(6, observers=[player])
# deck.shuffle()
#
# history_true_counts = []
# for i in range(5*int(1e6)):
#     if i % 100_000==0:
#         print(i)
#     card = deck.deal()
#     # print(f'{card}, {player.running_count}, {player.true_count()}')
#     history_true_counts.append(player.true_count())
#     if deck.index > int(0.75 * len(deck)):
#         deck.shuffle()
#
# import matplotlib.pyplot as plt
#
# min(history_true_counts)
# max(history_true_counts)
#
# count_values = list(range(-9, 10))
# freq = [
#     100
#     * sum([1 for c in history_true_counts if c == count_value])
#     / len(history_true_counts)
#     for count_value in count_values
# ]
#
#
# plt.bar(count_values, freq)
# plt.show()
# for count, f in zip(count_values, freq):
#     print(f'{count}: {f}%')