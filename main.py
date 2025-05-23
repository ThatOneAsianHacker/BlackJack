import blackjack_functions as bf
import blackjack_classes as bc
import tkinter as tk

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.title("Blackjack Game")
    root.geometry("800x600")

    # Create the game instance
    game = bc.BlackjackGame(root)

    # Start the game
    game.start_game()

    # Run the main loop
    root.mainloop()



