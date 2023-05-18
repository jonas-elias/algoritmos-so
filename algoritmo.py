import threading
import pandas as pd
import operator


def fcfs(lista):
    lista_interna = lista
    lista_interna = lista_interna.sort_values(by=['tempo_cheg'])
    print(lista_interna)
    lista_interna = lista_interna.to_numpy()
    processo = []
    for row in lista_interna:
        processo.append(row)

    qtd = len(processo)
    tempo_cpu = 0
    tempo_chegada = 0
    indice = []
    for i in range(qtd):
        indice = processo.pop(0)
        if tempo_cpu > indice[1]:
            tempo_chegada += tempo_cpu - indice[1]
            tempo_cpu += indice[2] + indice[1]
            continue
        tempo_cpu += indice[2] + indice[1]
    print((tempo_chegada) / qtd)


def main():
    data = pd.read_csv('./processos.csv')

    # fcfs(data)
    sjf(data)

def sjf(lista):
    lista_interna = lista
    lista_interna = lista_interna.sort_values(by=['temp_CPU'])
    print(lista_interna)
    lista_interna = lista_interna.to_numpy()
    processo = []
    for row in lista_interna:
        processo.append(row)
    qtd = len(processo)
    tempo_cpu = 0
    tempo_chegada = 0
    indice = []

    cont = 0
    # indice = processo.pop(0)
    # proximo = processo.pop(0)
    tempo_total = 0
    temp_aux = 0
    lista_ordenada_tempo_chegada = sorted(lista_interna, key=lambda x: (x[1], x[2]))
    # print(lista_ordenada_tempo_chegada)
    # for i in range(qtd):
            
    #     if tempo_total > processo[i][1]:
    #         temp_aux += tempo_total - processo[i][1]
    #         tempo_total += processo[i][2]
    #         print(tempo_total)
    #         # tempo_total += processo[i][2]
    #         continue
    #     tempo_total += processo[i][1] + processo[i][2] 
    #     print(tempo_total)
    # print(temp_aux / qtd)
    
    segundo_exato = 0
    lista_ordenada_aux = lista_ordenada_tempo_chegada
    lista_ordenada_aux = sorted(lista_ordenada_aux, key=lambda x: (x[1], x[2]))
    while lista_ordenada_aux != []:
        lista_ordenada_aux = sorted(lista_ordenada_aux, key=lambda x: (x[1], x[2]))
        print(lista_ordenada_aux)
        block = True
        for i in range(len(lista_ordenada_aux)):
            if (lista_ordenada_aux[i][2] == 0):
                lista_ordenada_aux.pop(i)
                break
            else:
                segundo_exato += 1
                if (block):
                    # lista_ordenada_aux[i][1] += 1
                    lista_ordenada_aux[i][2] -= 1
                block = False
                continue
    print(segundo_exato)
main()


import operator

processos = [
    [0, 0, 8, 0],
    [1, 1, 4, 0],
    [2, 2, 9, 0],
    [3, 3, 5, 0],
]

processos_not_emp = [
    [0, 0, 6, 0],
    [1, 0, 8, 0],
    [2, 0, 7, 0],
    [3, 0, 3, 0],    
]

processos_prioridade = [
    [0, 0, 3, 10],
    [1, 0, 1, 1],
    [2, 0, 4, 2],
    [3, 0, 5, 1],    
    [4, 0, 2, 5],    
]

# processos = sorted(processos, key=lambda x: (x[2]), reverse=False)
processos_tempo_cpu = sorted(processos, key=lambda x: (x[2]), reverse=False)
print(processos_tempo_cpu)

tempo_total = 0
# while True:
#     for i in range(len(processos)):
#         print(processos)

tempo_chegada = [p[1] for p in processos]
tempo_execucao_original = [p[2] for p in processos]
tempo_execucao_restante = tempo_execucao_original.copy()
ordem_execucao = []

tempo_total = 0
while True:
    processos_pendentes = [(i, tempo_chegada[i], tempo_execucao_restante[i]) for i in range(len(processos)) if tempo_execucao_restante[i] > 0 and tempo_chegada[i] <= tempo_total]
    
    # print(processos_pendentes)
    if not processos_pendentes:
        break
    
    processo_atual = min(processos_pendentes, key=lambda x: x[2])
    indice_processo = processo_atual[0]
    tempo_execucao_atual = min(tempo_execucao_original[indice_processo], 1)
    
    ordem_execucao.append(indice_processo)
    tempo_execucao_restante[indice_processo] -= tempo_execucao_atual
    tempo_total += tempo_execucao_atual

# print(tempo_total)

''' SJF PREEMPTIVO '''
total = 0
processos_pend = []
while True:
    for i in range(len(processos)):
        if (processos[i][1] <= total and processos[i][2] > 0):
            processos_pend.append(processos[i])
    if processos_pend == []:
        break
    total += 1
    processo_atual = min(processos_pend, key=lambda x: x[2])
    indice = processo_atual[0]
    processos[indice][2] -= 1
    processos_pend = []

print(total)

total = 0
processos_pend = []

''' SJF NÃO PREEMPTIVO '''
tempo_total = 0
tempo = []
processos_pendentes = []
while True:
    for i in range(len(processos_not_emp)):
        if (processos_not_emp[i][1] <= tempo_total and processos_not_emp[i][2] > 0):
            processos_pendentes.append(processos_not_emp[i])
    if not processos_pendentes:
        tempo_total = 0
        for i in range(len(processos_not_emp) - 1):
            tempo_total += tempo[i]
        break

    processo_atual = min(processos_pendentes, key=lambda x: x[2])
    indice_processo = processo_atual[0]
    tempo_total += processo_atual[2]
    tempo.append(tempo_total)
    processos_not_emp[indice_processo][2] = 0
    processos_pendentes = []

print(tempo_total)



processos_pendentes = []
tempo_total = 0
tempo = []
''' PRIORIDADES NÃO PREEMPTIVO'''
while True:
    for i in range(len(processos_prioridade)):
        if (processos_prioridade[i][1] <= tempo_total and processos_prioridade[i][3] > 0):
            processos_pendentes.append(processos_prioridade[i])
    if not processos_pendentes:
        tempo_total = 0
        for i in range(len(processos_prioridade) - 1):
            tempo_total += tempo[i]
        break

    processo_atual = min(processos_pendentes, key=lambda x: x[2])
    indice_processo = processo_atual[0]
    tempo_total += processo_atual[3]
    tempo.append(tempo_total)
    processos_prioridade[indice_processo][3] = 0
    processos_pendentes = []

print(tempo_total)
