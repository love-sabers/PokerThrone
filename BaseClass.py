from Const import GameEvent
class creature(object):
    """
    The base class of all creature
    including hero and monster
    """

    base_HP=100
    base_HP_min=0
    base_HP_max=100
    base_MP=2
    base_MP_min=0
    base_MP_max=50

    def __init__(self):
        self.HP=creature.base_HP
        self.MP=creature.base_MP
        return
    
    def add_HP(self,value):
        if(self.HP+value>creature.base_HP_max):
            self.HP=creature.base_HP_max
            return GameEvent.ADD_HP_OVER
        else:
            self.HP+=value
            return 0
        
    def lose_HP(self,value):
        if(self.HP-value<creature.base_HP_min):
            self.HP=creature.base_HP_min
            return GameEvent.LOSE_HP_OVER
        else:
            self.HP-=value
            return 0 
    
    def add_MP(self,value):
        if(self.MP+value>creature.base_MP_max):
            self.MP=creature.base_MP_max
            return GameEvent.ADD_MP_OVER
        else:
            self.MP+=value
            return 0
        
    def lose_MP(self,value):
        if(self.MP-value<creature.base_MP_min):
            self.MP=creature.base_MP_min
            return GameEvent.LOSE_MP_OVER
        else:
            self.MP-=value
            return 0 
        
class card(object):
    card_num=3
    def __init__(self):
        self.cardid=0
        pass
    def run(self):
        pass

class carddeck(object):
    pass

class poker(object):
    pass

class pokerdeck(object):
    pass