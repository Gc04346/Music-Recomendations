import pandas as pd
import numpy as np
import operator
from copy import deepcopy

# users = pd.read_csv("users_musics.csv")
# print(users)
music_data = pd.read_csv("music_data.csv")
hits = pd.read_csv("hits.csv")

# variaveis de controle para melhorar a legibilidade do codigo
music_id = 0
music = 1
music_value = 4
usr_id = 0
usr_musics = 1

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


def distance(user_target, one_user, length):
    dist = 0
    for i in range(length):
        dist += np.square(user_target[1][i][1] - one_user[1][i][1])
    return np.sqrt(dist)


def knearest(all_users, user_target, k):
    distances = {}
    length = len(user_target[1])

    for i in range(len(all_users)):
        dist = distance(user_target, all_users[i], length)
        distances[i] = dist

    # sortedDistances tem, de forma ordenada crescente, os usuarios com o gosto mais parecido com o que eu passei. na posicao 0
    # eu tenho o usuario mais parecido com o que eu passei.
    sortedDistances = sorted(distances.items(), key=operator.itemgetter(1))

    '''
    vetor combinado = musics
    for cada usuario dentro de k em sortedDistances
        pega o user correspondente no vetor users
            for cada musica que esse cara escutou
                soma o valor dessa musica na posicao dela no vetor combinado
    #vetor combinado = [[music_id1,music_value1],[music_id2,music_value2],[music_id3,music_value3]...]
    # recomendacoes = vetor combinado - user_target => como faz isso? com um for:
    recomendacoes = [[]for i in range(vetComb)]
    for i in range(len(vetor combinado))   
        recomendacoes[i].append(vetComb[i][0])
        #a linha abaixo significa: vetComb.music_value[1] - user.music_value[1]...
        recomendacoes[i].append(vetor combinado[i][1] - user_target[1][i][1])
    # agora tem que ordenar o vetor recomendacoes em ordem decrescente pelas valores das musicas
    # porque se o usr_target escutou uma musica 0 tempo e os parecidos com ele escutaram 10000000 tempo,
    # essa recomendacao tem que tar la no topo.
    retorna recomendacoes
    #na funcao get_recomendations, eu fatio o vetor recomendacoes no numero n de recomendacoes que passar como parametro         
    '''
    usuariosParecidos = [[]for i in range(k)]

    for i in range(k):
        usuariosParecidos[i] += sortedDistances[i]
    # aqui, em usuariosParecidos, eu tenho o id do usuario mais parecido e a distancia vetorial entre ele e user target

    vetComb = musics

    for i in range(len(usuariosParecidos)):
        usrTemp = users[usuariosParecidos[i][usr_id]]
        for ind in range(len(usrTemp[usr_musics])): # quantidade de musicas que tem no top do usrTemp. seria melhor usar isso ou len(top_musics)?
            vetComb[ind][1] += usrTemp[1][ind][1]

    recomendacoes = [[]for i in range(len(vetComb))]

    for i in range(len(vetComb)):  # nao seria melhor so pegar as musicas que o user_target ainda nao ouviu?
        recomendacoes[i].append(vetComb[i][0])  # recomendacoes[i][0] tem o id da musica
        recomendacoes[i].append(vetComb[i][1] - user_target[1][i][1])  # recomendacoes[i][1] tem o valor subtraido do quanto os usuarios parecidos escutaram aquela musica com o quanto o user_target a ouviu

    sortedRecomendacoes = sorted(recomendacoes, key=operator.itemgetter(1), reverse=True)
    finalRecomendations = []

    for i in range(len(sortedRecomendacoes)):
        finalRecomendations.append(sortedRecomendacoes[i][0])

    return finalRecomendations


def getRecommendations(n):
    recommended = knearest(users, users[0], 1)[:n]
    recommendations = {
        "user_id": users[0][0],
        "recommendations": recommended
    }
    return recommendations

print(getRecommendations(5))
