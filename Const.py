#此部分为游戏常量
from enum import Enum,unique

class Config(object):
    #游戏系统参数
    WINDOW_SIZE=(1080,720)
    FPS=60
    pass

@unique
class GameEvent(Enum):
    #游戏事件常量
    NULL=0
    ADD_HP_OVER=1
    LOSE_HP_OVER=2
    ADD_MP_OVER=3
    LOSE_MP_OVER=4
    SKILL_RELEASE=5
    IMMUNE=6
    HEAL=7
    RAGE=8
    SHOCK=9
    GETCARD=10
    ATTACK=11
    POISONED=12
    PURIFY=13
    POISONED2=14
    POISONED3=15

