class MoneyManager:
    def __init__(self, buyin, canvas, window):
        self.money_remaining = buyin
        self.current_bet = 0
        self.window = window
        self.canvas = canvas

        self.money_remaining_text = self.canvas.create_text(1150,
                                                100,
                                                text=f"Money Remaining: {self.money_remaining}",
                                                fill="white",
                                                font=("helvetica", 16, "bold"))

        self.current_bet_text = self.canvas.create_text(1150,
                                                            150,
                                                            text=f"Current Bet: {self.current_bet}",
                                                            fill="white",
                                                            font=("helvetica", 16, "bold"))

    def set_bet_amount(self, bet):
        self.money_remaining -= bet
        self.current_bet = bet

    def update_bankroll(self):
        self.canvas.itemconfig(self.money_remaining_text, text=f"Money Remaining: {self.money_remaining}")
        self.canvas.itemconfig(self.current_bet_text, text=f"Current Bet: {self.current_bet}")

    def win(self):
        self.money_remaining += 2*self.current_bet
        self.current_bet = 0
        self.update_bankroll()

    def lose(self):
        self.current_bet = 0
        self.update_bankroll()

    def push(self):
        self.money_remaining += self.current_bet
        self.current_bet = 0
        self.update_bankroll()

    def blackjack(self):
        self.money_remaining += self.current_bet*2.5
        self.current_bet = 0
        self.update_bankroll()

    def double_down(self):
        self.money_remaining -= self.current_bet
        self.current_bet = self.current_bet*2
        self.update_bankroll()
