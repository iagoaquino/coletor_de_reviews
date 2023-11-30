
import requests
import threading
import urllib
from datetime import datetime

class Conector:
    def __init__(self):
        self.nome = ""
        self.filter = "all"
        self.comment_type = "all"
        self.app_id = ""
        self.language = "all"
        self.limite = 10
        self.letras = "qazwsxedcrfvtgbyhnujmikolpç"
        self.numeros = "1234567890"
        self.simbolos = ",<.>;:/?~^=+!@#$%¨&*()-_ "
        self.quantidade_total_jogos = 0
        self.quantidade_total_jogos_analisados = 0
        self.jogos = {
            "nome" : [],
            "codigo" : [],
            "tempo_jogado": []
        }
        

    #getters e setters

    def set_nome(self,nome):
        self.nome = nome

    def get_nome(self):
        return self.nome
    
    def set_limite(self,limite):
        self.limite = limite

    def get_nome(self):
        return self.limite
    
    def set_filter(self,filter):
        self.filter = filter
        
    def get_filter(self):
        return self.filter

    def set_comment_type(self,comment_type):
        self.comment_type = comment_type
        
    def get_comment_type(self):
        return self.comment_type

    def set_app_id(self,app_id):
        self.app_id = app_id
        
    def get_app_id(self):
        return self.app_id

    def set_language(self,language):
        self.language = language
    
    def get_language(self):
        return self.language

    def set_quantidade_total_jogos(self,quantidade_total_jogos):
        self.quantidade_total_jogos = quantidade_total_jogos
    
    def get_quantidade_total_jogos(self):
        return self.quantidade_total_jogos
    
    def set_quantidade_total_jogos_analisados(self, quantidade_total_jogos_analisados):
        self.quantidade_total_jogos_analisados = quantidade_total_jogos_analisados

    def get_quantidade_total_jogos_analisados(self):
        return self.quantidade_total_jogos_analisados
    
    def get_alfabeto(self):
        return self.letras + self.letras.upper() + self.simbolos + self.numeros
    
    #funções
    def extrair_comentarios(self):
        comentarios ={
        "autor": [],
        "comentarios": [],
        "tempo_jogado": [],
        "idioma": [],
        "mes": [],
        "dia": [],
        "votos_positivos": [],
        "quantidade_jogos": [],
        "quantidade_analises": [],
        }
        cursor = "*"
        quantidade_coletada_total=0
        while 1:
            dados = requests.get("https://store.steampowered.com/appreviews/"+self.app_id+"?json=1&filter="+self.filter+"&cursor="+str(cursor)+"&language="+self.language+"&review_type="+self.comment_type)
            print("requisitado no link: "+"https://store.steampowered.com/appreviews/"+self.app_id+"?json=1&filter="+self.filter+"&cursor="+str(cursor)+"&review_type="+self.comment_type)
            print(dados)
            dados = dados.json()
            print("quantidade coletada total: " + str(quantidade_coletada_total))
            quantidade_coletada_total = quantidade_coletada_total + int(dados["query_summary"]["num_reviews"])
            print(quantidade_coletada_total)
            if quantidade_coletada_total >= self.limite:
                break
            if dados["query_summary"]["num_reviews"] == 0:
                break
            for comentario in dados['reviews']:
                comentarios["autor"].append(comentario["author"]["steamid"])
                comentarios["tempo_jogado"].append(comentario["author"]["playtime_at_review"])
                comentarios["comentarios"].append(comentario["review"])
                comentarios["idioma"].append(comentario["language"])
                comentarios["mes"].append(datetime.utcfromtimestamp(comentario["timestamp_created"]).strftime("%m"))
                comentarios["dia"].append(datetime.utcfromtimestamp(comentario["timestamp_created"]).strftime("%d"))
                comentarios["votos_positivos"].append(comentario["votes_up"])
                comentarios["quantidade_jogos"].append(comentario["author"]["num_games_owned"])
                comentarios["quantidade_analises"].append(comentario["author"]["num_reviews"])
            cursor = urllib.parse.quote(dados['cursor'])
            
        return comentarios
    



