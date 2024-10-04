import os
import json
import logging
import datetime
from dateutil.relativedelta import relativedelta

import pwnagotchi
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK

# Variável para ativar/desativar logging
ENABLE_LOGGING = False  # Defina como True para ativar os logs

class Birthday(plugins.Plugin):
    __author__ = 'nullm0ose'
    __version__ = '1.0.'
    __license__ = 'MIT'
    __description__ = 'A plugin that shows the age and birthday of your Pwnagotchi.'

    def __init__(self):
        self.born_at = 0

    def log(self, message):
        """Função para verificar se o log está ativado e exibir as mensagens."""
        if ENABLE_LOGGING:
            logging.info(message)

    def on_loaded(self):
        plugin_dir = os.path.dirname(__file__)
        data_path = os.path.join(plugin_dir, 'brain.json')  # Agora brain.json ficará na mesma pasta do plugin
        self.load_data(data_path)

    def on_ui_setup(self, ui):
        if self.options['show_age']:
            ui.add_element('Age', LabeledValue(color=BLACK, label=' ♥ Idade:    ', value='',
                                               position=(int(self.options['age_x_coord']),
                                                         int(self.options['age_y_coord'])),
                                               label_font=fonts.Bold, text_font=fonts.Medium))
        elif self.options['show_birthday']:
            ui.add_element('Birthday', LabeledValue(color=BLACK, label=' ♥ Born: ', value='',
                                                    position=(int(self.options['age_x_coord']),
                                                              int(self.options['age_y_coord'])),
                                                    label_font=fonts.Bold, text_font=fonts.Medium))

    def on_unload(self, ui):
        if self.options['show_age']:
            with ui._lock:
                ui.remove_element('Age')
        elif self.options['show_birthday']:
            with ui._lock:
                ui.remove_element('Birthday')

    def on_ui_update(self, ui):
        if self.options['show_age']:
            age = self.calculate_age()
            self.log(f"Idade calculada: {age}")  # Usando a função de log
            age_labels = []
            if age[0] == 1:
                age_labels.append(f'{age[0]}A')
            elif age[0] > 1:
                age_labels.append(f'{age[0]} anos')
            if age[1] > 0:
                age_labels.append(f'{age[1]}m')
            if age[2] > 0 or (age[0] == 0 and age[1] == 0):
                age_labels.append(f'{age[2]}d' if age[2] > 0 else 'Começando a explorar!')  # Exibir "Hoje" se tiver menos de 1 dia
            age_string = ' '.join(age_labels)
            self.log(f"Idade a ser mostrada: {age_string}")  # Usando a função de log
            ui.set('Age', age_string)
        elif self.options['show_birthday']:
            born_date = datetime.datetime.fromtimestamp(self.born_at)
            birthday_string = born_date.strftime('%b %d \'%y')
            self.log(f"Aniversário a ser mostrado: {birthday_string}")  # Usando a função de log
            ui.set('Birthday', birthday_string)

    def load_data(self, data_path):
        if os.path.exists(data_path):
            try:
                with open(data_path) as f:
                    data = json.load(f)
                    if 'born_at' in data:
                        self.born_at = data['born_at']
                        self.log(f'Dados carregados: born_at = {self.born_at}')
                    else:
                        self.born_at = datetime.datetime.now().timestamp()
                        self.save_data(data_path)
                        self.log(f'Dados ausentes no arquivo, criando com born_at = {self.born_at}')
            except json.JSONDecodeError as e:
                logging.error(f'Erro ao ler o arquivo JSON: {e}. Recriando o arquivo.')
                self.born_at = datetime.datetime.now().timestamp()
                self.save_data(data_path)
        else:
            self.log(f'O arquivo {data_path} não existe. Criando novo arquivo.')
            self.born_at = datetime.datetime.now().timestamp()
            self.save_data(data_path)

    def save_data(self, data_path):
        data = {
            'born_at': self.born_at
        }
        try:
            with open(data_path, 'w') as f:
                json.dump(data, f)
                self.log(f'Arquivo {data_path} salvo com sucesso.')
        except IOError as e:
            logging.error(f'Erro ao salvar o arquivo JSON: {e}')

    def calculate_age(self):
        born_date = datetime.datetime.fromtimestamp(self.born_at)
        today = datetime.datetime.now()
        age = relativedelta(today, born_date)
        self.log(f"Data de nascimento: {born_date}, Hoje: {today}, Idade: {age.years} anos, {age.months} meses, {age.days} dias")
        return age.years, age.months, age.days
