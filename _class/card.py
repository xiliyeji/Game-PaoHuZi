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

    def getName(cardList):
        """获取列表“list[Card]”的名字列表“list[Card.name]。"""
        nameList = []
        for card in cardList:
            nameList.append(card.name)
        return nameList

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


def deal(hands: list, card: Card):
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
    hands_cp, chance = hands, set()
    for card in hands_cp:
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
    return len(chance)

def analyze(hands: list[Card]):
    result = {'point': 0, 'chance': 0}
    result_cp = result.copy()
    for card in set(hands):
        hands_cp = hands.copy()
        hands_cp.remove(card)
        deal_list = deal(hands_cp, card)
        hands_deal_list, cards_deal_list = deal_list[0], deal_list[1]
        if len(cards_deal_list) == 0:
            continue
        else:
            for hands_deal, cards_deal in zip(hands_deal_list, cards_deal_list):
                result_alz = analyze(hands_deal)
                result_alz['point'] += 1
                if result_alz['point'] > result['point'] or (result_alz['point'] == result['point'] and result_alz['point'] > result['chance']):
                    result = result_alz
    if result == result_cp:
        result['chance'] = getChance(hands)
    return result

def main():                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    cards = newCards()
    hands = Card.sort(getHands(cards))
    print(Card.getName(hands), '  ', len(hands))
    print(analyze(hands))

def test():
    hands = [Card.一, Card.二, Card.四, Card.四, Card.五, Card.六, Card.七, Card.九, Card.壹, Card.贰, Card.叁, Card.陆, Card.柒, Card.拾]
    print(Card.getName(hands), '  ', len(hands))
    print(analyze(hands))

if __name__ == '__main__':
    if 0:
        main()
    else:
        test()
