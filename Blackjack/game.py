from cards import *


def blackjack(players=1, num_decks=6, sim=False, num_sims=100):

    shoe = Shoe(num_decks)
    shoe.shuffle()

    human = {}
    records = {}
    money = {}
    bet = {}
    for player in range(1, players + 1):
        if not sim:
            hoc = input("Player %d: Human or Computer? (h,c) " % player)
        else:
            hoc = 'c'
        human[player] = hoc == 'h'
        records[player] = [0, 0, 0]
        money[player] = 1000
        bet[player] = 10

    count = 0
    another = 'y'
    while another == 'y':
        count += 1
        player_cards = [[] for _ in range(players)]
        player_cards = dict(zip(range(1, players + 1), player_cards))
        house_cards = []
        totals = {}

        for _ in range(2):
            for player in range(1, players + 1):
                player_cards[player].append(shoe.deal_one())
            house_cards.append(shoe.deal_one())

        for player in player_cards:
            player_cards[player] = Deck(player_cards[player])
        print()
        house_cards = Deck(house_cards)
        dealer_card = house_cards.card_list[0].value
        print("House:    [%s, ??]" % house_cards.card_list[0])
        for player in player_cards:
            print("Player %d: %s %d" % (player, player_cards[player], player_cards[player].total()))
        print()

        if house_cards.total() == 21:
            print("House gets blackjack!")
            print("House:    %s %d" % (house_cards.card_list, house_cards.total()))
            print()
            dealerbj = True
        else:
            dealerbj = False

        for player in player_cards:
            hand = player_cards[player]
            if hand.total() == 21:
                print("Player %d gets blackjack!" % player)
                print()
                if not dealerbj:
                    money[player] += 1.5 * bet[player]
            elif not dealerbj:
                print("Player %d: %s %d" % (player, hand, hand.total()))
                if human[player]:
                    move = input("Player %d: h or s? " % player)
                else:
                    move = bookplay(hand, dealer_card)
                    print("Player %d: %s" % (player, move))

                while move != 's':
                    hand.add(shoe.deal_one())
                    print("Player %d: %s %d" % (player, hand, hand.total()))
                    if hand.total() > 21:
                        print("Player %d busts!" % player)
                        break
                    elif hand.total() == 21:
                        print("Player %d gets 21!" % player)
                        break
                    elif human[player]:
                        move = input("Player %d: h or s? " % player)
                    else:
                        move = bookplay(hand, dealer_card)
                        print("Player %d: %s" % (player, move))
                print()
            totals[player] = hand.total()

        print("House:    %s %d" % (house_cards.card_list, house_cards.total()))
        while house_cards.total() < 17:
            house_cards.add(shoe.deal_one())
            print("House:    %s %d" % (house_cards.card_list, house_cards.total()))
            if house_cards.total() > 21:
                print("House busts!")
        print()
        for player in totals:
            tot = totals[player]
            house_total = house_cards.total()

            if tot <= 21:
                if tot > house_total or house_total > 21:
                    print("Player %d wins with %d" % (player, tot))
                    records[player][0] += 1
                    money[player] += bet[player]
                elif tot == house_total:
                    print("Player %d pushes with %d" % (player, tot))
                    records[player][2] += 1
                else:
                    print("Player %d loses with %d" % (player, tot))
                    records[player][1] += 1
                    money[player] -= bet[player]
            else:
                print("Player %d busts with %d" % (player, tot))
                records[player][1] += 1
                money[player] -= bet[player]
        print()
        if not sim:
            another = input("Play again? (y,n) ")
        else:
            another = 'y'
        print()

        if count >= num_sims:
            break

        if len(shoe) <= 50:
            print("New shoe!")
            shoe = Shoe(num_decks)
            shoe.shuffle()

    print("Played %d hands" % count)
    print()
    for player in records:
        print("Player %d: %s, Finished with %d" % (player, records[player], money[player]))

blackjack(6, 6, True, 100)