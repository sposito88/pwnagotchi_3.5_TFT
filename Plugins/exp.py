import logging
import os
import json

import pwnagotchi
import pwnagotchi.agent
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK

# Static Variables
MULTIPLIER_ASSOCIATION = 1
MULTIPLIER_DEAUTH = 2
MULTIPLIER_HANDSHAKE = 3
MULTIPLIER_AI_BEST_REWARD = 5
TAG = "[EXP Plugin]"
FACE_LEVELUP = '(≧◡◡≦)'
BAR_ERROR = "|   error  |"
FILE_SAVE = "exp_stats"
FILE_SAVE_LEGACY = "exp"
JSON_KEY_LEVEL = "level"
JSON_KEY_EXP = "exp"
JSON_KEY_EXP_TOT = "exp_tot"

class EXP(plugins.Plugin):
    __author__ = 'Alan Sposito'  # Seu nome aqui
    __version__ = '1.0.5'
    __license__ = 'GPL3'
    __description__ = 'Get exp every time a handshake get captured.'

    def __init__(self):
        self.percent = 0
        self.calculateInitialXP = False
        self.exp = 0
        self.lv = 1
        self.exp_tot = 0
        self.save_file_mode = self.save_file_modes("json")
        self.save_file = self.get_save_file_name(self.save_file_mode)
        
        # Migra sistema de salvamento legado
        self.migrate_legacy_save()

        # Cria arquivo de salvamento se não existir
        if not os.path.exists(self.save_file):
            self.save(self.save_file, self.save_file_mode)
        else:
            try:
                self.load(self.save_file, self.save_file_mode)
            except:
                # Caso o arquivo JSON esteja corrompido, recalcular XP
                self.calculateInitialXP = True

        # Se for a primeira vez (sem dados anteriores), calcular XP inicial
        if self.lv == 1 and self.exp == 0:
            self.calculateInitialXP = True
        if self.exp_tot == 0:
            self.LogInfo("Calculando Total Exp")
            self.exp_tot = self.calc_actual_sum(self.lv, self.exp)
            self.save(self.save_file, self.save_file_mode)
        
        self.expneeded = self.calc_exp_needed(self.lv)

    def save_file_modes(self, argument):
        return {
            "txt": 0,
            "json": 1
        }.get(argument, 0)

    def save(self, file, save_file_mode):
        if save_file_mode == 0:
            self.save_to_txt_file(file)
        elif save_file_mode == 1:
            self.save_to_json_file(file)

    def save_to_txt_file(self, file):
        with open(file, 'w') as outfile:
            outfile.write(f"{self.exp}\n{self.lv}\n{self.exp_tot}\n")

    def load_from_txt_file(self, file):
        if os.path.exists(file):
            with open(file, 'r+') as outfile:
                lines = outfile.readlines()
                if len(lines) >= 3:
                    self.exp = int(lines[0])
                    self.lv = int(lines[1])
                    self.exp_tot = int(lines[2])

    def save_to_json_file(self, file):
        data = {
            JSON_KEY_LEVEL: self.lv,
            JSON_KEY_EXP: self.exp,
            JSON_KEY_EXP_TOT: self.exp_tot
        }
        with open(file, 'w') as f:
            json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))

    def load_from_json_file(self, file):
        if os.path.exists(file):
            with open(file, 'r') as f:
                data = json.load(f)
                if data:
                    self.lv = data.get(JSON_KEY_LEVEL, self.lv)
                    self.exp = data.get(JSON_KEY_EXP, self.exp)
                    self.exp_tot = data.get(JSON_KEY_EXP_TOT, self.exp_tot)

    def load(self, file, save_file_mode):
        if save_file_mode == 0:
            self.load_from_txt_file(file)
        elif save_file_mode == 1:
            self.load_from_json_file(file)

    def get_save_file_name(self, save_file_mode):
        file = os.path.join(os.path.dirname(os.path.realpath(__file__)), FILE_SAVE)
        return f"{file}.{'txt' if save_file_mode == 0 else 'json'}"

    def migrate_legacy_save(self):
        legacy_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"{FILE_SAVE_LEGACY}.txt")
        if os.path.exists(legacy_file):
            self.load_from_txt_file(legacy_file)
            self.save(self.save_file, self.save_file_mode)
            os.remove(legacy_file)

    def bar_string(self, symbols_count, p):
        if p > 100:
            return BAR_ERROR
        length = symbols_count - 2
        bar_char = '█'  # Bloco cheio para a parte preenchida
        blank_char = '-'  # Hífen para a parte não preenchida
        bar_length = int(round((length / 100) * p))

        res = f"|{bar_char * bar_length}{blank_char * (length - bar_length)}|"
        return res

    def on_ui_setup(self, ui):
        ui.add_element('Lv', LabeledValue(color=BLACK, label='Lv', value=0,
                                          position=(int(self.options["lvl_x_coord"]),
                                                    int(self.options["lvl_y_coord"])),
                                          label_font=fonts.Bold, text_font=fonts.Medium))
        ui.add_element('Exp', LabeledValue(color=BLACK, label='Xp', value=0,
                                           position=(int(self.options["exp_x_coord"]),
                                                     int(self.options["exp_y_coord"])),
                                           label_font=fonts.Bold, text_font=fonts.Medium))

    def on_ui_update(self, ui):
        self.expneeded = self.calc_exp_needed(self.lv)
        self.percent = int((self.exp / self.expneeded) * 100)
        symbols_count = int(self.options["bar_symbols_count"])

        # Melhorando a barra de XP com símbolos mais visíveis
        bar = self.bar_string(symbols_count, self.percent)
        
        # Organizando melhor o texto de nível e XP
        ui.set('Lv', f": {self.lv}")  # Exibe o nível
        ui.set('Exp', f"{bar} {self.exp}/{self.expneeded} exp")  # Barra de XP com a experiência atual

    def calc_exp_needed(self, level):
        return 5 if level == 1 else int((level ** 3) / 2)

    def exp_check(self, agent):
        if self.exp >= self.expneeded:
            self.exp = 1
            self.lv += 1
            self.expneeded = self.calc_exp_needed(self.lv)
            self.display_level_up(agent)

    def display_level_up(self, agent):
        view = agent.view()
        view.set('face', FACE_LEVELUP)
        view.set('status', "Level Up!")
        view.update(force=True)

    def on_association(self, agent, access_point):
        self.exp += MULTIPLIER_ASSOCIATION
        self.exp_tot += MULTIPLIER_ASSOCIATION
        self.exp_check(agent)
        self.save(self.save_file, self.save_file_mode)

    def on_deauthentication(self, agent, access_point, client_station):
        self.exp += MULTIPLIER_DEAUTH
        self.exp_tot += MULTIPLIER_DEAUTH
        self.exp_check(agent)
        self.save(self.save_file, self.save_file_mode)

    def on_handshake(self, agent, filename, access_point, client_station):
        self.exp += MULTIPLIER_HANDSHAKE
        self.exp_tot += MULTIPLIER_HANDSHAKE
        self.exp_check(agent)
        self.save(self.save_file, self.save_file_mode)

    def on_ai_best_reward(self, agent, reward):
        self.exp += MULTIPLIER_AI_BEST_REWARD
        self.exp_tot += MULTIPLIER_AI_BEST_REWARD
        self.exp_check(agent)
        self.save(self.save_file, self.save_file_mode)

    def on_ready(self, agent):
        if self.calculateInitialXP:
            sum = self.calculate_initial_sum(agent)
            self.exp_tot = sum
            self.calc_level_from_sum(sum, agent)
            self.save(self.save_file, self.save_file_mode)

    def calc_actual_sum(self, level, exp):
        sum = exp
        for lvl in range(1, level):
            sum += self.calc_exp_needed(lvl)
        return sum

    def calc_level_from_sum(self, sum, agent):
        level = 1
        while sum > self.calc_exp_needed(level):
            sum -= self.calc_exp_needed(level)
            level += 1
        self.lv = level
        self.exp = sum
        self.expneeded = self.calc_exp_needed(level) - sum
        if level > 1:
            self.display_level_up(agent)

    def calculate_initial_sum(self, agent):
        session_stats_active = "session-stats" in pwnagotchi.plugins.loaded
        sum = 0
        if session_stats_active:
            sum = self.parse_session_stats()
        else:
            sum = self.last_session_points(agent)
        return sum

    def last_session_points(self, agent):
        summary = 0
        summary += agent.LastSession.handshakes * MULTIPLIER_HANDSHAKE
        summary += agent.LastSession.associated * MULTIPLIER_ASSOCIATION
        summary += agent.LastSession.deauthed * MULTIPLIER_DEAUTH
        return summary

    def parse_session_stats(self):
        sum = 0
        dir = pwnagotchi.config['main']['plugins']['session-stats']['save_directory']
        for filename in os.listdir(dir):
            if filename.endswith(".json") and filename.startswith("stats"):
                sum += self.parse_session_stats_file(os.path.join(dir, filename))
        return sum

    def parse_session_stats_file(self, path):
        sum = 0
        with open(path) as json_file:
            data = json.load(json_file)
            for entry in data["data"]:
                deauths = data["data"][entry]["num_deauths"]
                handshakes = data["data"][entry]["num_handshakes"]
                associations = data["data"][entry]["num_associations"]
                sum += deauths * MULTIPLIER_DEAUTH
                sum += handshakes * MULTIPLIER_HANDSHAKE
                sum += associations * MULTIPLIER_ASSOCIATION
        return sum
