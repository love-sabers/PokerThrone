import pygame
import random
import GUI
from GUI import Rod
'''
    Poker 类
        属性:

        rank: 表示牌的等级(2, 3, ..., 10, Jack, Queen, King, Ace)
        suit: 表示牌的花色(Hearts, Diamonds, Clubs, Spades)
        方法:

        __init__(self, rank, suit): 构造方法,初始化一张牌的等级和花色。
        __repr__(self): 特殊方法,用于定义对象的“官方”字符串表示,这里返回例如"Ace of Spades"这样的字符串,方便打印和查看。
'''

OPTION_SINGLE_IN = 1
OPTION_GROUP_IN = 2

class Poker:
    '''
    rank: 表示牌的等级(2, 3, ..., 10, Jack, Queen, King, Ace)
    suit: 表示牌的花色(Hearts, Diamonds, Clubs, Spades)
    '''

    POKER_DISABLE_PATH='source/Poker0.drawio.png'
    POKER_ENABLE_PATH='source/Poker1.drawio.png'
    SUIT_ORDER={'Diamonds':0,'Hearts':1,'Spades':2,'Clubs':3}
    RANK_ORDER={'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6,
                '9': 7, '10': 8, 'Jack': 9, 'Queen': 10, 'King': 11, 'Ace': 12}
    def __init__(self, rank:str, suit:str,source=None,option=OPTION_SINGLE_IN)->None:
        self.rank = rank
        self.suit = suit
        self.rank_value = self.get_rank_value(rank)

        if option==OPTION_SINGLE_IN :
            img_disable=pygame.image.load(Poker.POKER_DISABLE_PATH)
            img_enable=pygame.image.load(Poker.POKER_ENABLE_PATH)
            if img_disable.get_rect().size==img_enable.get_rect().size :
                width=int(img_disable.get_rect().width/13)
                heigh=int(img_disable.get_rect().height/4)
                px=Poker.RANK_ORDER[self.rank]*width
                py=Poker.SUIT_ORDER[self.suit]*heigh
                image_set=[img_disable.subsurface((px,py),(width,heigh)),
                        img_enable.subsurface((px,py),(width,heigh))]
                self.ui=Rod((50,50),image_set,2,mode=GUI.LIST_IN)
            else :
                raise Exception("Poker DisableImage and EnableImage are not same size")
        elif option==OPTION_GROUP_IN :
            self.ui=Rod((50,50),source,2,mode=GUI.LIST_IN)
        else:
            raise Exception("No such pokerinit option")


    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def get_rank_value(self, rank)->int:
        return Poker.RANK_ORDER[rank]
    
    def set_pos(self,pos:tuple[int,int],option=GUI.LEFTTOP)->None:
        self.ui.set_pos(pos,option)
    
    def render(self,surface:pygame.Surface)->None:
        self.ui.render(surface)

    def check_click(self,event):
        self.ui.check_click(event)

    def is_selected(self)->bool:
        return self.ui.is_selected()



'''
Deck 类
Pokers:
类型: list of Poker
描述: 存储未抽出的牌。这个列表在初始化时被创建为一幅完整的52副牌堆,并在牌堆需要被重置时重新生成和打乱。
disPokered:
类型: list of Poker
描述: 存储已经被弃用的牌。这包括之前公开过但现在不再需要的牌。
revealed:
类型: list of Poker
描述: 存储当前公开的牌,这些牌是玩家可以看到的。
unrevealed:
类型: list of Poker
描述: 存储还未公开的牌。从这个列表中抽牌来更新revealed列表。

Deck 类方法
__init__(self):
作用: 初始化Deck类的实例,调用reset_deck方法来创建和打乱一副牌,并设置初始的牌堆状态。
reset_deck(self):
作用: 重置整个牌堆。这包括生成新的52张牌,打乱这些牌,以及清空disPokered、revealed和unrevealed列表。将所有的牌都放入unrevealed列表中,准备进行牌局。
update_revealed(self):
作用: 更新公开牌堆的操作方法。此方法会将revealed牌堆的牌移动到disPokered牌堆。如果unrevealed牌堆的牌少于5张,则将disPokered的牌重新加入到unrevealed牌堆,打乱后再抽牌。最后,从unrevealed牌堆中抽出最多5张牌移到revealed牌堆中。
show_revealed(self):
返回: list of Poker
作用: 返回当前公开的牌堆。这个方法允许外部查看revealed牌堆中的牌。
show_unrevealed(self):
返回: list of Poker
作用: 返回未公开的牌堆。这个方法允许外部查看unrevealed牌堆中的牌。
show_disPokered(self):
返回: list of Poker
作用: 返回弃牌堆。这个方法允许外部查看disPokered牌堆中的牌。
'''

ROYAL_FLUSH=1
STRAIGHT_FLUSH=2
FOUR_AKIND=3
FULL_HOUSE=4
FLUSH=5
STRAIGHT=6
THREE_AKIND=7
TWO_PAIRS=8
ONE_PAIR=9
HIGH_POKER=10

'''
牌型规则与判断逻辑
1.皇家同花顺(Royal Flush)
同时满足同花和顺子的条件,并且是最大的顺子(10, J, Q, K, A)。这是扑克牌中最强的手牌。
2.同花顺(Straight Flush)
同时满足同花和顺子的条件,但不是皇家同花顺。按牌的数值大小决定同花顺的强度。
3.四条(Four of a Kind)
有四张相同数值的牌。
4.葫芦(Full House)
一个三条加上一个对子。
5.同花(Flush)
五张牌花色相同,但不构成顺子。
6.顺子(Straight)
五张连续数值的牌,但花色不同。
7.三条(Three of a Kind)
有三张相同数值的牌。
8.两对(Two Pairs)
有两个对子。
9.一对(One Pair)
只有一个对子。
10.高牌(High Poker)
不符合以上任何一种牌型的情况。
'''
class PokerDeck:
    GAP=120
    POKER_BACK_PATH='source/pokerback.drawio.png'
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self,pos:tuple[int,int]):
        self.pos=pos
        self.img_disPokered = GUI.ImageSet((0,360),PokerDeck.POKER_BACK_PATH,1,option=GUI.LEFTCENTER)
        self.img_unrevealed = GUI.ImageSet((1080,360),PokerDeck.POKER_BACK_PATH,1,option=GUI.RIGHTCENTER)


        img_disable=pygame.image.load(Poker.POKER_DISABLE_PATH)
        img_enable=pygame.image.load(Poker.POKER_ENABLE_PATH)
        if img_disable.get_rect().size==img_enable.get_rect().size :
            width=int(img_disable.get_rect().width/13)
            heigh=int(img_disable.get_rect().height/4)
        else:    
            raise Exception("Poker DisableImage and EnableImage are not same size")

        self.unrevealed=[]
        for suit in self.SUITS:
            for rank in self.RANKS:
                px=Poker.RANK_ORDER[rank]*width
                py=Poker.SUIT_ORDER[suit]*heigh
                image_set=[ img_disable.subsurface((px,py),(width,heigh)),
                            img_enable.subsurface((px,py),(width,heigh))]
                self.unrevealed.insert(0,Poker(rank, suit, source=image_set, option=OPTION_GROUP_IN))
                
        random.shuffle(self.unrevealed)
        self.revealed = []
        self.revealed_tmp= []
        self.disPokered = []

    def reset_deck(self):
        """ Resets the entire deck, shuffles the Pokers, and clears all piles. """
        self.unrevealed+=self.revealed+self.disPokered
        random.shuffle(self.unrevealed)
        self.disPokered = []
        self.revealed = []

    def update_revealed(self):
        self.disPokered.extend(self.revealed)
        self.revealed = []

        """ Move 5 Pokers from unrevealed to revealed, disPoker old revealed Pokers. """
        if len(self.unrevealed) < 5:
            # If less than 5 Pokers are unrevealed, shuffle disPokered into unrevealed
            self.reset_deck()

        # DisPoker currently revealed Pokers
        
        # Move up to 5 Pokers to revealed, if less than 5 remain, move all
        self.revealed = [self.unrevealed.pop(0) for _ in range(5)]
        self.set_pos(self.pos)

    def evaluate_hand(self):
        if len(self.revealed) < 5:
            return None  # Not enough Pokers to evaluate

        ranks = sorted([Poker.rank_value for Poker in self.revealed])
        suits = [Poker.suit for Poker in self.revealed]
        rank_counts = {rank: ranks.count(rank) for rank in ranks}
        suit_counts = {suit: suits.count(suit) for suit in suits}
        is_flush = max(suit_counts.values()) == 5
        is_straight = len(set(ranks)) == 5 and (max(ranks) - min(ranks) == 4)

        ret_set=[]
        if is_flush and is_straight:
            if ranks == [10, 11, 12, 13, 14]:  # Checking for Ace high straight flush (Royal Flush)
                ret_set.append(ROYAL_FLUSH)
            ret_set.append(STRAIGHT_FLUSH)
        if 4 in rank_counts.values():
            ret_set.append(FOUR_AKIND)
            ret_set.append(THREE_AKIND)
            ret_set.append(ONE_PAIR)
        if sorted(rank_counts.values()) == [2, 3]:
            ret_set.append(FULL_HOUSE)
            ret_set.append(THREE_AKIND)
            ret_set.append(ONE_PAIR)
            ret_set.append(TWO_PAIRS)
        if is_flush:
            ret_set.append(FLUSH)
        if is_straight:
            ret_set.append(STRAIGHT)
        if 3 in rank_counts.values():
            ret_set.append(THREE_AKIND)
            ret_set.append(ONE_PAIR)
        if list(rank_counts.values()).count(2) == 2:
            ret_set.append(TWO_PAIRS)
            ret_set.append(ONE_PAIR)
        if list(rank_counts.values()).count(2) == 1:
            ret_set.append(ONE_PAIR)
        return ret_set  # High Poker

    def render(self,surface:pygame.Surface)->None:
        if len(self.disPokered) :
            self.img_disPokered.render(surface)
        if len(self.unrevealed) :
            self.img_unrevealed.render(surface)
        for poker in self.revealed :
            poker.render(surface)

    def check_click(self,event):
        for poker in self.revealed :
            poker.check_click(event)
        

    def set_pos(self,pos:tuple[int,int]):
        i=-2
        for poker in self.revealed:
            poker.ui.enabled()
            poker.set_pos((pos[0]+i*PokerDeck.GAP,pos[1]),option=GUI.CENTER)
            i+=1

    def reload_user(self):
        # 统计选中的牌的个数
        selected_num=0
        for poker in self.revealed:
            if poker.is_selected() :
                selected_num+=1
        if len(self.unrevealed) >= selected_num:
            # Move specified Pokers to disPokered pile
            new_pokers=[]
            for poker in self.revealed :
                if poker.is_selected() :
                    self.disPokered.append(poker)
                else:
                    new_pokers.append(poker)
                    
            # Replace with random Pokers from the unrevealed pile
            random.shuffle(self.unrevealed)  # Shuffle for randomness
            new_pokers+= [self.unrevealed.pop(0) for _ in range(selected_num)]
            self.revealed=new_pokers
            self.set_pos(self.pos)

    def show_revealed(self):
        return self.revealed

    def show_unrevealed(self):
        return self.unrevealed

    def show_disPokered(self):
        return self.disPokered


# #Usage
# deck = Deck()
# print("Initial unrevealed Pokers:", deck.show_unrevealed())
# for i in range(12):
#     deck.update_revealed()
#     print(type(deck.show_revealed()),len(deck.show_revealed()))
#     print("Revealed Pokers:", len(deck.show_revealed()))
#     print("Remaining Unrevealed Pokers after update:", len(deck.show_unrevealed()))
#     print("DisPokered Pokers:", len(deck.show_disPokered()))
#     print("Poker hand rank:", deck.evaluate_hand())