from poker import Range
from poker.hand import Combo

import holdem_calc
import holdem_functions

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.core.display import display, HTML

hero_hand = Combo('6sJc')
villan_hand = None
board = []
exact_calculation = False
num_sims = 1
read_from_file = False
verbose = True

odds = holdem_calc.calculate_odds_villan(board, exact_calculation,
                            num_sims, read_from_file ,
                            hero_hand, villan_hand,
                            verbose, print_elapsed_time = True)
print(odds)
