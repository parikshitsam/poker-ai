from converter import convert_to_form

def convert_board(board_object):

    board_converted = []
    for card in board_object:
        card = str(card)
        card_converted = convert_to_form(card)
        board_converted.append(card_converted)
    
    return board_converted


