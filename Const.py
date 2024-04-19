class Config(object):
    WINDOW_SIZE=(1080,720)
    FPS=30
    pass

class GameEvent(object):
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
    ATTACK=10
    DEFENSE=11