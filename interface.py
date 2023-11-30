from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from classes.conector import Conector
from functools import partial
import math
import threading
import pandas as pd
conector = Conector()

class FilterDropDown(DropDown):
    pass

class LanguageDropDown(DropDown):
    pass

class TypeDropDown(DropDown):
    pass

class LimiteDropDown(DropDown):
    pass

class TypeButton(Button):
    pass

class FilterButton(Button):
    pass

class LanguageButton(Button):
    pass

class LimiteButton(Button):
    pass

class Tela(BoxLayout):
    def __init__(self,**kwargs):
        super(Tela, self).__init__(**kwargs)
        self.orientation = "vertical"

        #dropdown do filtro
        botao_filter = FilterButton(text="sort by")
        filter_dropdown = FilterDropDown()
        botao_filter.bind(on_press=filter_dropdown.open)
        self.ids.selecionador.add_widget(botao_filter)
        filter_dropdown.bind(on_select=partial(self.setar_filter,botao_filter))

        #dropdown da linguagem
        botao_language = LanguageButton(text="language")
        language_dropdown = LanguageDropDown()
        botao_language.bind(on_press=language_dropdown.open)
        self.ids.selecionador.add_widget(botao_language)
        language_dropdown.bind(on_select=partial(self.setar_lenguage,botao_language))

        #dropdown do tipo
        botao_type = TypeButton(text="type")
        type_dropdown = TypeDropDown()
        botao_type.bind(on_press=type_dropdown.open)
        self.ids.selecionador.add_widget(botao_type)
        type_dropdown.bind(on_select=partial(self.setar_type,botao_type))

        #dropdown do tipo
        botao_limite = TypeButton(text="threshold")
        limite_dropdown = LimiteDropDown()
        botao_limite.bind(on_press=limite_dropdown.open)
        self.ids.selecionador.add_widget(botao_limite)
        limite_dropdown.bind(on_select=partial(self.setar_threshold,botao_limite))

        #botão de finalizar
        botao_finalizar = Button(text="gerar arquivo xlsx", size_hint=(0.7, 0.5), on_release=self.gerar)
        self.ids.finalizador.add_widget(botao_finalizar)

    def gerar(self,nome):
        conector.set_app_id(self.ids.codigo_jogo.text)
        print("codigo="+str(conector.get_app_id())+" , language="+conector.get_language()+" , filter="+conector.get_filter()+" , type="+conector.get_comment_type())
        comentarios = conector.extrair_comentarios()
        print(comentarios)
        comentarios_df = pd.DataFrame(comentarios)
        with pd.ExcelWriter(str(self.ids.codigo_jogo.text)+ ".xlsx") as writer:
            comentarios_df.to_excel(writer)

    def setar_lenguage(self, *args, **kwargs):
        args[0].text = args[2]
        conector.set_language(args[2])
    
    def setar_type(self, *args, **kwargs):
        args[0].text = args[2]
        conector.set_comment_type(args[2])

    def setar_filter(self,*args, **kwargs):
        args[0].text = args[2]
        conector.set_filter(args[2])
    
    def setar_threshold(self,*args, **kwargs):
        args[0].text = args[2]
        conector.set_limite(int(args[2]))

        


class Interface(App):
    def build(self):
        return Tela()

Interface().run()