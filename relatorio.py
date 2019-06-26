import pandas as pd
import requests
import base64
from datetime import datetime

class MelhoresPorCategoria:

    def __init__(self, path_csv):
        self.dados = pd.read_csv(path_csv)
        self.array_dados_music_book = []

    def selecionarPorGenero(self, genero):
        self.genero = [genero]
        self.selecaoDeGeneroNews = self.dados['prime_genre'].isin(self.genero)
        self.itensFiltradosGenero = self.dados[self.selecaoDeGeneroNews]
        return self.itensFiltradosGenero

    def retorna10MelhoresPorAvaliacoes(self, genero):
        grupo_track_name = self.selecionarPorGenero(genero).groupby('track_name')
        dados_filtrados = grupo_track_name[["rating_count_tot"]].max()
        top10 = dados_filtrados.rating_count_tot.sort_values(ascending=False).head(10)
        return top10

    def authorization(self):
        self.token = "897644245607223297-TSowyDAPxcZ1FcSW3hBjyAXLOJkwT9p"
        self.baseurl = 'https://api.twitter.com/'
        self.auth_url = '{}oauth2/token'.format(self.baseurl)
        self.client_key = "Q7Ui7rCiBoCquM8QotxcgwJw5"
        self.client_secret = "i43VmmpPujgyZzPaHgylLkUAN5nhR1XZoS6TEOPPCMwph2aQ58"
        self.key_secret = '{}:{}'.format(self.client_key, self.client_secret).encode('ascii')
        self.b64_encoded_key = base64.b64encode(self.key_secret)
        self.b64_encoded_key = self.b64_encoded_key.decode('ascii')
        self.auth_headers = {
            'Authorization': 'Basic {}'.format(self.b64_encoded_key),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        self.auth_data = {
            'grant_type': 'client_credentials'
        }
        self.auth_resp = requests.post(self.auth_url, headers=self.auth_headers, data=self.auth_data)
        self.access_token = self.auth_resp.json()['access_token']

    def pesquisa(self, nome_pesquisa):
        self.authorization()
        self.search_headers = {
            'Authorization': 'Bearer {}'.format(self.access_token)
        }
        self.search_params = {
            'q': '{}'.format(nome_pesquisa),
            'result_type': 'recent',
            'count': 100,
        }
        self.search_url = '{}1.1/search/tweets.json'.format(self.baseurl)
        self.search_resp = requests.get(self.search_url, headers=self.search_headers, params=self.search_params)
        return self.search_resp.json()['statuses']

    def criar_lista_book(self):
        lista_pesquisa = self.selecionarPorGenero("Book")["track_name"]
        for name_track in lista_pesquisa:
            retweet = 0
            for i in self.pesquisa("{}".format(name_track)):
                retweet = retweet + i['retweet_count']
            dados = {
                "retweet_count": retweet,
                "track_name": "{}".format(name_track)
            }
            self.array_dados_music_book.append(dados)

    def criar_lista_music(self):
        lista_pesquisa = self.selecionarPorGenero("Music")["track_name"]
        for name_track in lista_pesquisa:
            retweet = 0
            for i in self.pesquisa("{}".format(name_track)):
                retweet = retweet + i['retweet_count']
            dados = {
                "retweet_count": retweet,
                "track_name": "{}".format(name_track)
            }
            self.array_dados_music_book.append(dados)

    def unir_listas(self):
        self.criar_lista_music()
        self.criar_lista_book()
        teste = pd.DataFrame(self.array_dados_music_book)
        teste.to_csv("arquivo.csv")

    def retornar_top10_books_music(self):
        dados = pd.read_csv("arquivo.csv")
        dados.drop("Unnamed: 0", axis=1, inplace=True)
        track_names = dados.groupby("track_name")
        dados_filtrados = track_names[["retweet_count"]].max()
        dados_filtrados.retweet_count.sort_values(ascending=False).head(10)
        print(dados_filtrados)

        # return

    # def gerar_csvs_com_tops(self):
    #     # lista_track = []
    #     # for track in self.retornar_top10_books_music():
    #     #     lista_track.append(track)
    #     print(self.retornar_top10_books_music())

    def cria_csvs_temporais(self):
        self.retornar_top10_books_music()

    def series_temporais(self):
        pass


if __name__ == "__main__":
    teste = MelhoresPorCategoria("AppleStore.csv")
    # teste.unir_listas()
    # teste.cria_csvs_temporais()
    # print(teste.retornar_top10_books_music())
    teste.retornar_top10_books_music()