import pandas as pd
import requests
import base64
from datetime import datetime

class MelhoresPorCategoria:

    def __init__(self, path_csv):
        self.dados = pd.read_csv(path_csv)
        self.array_dados_music_book = []
        self.token = ""
        self.baseurl = 'https://api.twitter.com/'
        self.auth_url = '{}oauth2/token'.format(self.baseurl)
        self.client_key = ""
        self.client_secret = ""
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

    def pesquisa(self, nome_pesquisa):
        # self.authorization()
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
        try:
            return self.search_resp.json()['statuses']
        except KeyError:
            return []

    def criar_lista_book(self):
        lista_pesquisa = self.selecionarPorGenero("Book")["track_name"]
        for name_track in lista_pesquisa:
            retweet = 0
            for i in self.pesquisa("{}".format(name_track)):
                print(i)
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
                print(i)
                retweet = retweet + i['retweet_count']
            dados = {
                "retweet_count": retweet,
                "track_name": "{}".format(name_track)
            }
            self.array_dados_music_book.append(dados)

    def unir_listas(self):
        self.criar_lista_music()
        self.criar_lista_book()
        listas = pd.DataFrame(self.array_dados_music_book)
        listas.to_csv("arquivo.csv")

    def retornar_top10_books_music(self):
        dados = pd.read_csv("arquivo.csv")
        data = dados.sort_values(['retweet_count'], ascending=False)
        data.drop("Unnamed: 0", axis=1, inplace=True)
        return data[["track_name", "retweet_count"]]

    def redefinir_dataframe(self):
        lista_selecao = []
        for track_name in self.retornar_top10_books_music().head(10)["track_name"]:
            lista_selecao.append(track_name)
        selecionar_track_names = self.dados["track_name"].isin(lista_selecao)
        csv_selecionado = self.dados[selecionar_track_names]
        csv_selecionado.drop("Unnamed: 0", axis=1, inplace=True)
        csv_selecionado.drop("currency", axis=1, inplace=True)
        csv_selecionado.drop("rating_count_ver", axis=1, inplace=True)
        csv_selecionado.drop("cont_rating", axis=1, inplace=True)
        csv_selecionado.drop("sup_devices.num", axis=1, inplace=True)
        csv_selecionado.drop("ipadSc_urls.num", axis=1, inplace=True)
        csv_selecionado.drop("lang.num", axis=1, inplace=True)
        csv_selecionado.drop("vpp_lic", axis=1, inplace=True)
        csv_selecionado.drop("user_rating_ver", axis=1, inplace=True)
        csv_selecionado.drop("user_rating", axis=1, inplace=True)
        csv_selecionado.drop("ver", axis=1, inplace=True)
        csv_selecionado.drop("rating_count_tot", axis=1, inplace=True)
        return csv_selecionado

    def merge_dataframes(self):
        data_frame_merge = pd.merge(self.retornar_top10_books_music().head(10), self.redefinir_dataframe())
        df_renomeado_colunas = data_frame_merge[["id", "track_name", "retweet_count", "size_bytes", "price", "prime_genre"]]
        rename_data_frame = df_renomeado_colunas.rename(index=str, columns={"retweet_count": "n_citacoes"})
        hoje = datetime.now()
        rename_data_frame.to_csv("{}-{}--{}:{}-top10.csv".format(hoje.day, hoje.month, hoje.hour, hoje.minute))



    def series_temporais(self):
        pass


if __name__ == "__main__":
    teste = MelhoresPorCategoria("AppleStore.csv")
    print("Aguarde ...")
    teste.unir_listas()
    teste.redefinir_dataframe()
    teste.merge_dataframes()
