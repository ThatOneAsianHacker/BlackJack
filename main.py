import random
import classes
from classes import Deck, Card, Hand
import tkinter as tk
from tkinter import messagebox
money = 1000
suits = ['hearts', 'diamonds', 'spades', 'clubs']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
bet_amount = 0
value = 0
dealer_value = 0
deck = None
card_count = 0
your_hand = Hand()
dealer_hand = Hand()

def get_money():
    global money
    while True:
        try:
            money = int(input("Enter your starting money (default 1000): ") or 1000)
            if money > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def reset_deck():
    global deck
    deck = Deck()
    print("Deck reset. New cards are available.")

def reset_game():
    global value, dealer_value, bet_amount, card_count
    value = 0
    dealer_value = 0
    bet_amount = 0
    card_count = 0
    reset_deck()
    print("Game reset. You can place a new bet.")


def place_bet():
    global bet_amount
    while True:
        try:
            bet = int(input(f"Enter your bet amount (1-{money}): "))
            if 1 <= bet <= money:
                bet_amount = bet
                break
            else:
                print(f"Please enter a valid amount between 1 and {money}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_hand_value(your_hand):
    value = 0
    aces = 0
    for card in your_hand:
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

def hit():
    global deck, your_hand, money, bet_amount
    your_hand.draw(deck)
    update_display()
    if get_hand_value(your_hand) == 21:
        print("Blackjack!")
        bet_amount *= 2
        money += bet_amount
        print(f"You won! Your new balance is {money}.")
        deal()
        update_display()
    elif get_hand_value(your_hand) > 21:
        print("Bust! You lose your bet.")
        money -= bet_amount
        print(f"Your new balance is {money}.")
        deal()
        update_display()

def update_display():
    global your_hand, dealer_hand
    display_hand_text(your_hand, player_frame)
    display_hand_text(dealer_hand, dealer_frame)
    value = get_hand_value(your_hand)
    card_count_var.set(f"Cards left in deck: {len(deck.cards)}")
    money_remaining_var.set(f"Money remaining: ${money}")
    update_status(f"Your value: {value}, Bet: {bet_amount}")

def update_stand_display():
    global dealer_hand, value
    dealer_value = get_hand_value(dealer_hand)
    value = get_hand_value(your_hand)
    display_hand_text(your_hand, player_frame)
    display_hand_text(dealer_hand, dealer_frame)
    update_status(f"Your value: {value}, Dealer value: {dealer_value}, Bet: {bet_amount}")

def deal():
    global your_hand, dealer_hand, deck
    deck.shuffle()
    your_hand = Hand()
    dealer_hand = Hand()
    
    # Deal two cards to each player
    your_hand.draw(deck)
    your_hand.draw(deck)
    dealer_hand.draw(deck)
    dealer_hand.draw(deck)

def stand():
    global money, bet_amount
    global dealer_hand, your_hand  
    dealer_value = get_hand_value(dealer_hand)
    value = get_hand_value(your_hand)
    update_stand_display()
    while dealer_value < 17:
        dealer_hand.draw(deck)
        dealer_value = get_hand_value(dealer_hand)
        update_stand_display()
    if dealer_value > 21 or dealer_value < value:
        print("You win!")
        money += bet_amount
        deal()
        update_display()
    elif dealer_value == value:
        print("It's a tie!")
        deal() 
        update_display()
    else:
        print("Dealer wins!")
        money -= bet_amount
        deal()
        update_display()
        
def double_down():
    global bet_amount, money
    if bet_amount * 2 <= money:
        bet_amount *= 2
        print(f"Bet doubled to {bet_amount}.")
        hit()
        stand()
    else:
        print("Not enough money to double down.")

def split():
    global your_hand, bet_amount
    if len(your_hand.cards) == 2 and your_hand[0].rank == your_hand[1].rank:
        new_hand = [your_hand.pop()]
        new_bet = bet_amount // 2
        if new_bet <= money:
            bet_amount = new_bet
            print(f"Split! New bet for second hand: {new_bet}.")
            hit()
            stand()
        else:
            print("Not enough money to split.")
    else:
        print("Cannot split. You need two cards of the same rank.")


def start_game():
    global deck, your_hand, dealer_hand
    deck = Deck()
    your_hand = Hand()
    dealer_hand = Hand()  
    # Initial 2 cards for each
    for _ in range(2):
        your_hand.draw(deck)
        dealer_hand.draw(deck)
    
    print("Game started.")
    print("Your hand:", your_hand)
    print("Dealer's hand:", dealer_hand.cards[0], "and [hidden]")



# Start tkinter app
if __name__ == "__main__":
    import tkinter as tk
    from tkinter import messagebox

    window = tk.Tk()
    window.title("Blackjack")
    window.geometry("800x600")

    # ----- Variables -----
    money_var = tk.StringVar(value="1000")
    bet_var = tk.StringVar()
    status_var = tk.StringVar()
    card_count_var = tk.StringVar()
    money_remaining_var = tk.StringVar()

    money = 1000
    bet_amount = 0

    RANK_MAP = {
        '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
        '7': '7', '8': '8', '9': '9', '10': '10',
        'jack': 'J', 'queen': 'Q', 'king': 'K', 'ace': 'A'
    }

    SUIT_SYMBOLS = {
        'hearts': '♥',
        'diamonds': '♦',
        'clubs': '♣',
        'spades': '♠'
    }

    # ----- UI Input Fields -----
    tk.Label(window, text="Enter Money:").pack()
    money_entry = tk.Entry(window, textvariable=money_var)
    money_entry.pack()

    tk.Label(window, text="Enter Bet:").pack()
    bet_entry = tk.Entry(window, textvariable=bet_var)
    bet_entry.pack()

    tk.Label(window, textvariable=status_var, fg="blue").pack(pady=10)
    tk.Label(window, textvariable=card_count_var, fg="green", font=("Arial", 12)).pack()
    tk.Label(window, textvariable=money_remaining_var, fg="green", font=("Arial", 12)).pack()

    # ----- Card Display Frames -----
    player_frame = tk.Frame(window)
    player_frame.pack(pady=10)
    tk.Label(player_frame, text="Your Hand:", font=("Arial", 14)).pack()

    your_cards_frame = tk.Frame(player_frame)
    your_cards_frame.pack()

    dealer_frame = tk.Frame(window)
    dealer_frame.pack(pady=10)
    tk.Label(dealer_frame, text="Dealer's Hand:", font=("Arial", 14)).pack()

    dealer_cards_frame = tk.Frame(dealer_frame)
    dealer_cards_frame.pack()

    # ----- Buttons -----
    button_frame = tk.Frame(window)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Start Game", command=lambda: gui_start_game()).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Place Bet", command=lambda: gui_place_bet()).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Hit", command=lambda: hit()).grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="Stand", command=lambda: stand()).grid(row=0, column=3, padx=5)
    tk.Button(button_frame, text="Double Down", command=lambda: double_down()).grid(row=1, column=0, padx=5)
    tk.Button(button_frame, text="Split", command=lambda: split()).grid(row=1, column=1, padx=5)
    tk.Button(button_frame, text="Reset Game", command=lambda: reset_game()).grid(row=1, column=2, padx=5)

    # ----- Functions -----

    def update_status(text):
        status_var.set(text)

    def display_hand_text(hand, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        card_texts = []
        for card in hand.cards:
            rank = RANK_MAP.get(card.rank.lower(), '?')
            suit = SUIT_SYMBOLS.get(card.suit.lower(), '?')
            card_texts.append(f"{rank}{suit}")
        label = tk.Label(frame, text='  '.join(card_texts), font=("Courier", 18))
        label.pack()
    
    def display_hand_text(hand, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        card_texts = []
        for card in hand.cards:
            rank = RANK_MAP.get(card.rank.lower(), '?')
            suit = SUIT_SYMBOLS.get(card.suit.lower(), '?')
            card_texts.append(f"{rank}{suit}")
        label = tk.Label(frame, text='  '.join(card_texts), font=("Courier", 18))
        label.pack()

    def update_display():
        global your_hand, dealer_hand
        # Show all player's cards
        display_hand_text(your_hand, your_cards_frame)

        # Show only the first dealer card and hide the second
        for widget in dealer_cards_frame.winfo_children():
            widget.destroy()

        dealer_cards = dealer_hand.cards
        if dealer_cards:
            shown_card = dealer_cards[0]
            rank = RANK_MAP.get(shown_card.rank.lower(), '?')
            suit = SUIT_SYMBOLS.get(shown_card.suit.lower(), '?')
            display_text = f"{rank}{suit}  [?]"
        else:
            display_text = "[No cards]"

        label = tk.Label(dealer_cards_frame, text=display_text, font=("Courier", 18))
        label.pack()
        

        # Update status and info
        value = get_hand_value(your_hand)
        card_count_var.set(f"Cards left in deck: {len(deck.cards)}")
        money_remaining_var.set(f"Money remaining: ${money}")
        update_status(f"Your value: {value}, Bet: {bet_amount}")

    def gui_start_game():
        global money
        try:
            money = int(money_var.get())
            if money <= 0:
                raise ValueError
            start_game()
            update_display()
            update_status(f"Game started with ${money}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive number.")

    def gui_place_bet():
        global bet_amount, money
        try:
            bet = int(bet_var.get())
            if 1 <= bet <= money:
                bet_amount = bet
                update_status(f"Bet placed: ${bet_amount}")
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Bet", f"Enter a number between 1 and {money}.")

    # Start the game
    window.mainloop()
