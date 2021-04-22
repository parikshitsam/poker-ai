from poker.hand import Combo
import holdem_calc
import numpy as np
import matplotlib.pyplot as plt
from converter import convert_to_form





def bar_saver(player_hands,players):
    """Takes a list of player hands of the form 
        [['Two of Hearts','Three of Diamonds'],['Jack of Clubs','Queen of Spades'],etc]
        outputs a save_file of player_probabilities"""
 
    player_cards = []   
    for hand in player_hands:
        card_1 = convert_to_form(hand[0])
        card_2 = convert_to_form(hand[1])
        player_cards.append(Combo(card_1+card_2))
    
    villan_hand = None
    board = []
    exact_calculation = False
    num_sims = 1
    read_from_file = False
    verbose = True
    
    prob_list = []
    
    for hero_hand in player_cards:
    
        odds = holdem_calc.calculate_odds_villan(board, exact_calculation,
                                num_sims, read_from_file ,
                                hero_hand, villan_hand,
                                verbose, print_elapsed_time = False)[0]['win']*100
    
        prob_list.append(odds)

    print(prob_list)

    # players = ['player 1', 'player 2','player 3','player 4','player 5']
    # players = []

    for player in
    
    fig, ax = plt.subplots()
    width = 0.75 # the width of the bars
    ind = np.arange(len(prob_list))  # the x locations for the groups
    ax.barh(players, prob_list, width, color="blue")
    ax.set_yticks(ind+width/2)
    ax.set_yticklabels(players, minor=False)
    plt.title('prob_winning')
    plt.xlabel('prob_winning')
    plt.ylabel('Players')
    # plt.show()
    plt.savefig('cards/test.png', dpi=300, format='png', bbox_inches='tight')
    
    # def bar_saver(player_cards):
    #     """Takes players cards and outputs
    #      everyones probablity of winning"""

