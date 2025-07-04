# classes.py
import random

suits = ['hearts', 'diamonds', 'spades', 'clubs']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self, num_decks):
        self.num_decks = num_decks
        if not num_decks.isdigit() or int(num_decks) < 1:
            num_decks = 1
        self.cards = [Card(suit, rank) for x in range(int(num_decks)) for suit in suits for rank in ranks]
        random.shuffle(self.cards)
        self.card_count = 0
    
    def shuffle(self):
        random.shuffle(self.cards)
   
    def draw_card(self):
        if not self.cards:
            return None
        card = self.cards.pop()
        self._update_count(card)
        return card

    def _update_count(self, card):
        if card.rank in ['2', '3', '4', '5', '6']:
            self.card_count += 1
        elif card.rank in ['10', 'jack', 'queen', 'king', 'ace']:
            self.card_count -= 1

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)



class Hand:
    def __init__(self, initial_cards=None): # Add initial_cards parameter with a default of None
        if initial_cards is None:
            self.cards = []
        else:
            self.cards = list(initial_cards) # Ensure it's a list if a non-list iterable is passed

    def draw(self, deck):
        card = deck.draw_card()
        # Ensure update_count is properly handled here, assuming it's part of your Deck logic
        # You might need to adjust how deck._update_count is called based on your Deck class
        update_count = deck._update_count(card)
        if card:
            self.cards.append(card)

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

    def __iter__(self):
        return iter(self.cards)