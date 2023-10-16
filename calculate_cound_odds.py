from rules import Round
from card import Deck
from player import BasicStrategyPlayer, CardCounter
import matplotlib.pyplot as plt
from numpy import average



starting_bank_roll = 1000
player = BasicStrategyPlayer(starting_bank_roll, 25.0)
deck = Deck(6, observers=[player])
deck.shuffle()
deck.burn()

n = 0
history_bank_roll = []
history_win_loss = []
round = Round(player, deck, dealer_must_hit_at_soft_17=True)

for i  in range(int(n)):
    if i % 1000 == 0:
        print(i)
    out.append(round.play_round(1))

    deck.shuffle()
    deck.burn()
print(f'{average(out) *100:.2f}%')

