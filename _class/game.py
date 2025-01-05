import random 
from enum import Enum

from _class.player import *
from _class.card import *


# 上回合结果
class RoundResult(Enum):
    roundPass = 0          # 回合过牌
    playerDeal = 1         # 玩家要牌

class Game():
    # 游戏开始
    def __init__(self, num_players: int):
        self.round = 0
        self.roundResult = RoundResult.roundPass
        self.card_current: Card = None
        self.cards: list[Card] = []
        self.nobodyWin = False
        self.winner: Player = None
        self.banker: Player = None
        self.players: list[Player] = []

        # 创建玩家实例
        self.players.extend([Player() for _ in range(num_players)])
        print('!----------<玩家创建完成>-----------!')

        # 庄家初始化
        self.banker = self.players[random.randint(0, 3)] 

    # 开始游戏
    def startGame(self):
        # 创建新牌库
        self.newCards()

        # 发手牌
        self.getHand()
        
        # 玩家手牌
        self.showHand()

        # 游戏进行
        while(self.winner == None):
            self.roundBegin()
            if self.nobodyWin == True:
                print('流局！')
                return
            
            self.roundGoing()
        self.gameOver()
    
    def gameOver(self):
        """游戏结束。"""
        if self.winner != None: 
            print('游戏结束！')
    
    def newCards(self):
        """创建一个新牌库。"""
        self.cards = [card for card in Card] * 4
        return random.shuffle(self.cards)

    def getHand(self):
        """给所有玩家发手牌。"""
        for player in self.players:
            player.hand.clear()
            player.gold.clear()
            for _ in range(14):
                player.hand.append(self.cards.pop())

    def showHand(self):
        """
        展示所有玩家的手牌。
        """
        for player in self.players:
            print(f'玩家{player.number}的手牌: {Card.getName(Card.sort(player.hand))}, 共{len(player.hand)}张')

    def showGold(self):
        """展示所有玩家的胡子。"""
        for player in self.players:
            print(f'玩家{player.number}的胡子: {Card.getName(player.gold)}, 共{len(player.gold)}张')

    # 回合开始
    def roundBegin(self):
        self.round += 1
        print(f'!——————————————回合{self.round}:——————————————!')
        # 回合结果：过牌 
        if self.roundResult == RoundResult.roundPass:   
            if len(self.cards) > 0:
                self.card_current = self.cards.pop()
            else:
                self.nobodyWin = True
                return
            self.banker.getCard(self.card_current)
        elif self.roundResult == RoundResult.playerDeal:
            self.card_current = self.banker.playcard()

    # 回合进行
    def roundGoing(self):
        for action in Player_action:
            player = self.ask(action)
            # 玩家要牌
            if player != None:
                if action == Player_action.胡:
                    self.winner = player
                    self.gameOver()
                    return 
                player.deal(action)
                self.roundResult = RoundResult.playerDeal
                self.banker = player
                break
        # 无玩家要牌    
        self.roundResult = RoundResult.roundPass
        self.banker = self.players[(self.banker.get_number() + 1) % 4]

    # 回合结束
    def roundOver(self):
        pass
        
    # 询问是否有玩家要牌
    def ask(self, action: Player_action) -> Player:
        players: list[Player] = []      # 询问玩家列表
        if action == Player_action.吃:
            if self.roundResult == RoundResult.roundPass:
                players.extend([self.banker, self.players[(self.banker.get_number() + 1) % 4]])
            else:
                players.extend([self.players[(self.banker.get_number() + 1 % 4)]])    
        else:
            players = self.players
        for player in players:
            if player.tryDeal(action, self.card_current):
                return player