from cards import shuffle_cards, create_shoe
from tkinter import Canvas
from images import resize
# from main import background_text, background_canvas


image_refs = []
deck = create_shoe(1)
shuffle_cards(deck)
window = None
background_text = None
background_canvas = None
face_down_card_canvas = None

all_card_canvases = []


def place_face_down_card():
    global face_down_card_canvas
    face_down_card_image = resize("./Face Down Card.jpeg", 125, 182)
    image_refs.append(face_down_card_image)
    face_down_card_canvas = Canvas(width=125, height=182, bg="white")
    face_down_card_canvas.place(x=625, y=50)
    face_down_card_canvas.create_image(2, 2, image=face_down_card_image, anchor="nw")


# noinspection PyUnresolvedReferences
def remove_face_down_card():
    global face_down_card_canvas
    try:
        face_down_card_canvas.destroy()
        face_down_card_canvas = None
    except AttributeError:
        pass


def set_window(w, bt, bc):
    global window, background_text, background_canvas
    window = w
    background_text = bt
    background_canvas = bc


def create_and_place_card(card, posx, posy):
    card_image = resize(card.image_path, 125, 182)
    image_refs.append(card_image)
    card_canvas = Canvas(width=125, height=182, bg="black")
    card_canvas.place(x=posx, y=posy)
    card_canvas.create_image(2, 2, image=card_image, anchor="nw")
    all_card_canvases.append(card_canvas)


class Hand:
    def __init__(self, shoe: list):
        self.shoe = shoe
        self.player_cards = []
        self.dealer_cards = []
        self.is_double = False
        self.player_cards1 = []
        self.player_cards2 = []
        self.game_is_on = False
        self.player_card_position_x = 550
        self.player_card_position_y = 500
        self.player_has_bust = False
        self.dealer_has_bust = False
        self.is_blackjack = False

    def draw_a_card(self):
        card_drawn = self.shoe[0]
        self.shoe.pop(0)
        return card_drawn

    # noinspection PyUnresolvedReferences
    def deal_hand(self):
        self.reset_hand()
        self.game_is_on = True
        for i in range(2):
            player_card = self.draw_a_card()
            self.player_cards.append(player_card)
            window.after(200 + (i * 400), lambda card=player_card,
                                                 x=self.player_card_position_x,
                                                 y=self.player_card_position_y: create_and_place_card(card, x, y))
            self.player_card_position_x += 50
            self.player_card_position_y -= 50
            dealer_card = self.draw_a_card()
            self.dealer_cards.append(dealer_card)
            window.after(400 + (i * 400), lambda
                card=dealer_card, x=475 + (i * 150), y=50: create_and_place_card(card, x, y))
        window.after(800, place_face_down_card)
        if self.get_sum(self.player_cards) == 21 or self.get_sum(self.dealer_cards) == 21:
            self.is_blackjack = True
            self.stand()

    @staticmethod
    def get_sum(cards: list):
        value_sum = 0
        for card in cards:
            value_sum += card.value
        return value_sum

    def hit(self):
        if self.game_is_on:
            if not self.player_has_bust:
                new_player_card = self.draw_a_card()
                self.player_cards.append(new_player_card)
                create_and_place_card(new_player_card, self.player_card_position_x, self.player_card_position_y)
                self.player_card_position_x += 50
                self.player_card_position_y -= 50
                if self.get_sum(self.player_cards) == 21:
                    self.stand()
                elif self.get_sum(self.player_cards) > 21:
                    self.player_has_bust = True
                    self.stand()

    def double_down(self):
        self.hit()
        self.stand()

    def split(self):
        if self.player_cards[0].number == self.player_cards[1].number:
            self.player_cards1 = [self.player_cards[0]]
            self.player_cards2 = [self.player_cards[1]]

    def reset_hand(self):
        remove_face_down_card()
        self.player_cards.clear()
        self.dealer_cards.clear()
        self.player_cards1.clear()
        self.player_cards2.clear()
        self.game_is_on = False
        for card in all_card_canvases:
            card.destroy()
        self.player_card_position_x = 550
        self.player_card_position_y = 500
        self.player_has_bust = False
        self.dealer_has_bust = False
        self.is_blackjack = False
        # noinspection PyUnresolvedReferences
        background_canvas.itemconfig(background_text, text="BlackJack")

    # noinspection PyUnresolvedReferences
    def stand(self):
        if self.game_is_on:
            card_position = 775
            remove_face_down_card()
            timer = 500
            if not self.player_has_bust and not self.is_blackjack:
                while self.get_sum(self.dealer_cards) < 17:
                    dealer_card = self.draw_a_card()
                    self.dealer_cards.append(dealer_card)
                    window.after(timer, lambda card=dealer_card,
                                               x=card_position,
                                               y=50: create_and_place_card(card, x, y))
                    card_position += 150
                    timer += 500
                if self.get_sum(self.dealer_cards) > 21:
                    self.dealer_has_bust = True
            self.result()
            self.game_is_on = False

    # noinspection PyUnresolvedReferences
    def result(self):
        player_final_sum = self.get_sum(self.player_cards)
        dealer_final_sum = self.get_sum(self.dealer_cards)
        if self.is_blackjack:
            if player_final_sum > dealer_final_sum:
                background_canvas.itemconfig(background_text, text="Player Has BlackJack, Player Wins")
            elif player_final_sum < dealer_final_sum:
                background_canvas.itemconfig(background_text, text="Dealer Has BlackJack, Dealer Wins")
            else:
                background_canvas.itemconfig(background_text, text="Push")
        elif self.player_has_bust:
            background_canvas.itemconfig(background_text, text="Dealer Wins, Player Has Bust")
        elif self.dealer_has_bust:
            background_canvas.itemconfig(background_text, text="Player Wins, Dealer Has Bust")
        elif player_final_sum > dealer_final_sum:
            background_canvas.itemconfig(background_text, text="Player Wins")
        elif player_final_sum == dealer_final_sum:
            background_canvas.itemconfig(background_text, text="Push")
        else:
            background_canvas.itemconfig(background_text, text="Dealer Wins")
