import tkinter as tk
import blackjack_functions as bf
import classes
from classes import Deck, Hand

money = 1000
deck = None
your_hand = Hand()
dealer_hand = Hand()

def start_game():
    global deck, your_hand, dealer_hand
    deck = Deck()
    # Initial 2 cards for each
    for _ in range(2):
        your_hand.draw(deck)
        dealer_hand.draw(deck)
    
    print("Game started.")
    print("Your hand:", your_hand)
    print("Dealer's hand:", dealer_hand.cards[0], "and [hidden]")

# Start tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Blackjack Game")
    root.geometry("800x600")

    # Start the game
    start_game()

    root.mainloop()