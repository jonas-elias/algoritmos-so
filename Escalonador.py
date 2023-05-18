import operator
import threading
import pandas as pd
from itertools import groupby
import time

class Processo:

    def __init__(self, id, chegada, tempo_cpu, prioridade):
        self.id = id
        self.chegada = chegada
        self.tempo_cpu = tempo_cpu
        self.prioridade = prioridade

    def get_id(self):
        return self.id

    def decrement(self):
        self.tempo_cpu -= 1

    def get_chegada(self):
        return self.chegada

    def get_tempo_cpu(self):
        return self.tempo_cpu

    def get_prioridade(self):
        return self.prioridade


class FilaAptos:
    listaProcessos = []
    ordemExecucao = []

    def __init__(self):
        pass

    def insere_processo(self, processo):
        self.listaProcessos.append(processo)

    # def mostra_dados_processo(self, posicao):
    #     print(f'Identificação......: {self.listaProcessos[posicao].get_id()}')
    #     print(
    #         f'Chegada............: {self.listaProcessos[posicao].get_chegada()}'
    #     )
    #     print(f'CPU................: {self.listaProcessos[posicao].get_cpu()}')

    # def get_proximo_processo(self):
    #     return self.listaProcessos.pop(0)

    # def mostra_processos_lista(self):
    #     for i in range(len(self.listaProcessos)):
    #         self.mostra_dados_processo(i)

    # def tamanho_lista(self):
    #     return len(self.listaProcessos)

class SJF(threading.Thread):
    tempo = 0
    media = 0.0
    def __init__(self, fila_aptos, preemptivo):
        self.fila = fila_aptos
        self.preemptivo = preemptivo
        threading.Thread.__init__(self)
    
    def escalonar(self):
        if (self.preemptivo):
            processos_pendentes = []
            listaProcessos = self.fila.listaProcessos
            print(listaProcessos[0].get_tempo_cpu())
            while True:
                for i in range(len(listaProcessos)):
                    if (listaProcessos[i].get_chegada() <= self.tempo and listaProcessos[i].get_tempo_cpu() > 0):
                        processos_pendentes.append(listaProcessos[i])
                if processos_pendentes == []:
                    break
                self.tempo += 1
                processo_atual = min(processos_pendentes, key=operator.attrgetter('tempo_cpu'))
                indice = processo_atual.get_id() - 1
                listaProcessos[indice].decrement()
                processos_pendentes = []
            self.media = self.tempo / len(listaProcessos)
            return self.media
        else:
            tempo_aux = []
            processos_pendentes = []
            while True:
                for i in range(len(self.fila.listaProcessos)):
                    if (self.fila.listaProcessos[i].get_chegada() <= self.tempo and self.fila.listaProcessos[i].get_tempo_cpu() > 0):
                        processos_pendentes.append(self.fila.listaProcessos[i])
                if processos_pendentes == []:
                    self.tempo = 0
                    for i in range(len(self.fila.listaProcessos) - 1):
                        self.tempo += tempo_aux[i]
                    break
                processo_atual = min(processos_pendentes, key=operator.attrgetter('tempo_cpu'))
                indice_processo = processo_atual.get_id() - 1
                self.tempo += processo_atual.get_tempo_cpu()
                tempo_aux.append(self.tempo)
                self.fila.listaProcessos[indice_processo].tempo_cpu = 0
                processos_pendentes = []
            self.media = self.tempo / len(self.fila.listaProcessos)
            return self.media

    def run(self):
        print('Algoritmo SJF')
        print(f'Media de espera: {self.escalonar()}')

class Prioridade(threading.Thread):
    tempo = 0
    media = 0.0
    def __init__(self, fila_aptos, preemptivo):
        self.fila = fila_aptos
        self.preemptivo = preemptivo
        threading.Thread.__init__(self)

    def escalonar(self):
        if (self.preemptivo):
            processo_anterior = dict()
            resultante_tarefa = dict()
            processos_pendentes = []
            listaProcessos = self.fila.listaProcessos
            while True:
                for i in range(len(listaProcessos)):
                    if (listaProcessos[i].get_chegada() <= self.tempo and listaProcessos[i].get_tempo_cpu() > 0):
                        processos_pendentes.append(listaProcessos[i])
                if processos_pendentes == []:
                    break
                self.tempo += 1
                processo_atual = min(processos_pendentes, key=operator.attrgetter('prioridade'))
                self.fila.ordemExecucao.append(processo_atual)
                indice = processo_atual.get_id() - 1
                if indice in processo_anterior:
                    processo_anterior[indice] += 1
                else:
                    processo_anterior[indice] = 1
                resultante_tarefa[indice] = self.tempo - processo_anterior[indice] - processo_atual.get_chegada()
                listaProcessos[indice].decrement()
                processos_pendentes = []
            self.tempo = 0
            self.geraArquivoAnalise(self.preemptivo)
            for value in resultante_tarefa.values():
                self.tempo += value
            self.media = self.tempo / len(listaProcessos)
            listaProcessos = []
            return self.media
        else:
            tempo_aux = []
            processos_pendentes = []
            while True:
                for i in range(len(self.fila.listaProcessos)):
                    if (self.fila.listaProcessos[i].get_chegada() <= self.tempo and self.fila.listaProcessos[i].get_tempo_cpu() > 0):
                        processos_pendentes.append(self.fila.listaProcessos[i])
                if processos_pendentes == []:
                    self.tempo = 0
                    for i in range(len(self.fila.listaProcessos) - 1):
                        self.tempo += tempo_aux[i]
                    break
                processo_atual = min(processos_pendentes, key=operator.attrgetter('prioridade'))
                indice_processo = processo_atual.get_id() - 1
                self.tempo += processo_atual.get_tempo_cpu()
                tempo_aux.append(self.tempo)
                self.fila.listaProcessos[indice_processo].tempo_cpu = 0
                processos_pendentes = []
            self.media = self.tempo / len(self.fila.listaProcessos)
            return self.media
    
    def geraArquivoAnalise(self, preemptivo):
        if preemptivo:
            nome_arquivo = "preemptivo_prioridade.txt"
        else:
            nome_arquivo = "nao_preemptivo_prioridade.txt"
        lista = []
        for i in range(len(self.fila.ordemExecucao)):
            lista.append(self.fila.ordemExecucao[i].get_id())
        chaves_valores = [(k, sum(1 for _ in g)) for k, g in groupby(lista)]
        arquivo = open(nome_arquivo, "w")
        texto = chaves_valores
        arquivo.write(str(texto))
        arquivo.close()

    def run(self):
        print('Algoritmo Prioridade')
        print(f'Media de espera: {self.escalonar()}')

class Teste(threading.Thread):
    def __init__(self, fila):
        self.fila = fila
        threading.Thread.__init__(self)
        
    def run(self):
        print(self.fila.listaProcessos[0].get_tempo_cpu())

def main():
    # dataSet = pd.read_csv('./processos.csv')
    # processos = []
    # for row in dataSet.values:
    #     processos.append(Processo(row[0], row[1], row[2], row[3]))

    # fila = FilaAptos()
    # for i in range(len(processos)):
    #     fila.insere_processo(processo=processos[i])

    p1 = Processo(1, 0, 23, 1)
    p2 = Processo(2, 0, 3, 2)
    p3 = Processo(3, 0, 3, 3)

    f_aptos = FilaAptos()
    f_aptos.insere_processo(p1)
    f_aptos.insere_processo(p2)
    f_aptos.insere_processo(p3)
    sjf = SJF(f_aptos, True)
    prioridade = Prioridade(f_aptos, True)

    sjf.start()
    prioridade.start()
    sjf.join()
    prioridade.join()
    # teste.start()
    # teste.join()

main()