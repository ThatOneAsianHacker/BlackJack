import random
import classes
from classes import Deck, Card, Hand
import tkinter as tk
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
    elif get_hand_value(your_hand) > 21:
        print("Bust! You lose your bet.")
        money -= bet_amount
        print(f"Your new balance is {money}.")
        deal()

def update_display():
    global your_hand, dealer_hand, value, dealer_value
    value = get_hand_value(your_hand)
    dealer_value = get_hand_value(dealer_hand)
    print(f"Your hand: {your_hand} (Value: {value})")
    print(f"Dealer's hand: {dealer_hand.cards[0]}, [hidden]")
    print(f"Current bet: {bet_amount}, Money left: {money}")

def update_stand_display():
    global dealer_hand, dealer_value
    dealer_value = get_hand_value(dealer_hand)
    print(f"Dealer's hand: {dealer_hand} (Value: {dealer_value})")
    print(f"Your hand: {your_hand} (Value: {value})")
    print(f"Current bet: {bet_amount}, Money left: {money}")

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
    update_display()

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
    elif dealer_value == value:
        print("It's a tie!")
        deal() 
    else:
        print("Dealer wins!")
        money -= bet_amount
        deal()
        
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
    if len(your_hand) == 2 and your_hand[0].rank == your_hand[1].rank:
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
    window = tk.Tk()
    window.title("Blackjack")
    window.geometry("800x600") 
    player_label = tk.Label(window, text="Your Hand: ", font=("Arial", 16))
    player_label.pack(pady=10)

    dealer_label = tk.Label(window, text="Dealer's Hand: ", font=("Arial", 16))
    dealer_label.pack(pady=10)

    status_label = tk.Label(window, text="", font=("Arial", 14), fg="blue")
    status_label.pack(pady=10)
    button_frame = tk.Frame(window)
    button_frame.pack(pady=20)

    hit_button = tk.Button(button_frame, text="Hit", width=10, command= hit)
    hit_button.grid(row=0, column=0, padx=5)

    stand_button = tk.Button(button_frame, text="Stand", width=10, command= stand)
    stand_button.grid(row=0, column=1, padx=5)
    
    new_game_button = tk.Button(button_frame, text="New Game", width=10, command=start_game)
    new_game_button.grid(row=0, column=2, padx=5)

    # Start the game
    start_game()

    window.mainloop()