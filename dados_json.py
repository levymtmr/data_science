import pandas as pd
import pprint

dados1 = pd.read_csv("series_csvs/26-6--23:56-top10.csv")
dados1.drop("Unnamed: 0", axis=1, inplace=True)
pprint.pprint(dados1.to_json())
dados2 = pd.read_csv("series_csvs/26-6--23:59-top10.csv")
dados2.drop("Unnamed: 0", axis=1, inplace=True)
pprint.pprint(dados2.to_json())
dados3 = pd.read_csv("series_csvs/27-6--0:21-top10.csv")
dados3.drop("Unnamed: 0", axis=1, inplace=True)
pprint.pprint(dados3.to_json())
dados4 = pd.read_csv("series_csvs/27-6--0:29-top10.csv")
dados4.drop("Unnamed: 0", axis=1, inplace=True)
pprint.pprint(dados4.to_json())
dados5 = pd.read_csv("series_csvs/27-6--0:34-top10.csv")
dados5.drop("Unnamed: 0", axis=1, inplace=True)
pprint.pprint(dados5.to_json())