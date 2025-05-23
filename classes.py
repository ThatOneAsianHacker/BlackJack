class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
         return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop() if self.cards else None

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)


class Hand:
    global bet_amount
    def __init__(self, hand):
        self.hand = get_hand_value(hand)
        self.cards = hand