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
    SHOW_PUK_INDICATOR = "mxMeter.showPukIndicator"
    UPDATE_PUK_INDICATOR = "mxMeter.updatePukIndicator"
    HIDE_PUK_INDICATOR = "mxMeter.hidePukIndicator"

    PUK_FORMAT = u"%0.2fПУК"
    NO_PUK = u"-"

    def __init__(self):
        self.battle_started = False
        self.post_battle_results = False
        self.puk_total = 0.0
        self.players_health = {}
        self.init_state()
        self.setup_events()

    def init_state(self, battle_start=False):
        self.puk_total = 0.0
        self.players_health = {}
        if battle_start:
            players_info_collection = battle.getPlayersInfo()
            for playerId in players_info_collection:
                player_info = players_info_collection[playerId]
                self.players_health[player_info.shipId] = player_info.maxHealth

    def change_state(self):
        if self.battle_started or self.post_battle_results:
            interface_scale = self.get_interface_scale()
            x = int(round(-170 * interface_scale))
            y = int(round(0 * interface_scale))
            font_size = int(round(18 * interface_scale))
            width = int(round(75 * interface_scale))
            if self.puk_total > 0:
                flash.call(MxMeter.SHOW_PUK_INDICATOR, [x, y, font_size, width, MxMeter.PUK_FORMAT % self.puk_total])
            else:
                flash.call(MxMeter.SHOW_PUK_INDICATOR, [x, y, font_size, width, MxMeter.NO_PUK])
        else:
            flash.call(MxMeter.HIDE_PUK_INDICATOR, [])

    def setup_events(self):
        events.onReceiveShellInfo(self.on_receive_shell_info)
        events.onGotRibbon(self.on_got_ribbon)
        events.onBattleStart(self.on_battle_start)
        events.onBattleQuit(self.on_battle_quit)
        events.onSFMEvent(self.on_sfm_event)

    def on_receive_shell_info(self, victim_id, shooter_id, ammo_id, mat_id, shot_id, booleans, damage, shot_position, yaw, *args, **kwargs):
        """

        :param victim_id: идентификатор атакованного
        :param shooter_id: идентификатор атакующего
        :param ammo_id: тип снаряда
        :param mat_id: тип материала, в который было попадание
        :param shot_id: идентификатор выстрела
        :param booleans: if(booleans & 1) урон получил наш корабль
        :param damage: кол-во нанесенного урона
        :param shot_position:  точка попадания
        :param yaw: yaw снаряда
        :param args:
        :param kwargs:
        :return:
        """
        if (booleans & 1) == 0 and victim_id in self.players_health:
            puk = float(damage) / float(self.players_health[victim_id])
            self.add_puk(puk)

    def on_got_ribbon(self, ribbon_id):
        ribbon = MxRibbon(ribbon_id)
        puk = ribbon.getPuk()
        self.add_puk(puk)

    def add_puk(self, puk):
        self.puk_total += puk
        if puk > 0:
            flash.call(MxMeter.UPDATE_PUK_INDICATOR, [MxMeter.PUK_FORMAT % self.puk_total])

    def on_battle_start(self):
        # utils.logInfo('mxMeter', {
        #     'event': 'onBattleStart',
        # })
        self.init_state(battle_start=True)
        self.battle_started = True
        self.change_state()

    def on_battle_quit(self, arg):
        # utils.logInfo('mxMeter', {
        #     'event': 'onBattleQuit',
        #     'arg': arg,
        # })
        self.battle_started = False
        self.change_state()

    def on_sfm_event(self, event_name, event_data):
        # utils.logInfo('mxMeter', {
        #     'event_name': event_name,
        #     'event_data': event_data,
        # })
        if event_name == 'window.show' and event_data['windowName'] == 'ResultsScreen':
            self.post_battle_results = True
            self.change_state()
        elif event_name == 'window.hide' and event_data['windowName'] == 'ResultsScreen':
            self.post_battle_results = False
            self.change_state()

    def xml_cut(self, xml_string, tag):
        result = ''
        open_tag_start = xml_string.find('<' + tag)
        if open_tag_start >= 0:
            open_tag_end = xml_string.find('>', open_tag_start)
            if open_tag_end >= 0:
                end_tag_start = xml_string.find('</' + tag, open_tag_end)
                if end_tag_start >= 0:
                    result = xml_string[open_tag_end + 1:end_tag_start]
        return result

    def get_interface_scale(self):
        interface_scale = 1.0
        with open(utils.getModDir() + '\\..\\..\\..\\..\\..\\..\\preferences.xml', 'r') as prefsFile:
            prefs_data = prefsFile.read()
            interface_scale_str = self.xml_cut(prefs_data, 'interfaceScale').strip()
            if not interface_scale_str:
                ini_file = ini.MyIniFile(utils.getModDir() + '/mxmeter.ini')
                interface_scale_str = ini_file.get('interfaceScale')
            if interface_scale_str:
                try:
                    interface_scale = float(interface_scale_str)
                except ValueError:
                    pass

        return interface_scale


g_mxMeter = MxMeter()
