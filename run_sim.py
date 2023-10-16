from player import BasicStrategyPlayer
from card import Deck, Card
from rules import Round
import numpy as np




starting_bank_roll = int(2000/25)
player = BasicStrategyPlayer(starting_bank_roll, 1.)
deck = Deck(6, observers=[player])
deck.shuffle()
deck.burn()



n = 0
history_bank_roll = []
history_win_loss = []
round = Round(player, deck, dealer_must_hit_at_soft_17=True)
while (player.bankroll > 0) and (n<1e6):
    n += 1
    # print(f'round {n}')
    bet = player.bet()
    winloss = round.play_round()
    # print(f'winloss {winloss}')
    player.bankroll += winloss
    # print(f'bankroll: {player.bankroll}')
    history_win_loss.append(winloss)
    history_bank_roll.append(player.bankroll)

    if deck.index > 6 * 52 * 0.75:
        deck.shuffle()
        deck.burn()

import matplotlib.pyplot as plt

plt.plot(range(len(history_bank_roll)), history_bank_roll)
plt.show()