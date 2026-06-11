from tkinter import Tk, Canvas, Button, Scale
from images import resize
from cards import create_shoe, shuffle_cards
from dealer import Hand, set_window
from bankroll import MoneyManager

shoe = create_shoe(6)
shuffle_cards(shoe)

window = Tk()
window.title("BlackJack")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.geometry("1312x720")


table_background = resize("./table_background.jpg", 1312, 720)

background_canvas = Canvas(window, width=1312, height=720)
background_canvas.place(x=0, y=0, relwidth=1, relheight=1)
background_canvas.create_image(0, 0, image=table_background, anchor="nw")
background_text = background_canvas.create_text(625,
                                                350,
                                                text="BlackJack",
                                                fill="white",
                                                font=("helvetica", 16, "bold"))
score_text = background_canvas.create_text(100, 100, text="Score", fill="white", font=("helvetica", 16, "bold"))
count_text = background_canvas.create_text(100, 600, text="", fill="white", font=("helvetica", 16, "bold"))
set_window(window, background_text, background_canvas, score_text, count_text)

bankroll = MoneyManager(1000, background_canvas, window)
hand = Hand(shoe, bankroll)


def click_deal():
    if not hand.game_is_on:
        bankroll.set_bet_amount(bet_amount.get())
        bankroll.update_bankroll()
        hand.deal_hand()

def click_double():
    if hand.game_is_on and len(hand.player_cards) == 2 and not hand.is_split:
        bankroll.double_down()
        hand.double_down()


hit = Button(window, text="HIT",
             command=hand.hit,
             width=15,
             height=2,
             bg="green",
             fg="white",
             font=("courier", 10, "bold"))
hit.place(x=1150, y=270)

stand = Button(window, text="STAND",
               command=hand.stand,
               width=15,
               height=2,
               bg="green",
               fg="white",
               font=("courier", 10, "bold"))
stand.place(x=1150, y=320)

show_count = Button(window, text="SHOW/HIDE COUNT",
               command=hand.show_or_hide_count,
               width=15,
               height=2,
               bg="green",
               fg="white",
               font=("courier", 10, "bold"))
show_count.place(x=1150, y=370)

deal = Button(window, text="DEAL",
              command=click_deal,
              width=15,
              height=2,
              bg="green",
              fg="white",
              font=("courier", 10, "bold"))
deal.place(x=1150, y=220)

double = Button(window, text="DOUBLE",
                command=click_double,
                width=15,
                height=2,
                bg="green",
                fg="white",
                font=("courier", 10, "bold"))
double.place(x=1150, y=420)

reset = Button(window, text="RESET",
                command=hand.reset_hand,
                width=15,
                height=2,
                bg="green",
                fg="white",
                font=("courier", 10, "bold"))
reset.place(x=1150, y=470)

split_btn = Button(window, text="SPLIT",
                command=hand.split,
                width=15,
                height=2,
                bg="green",
                fg="white",
                font=("courier", 10, "bold"))
split_btn.place(x=1150, y=520)

bet_amount = Scale(window,
                   orient="vertical",
                   from_=0,
                   to=bankroll.money_remaining,
                   bg="green",
                   fg="white",
                   width=20,
                   length=335,
                   troughcolor="white",
                   highlightcolor="black",
                   font=("courier", 10, "bold"))
bet_amount.place(x=1075, y=220)

window.mainloop()
