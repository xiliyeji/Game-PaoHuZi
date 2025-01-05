from enum import Enum
import random

from _class.card import Card

# 玩家行为
class Player_action(Enum):
    胡 = 0
    杠 = 1
    碰 = 2
    吃 = 3

# 玩家类
class Player:
    # 玩家计数
    count = 0

    def __init__(self):
        self.number = Player.count                    # 序号
        self.hand: list[Card] = []                    # 手牌
        self.gold: list[Card] = []                    # 胡子
        self.cardList_deal: list[Card] = []           # 交易牌组
        Player.count += 1                             # 玩家计数

    def get_number(self):
        '''获取编号'''
        return self.number

    def playcard(self) -> Card:
        '''玩家随机出牌'''

        if len(self.hand) <= 0:
            return
        while(True):
            card = self.hand[random.randint(0, len(self.hand) - 1)]
            if self.hand.count(card) < 3:
                self.hand.remove(card)
                print(f'玩家{self.number}出牌：{card.name}')
                print(f'玩家{self.number}手牌: {Card.getName(self.hand)}, 共{len(self.hand)}张')
                return card
  
    def getCard(self, card: Card):
        '''玩家摸牌'''
        print(f'玩家{self.number}摸牌：{card.name}')
    
    def tryDeal(self, action: Player_action, card: Card):
        """
        判断玩家是否要牌
        action: 杠/碰/吃/胡
        card: 响应牌
        """
        # 尝试：杠
        if action == Player_action.杠:
            if self.hand.count(card) == 3:
                self.cardList_deal = [card] * 4
                return True
            else:
                return False
        # 尝试：碰
        elif action == Player_action.碰:
            if self.hand.count(card) == 2:
                self.cardList_deal = [card] * 3
                return True
            else:
                return False
        # 尝试：吃
        elif action == Player_action.吃:
            if len(self.hand) < 2 or self.hand.count(card) >= 3:
                return False
            else:
                # 一、 红吃：   二七十，贰柒拾
                list_chi = [[Card.二, Card.七, Card.十], [Card.贰, Card.柒, Card.拾]]         
                for list in list_chi:
                    if not card in list:
                        break
                    else:       
                        idx = list.index(card)
                        if (1 <= self.hand.count(list[(idx+1)%3]) < 3) and (1 <= self.hand.count(list[(idx+2)%3]) < 3):
                            self.cardList_deal = [card, list[(idx+1)%3], list[(idx+2)%3]]
                            return True

                # 二、 顺吃：   壹贰叁，二三四
                ## a. 目标牌为中位
                if (1 <= self.hand.count(card.get(-1)) < 3) and (1 <= self.hand.count(card.get(+1)) < 3):
                    self.cardList_deal = [card, card.get(-1), card.get(+1)]
                    return True
                ## b. 目标牌为边位
                ### 1. 目标牌为小牌
                if (1 <= self.hand.count(card.get(+1)) < 3) and (1 <= self.hand.count(card.get(+2)) < 3):
                    self.cardList_deal = [card, card.get(+1), card.get(+2)]
                    return True
                ### 2. 目标牌为大牌
                if (1 <= self.hand.count(card.get(-1)) < 3) and (1 <= self.hand.count(card.get(-2)) < 3):
                    self.cardList_deal = [card, card.get(-2), card.get(-1)]
                    return True

                # 三、 同吃：   一一壹, 壹壹一
                ## a. 一一壹，壹壹一
                if (self.hand.count(card) == 1) and (1 <= self.hand.count(card.get(0)) < 3):
                    self.cardList_deal = [card] * 2 + [card.get(0)]
                    return True
                ## b. 二贰贰，贰二二
                if self.hand.count(card.get(0)) == 2:
                    self.cardList_deal = [card] + [card.get(0)] * 2
                    return True
                
        # 尝试：胡
        elif action == Player_action.胡:
            if len(self.hand) <= 0:
                return True
            else:  
                return False
        return False
        
    def deal(self, action: Player_action):
        '''玩家要牌'''
        if action == Player_action.胡:
            print(f'玩家{self.number}胡了!')
        # 更新手牌
        for i in range(1, len(self.cardList_deal)):
            self.hand.remove(self.cardList_deal[i])
        # 打印结果
        print(f'玩家{self.number}{action.name}: {Card.getName(self.cardList_deal)}')
        self.cardList_deal.clear()

        # 手牌判定
        card = self.hand[0]
        for num in range(2, 5):
            if len(self.hand) == num:
                if num == 3:
                    for action in Player_action:
                        if self.tryDeal(action, card):
                            print(f'玩家{self.number}获胜！')
                            return
                if self.hand.count(card) == num:
                    return

        # 玩家出牌
        self.playcard()

    def analysis(self):
        '''分析手牌统计进张'''
        pass