# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 13:58:28 2021

@author: parik
"""
## ***Post River***

def prob_winning(hand1, comm_cards):
    """Takes hand1 as given
    Returns prob of winning"""
    all_hands = list_of_all_possible_hands()
    
    win_list = []
    
    counter = 0
    
    for hand in all_hands:
        if better_than(hand1,hand):
            win_list[counter] = 1
        else:
            win_list[counter] = 0
        
        counter+= 1
    
    p_winning = sum(win_list)/len(win_list)
    
    return p_winning
    