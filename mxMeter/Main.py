# coding=utf-8
#from API_v_1_0 import *
from Ribbon import mxRibbon

API_VERSION = 'API_v1.0'
MOD_NAME = 'mxMeter'

"""
https://forum.worldofwarships.ru/topic/68750-изменения-экономики-до-и-после-0512/

Учитываются:
Урон ГК, ПМК, Торпед и Бомб
Сбитые самолёты
Фраги

Не учитываются:
Пожары
Затопления
Разность в уровнях кораблей
Восстановление хилкой (реально ПУК будет меньше)
Потенциальный урон
Обнаружение
Урон по засвету
Нелинейнось роста награды
Участие в захвате точек
Пониженный захват в режиме Эпицентр
Защита точек
Блокировка точек
"""
class mxMeter:
    SHOW_PUK_INDICATOR = "mxMeter.showPukIndicator"
    UPDATE_PUK_INDICATOR = "mxMeter.updatePukIndicator"
    HIDE_PUK_INDICATOR = "mxMeter.hidePukIndicator"

    PUK_FORMAT = u"%0.2fПУК"
    NO_PUK = u"-"

    def __init__(self):
        self.initState(battle_end=True)
        self.setupEvents()

    def initState(self, battle_start=False, battle_end=False):
        if battle_start:
            self.in_battle = True
            self.puk_total = 0.0
            self.players_health = {}
            players_info_collection = battle.getPlayersInfo()
            for playerId in players_info_collection:
                player_info = players_info_collection[playerId]
                self.players_health[player_info.shipId] = player_info.maxHealth
            self.ribbons = {}
        if battle_end:
            self.in_battle = False
            self.puk_total = 0.0
            self.players_health = None
            self.ribbons = {}

    def setupEvents(self):
        events.onReceiveShellInfo(self.onReceiveShellInfo)
        events.onGotRibbon(self.onGotRibbon)
        events.onBattleStart(self.onBattleStart)
        events.onBattleQuit(self.onBattleQuit)

    def onReceiveShellInfo(self
            ,victimID # - идентификатор атакованного
            ,shooterID # - идентификатор атакующего
            ,ammoId # - тип снаряда
            ,matId # - тип материала, в который было попадание
            ,shotID # - идентификатор выстрела
            ,booleans # - if(booleans & 1) урон получил наш корабль
            ,damage # - кол-во нанесенного урона
            ,shotPosition # - точка попадания
            ,yaw # - yaw снаряда
            ,*args
            ,**kwargs
    ):
        if (booleans & 1) == 0 and victimID in self.players_health:
            print "mxMeter shell_hit ", victimID, ammoId, damage
            puk = float(damage) / float(self.players_health[victimID])
            self.addPuk(puk)

    def onGotRibbon(self, ribbon_id):
        print "mxMeter onGotRibbon", ribbon_id
        if ribbon_id in self.ribbons:
            self.ribbons[ribbon_id] += 1
        else:
            self.ribbons[ribbon_id] = 1
        print "mxMeter self.ribbons", self.ribbons
        ribbon = mxRibbon(ribbon_id)
        puk = ribbon.getPuk()
        self.addPuk(puk)

    def addPuk(self, puk):
        self.puk_total += puk
        print "mxMeter puk_total ", self.puk_total
        if puk > 0:
            flash.call(mxMeter.UPDATE_PUK_INDICATOR, [mxMeter.PUK_FORMAT % self.puk_total])

    def onBattleStart(self):
        print "mxMeter: in_battle True"
        self.initState(battle_start=True)
        flash.call(mxMeter.SHOW_PUK_INDICATOR, [mxMeter.NO_PUK])

    def onBattleQuit(self, arg):
        print "mxMeter: in_battle False"
        self.initState(battle_end=True)
        flash.call(mxMeter.HIDE_PUK_INDICATOR, [])


g_mxMeter = mxMeter()
