from cards import *
from random import randint


def blackjack(players=1, num_decks=6, sim=False, num_sims=100):

    shoe = Shoe(num_decks)
    shoe.shuffle()

    human = {}
    records = {}
    money = {}
    for player in range(1, players + 1):
        if not sim:
            hoc = input("Player %d: Human or Computer? (h,c) " % player)
        else:
            hoc = 'c'
        human[player] = hoc == 'h'
        records[player] = [0, 0, 0, 0]
        money[player] = 0

    count = 0
    another = 'y'
    while another == 'y':
        count += 1
        player_cards = [[] for _ in range(players)]
        house_cards = []

        for _ in range(2):
            for hand in player_cards:
                hand.append(shoe.deal_one())
            house_cards.append(shoe.deal_one())

        for i in range(len(player_cards)):
            player_cards[i] = Deck(player_cards[i], i + 1, 1)
            if human[i + 1] == 'h':
                bet = input("Player %d: How much do you want to bet? " % player)
            else:
                bet = 10
            player_cards[i].bet(int(bet))

        print()
        house_cards = Deck(house_cards)
        dealer_card = house_cards.card_list[0].value
        print("House:    [%s, ??]" % house_cards.card_list[0])
        for hand in player_cards:
            pass
            print("Player %d: %s %d" % (hand.player, hand, hand.total()))
        print()

        if house_cards.total() == 21:
            print("House gets blackjack!")
            print("House:    %s %d" % (house_cards.card_list, house_cards.total()))
            print()
            dealerbj = True
        else:
            dealerbj = False

        i = 0
        while i < len(player_cards):
            hand = player_cards[i]
            player = hand.player
            print("Player %d, Hand %d: %s %d" % (player, hand.hand_num, hand, hand.total()))
            if hand.total() == 21:
                print("Player %d gets blackjack!" % player)
                print()
                if not dealerbj:
                    hand.bj = True
            elif not dealerbj:
                split = False
                if hand.is_split():
                    split = True
                    if human[player]:
                        move = input("Player %d: h, s, d, t, x? " % player)
                    else:
                        move = bookplay(hand, dealer_card)
                        print("Player %d: %s" % (player, move))
                    if move == 't':
                        hand1 = Deck([hand.card_list[0], shoe.deal_one()], player, hand.hand_num)
                        hand2 = Deck([hand.card_list[1], shoe.deal_one()], player, hand.hand_num + 1)
                        hand1.bet(hand.bet_amount)
                        hand2.bet(hand.bet_amount)
                        j = 1
                        while i + j < len(player_cards) and player_cards[i + j].player == player:
                            player_cards[i + j].hand_num += 1
                            j += 1
                        rest = player_cards[i + 1:]
                        player_cards = player_cards[:i] + [hand1, hand2] + rest
                        print()
                        continue

                if not split:
                    if human[player]:
                        move = input("Player %d: h, s, d, x? " % player)
                    else:
                        move = bookplay(hand, dealer_card)
                        print("Player %d: %s" % (player, move))

                if move == 'x':
                    print("Player %d surrenders" % player)
                    hand.surrender = True
                    move = 's'

                while move != 's':
                    hand.add(shoe.deal_one())
                    print("Player %d: %s %d" % (player, hand, hand.total()))
                    if hand.total() > 21:
                        print("Player %d busts!" % player)
                        break
                    elif hand.total() == 21:
                        print("Player %d gets 21!" % player)
                        break
                    elif move == 'd':
                        hand.bet(2 * hand.bet_amount)
                        break
                    elif human[player]:
                        move = input("Player %d: h or s? " % player)
                    else:
                        move = bookplay(hand, dealer_card)
                        print("Player %d: %s" % (player, move))

                print()
            i += 1

        print("House:    %s %d" % (house_cards.card_list, house_cards.total()))
        while house_cards.total() < 17:
            house_cards.add(shoe.deal_one())
            print("House:    %s %d" % (house_cards.card_list, house_cards.total()))
            if house_cards.total() > 21:
                pass
                print("House busts!")
        print()
        for hand in player_cards:
            player = hand.player
            tot = hand.total()
            house_total = house_cards.total()
            if hand.surrender:
                print("Player %d, Hand %d surrenders with %d" % (player, hand.hand_num, tot))
                money[player] -= hand.bet_amount / 2
                records[player][3] += 1
            elif hand.bj:
                if dealerbj:
                    print("Player %d, Hand %d pushes with %d" % (player, hand.hand_num, tot))
                    records[player][2] += 1
                else:
                    print("Player %d, Hand %d wins with %d" % (player, hand.hand_num, tot))
                    records[player][0] += 1
                    money[player] += 1.5 * hand.bet_amount
            elif tot <= 21:
                if tot > house_total or house_total > 21:
                    print("Player %d, Hand %d wins with %d" % (player, hand.hand_num, tot))
                    records[player][0] += 1
                    money[player] += hand.bet_amount
                elif tot == house_total:
                    print("Player %d, Hand %d pushes with %d" % (player, hand.hand_num, tot))
                    records[player][2] += 1
                else:
                    print("Player %d, Hand %d loses with %d" % (player, hand.hand_num, tot))
                    records[player][1] += 1
                    money[player] -= hand.bet_amount
            else:
                print("Player %d, Hand %d busts with %d" % (player, hand.hand_num, tot))
                records[player][1] += 1
                money[player] -= hand.bet_amount
        print()

        if not sim:
            another = input("Play again? (y,n) ")
            print()
        else:
            another = 'y'

        if count >= num_sims:
            break

        if len(shoe) <= 50:
            print("New shoe!")
            print()
            shoe = Shoe(num_decks)
            shoe.shuffle()

    print("Played %d hands" % count)
    print()
    for player in records:
        print("Player %d: %s, Finished with %d" % (player, records[player], money[player]))

blackjack(1, 6, True, 10)