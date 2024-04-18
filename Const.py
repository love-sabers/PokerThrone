class Config(object):
    WINDOW_SIZE=(1080,720)
    pass

class GameEvent(object):
    NULL=0
    ADD_HP_OVER=1
    LOSE_HP_OVER=2
    ADD_MP_OVER=3
    LOSE_MP_OVER=4