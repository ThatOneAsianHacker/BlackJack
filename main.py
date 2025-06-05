import random
import tkinter as tk
from tkinter import messagebox
from classes import Deck, Card, Hand, suits, ranks

# Global variables
money = 10000
bet_amount = 0
deck = None
your_hand = Hand()
dealer_hand = Hand()

def get_hand_value(hand_obj):
    value = 0
    aces = 0
    for card in hand_obj.cards:
        if card.rank in ['jack', 'queen', 'king']:
            value += 10
        elif card.rank == 'ace':
            aces += 1
            value += 11
        else:
            value += int(card.rank)

    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def reset_deck():
    global deck
    num_decks_str = decks_entry.get()
    deck = Deck(num_decks_str)

def reset_game():
    global your_hand, dealer_hand, bet_amount, money
    bet_amount = 0
    your_hand = Hand()
    dealer_hand = Hand()
    reset_deck()
    update_display()
    bet_var.set("")
    update_status("Game reset. Place your bet to start a new round.")
    money_remaining_var.set(f"Money remaining: ${money}")

def deal_initial_cards():
    global your_hand, dealer_hand, deck, bet_amount

    if bet_amount == 0:
        messagebox.showwarning("No Bet", "Please place a bet before dealing cards.")
        return

    your_hand = Hand()
    dealer_hand = Hand()

    your_hand.draw(deck)
    dealer_hand.draw(deck)
    your_hand.draw(deck)
    dealer_hand.draw(deck)

    update_display()

    player_value = get_hand_value(your_hand)
    dealer_hidden_value = get_hand_value(Hand([dealer_hand.cards[0]]))

    if player_value == 21 and len(your_hand.cards) == 2:
        update_status("Blackjack! You win!")
        global money
        money += bet_amount * 1.5
        money_remaining_var.set(f"Money remaining: ${money}")
        window.after(2000, start_new_round)
    elif get_hand_value(dealer_hand) == 21 and len(dealer_hand.cards) == 2:
        update_status("Dealer Blackjack! You lose.")
        money -= bet_amount
        money_remaining_var.set(f"Money remaining: ${money}")
        window.after(2000, start_new_round)
    else:
        update_status(f"Your value: {player_value}, Dealer shows: {dealer_hidden_value}")

def hit():
    global deck, your_hand, money, bet_amount

    if bet_amount == 0 or not your_hand.cards:
        messagebox.showwarning("Game State", "Please place a bet and deal cards first.")
        return

    your_hand.draw(deck)
    update_display()
    hand_value = get_hand_value(your_hand)

    if hand_value > 21:
        update_status("Bust! You lose your bet.")
        money -= bet_amount
        money_remaining_var.set(f"Money remaining: ${money}")
        show_all_cards()
        window.after(2000, start_new_round)
    elif hand_value == 21:
        update_status("You hit 21! Standing automatically.")
        window.after(1000, stand)

def stand():
    global money, bet_amount, dealer_hand, your_hand

    if bet_amount == 0 or not your_hand.cards:
        messagebox.showwarning("Game State", "Please place a bet and deal cards first.")
        return

    display_hand_text(dealer_hand, dealer_cards_frame, hide_second=False)
    update_status("Dealer revealing hand...")

    def dealer_plays_animation():
        dealer_value = get_hand_value(dealer_hand)
        value = get_hand_value(your_hand)
        update_status(f"Your value: {value}, Dealer value: {dealer_value}")

        if dealer_value < 17:
            dealer_hand.draw(deck)
            display_hand_text(dealer_hand, dealer_cards_frame, hide_second=False)
            window.after(1000, dealer_plays_animation)
        else:
            determine_winner()

    dealer_plays_animation()

def determine_winner():
    global money, bet_amount
    dealer_value = get_hand_value(dealer_hand)
    player_value = get_hand_value(your_hand)

    if dealer_value > 21:
        update_status("Dealer busts! You win!")
        money += bet_amount
    elif dealer_value < player_value:
        update_status("You win!")
        money += bet_amount
    elif dealer_value == player_value:
        update_status("It's a push (tie)!")
    else:
        update_status("Dealer wins! You lose.")
        money -= bet_amount

    money_remaining_var.set(f"Money remaining: ${money}")
    show_all_cards()
    window.after(2000, start_new_round)

def double_down():
    global bet_amount, money, your_hand, deck

    if bet_amount == 0 or len(your_hand.cards) != 2:
        messagebox.showwarning("Invalid Action", "You can only double down on your initial two cards.")
        return
    if bet_amount * 2 > money:
        messagebox.showerror("Not Enough Money", "You don't have enough money to double down.")
        return

    bet_amount *= 2
    bet_var.set(str(bet_amount))
    update_status(f"Bet doubled to ${bet_amount}. Drawing one card...")
    your_hand.draw(deck)
    update_display()
    window.after(1000, stand)

def split():
    messagebox.showinfo("Split Feature", "Split is not implemented.")

def start_new_round():
    global your_hand, dealer_hand, bet_amount
    your_hand = Hand()
    dealer_hand = Hand()
    bet_amount = 0
    bet_var.set("")
    update_display()
    update_status("Place your bet for the next round!")

def update_status(text):
    status_var.set(text)

def display_hand_text(hand, frame, hide_second=False):
    for widget in frame.winfo_children():
        widget.destroy()

    card_texts = []
    if hide_second and len(hand.cards) > 1:
        first_card = hand.cards[0]
        rank = RANK_MAP.get(first_card.rank.lower(), '?')
        suit = SUIT_SYMBOLS.get(first_card.suit.lower(), '?')
        card_texts.append(f"{rank}{suit}")
        card_texts.append("[?]")
    else:
        for card in hand.cards:
            rank = RANK_MAP.get(card.rank.lower(), '?')
            suit = SUIT_SYMBOLS.get(card.suit.lower(), '?')
            card_texts.append(f"{rank}{suit}")

    label = tk.Label(frame, text='   '.join(card_texts), font=("Courier", 24))
    label.pack()

def update_display():
    display_hand_text(your_hand, your_cards_frame, hide_second=False)
    display_hand_text(dealer_hand, dealer_cards_frame, hide_second=True)
    player_value = get_hand_value(your_hand)
    money_remaining_var.set(f"Money remaining: ${money}")
    update_status(f"Your value: {player_value}, Current Bet: ${bet_amount}")

def show_all_cards():
    display_hand_text(your_hand, your_cards_frame, hide_second=False)
    display_hand_text(dealer_hand, dealer_cards_frame, hide_second=False)

def gui_start_game():
    money = 10000
    money_remaining_var.set(f"Money remaining: ${money}")
    reset_game()
    update_status(f"Game started with ${money}. Place your bet!")

def gui_place_bet():
    global bet_amount, money

    if money <= 0:
        messagebox.showerror("No Money", "You have no money left.")
        return
    if your_hand.cards:
        messagebox.showwarning("Game State", "Finish the current round or reset the game.")
        return

    try:
        bet = int(bet_var.get())
        if 1 <= bet <= money:
            bet_amount = bet
            update_status(f"Bet placed: ${bet_amount}. Dealing cards...")
            deal_initial_cards()
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Bet", f"Enter a number between 1 and {money}.")

# --- GUI Setup ---
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Blackjack")
    window.geometry("800x600")

    money_var = tk.StringVar(value="1000")
    bet_var = tk.StringVar(value="")
    status_var = tk.StringVar()
    money_remaining_var = tk.StringVar(value=f"Money remaining: ${money}")

    RANK_MAP = {'2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '10': '10', 'jack': 'J', 'queen': 'Q', 'king': 'K', 'ace': 'A'}
    SUIT_SYMBOLS = {'hearts': '♥', 'diamonds': '♦', 'clubs': '♣', 'spades': '♠'}

    tk.Label(window, text="Enter Bet Amount:").pack(pady=(10,0))
    bet_entry = tk.Entry(window, textvariable=bet_var, width=20, justify='center')
    bet_entry.pack()

    tk.Label(window, text="Number of Decks (e.g., 1, 6):").pack(pady=(10,0))
    decks_entry = tk.Entry(window, width=20, justify='center')
    decks_entry.pack()
    decks_entry.insert(0, "1")

    tk.Label(window, textvariable=status_var, fg="blue", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(window, textvariable=money_remaining_var, fg="darkblue", font=("Arial", 12, "bold")).pack()

    player_frame = tk.Frame(window, bd=2, relief="groove")
    player_frame.pack(pady=10, padx=20, fill='x')
    tk.Label(player_frame, text="Your Hand:", font=("Arial", 14, "underline")).pack(pady=5)
    your_cards_frame = tk.Frame(player_frame)
    your_cards_frame.pack(pady=5)

    dealer_frame = tk.Frame(window, bd=2, relief="groove")
    dealer_frame.pack(pady=10, padx=20, fill='x')
    tk.Label(dealer_frame, text="Dealer's Hand:", font=("Arial", 14, "underline")).pack(pady=5)
    dealer_cards_frame = tk.Frame(dealer_frame)
    dealer_cards_frame.pack(pady=5)

    button_frame = tk.Frame(window)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Start Game", command=gui_start_game, width=15, height=2).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Place Bet", command=gui_place_bet, width=15, height=2).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(button_frame, text="Hit", command=hit, width=15, height=2).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(button_frame, text="Stand", command=stand, width=15, height=2).grid(row=0, column=3, padx=5, pady=5)
    tk.Button(button_frame, text="Double Down", command=double_down, width=15, height=2).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Split", command=split, width=15, height=2).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(button_frame, text="Show All Cards", command=show_all_cards, width=15, height=2).grid(row=1, column=2, padx=5, pady=5)
    tk.Button(button_frame, text="Reset Game", command=reset_game, width=15, height=2).grid(row=1, column=3, padx=5, pady=5)

    reset_deck()
    update_display()
    update_status("Welcome to Blackjack! Enter your starting money and click 'Start Game'.")

    window.mainloop()
