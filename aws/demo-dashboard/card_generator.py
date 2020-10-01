from jinja2 import Template
import os
from config import Config


class CardGenerator(object):

    def __init__(self, template_directory):
        self.type = []
        self.template = {}
        self.default_card = Config.DEFAULT_CARD_TEMPLATE

        for file in os.listdir(template_directory):
            if file[-5:] == '.html':
                type_name = file[:-5]
                self.type.append(type_name)
                f = open(os.path.join(template_directory, file), 'r')
                self.template[type_name] = f.read()

    def render(self, template_name=None, **kwargs):
        if not template_name:
            template_name = self.default_card

        template = Template(self.template[template_name])
        return template.render(**kwargs)

    def render_list(self, card_list):
        cards_html = ''
        for card in card_list:
            template_name = card.get('source_type', self.default_card)
            cards_html += self.render(template_name, **card) + '\n'
        return cards_html

    def render_card(self, card):
        template_name = card.get('source_type', self.default_card)
        return self.render(template_name, **card)















