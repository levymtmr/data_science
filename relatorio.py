import pandas as pd
import requests, base64, pprint


class MelhoresPorCategoria:

    def __init__(self, path_csv):
        self.dados = pd.read_csv(path_csv)
        self.dataframe_filtrado = None

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
            'result_type': 'popular',
            'count': 500
        }
        self.search_url = '{}1.1/search/tweets.json'.format(self.baseurl)
        self.search_resp = requests.get(self.search_url, headers=self.search_headers, params=self.search_params)
        return self.search_resp.json()['statuses']

    def retorna_quantidade_por_pesquisa(self, genero, nome_pesquisa):
        # pprint.pprint(self.pesquisa(nome_pesquisa))
        self.list_dados = []
        for track_name in self.selecionarPorGenero(genero)["track_name"]:
            for dado in self.pesquisa(track_name):
                dados = {
                    "track_name": track_name,
                    "user": dado['user']['screen_name'],
                    "retweet_count": dado['retweet_count']+ dado['retweet_count'],
                    "text": dado['text'],
                }
                self.list_dados.append(dados)
        self.dataframe_filtrado = pd.DataFrame(self.list_dados)
        self.dataframe_filtrado.to_csv("teste.csv")
        return self.dataframe_filtrado

    ## criar um dataframe ou arquivo csv

    def retornaBookMaisMencionado(self):
        pass


if __name__ == "__main__":
    teste = MelhoresPorCategoria("AppleStore.csv")
    # print(teste.dados)
    print(teste.retorna_quantidade_por_pesquisa("Book", "pandora"))
    # teste.retornaQuantidadeMencionada("Music", "pandora")
    # print(teste.selecionarPorGenero("Music"))
    # print(teste.retorna10MelhoresPorAvaliacoes("Music"))
#     teste.retornaSoMusic()
#     print(teste.authorization())

#     for i in teste.pesquisa():
#         print(i['text'])
