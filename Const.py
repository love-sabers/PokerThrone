from enum import Enum,unique
class Config(object):
    WINDOW_SIZE=(1080,720)
    FPS=60
    pass

@unique
class GameEvent(Enum):
    NULL=0
    ADD_HP_OVER=1
    LOSE_HP_OVER=2
    ADD_MP_OVER=3
    LOSE_MP_OVER=4
    SKILL_RELEASE=5
    SKILL_RELEASE_FAIL=-1
    IMMUNE=6
    HEAL=7
    RAGE=8
    SHOCK=9
    RESHUFFLE=10
    ATTACK=11
    DEFENSE=12