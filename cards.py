import random


class Card:
    def __init__(self):
        pass


def create_shoe(number_of_decks):
    ranks = [i + 2 for i in range(9)]
    ranks = ranks + ["A", "K", "Q", "J"]
    suits = ["spades", "hearts", 'clubs', "diamonds"]
    shoe = []
    for suit in suits:
        for rank in ranks:
            card = Card()
            card.number = rank
            card.suit = suit
            if rank == "K" or rank == "Q" or rank == "J":
                card.value = 10
            elif rank == "A":
                card.value = 11
            else:
                card.value = rank
            card.image_path = f"./PNG-cards-1.3/{rank}_of_{suit}.png"
            for i in range(number_of_decks):
                shoe.append(card)
    return shoe


def shuffle_cards(deck: list):
    random.shuffle(deck)
    return deck
