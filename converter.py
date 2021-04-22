#define a function that converts the format of cards from
# Two of Hearts to 2h




def convert_to_form(string):
    """Takes string of the type 'Two of Hearts'
    and Converts it to '2h'. """
    dict_conv = {
        'Ace': 'A',
        'Two': '2',
        'Three': '3',
        'Four': '4',
        'Five': '5',
        'Six': '6',
        'Seven': '7',
        'Eight': '8',
        'Nine': '9',
        'Ten': 'T',
        'Jack': 'J',
        'Queen': 'Q',
        'King': 'K'}
    print(string)
    # string = string.card_string()
    string = str(string)
    list_words = string.split()
    number = dict_conv[list_words[0]]
    suit = list_words[2][0]
    suit = suit.lower()
    return number+suit


