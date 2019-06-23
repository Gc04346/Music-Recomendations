import pandas as pd
import numpy as np
from copy import deepcopy

# variaveis de controle para melhorar a legibilidade do codigo
music_id = 0
music = 1
music_value = 4
usr_id = 0
usr_musics = 1

music_data = pd.read_csv("music_data.csv")
hits = pd.read_csv("hits.csv")

musics = [[]for i in range(100)]
# modelo do vetor usr = [0,[[105301,69],[51,0],...]]
# numUsers = hits.groupby(['user_id']).count()
users = [[]for i in range(1500)]

# pegando as top 100 musicas, baseado em numero de plays
music_data.sort_values(['plays'], ascending=False, inplace=True)
top_musics = np.array(music_data['music_id'][:100])

# fazendo o vetor base de musicas com todos os valores 0
for i in range(len(top_musics)):
    musics[i].append(top_musics[i])
    musics[i].append(0)

linha = 0
for j in range(1500):
    users[j] = [hits.iloc[linha, usr_id], musics]
    if linha < len(hits):
        listaMusicas = deepcopy(musics)
        while hits.iloc[linha, music_id] == j:
            # tenho que achar o music_id daquela linha em musics(dentro de users) e atribuir hits.iloc[linha][4] no lugar do 0
            musica = hits.iloc[linha, music]
            for i in range(len(top_musics)):
                if users[j][usr_musics][i][music_id] == musica:
                    listaMusicas[i][music] = hits.iloc[linha][music_value]
            linha += 1
        users[j] = [hits.iloc[linha, usr_id], listaMusicas]

