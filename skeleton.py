# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 11:18:50 2021

@author: parik
"""


ai_hand = random_hand()

opp_hand = random_hand()

# Assign Roles

# **PREFLOP**

# prob_winning(your_hand)

sb_move = move(roles,hands)

bb_move = move(roles,hands, sb_move)

# Assign roles

# **FLOP**


# prob_winning(flopcards, your_hand)

flop = show_flop()

p1_move = flop_move(history, flop, your_hand)
p2_move = flop_move(history, flop, your_hand)





# **TURN**



turn = show_turn()

# **RIVER**

river = show_river()
    
    