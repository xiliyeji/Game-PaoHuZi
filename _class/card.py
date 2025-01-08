import random
from enum import Enum

class Card(Enum):
    一 = 1
    二 = 2
    三 = 3
    四 = 4
    五 = 5
    六 = 6
    七 = 7
    八 = 8
    九 = 9
    十 = 10
    壹 = 21
    贰 = 22
    叁 = 23
    肆 = 24
    伍 = 25
    陆 = 26
    柒 = 27
    捌 = 28
    玖 = 29
    拾 = 30

    def get(self, diff: int) -> 'Card':
        """
        按差值“diff”查找Card对象。  当diff=0时，代表查找对应小/大写
        """
        try:
            if diff > 10:
                return None
            if diff == 10:
                if self.value <= 10:
                    return Card(self.value + 20)
                else:
                    return Card(self.value - 20)
            elif diff == 0:
                return Card(self.value)
            else:
                return Card(self.value + diff)
        except ValueError:
            return None

    def getName(cards): 
        """获取列表“list[Card]”的名字列表“list[Card.name]。"""
        if isinstance(cards, list):
            nameList = []
            for card in cards:
                nameList.append(card.name)
            return nameList
        elif isinstance(cards, Card):
            return cards.name
            
    def sort(cardList: list['Card']) -> list['Card']:
        """
        将列表“list[Card]”按值进行增序排序。
        """
        valueList = []
        for card in cardList:
            valueList.append(card.value)
        valueList.sort()
        cardList_new = []
        for value in valueList:
            cardList_new.append(Card(value))
        return cardList_new


def newCards():
    """创建一个新牌库。"""
    cards = [card for card in Card] * 4
    random.shuffle(cards)
    return cards


def getHands(cards: list):
    hands = []
    for _ in range(14):
        hands.append(cards.pop())
    return hands


def getCard(cards: list) -> Card:
    return cards.pop()


class DealType(Enum):
    碰_杠 = 0
    顺吃 = 1
    同吃 = 2
    红吃 = 3


def try_deal(hands: list, card: Card, dealType: DealType, list: list = []):
    if dealType == DealType.碰_杠:
        if hands.count(card) >= 2:
            return True
        else:
            return False

    elif dealType == DealType.顺吃:
        count = hands.count(card)
        if count >= 3:
            return False
        if not all(0 < hands.count(card.get(num)) < 3 for num in list):
            return False
        if count == 0:
            return True
        else:
            hands_cp = hands.copy()
            hands_cp.remove(card)
            for _num in list:
                hands_cp.remove(card.get(_num))
            if len(deal(hands_cp, card)[1]) > 0:
                return True
        return False

    elif dealType == DealType.同吃:
        count = hands.count(card)
        if count >= 3:
            return False
        card1, card2 = card.get(list[0]), card.get(list[1])
        if card1.value == card2.value:
            if hands.count(card1) != 2:
                return False
            if count == 0:
                return True
            else:
                hands_cp = hands.copy()
                for _card in [card, card1, card2]:
                    hands_cp.remove(_card)
                if len(deal(hands_cp, card)[1]) > 0:
                    return True
        else:
            if not (0 < hands.count(card1) < 3 and 0 < hands.count(card2) < 3):
                return False
            if count == 1:
                return True
            else:
                hands_cp = hands.copy()
                for _card in [card, card1, card2]:
                    hands_cp.remove(_card)
                if len(deal(hands_cp, card)[1]) > 0:
                    return True
        return False

    elif dealType == DealType.红吃:
        if not all(0 < hands.count(_card) < 3 for _card in list):
            return False
        count = hands.count(card)
        if count >= 3:
            return False
        elif count == 0:
            return True
        else:
            hands_cp = hands.copy()
            hands_cp.remove(card)
            for _card in list:
                hands_cp.remove(_card)
            if len(deal(hands_cp, card)[1]) > 0:
                return True
        return False


def deal(hands: list, card: Card) -> list[list[list[Card]]]:
    '''
    用于分析hands所有需要card的组合与结果；返回一个list, 其中: list[0]=hands_new, list[1]=cards_deal。
    hands: 手牌; card: 响应牌; hands_new: 要牌后的手牌; cards_deal: 要牌组合
    '''
    hands_new, cards_deal = [], []
    if try_deal(hands, card, DealType.碰_杠):
        hands_temp = hands.copy()
        cards_deal_temp = []
        while card in hands_temp:
            hands_temp.remove(card)
            cards_deal_temp.append(card)
        hands_new.append(hands_temp)
        cards_deal_temp.append(card)
        cards_deal.append(cards_deal_temp)

    for numList in [[-2, -1], [-1, 1], [1, 2]]:
        if try_deal(hands, card, DealType.顺吃, numList):
            hands_temp, cards_deal_temp = hands.copy(), [card]
            for num in numList:
                card_temp = card.get(num)
                hands_temp.remove(card_temp)
                cards_deal_temp.append(card_temp)
            hands_new.append(hands_temp)
            cards_deal.append(Card.sort(cards_deal_temp))

    for numList in [[10, 10], [10, 0]]:
        card1, card2 = card.get(numList[0]), card.get(numList[1])
        if try_deal(hands, card, DealType.同吃, numList):
            hands_temp = hands.copy()
            hands_temp.remove(card1)
            hands_temp.remove(card2)
            hands_new.append(hands_temp)
            cards_deal.append(Card.sort([card, card1, card2]))

    if card.value <= 10:
        _cards = [Card.二, Card.七, Card.十]
    else:
        _cards = [Card.贰, Card.柒, Card.拾]
    if card in _cards:
        _cards_cp = _cards.copy()
        _cards_cp.remove(card)
        if try_deal(hands, card, DealType.红吃, _cards_cp):
            _hands = hands.copy()
            for c in _cards_cp:
                _hands.remove(c)
            hands_new.append(_hands)
            cards_deal.append(_cards)
    return [hands_new, cards_deal]

def getChance(hands: list[Card]):
    '''
    获取hands的进张数量。
    '''
    chance = set()
    for card in set(hands):
        hands_cp = hands.copy()
        hands_cp.remove(card)
        for try_list in [[Card.二, Card.七, Card.十], [Card.贰, Card.柒, Card.拾]]:
            if card in try_list:
                try_list.remove(card)
                card1, card2 = try_list[0], try_list[1]
                if card1 in hands_cp:
                    chance.add(card2)
                if card2 in hands_cp:
                    chance.add(card1)
        if card in hands_cp:
            chance.update([card, card.get(10)])
        if card.get(10) in hands_cp:
            chance.update([card.get(10), card])
        if card.get(1) in hands_cp:
            chance.update([card.get(2), card.get(-1)])
        if card.get(-1) in hands_cp:
            chance.update([card.get(-2), card.get(1)])
        if card.get(2) in hands_cp:
            chance.add(card.get(1))
        if card.get(-2) in hands_cp:
            chance.add(card.get(-1))
    if None in chance:
        chance.remove(None)
    return len(chance)

def analyze(hands: list[Card]):
    result = {'point': 0, 'chance': 0}
    if hands == []:
        return result
    result_cp = result.copy()
    for card in set(hands):
        flag_cantDeal = False
        hands_cp = hands.copy()
        hands_cp.remove(card)
        deal_list = deal(hands_cp, card)
        hands_deal_list, cards_deal_list = deal_list[0], deal_list[1]
        if len(cards_deal_list) == 0:
            flag_cantDeal = True
        else:
            for hands_deal, cards_deal in zip(hands_deal_list, cards_deal_list):
                result_alz = analyze(hands_deal)
                result_alz['point'] += 1
                if result_alz['point'] > result['point'] or (result_alz['point'] == result['point'] and result_alz['chance'] > result['chance']):
                    result = result_alz
        if flag_cantDeal and result_cp['point'] >= result['point']:
            result['chance'] = getChance(hands)
    return result

def check_win(hands: list[Card], card: Card = None) -> bool:
    '''
    判断是否胡牌。
    '''
    if card != None:
        hands = hands.copy()
        hands.append(card)
    state = analyze(hands)
    if hands == [] or (state['chance'] == 0 and state['point']*3 == len(hands)):
        return True
    return False

def playCard(hands: list[Card]) -> Card:
    '''
    根据最优牌效出牌。
    '''
    if check_win(hands):
        return None
    card_play_best = None
    state = dict()
    for card_play in set(hands):
        if hands.count(card_play) >= 3:
            continue
        hands_new = hands.copy()
        hands_new.remove(card_play)
        state_new = analyze(hands_new)
        if card_play_best == None or state_new['point'] > state['point'] or (state_new['point'] == state['point'] and state_new['chance'] > state['chance']):
            card_play_best = card_play
            state = state_new.copy()
    hands.remove(card_play_best)
    if card_play_best == None:
        raise Exception('Card.playCard()错误返回！')
    return card_play_best
         
def thinkThenDo(hands: list[Card], card: Card) -> Card:
    '''
    对于card，分析hands是否要牌。如果要牌，则根据最优牌效出牌（返回值）。
    '''
    if hands == []:
        return None
    state = analyze(hands)
    card_play_best, cards_deal_best = None, []
    hands_deal_list = deal(hands, card)
    for hands_deal, cards_deal in zip(hands_deal_list[0], hands_deal_list[1]):
        card_play = playCard(hands_deal)
        if card_play == None:
            return None
        state_deal = analyze(hands_deal)
        state_deal['point'] += 1
        if state_deal['point'] > state['point'] or (state_deal['point'] == state['point'] and state_deal['chance'] > state['chance']):
            state = state_deal
            card_play_best, cards_deal_best[:] = card_play, cards_deal
            hands[:] = hands_deal
    if card_play_best != None:
        print(f'摸牌: {card}    要牌:{Card.getName(cards_deal_best)}    出牌: {Card.getName(card_play_best)}')
        print(f'手牌: {Card.getName(hands)}  {analyze(hands)}  {len(hands)}')
    return  card_play_best

def main():
    cards = newCards()
    hands = Card.sort(getHands(cards))
    print(Card.getName(hands), analyze(hands), len(hands))
    
    while cards != []:
        card = cards.pop()
        if check_win(hands, card):
            return print(f'玩家获胜！')
        thinkThenDo(hands, card)                        
    print('流局！')

def test():
    cards = newCards()
    hands = Card.sort(getHands(cards))
    print(Card.getName(hands), analyze(hands), len(hands))
    
    round = 0
    while True:
        round += 1
        # card = cards.pop()
        for card in Card:
            if thinkThenDo(hands, card) != None:
                break
            else:
                if check_win(hands, card):
                    print(f'回合数:{round}')
                    return print(f'玩家获胜！')
        if round > 5:
            return print('流局！')

if __name__ == '__main__':
    doTest = 0
    if doTest:
        test()
    else:
        main()
    pass
