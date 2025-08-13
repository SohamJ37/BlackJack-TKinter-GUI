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
score_text = None

all_card_canvases = []


def place_face_down_card():
    global face_down_card_canvas
    face_down_card_image = resize("./Face Down Card.jpeg", 125, 182)
    image_refs.append(face_down_card_image)
    face_down_card_canvas = Canvas(window, width=125, height=182, bg="white")
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


def set_window(w, bt, bc, st):
    global window, background_text, background_canvas, score_text
    window = w
    background_text = bt
    background_canvas = bc
    score_text = st


def create_and_place_card(card, posx, posy):
    card_image = resize(card.image_path, 125, 182)
    image_refs.append(card_image)
    card_canvas = Canvas(window, width=125, height=182, bg="black")
    card_canvas.place(x=posx, y=posy)
    card_canvas.create_image(2, 2, image=card_image, anchor="nw")
    all_card_canvases.append(card_canvas)


class Hand:
    def __init__(self, shoe: list, bankroll):
        self.shoe = shoe
        self.player_cards = []
        self.dealer_cards = []
        self.player_current_sum = 0
        self.dealer_current_sum = 0
        self.is_double = False
        self.player_cards1 = []
        self.player_cards2 = []
        self.game_is_on = False
        self.player_card_position_x = 550
        self.player_card_position_y = 500
        self.player_has_bust = False
        self.dealer_has_bust = False
        self.is_blackjack = False
        self.player_ace_dealt_once = False
        self.dealer_ace_dealt_once = False
        self.bankroll = bankroll

    def draw_a_card(self):
        card_drawn = self.shoe[0]
        self.shoe.pop(0)
        return card_drawn

    # noinspection PyUnresolvedReferences
    def deal_hand(self):
        if not self.game_is_on:
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
            if self.get_sum(self.player_cards) == 21 or self.get_sum(self.dealer_cards) == 21:
                self.is_blackjack = True
                self.stand()
            else:
                window.after(800, place_face_down_card)
            self.player_current_sum = self.get_sum(self.player_cards)
            self.dealer_current_sum = self.get_sum(self.dealer_cards)
            background_canvas.itemconfig(score_text, text=self.player_current_sum)
            # background_canvas.itemconfig(background_text, text="")

    @staticmethod
    def get_sum(cards: list):
        value_sum = 0
        for card in cards:
            value_sum += card.value
        return value_sum

    # noinspection PyUnresolvedReferences
    def hit(self):
        if self.game_is_on:
            if not self.player_has_bust:
                new_player_card = self.draw_a_card()
                self.player_cards.append(new_player_card)
                self.player_current_sum += new_player_card.value
                background_canvas.itemconfig(score_text, text=self.player_current_sum)
                create_and_place_card(new_player_card, self.player_card_position_x, self.player_card_position_y)
                self.player_card_position_x += 50
                self.player_card_position_y -= 50
                if self.player_current_sum == 21:
                    self.stand()
                elif self.ace_present("player") and self.player_current_sum > 21 and not self.player_ace_dealt_once:
                    self.player_current_sum = self.get_sum(self.player_cards) - self.number_of_aces("player")*10
                    background_canvas.itemconfig(score_text, text=self.player_current_sum)
                    self.player_ace_dealt_once = True
                elif self.player_current_sum > 21:
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
        all_card_canvases.clear()
        image_refs.clear()
        self.player_card_position_x = 550
        self.player_card_position_y = 500
        self.player_has_bust = False
        self.dealer_has_bust = False
        self.is_blackjack = False
        self.player_ace_dealt_once = False
        self.player_current_sum = 0
        self.dealer_current_sum = 0
        self.player_ace_dealt_once = False
        self.dealer_ace_dealt_once = False
        # noinspection PyUnresolvedReferences
        background_canvas.itemconfig(background_text, text="")
        # noinspection PyUnresolvedReferences
        background_canvas.itemconfig(score_text, text="")

    # noinspection PyUnresolvedReferences
    def stand(self):
        background_canvas.itemconfig(score_text,
                                     text=f"{self.player_current_sum} vs {self.dealer_current_sum}")
        if self.game_is_on:
            card_position = 775
            remove_face_down_card()
            timer = 500
            if not self.player_has_bust and not self.is_blackjack:
                while self.dealer_current_sum < 17:
                    dealer_card = self.draw_a_card()
                    self.dealer_cards.append(dealer_card)
                    self.dealer_current_sum += dealer_card.value
                    window.after(timer, lambda card=dealer_card,
                                               x=card_position,
                                               y=50: create_and_place_card(card, x, y))
                    card_position += 150
                    timer += 500
                    background_canvas.itemconfig(score_text,
                                                 text=f"{self.player_current_sum} vs {self.dealer_current_sum}")
                    if self.dealer_current_sum > 21 and not self.dealer_ace_dealt_once and self.ace_present("dealer"):
                        self.dealer_current_sum = self.get_sum(self.dealer_cards) - 10*self.number_of_aces("dealer")
                        background_canvas.itemconfig(score_text,
                                                     text=f"{self.player_current_sum} vs {self.dealer_current_sum}")
                        self.dealer_ace_dealt_once = True

                if self.dealer_current_sum > 21:
                    self.dealer_has_bust = True
            self.result()
            self.game_is_on = False

    # noinspection PyUnresolvedReferences
    def result(self):
        player_final_sum = self.player_current_sum
        dealer_final_sum = self.dealer_current_sum
        if self.is_blackjack:
            if self.get_sum(self.player_cards) > self.get_sum(self.dealer_cards):
                self.bankroll.blackjack()
                background_canvas.itemconfig(background_text, text="Player Has BlackJack, Player Wins")
            elif self.get_sum(self.dealer_cards) > self.get_sum(self.player_cards):
                self.bankroll.lose()
                background_canvas.itemconfig(background_text, text="Dealer Has BlackJack, Dealer Wins")
            else:
                self.bankroll.push()
                background_canvas.itemconfig(background_text, text="Push")
        elif self.player_has_bust:
            self.bankroll.lose()
            background_canvas.itemconfig(background_text, text="Dealer Wins, Player Has Bust")
        elif self.dealer_has_bust:
            self.bankroll.win()
            background_canvas.itemconfig(background_text, text="Player Wins, Dealer Has Bust")
        elif player_final_sum > dealer_final_sum:
            self.bankroll.win()
            background_canvas.itemconfig(background_text, text="Player Wins")
        elif player_final_sum == dealer_final_sum:
            self.bankroll.push()
            background_canvas.itemconfig(background_text, text="Push")
        else:
            self.bankroll.lose()
            background_canvas.itemconfig(background_text, text="Dealer Wins")

    def ace_present(self, subject="player"):
        if subject == "dealer":
            for card in self.dealer_cards:
                if card.value == 11:
                    return True
        elif subject == "player":
            for card in self.player_cards:
                if card.value == 11:
                    return True

    def number_of_aces(self, subject="player"):
        number_of_ace = 0
        if subject == "dealer":
            for card in self.dealer_cards:
                if card.value == 11:
                    number_of_ace += 1
        elif subject == "player":
            for card in self.player_cards:
                if card.value == 11:
                    number_of_ace += 1
        return number_of_ace
