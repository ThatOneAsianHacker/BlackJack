
import random
import classes
from classes import Deck, Card
money = 1000
suits = ['hearts', 'diamonds', 'spades', 'clubs']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
bet_amount = 0
value = 0
dealer_value = 0
your_hand = []
dealer_hand = []

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

def start_game():
    global deck, hand, dealer_hand, value, dealer_value
    deck = Deck()
    while i > 2:   
        hand.append(deck.draw_cards) '
        deale.append(deck.draw_cards)
        i++
    value = 0
    dealer_value = 0
    print("Game started. You can draw cards now.")

def draw_card():
    global value
    card = random.choice(ranks)
    if card in ['jack', 'queen', 'king']:
        value += 10
    elif card == 'ace':
        value += 11
    else:
        value += int(card)
    print(f"Drew card: {card}. Current hand value: {value}")

def reset_deck():
    global deck
    deck = Deck()
    print("Deck reset. New cards are available.")

def reset_game():
    global value, dealer_value, bet_amount
    value = 0
    dealer_value = 0
    bet_amount = 0
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

def get_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
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
    if get_hand_value(hand) == 21:
        print("Blackjack!")
        bet_amount *= 2
        money += bet_amount
        print(f"You won! Your new balance is {money}.")
    elif get_hand_value(hand) > 21:
        print("Bust! You lose your bet.")
        money -= bet_amount
        print(f"Your new balance is {money}.")

def stand():
    global dealer_value
    while dealer_value < 17:
        card = deck.deal_card()
        if card:
            dealer_hand.append(card)
            dealer_value = get_hand_value(dealer_hand)
            print(f"Dealer drew: {card}. Dealer's hand value: {dealer_value}")
        else:
            print("No more cards in the deck.")
            break
    if dealer_value > 21 or dealer_value < value:
        print("You win!")
        money += bet_amount
    elif dealer_value == value:
        print("It's a tie!")
    else:
        print("Dealer wins!")
        money -= bet_amount
        
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
    global hand, bet_amount
    if len(hand) == 2 and hand[0].rank == hand[1].rank:
        new_hand = [hand.pop()]
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
