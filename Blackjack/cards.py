from random import shuffle


class Card():
    def __init__(self, num, suit):
        self.num = num
        self.suit = suit
        if num in '23456789':
            self.value = int(num)
            self.ace = False
        elif num == 'A':
            self.value = 11
            self.ace = True
        else:
            self.value = 10
            self.ace = False

    def __str__(self):
        return self.num + self.suit

    def __repr__(self):
        return self.num + self.suit


class Deck():
    def __init__(self, card_list=None, player=None, hand_num=None):
        if card_list:
            self.card_list = card_list
        else:
            nums = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']
            suits = ['C', 'S', 'H', 'D']
            self.card_list = [Card(n, s) for n in nums for s in suits]
        self.ace_count = sum([1 for card in self.card_list if card.ace])
        if len(self) == 2 and self.ace_count == 2:
            self.card_list[1].value = 1
            self.card_list[1].ace = False
            self.ace_count = 1
        self.player = player
        self.hand_num = hand_num
        self.surrender = False
        self.bet_amount = 0
        self.bj = False

    def shuffle(self):
        shuffle(self.card_list)

    def add(self, card):
        if card.ace:
            if self.ace_count == 1 or self.total() > 10:
                card.ace = False
                card.value = 1
        elif self.ace_count == 1:
            if self.total() + card.value > 21:
                for c in self.card_list:
                    if c.ace:
                        c.value -= 10
                        c.ace = False
                        break
        self.card_list.append(card)

    def total(self):
        return sum([card.value for card in self.card_list])

    def is_soft(self):
        return self.ace_count == 1

    def is_split(self):
        return len(self) == 2 and self.card_list[0].value == self.card_list[1].value

    def bet(self, amt):
        self.bet_amount = amt

    def __len__(self):
        return len(self.card_list)

    def __repr__(self):
        return '[' + ', '.join([str(c) for c in self.card_list]) + ']'

    def __str__(self):
        return '[' + ', '.join([str(c) for c in self.card_list]) + ']'


class Shoe():
    def __init__(self, num_decks=6):
        self.card_list = []
        for _ in range(num_decks):
            deck = Deck()
            self.card_list += deck.card_list

    def shuffle(self):
        shuffle(self.card_list)

    def deal_one(self):
        card = self.card_list[0]
        del self.card_list[0]
        return card

    def __len__(self):
        return len(self.card_list)

    def __repr__(self):
        return self.card_list

    def __str__(self):
        return '[' + ', '.join([str(c) for c in self.card_list]) + ']'


def bookplay(hand, dealer_card):
    tot = hand.total()

    if hand.is_split() and hand.card_list[0].value not in [5, 10]:
        num = hand.card_list[0].num
        if num in ['8', 'A']:
            return 't'
        elif num == '9':
            if dealer_card in [7, 10, 11]:
                return 's'
            else:
                return 't'
        elif num in ['2', '3', '4', '6', '7'] and 2 <= dealer_card <= 7:
            if num == '4' and 2 <= dealer_card <= 4 or dealer_card == 7 and num in ['4', '6']:
                return 'h'
            else:
                return 't'
        else:
            return 'h'

    elif not hand.is_soft():
        if tot >= 17:
            return 's'
        elif tot >= 12:
            if tot == 12 and dealer_card in [2, 3]:
                return 'h'
            if dealer_card <= 6:
                return 's'
            if tot == 16 and dealer_card in [9, 10, 11] or tot == 15 and dealer_card == 10:
                if len(hand) == 2:
                    return 'x'
                else:
                    return 'h'
            else:
                return 'h'
        elif tot == 10 and dealer_card not in [10, 11] or tot == 11 and dealer_card != 11 or tot == 9 and dealer_card in [3, 4, 5, 6]:
            if len(hand) == 2:
                return 'd'
            else:
                return 'h'
        else:
            return 'h'

    else:
        if tot >= 19 or (tot == 18 and dealer_card in [2, 7, 8]):
            return 's'
        elif tot == 18 and 3 <= dealer_card <= 6:
            if len(hand) == 2:
                return 'd'
            else:
                return 's'
        elif dealer_card in [5, 6] or dealer_card == 4 and 15 <= tot <= 18 or dealer_card == 3 and tot == 18:
            if len(hand) == 2:
                return 'd'
            else:
                return 'h'
        return 'h'