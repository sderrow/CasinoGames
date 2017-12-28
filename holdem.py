import time
from random import shuffle
from itertools import combinations


class PokerHand:
    def __init__(self, cards):
        global cdict

        self.raw = cards
        self.cards = [(cdict[card[0]], card[1]) for card in cards]
        self.values = [c[0] for c in self.cards]
        self.suits = [c[1] for c in self.cards]

        # Check for Flush
        if self.suits == list(self.suits[0] * 5):
            self.flush = True
        else:
            self.flush = False

        # Check for Straight
        s = sorted(self.values)
        if s == list(range(s[0], s[0] + 5)):
            self.straight = True
        elif s == [2, 3, 4, 5, 14]:
            self.straight = True
            self.values.remove(14)
            self.values.append(1)
        else:
            self.straight = False

        vals = self.values
        pairs = []
        trips = 0
        quads = 0
        if not self.straight and not self.flush:
            for val in set(vals):
                if vals.count(val) == 2:
                    pairs.append(val)
                elif vals.count(val) == 3:
                    trips = val
                elif vals.count(val) == 4:
                    quads = val
        if len(pairs) == 1:
            if trips:  # If there's a full house
                s = [[6, trips, trips, trips, pairs[0], pairs[0]]]
                self.type = "Full house"
            else:  # If there's a pair
                s = [[1, pairs[0], pairs[0]]]
                vals = sorted([x for x in vals if x not in pairs], reverse=True)
                s.append(vals)
                self.type = "Pair"
        elif len(pairs) == 2:  # If there's two pair
            s = [[2, max(pairs), max(pairs), min(pairs), min(pairs)]]
            vals = [x for x in vals if x not in pairs]
            s.append(vals)
            self.type = "Two pair"
        elif trips:  # If there's 3 of a kind
            vals = [x for x in vals if x != trips]
            s = [[3, trips, trips, trips], vals]
            self.type = "Three of a kind"
        elif self.straight and not self.flush:  # If there's a straight
            s = [[4], sorted(self.values, reverse=True)]
            self.type = "Straight"
        elif self.flush and not self.straight:  # If there's a flush
            s = [[5], sorted(self.values, reverse=True)]
            self.type = "Flush"
        elif quads:  # If there's 4 of a kind
            vals = [x for x in vals if x != quads]
            s = [[7, quads, quads, quads, quads], vals]
            self.type = "Four of a kind"
        elif self.flush and self.straight:  # If there's a straightflush
            if max(self.values) == 14:
                self.type = "Royal flush"
                s = [[9]]
            else:
                self.type = "Straight flush"
                s = [[8]]
            s.append(sorted(self.values, reverse=True))
        else:  # If there's high card
            s = [[0], sorted(self.values, reverse=True)]
            self.type = "High card"
        s = [item for sublist in s for item in sublist]
        self.score = s


def generate_cards(num):
    global deck
    deck1 = list(deck)
    shuffle(deck1)
    return deck1[:num]


def generate_best_hands(players):
    raw = generate_cards(2 * players + 5)
    board = raw[-5:]
    p = []
    hands = []
    for i in range(0, 2 * players, 2):
        p.append(raw[i:i + 2])
        ms = []
        mh = None
        for hand in combinations(board + p[i // 2], 5):
            h = PokerHand(list(hand))
            s = h.score
            if s > ms:
                ms = s
                mh = h
        hands.append(mh)
    return board, p, hands


def index_max(values):
    return max(list(range(len(values))), key=values.__getitem__)


def texas(players, rounds):
    ties = 0
    stats = [0] * 10
    if players > 10:
        if prnt: print("Too many players!")
        return [0] * players, ties, stats
    wins = [0] * players
    for line in range(rounds):
        if prnt: print("Round:", line + 1)
        (board, pockets, hands) = generate_best_hands(players)
        if prnt:
            for dawg in range(players):
                print("Player %d started with %s" % (dawg + 1, pockets[dawg]))
            print()
            print("The board was", board)
            print()
            for dawg in range(players):
                print("Player %d's best hand was %s (%s)" % (dawg + 1, hands[dawg].raw, hands[dawg].type))
            print()
        w = index_max([i.score for i in hands])
        winners = [w + 1]
        for i, d in enumerate(hands):
            if i != w and d.score == hands[w].score: winners.append(i + 1)
        if len(winners) == 1:
            if prnt: print("Player %d wins!" % (w + 1))
            wins[w] += 1
        else:
            if prnt: print("It's a tie between Players %s!" % (winners))
            ties += 1
        if prnt: print()
        royal = False
        quad_ace = False
        for p in hands:
            if p.score[0] == 9:
                royal = True
            if p.score[0] == 7 and p.score[1] == 14:
                quad_ace = True
            stats[p.score[0]] += 1
        if royal and quad_ace:
            print("Royal flush against quad aces!")
            for dawg in range(players):
                print("Player %d started with %s" % (dawg + 1, pockets[dawg]))
            print()
            print("The board was", board)
            print()
            for dawg in range(players):
                print("Player %d's best hand was %s (%s)" % (dawg + 1, hands[dawg].raw, hands[dawg].type))
            print()
    return wins, ties, stats


start = time.time()

# ENTER NUMBER OF PLAYERS AND NUMBER OF ROUNDS BELOW (expect ~350ms per 1000 player-rounds)
players = 5
rounds = 2000

# MAKE THE prnt VARIABLE TRUE IF YOU WANT TO SEE EXACTLY WHAT HAPPENS IN EVERY ROUND
prnt = False

# DON'T MESS WITH THE BELOW!
nums = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'] * 4
suits = sorted(['C', 'H', 'D', 'S'] * 13)
deck = [c + suits[i] for i, c in enumerate(nums)]
cdict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

(wins, ties, stats) = texas(players, rounds)
hand_names = ('high card', 'pair', 'two pair', 'three of a kind', 'straight', 'flush', 'full house', 'four of a kind', 'straight flush', 'royal flush')

print("A total of", rounds, "rounds were played")
for p in range(players):
    print("Player %d won %d rounds" % (p + 1, wins[p]))
print(ties, "rounds were ties")
for i in range(10):
    print("There were %d (%.6f%s) %s hands" % (stats[i], stats[i] * 100 / (players * rounds), "%", hand_names[i]))

elapsed = time.time() - start
if elapsed < 1:
    elapsed *= 1000
    text = "milliseconds"
else:
    text = "seconds"
print("Program took:", elapsed, text)
