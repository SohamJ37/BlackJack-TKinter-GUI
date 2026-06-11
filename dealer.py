from cards import shuffle_cards, create_shoe
from tkinter import Canvas
from images import resize

image_refs = []
window = None
background_text = None
background_canvas = None
face_down_card_canvas = None
score_text = None
count_text = None

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


def set_window(w, bt, bc, st, ct):
    global window, background_text, background_canvas, score_text, count_text
    window = w
    background_text = bt
    background_canvas = bc
    score_text = st
    count_text = ct


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
        self.count_visible = False
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
        self.bankroll = bankroll
        self.running_count = 0

        self.is_split = False
        self.active_hand_index = 0
        self.split_hands = []
        self.split_busts = [False, False] 
        self.split_x_positions = [350, 800]

    def draw_a_card(self):
        card_drawn = self.shoe[0]
        self.shoe.pop(0)
        if card_drawn.number in [i + 2 for i in range(5)]:
            self.running_count += 1
        elif card_drawn.number in [10, 'A', 'K', 'Q', 'J']:
            self.running_count -= 1
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

    @staticmethod
    def get_sum(cards: list):
        value_sum = 0
        aces = 0

        for card in cards:
            if card.value == 11:
                aces += 1
            value_sum += card.value

        while value_sum > 21 and aces > 0:
            value_sum -= 10
            aces -= 1

        return value_sum

    # noinspection PyUnresolvedReferences
    def hit(self):
        if self.game_is_on:
            target_hand = self.split_hands[self.active_hand_index] if self.is_split else self.player_cards
            has_bust = self.split_busts[self.active_hand_index] if self.is_split else self.player_has_bust
            
            if not has_bust:
                new_card = self.draw_a_card()
                target_hand.append(new_card)
                current_sum = self.get_sum(target_hand)
                
                prefix = f"Hand {self.active_hand_index + 1}: " if self.is_split else ""
                background_canvas.itemconfig(score_text, text=f"{prefix}{current_sum}")
                
                create_and_place_card(new_card, self.player_card_position_x, self.player_card_position_y)
                self.player_card_position_x += 50
                self.player_card_position_y -= 50
                
                if current_sum > 21:
                    if self.is_split:
                        self.split_busts[self.active_hand_index] = True
                    else:
                        self.player_has_bust = True
                    self.stand()
                elif current_sum == 21:
                    self.stand()

    def double_down(self):
        self.hit()
        self.stand()

# noinspection PyUnresolvedReferences
    def split(self):
        if self.game_is_on and len(self.player_cards) == 2 and self.player_cards[0].value == self.player_cards[1].value and not self.is_split:
            
            self.is_split = True
            self.active_hand_index = 0
            
            self.bankroll.money_remaining -= self.bankroll.current_bet
            self.bankroll.update_bankroll()
            
            self.split_hands = [[self.player_cards[0]], [self.player_cards[1]]]
            
            for canvas in all_card_canvases:
                canvas.destroy()
            all_card_canvases.clear()
            
            # --- THE VISUAL FIX: Redraw BOTH dealer cards and replace cover ---
            remove_face_down_card()
            create_and_place_card(self.dealer_cards[0], 475, 50)
            create_and_place_card(self.dealer_cards[1], 625, 50) # The invisible hole card
            place_face_down_card()
            
            create_and_place_card(self.split_hands[0][0], self.split_x_positions[0], 500)
            create_and_place_card(self.split_hands[1][0], self.split_x_positions[1], 500)
            
            new_card_1 = self.draw_a_card()
            new_card_2 = self.draw_a_card()
            self.split_hands[0].append(new_card_1)
            self.split_hands[1].append(new_card_2)
            
            create_and_place_card(new_card_1, self.split_x_positions[0] + 50, 450)
            create_and_place_card(new_card_2, self.split_x_positions[1] + 50, 450)
            
            self.player_card_position_x = self.split_x_positions[0] + 100
            self.player_card_position_y = 400
            
            current_sum = self.get_sum(self.split_hands[self.active_hand_index])
            background_canvas.itemconfig(score_text, text=f"Hand 1: {current_sum}")

    def reset_hand(self):
        remove_face_down_card()
        self.player_cards.clear()
        self.dealer_cards.clear()
        
        # --- THE STATE FIX: Reset all split tracking variables ---
        self.is_split = False
        self.active_hand_index = 0
        self.split_hands.clear()
        self.split_busts = [False, False]
        
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
        self.player_current_sum = 0
        
        # noinspection PyUnresolvedReferences
        background_canvas.itemconfig(background_text, text="")
        # noinspection PyUnresolvedReferences
        background_canvas.itemconfig(score_text, text="")

    # noinspection PyUnresolvedReferences
    def stand(self):
        if self.game_is_on:
            if self.is_split and self.active_hand_index == 0:
                self.active_hand_index = 1
                self.player_card_position_x = self.split_x_positions[1] + 100
                self.player_card_position_y = 400
                
                current_sum = self.get_sum(self.split_hands[1])
                background_canvas.itemconfig(score_text, text=f"Hand 2: {current_sum}")
                return
                
            remove_face_down_card()
            card_position = 775
            timer = 500
            
            player_all_busted = (self.is_split and all(self.split_busts)) or (not self.is_split and self.player_has_bust)
            
            if not player_all_busted and not self.is_blackjack:
                while self.get_sum(self.dealer_cards) < 17:
                    dealer_card = self.draw_a_card()
                    self.dealer_cards.append(dealer_card)
                    
                    window.after(timer, lambda card=dealer_card, x=card_position, y=50: create_and_place_card(card, x, y))
                    card_position += 150
                    timer += 500

            window.after(timer, self.result)
            self.game_is_on = False

    # noinspection PyUnresolvedReferences
    def result(self):
        dealer_final_sum = self.get_sum(self.dealer_cards)
        self.dealer_has_bust = dealer_final_sum > 21
        
        hands_to_evaluate = self.split_hands if self.is_split else [self.player_cards]
        busts_to_evaluate = self.split_busts if self.is_split else [self.player_has_bust]
        
        result_texts = []
        original_bet = self.bankroll.current_bet

        for i, hand in enumerate(hands_to_evaluate):
            self.bankroll.current_bet = original_bet
            
            player_sum = self.get_sum(hand)
            prefix = f"Hand {i + 1}: " if self.is_split else ""
            
            # --- Explicit Blackjack Checks ---
            player_has_bj = (player_sum == 21 and len(hand) == 2 and not self.is_split)
            dealer_has_bj = (dealer_final_sum == 21 and len(self.dealer_cards) == 2)
            
            if player_has_bj and dealer_has_bj:
                self.bankroll.push()
                result_texts.append("Push (Both Blackjack)")
            elif player_has_bj:
                self.bankroll.blackjack()
                result_texts.append("Blackjack! Player Wins")
            elif dealer_has_bj:
                self.bankroll.lose()
                result_texts.append(f"{prefix}Loss (Dealer Blackjack)")
            elif busts_to_evaluate[i]:
                self.bankroll.lose()
                result_texts.append(f"{prefix}Bust")
            elif self.dealer_has_bust:
                self.bankroll.win()
                result_texts.append(f"{prefix}Win (Dealer Bust)")
            elif player_sum > dealer_final_sum:
                self.bankroll.win()
                result_texts.append(f"{prefix}Win")
            elif player_sum == dealer_final_sum:
                self.bankroll.push()
                result_texts.append(f"{prefix}Push")
            else:
                self.bankroll.lose()
                result_texts.append(f"{prefix}Loss")

        self.bankroll.current_bet = 0
        self.bankroll.update_bankroll()

        final_text = " | ".join(result_texts)
        background_canvas.itemconfig(background_text, text=final_text)
        background_canvas.itemconfig(score_text, text=f"Dealer Total: {dealer_final_sum}")

        if len(self.shoe) <= 60:
            window.after(2000, lambda: background_canvas.itemconfig(background_text, text="Resetting Shoe and Count..."))
            from cards import create_shoe, shuffle_cards
            self.shoe = shuffle_cards(create_shoe(6))
            self.running_count = 0

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

    def show_or_hide_count(self):
        if not self.count_visible:
            # noinspection PyUnresolvedReferences
            background_canvas.itemconfig(count_text, text=f'Running Count: {self.running_count}\n'
                                                          f'True Count: {round(self.running_count / round((len(self.shoe)) / 52))}')
            self.count_visible = True
        else:
            # noinspection PyUnresolvedReferences
            background_canvas.itemconfig(count_text, text="")
            self.count_visible = False
