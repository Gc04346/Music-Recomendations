import pandas as pd
import numpy as np
import operator
from copy import deepcopy

genre = pd.read_csv("genre.csv")
music_data = pd.read_csv("music_data.csv")
hits = pd.read_csv("hits.csv")
target = pd.read_csv("target.csv")

# variaveis de controle para melhorar a legibilidade do codigo
music_id = 0
music = 1
music_value = 4
usr_id = 0
usr_musics = 1
topHits = 100  # decidi por utilizar 100 top hits para a recomendação
numUsers = len(hits.groupby(['user_id']).count())-1


musics = [[]for i in range(topHits)]
# modelo do vetor user = [0,[[105301,69],[51,0],...]]
users = [[]for i in range(numUsers)]

# pegando as top 100 musicas, baseado em numero de plays
music_data.sort_values(['plays'], ascending=False, inplace=True)
top_musics = np.array(music_data['music_id'][:topHits])

# fazendo o vetor base de musicas com todos os valores 0
for i in range(len(top_musics)):
    musics[i].append(top_musics[i])
    musics[i].append(0)

linha = 0
for j in range(numUsers):
    users[j] = [hits.iloc[linha, usr_id], musics]  # users[j] = [user_id, vetor base com os top 100 hits]
    if linha < len(hits):  # if usado para garantir que na última iteração não ocorra um index out of bounds
        listaMusicas = deepcopy(musics)  # deepcopy para que apenas os valores de musics sejam transferidos para listaMusicas. Particularidade da linguagem Python.
        while hits.iloc[linha, usr_id] == j:  # hits tem várias linhas de informação para cada usuário. Enquanto eu estiver no mesmo usuário faça:
            musica = hits.iloc[linha, music]
            for i in range(len(top_musics)):
                if users[j][usr_musics][i][music_id] == musica:  # se a musica atual em hits existir no vetor do usuario(tambem vale: se estiver no top 100)
                    listaMusicas[i][music] = hits.iloc[linha][music_value]
            linha += 1
        users[j] = [hits.iloc[linha, usr_id], listaMusicas]  # atribui listaMusicas com os valores atualizados daquele usuário à sua matriz


def distance(user_target, one_user, length):
    dist = 0
    for i in range(length):
        dist += np.square(user_target[1][i][1] - one_user[1][i][1])
    return np.sqrt(dist)

def knearest(all_users, user_target, k):
    distances = {}
    length = len(user_target[1])  # length = quantas musicas tem na matriz do usuario (top_hits)

    for i in range(len(all_users)):
        dist = distance(user_target, all_users[i], length)
        distances[i] = dist

    # sortedDistances tem, de forma ordenada crescente, os usuarios com o gosto mais parecido com o que eu passei.
    # na posicao 0 eu tenho o usuario mais parecido com o que eu passei.
    sortedDistances = sorted(distances.items(), key=operator.itemgetter(1))

    usuariosParecidos = [[]for i in range(k)]

    for i in range(k):
        usuariosParecidos[i] += sortedDistances[i]
    # aqui, em usuariosParecidos, eu tenho o id do usuario mais parecido e a distancia vetorial entre ele e user target

    vetComb = musics

    for i in range(len(usuariosParecidos)):
        usrTemp = users[usuariosParecidos[i][usr_id]]
        for ind in range(len(usrTemp[usr_musics])): # quantidade de musicas que tem no top do usrTemp.
            vetComb[ind][1] += (usrTemp[1][ind][1]/len(top_musics))  # média dos valores, para uma recomendação mais confiável

    recomendacoes = [[]for i in range(len(vetComb))]

    for i in range(len(vetComb)):
        recomendacoes[i].append(vetComb[i][0])  # recomendacoes[i][0] tem o id da musica
        recomendacoes[i].append(vetComb[i][1] - user_target[1][i][1])  # recomendacoes[i][1] tem o valor subtraido do quanto os usuarios parecidos escutaram aquela musica com o quanto o user_target a ouviu

    sortedRecomendacoes = sorted(recomendacoes, key=operator.itemgetter(1), reverse=True)
    finalRecomendations = []

    for i in range(len(sortedRecomendacoes)):
        finalRecomendations.append(sortedRecomendacoes[i][0])

    return finalRecomendations


def getRecommendations(n):
    user_target_id = 0
    kval = 5
    user_target = users[user_target_id]
    recommended = knearest(users, user_target, kval)[:n]

    recommendations = {
        "user_id": user_target[0],
        "recommendations": recommended
    }

    return recommendations

print(getRecommendations(1))