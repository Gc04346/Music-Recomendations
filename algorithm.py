import pandas as pd
import numpy as np
import math as mth
import operator
from copy import deepcopy

# users = pd.read_csv("users_musics.csv")
# print(users)
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
            vetComb[ind][1] += (usrTemp[1][ind][1]/len(top_musics))  # média dos valores, para uma recomendação mais confiável

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
    # recommendations = []
    # alvos = np.array(target['user_id'])
    # targets = [[] for i in range(len(alvos))]
    # linha = 637515
    # print(hits.iloc[linha, usr_id])
    # for j in range(len(alvos)):
    #     targets[j] = [alvos[j], musics]
    #     if linha < len(hits):
    #         listaMusicas = deepcopy(musics)
    #         while hits.iloc[linha, usr_id] == targets[j][usr_id]:
    #             musica = hits.iloc[linha, music]
    #             for i in range(len(top_musics)):
    #                 print("musica no target: " + str(targets[j][usr_musics][i][music_id]))
    #                 print(musica)
    #                 if targets[j][usr_musics][i][music_id] == musica:
    #                     listaMusicas[i][music] = hits.iloc[linha][music_value]
    #                     # print(listaMusicas)
    #             linha += 1
    #         targets[j][1] = [listaMusicas]
    #         # print("target "+str(j)+":  ==>  "+str(targets[j]))
    # print(targets)
    # user_target = [1, [[4649906, 7], [4331583, 0], [4699022, 9], [4863364, 8], [4921936, 50], [5191668, 60], [4567008, 2], [4599565, 4], [5313837, 0], [5080551, 0], [3879587, 0], [4608738, 0], [5028362, 0], [4870797, 0], [4365419, 0], [5320937, 0], [5045760, 0], [4251249, 0], [4767285, 0], [3879591, 0], [3598892, 0], [5070006, 0], [5194102, 0], [4673544, 0], [4086688, 0], [3109269, 0], [4174842, 0], [4499041, 0], [4255462, 0], [4027166, 0], [5329029, 0], [4427567, 0], [3598889, 0], [5124978, 0], [5038927, 0], [5323370, 0], [5215254, 0], [5201812, 0], [5345937, 0], [3598886, 0], [5079289, 0], [3217646, 0], [4663922, 0], [5290238, 0], [4599566, 0], [2599391, 0], [2725886, 0], [3485867, 0], [4139633, 0], [5227064, 0], [4483944, 0], [3123744, 0], [3107897, 0], [4392830, 0], [5208492, 0], [4599559, 0], [4599563, 0], [4358071, 0], [3123735, 0], [5104871, 0], [3598883, 0], [5406631, 0], [2047611, 0], [4599560, 0], [4442318, 0], [4874079, 0], [3731183, 0], [2486181, 0], [5341333, 0], [5104666, 0], [4779702, 0], [5045756, 0], [4852089, 0], [4481483, 0], [4608007, 0], [4988690, 0], [4328906, 0], [3847300, 0], [4493454, 0], [5159051, 0], [4874077, 0], [4510947, 0], [5194105, 0], [5195280, 0], [2486186, 0], [5088211, 0], [5375875, 0], [3912400, 0], [4462465, 0], [3598885, 0], [4992457, 0], [4220034, 0], [4810361, 0], [5194104, 0], [4998381, 0], [3021833, 0], [5072188, 0], [2248342, 0], [2003691, 0], [4621271, 0]]]
    recommendations = {}
    for i in range(100):
        user_target = users[i]
        recommended = knearest(users, user_target, 1)[:n]
        recommendations[user_target[0]] = deepcopy(recommended)

    return recommendations

print(getRecommendations(1))
