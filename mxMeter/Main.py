# coding=utf-8
# from API_v_1_0 import *
from Ribbon import MxRibbon
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

class MxMeter:
    def __init__(self):
        self.PUK_FORMAT = u"%0.2fПУК"
        self.NO_PUK = u"-"
        self.PUK_SCALE = 1.0  # use 100.0 to display in percent
        self.POSITION_X = -174

        self.battle_started = False
        self.post_battle_results = False
        self.puk_total = 0.0
        self.players_health = {}
        self.setup_events()
        self.apply_ini_settings()
        flash.setUbMarkup('MxMeter.xml', 'MxMeter.swf', 'MxMeter')

    def setup_events(self):
        events.onReceiveShellInfo(self.on_receive_shell_info)
        events.onGotRibbon(self.on_got_ribbon)
        events.onBattleStart(self.on_battle_start)
        events.onBattleQuit(self.on_battle_quit)
        events.onSFMEvent(self.on_sfm_event)

    def apply_ini_settings(self):
        try:
            ini_file = ini.MyIniFile(utils.getModDir() + '\\..\\..\\..\\..\\..\\mxmeter.ini')
        except:
            try:
                ini_file = ini.MyIniFile(utils.getModDir() + '/mxmeter.ini')
            except:
                ini_file = None
        if ini_file:
            PUK_FORMAT = ini_file.get('PUK_FORMAT')
            if PUK_FORMAT:
                self.PUK_FORMAT = PUK_FORMAT
            NO_PUK = ini_file.get('NO_PUK')
            if NO_PUK:
                self.NO_PUK = NO_PUK

            PUK_SCALE = ini_file.get('PUK_SCALE')
            if PUK_SCALE:
                try:
                    self.PUK_SCALE = float(PUK_SCALE)
                except:
                    None

            POSITION_X = ini_file.get('POSITION_X')
            if POSITION_X:
                try:
                    self.POSITION_X = int(float(POSITION_X))
                except:
                    None

    def init_state(self):
        self.puk_total = 0.0
        self.players_health = {}
        players_info_collection = battle.getPlayersInfo()
        for playerId in players_info_collection:
            player_info = players_info_collection[playerId]
            self.players_health[player_info.shipId] = player_info.maxHealth

    def update_ui(self):
        if not self.battle_started and not self.post_battle_results:
            flash.setUbData({
                'mx_visible': 0,
                'mx_print': '',
                'mx_position_x': self.POSITION_X,
            })
        elif self.puk_total > 0.0:
            flash.setUbData({
                'mx_visible': 1,
                'mx_print': self.PUK_FORMAT % (self.puk_total * self.PUK_SCALE),
                'mx_position_x': self.POSITION_X,
            })
        else:
            flash.setUbData({
                'mx_visible': 1,
                'mx_print': self.NO_PUK,
                'mx_position_x': self.POSITION_X,
            })

    def add_puk(self, puk):
        self.puk_total += puk
        self.update_ui()

    def on_receive_shell_info(self, victim_id, shooter_id, ammo_id, mat_id, shot_id, booleans, damage, shot_position, yaw, *args, **kwargs):
        """
        :param victim_id: идентификатор атакованного
        :param shooter_id: идентификатор атакующего
        :param ammo_id: тип снаряда
        :param mat_id: тип материала, в который было попадание
        :param shot_id: идентификатор выстрела
        :param booleans: if(booleans & 1) урон получил наш корабль
        :param damage: кол-во нанесенного урона
        :param shot_position: точка попадания
        :param yaw: yaw снаряда
        :param args:
        :param kwargs:
        :return:
        """
        if (booleans & 1) == 0 and victim_id in self.players_health:
            puk = float(damage) / float(self.players_health[victim_id])
            self.add_puk(puk)

    def on_got_ribbon(self, ribbon_id, a_value):
        ribbon = MxRibbon(ribbon_id)
        puk = ribbon.getPuk()
        self.add_puk(puk)

    def on_battle_start(self):
        self.init_state()
        self.battle_started = True
        self.update_ui()

    def on_battle_quit(self, arg):
        self.battle_started = False
        self.update_ui()

    def on_sfm_event(self, event_name, event_data):
        if event_name == 'window.show' and event_data['windowName'] == 'ResultsScreen':
            self.post_battle_results = True
            self.update_ui()
        elif event_name == 'window.hide' and event_data['windowName'] == 'ResultsScreen':
            self.post_battle_results = False
            self.update_ui()


g_mxMeter = MxMeter()
