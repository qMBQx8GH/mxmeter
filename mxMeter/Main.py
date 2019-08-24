# coding=utf-8
#from API_v_1_0 import *
from Ribbon import mxRibbon
import ini

API_VERSION = 'API_v1.0'
MOD_NAME = 'mxMeter'

"""
https://forum.worldofwarships.ru/topic/68750-изменения-экономики-до-и-после-0512/

Учитываются:
Урон ГК, ПМК, Торпед и Бомб
Сбитые самолёты = 1/30
Фраги = 1/5
Захват точки = 1/3
Обнаружение = 1/120

Не учитываются:
Пожары
Затопления
Разность в уровнях кораблей
Восстановление хилкой (реально ПУК будет меньше)
Потенциальный урон
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
        self.battle_started = False
        self.post_battle_results = False
        self.initState()
        self.setupEvents()

    def initState(self, battle_start=False):
        self.puk_total = 0.0
        self.players_health = {}
        if battle_start:
            players_info_collection = battle.getPlayersInfo()
            for playerId in players_info_collection:
                player_info = players_info_collection[playerId]
                self.players_health[player_info.shipId] = player_info.maxHealth

    def changeState(self):
        if self.battle_started or self.post_battle_results:
            interface_scale = self.getInterfaceScale()
            x = int(-170 * interface_scale)
            y = int(0 * interface_scale)
            font_size = int(18 * interface_scale)
            width = int(75 * interface_scale)
            if self.puk_total > 0:
                flash.call(mxMeter.SHOW_PUK_INDICATOR, [x, y, font_size, width, mxMeter.PUK_FORMAT % self.puk_total])
            else:
                flash.call(mxMeter.SHOW_PUK_INDICATOR, [x, y, font_size, width, mxMeter.NO_PUK])
        else:
            flash.call(mxMeter.HIDE_PUK_INDICATOR, [])

    def setupEvents(self):
        events.onReceiveShellInfo(self.onReceiveShellInfo)
        events.onGotRibbon(self.onGotRibbon)
        events.onBattleStart(self.onBattleStart)
        events.onBattleQuit(self.onBattleQuit)
        events.onSFMEvent(self.onSFMEvent)

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
            #print "mxMeter shell_hit ", victimID, ammoId, damage
            puk = float(damage) / float(self.players_health[victimID])
            self.addPuk(puk)

    def onGotRibbon(self, ribbon_id):
        #print "mxMeter onGotRibbon", ribbon_id
        ribbon = mxRibbon(ribbon_id)
        puk = ribbon.getPuk()
        self.addPuk(puk)

    def addPuk(self, puk):
        self.puk_total += puk
        #print "mxMeter puk_total ", self.puk_total
        if puk > 0:
            flash.call(mxMeter.UPDATE_PUK_INDICATOR, [mxMeter.PUK_FORMAT % self.puk_total])

    def onBattleStart(self):
        print "mxMeter: onBattleStart SHOW_PUK_INDICATOR"
        self.initState(battle_start=True)
        self.battle_started = True
        self.changeState()

    def onBattleQuit(self, arg):
        print "mxMeter: onBattleQuit HIDE_PUK_INDICATOR"
        self.battle_started = False
        self.changeState()

    def onSFMEvent(self, eventName, eventData):
        if eventName == 'window.show' and eventData['windowName'] == 'PostBattle':
            print "mxMeter: onSFMEvent SHOW_PUK_INDICATOR"
            self.post_battle_results = True
            self.changeState()
        elif eventName == 'window.hide' and eventData['windowName'] == 'PostBattle':
            print "mxMeter: onSFMEvent HIDE_PUK_INDICATOR"
            self.post_battle_results = False
            self.changeState()

    def xmlCut(self, str, tag):
        result = ''
        open_tag_start = str.find('<' + tag)
        if open_tag_start >= 0:
            open_tag_end = str.find('>', open_tag_start)
            if open_tag_end >= 0:
                end_tag_start = str.find('</' + tag, open_tag_end)
                if end_tag_start >= 0:
                    result = str[open_tag_end + 1:end_tag_start]
        return result

    def getInterfaceScale(self):
        interface_scale = 1.0
        with open(utils.getModDir() + '\\..\\..\\..\\..\\preferences.xml', 'r') as prefsFile:
            prefsData = prefsFile.read()
            interface_scale_str = self.xmlCut(prefsData, 'interfaceScale').strip()
            if not interface_scale_str:
                ini_file = ini.MyIniFile(utils.getModDir() + '/mxmeter.ini')
                interface_scale_str = ini_file.get('interfaceScale')
            if interface_scale_str:
                try:
                    interface_scale = float(interface_scale_str)
                except ValueError:
                    pass

        return interface_scale

g_mxMeter = mxMeter()
