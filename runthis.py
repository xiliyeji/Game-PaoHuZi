from _class.game import *

def test(game: Game):
    game.newCards()
    game.getHand()
    player = game.players[0]


    print('----------------------------------------------------------------------------------')
    print(f'玩家手牌: {Card.getName(Card.sort(player.hand))}, 共{len(player.hand)}张')
    print(f'玩家胡子: {Card.getName(player.gold)}, 共{len(player.gold)}张')

    # 除去：杠/碰
    for card in player.hand:
        for num in [4, 3]:
            if player.hand.count(card) == num:
                player.gold.extend([card] * num)
                for _ in range(num):
                    player.hand.remove(card)    
    print('----------------------------------------------------------------------------------')
    print(f'玩家手牌: {Card.getName(Card.sort(player.hand))}, 共{len(player.hand)}张')
    print(f'玩家胡子: {Card.getName(player.gold)}, 共{len(player.gold)}张')

    # 除去：吃
    try:
        idx = 0
        while True:
            ifChange = False
            hand = player.hand.copy()
            card = player.hand.pop(idx)
            if player.tryDeal(Player_action.吃, card):
                for _card in player.cardList_deal:
                    player.gold.append(_card)
                    hand.remove(_card)
            else:
                idx += 1
            player.hand = hand.copy()            

            if ifChange:
                print('----------------------------------------------------------------------------------')
                game.showHand()
                game.showGold()
    except IndexError:
        pass

    print('----------------------------------------------------------------------------------')
    print(f'玩家手牌: {Card.getName(Card.sort(player.hand))}, 共{len(player.hand)}张')
    print(f'玩家胡子: {Card.getName(player.gold)}, 共{len(player.gold)}张')

                                                                                                                                                                                                                                                                                                                                        
def main():
    num_players = 4     # 玩家数量
    game = Game(num_players)
    # game.startGame()
    for _ in range(1):
        test(game)

if __name__ == "__main__":
    main()