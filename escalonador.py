from collections.abc import Callable, Iterable, Mapping
import operator
import threading
from typing import Any
import pandas as pd
from itertools import groupby
import time
import copy


class Processo:

    def __init__(self, id, chegada, tempo_cpu, prioridade):
        self.id = id
        self.chegada = chegada
        self.tempo_cpu = tempo_cpu
        self.prioridade = prioridade

    def get_id(self):
        return self.id

    def get_chegada(self):
        return self.chegada

    def get_tempo_cpu(self):
        return self.tempo_cpu

    def get_prioridade(self):
        return self.prioridade  

class FilaAptos:
    listaProcessos = []

    def __init__(self):
        pass

    def insere_processo(self, processo):
        self.listaProcessos.append(processo)

    def mostra_dados_processo(self, posicao):
        print(f'Identificação......: {self.listaProcessos[posicao].get_id()}')
        print(
            f'Chegada............: {self.listaProcessos[posicao].get_chegada()}'
        )
        print(
            f'CPU................: {self.listaProcessos[posicao].get_tempo_cpu()}'
        )
        print(
            f'Prioridade.........: {self.listaProcessos[posicao].get_prioridade()}'
        )
        print('\n')

    def mostra_processos_lista(self):
        for i in range(len(self.listaProcessos)):
            self.mostra_dados_processo(i)


class FCSFS(threading.Thread):
    tempo = 0
    media = 0.0
    ordemExecucao = []

    def __init__(self, fila_aptos):
        threading.Thread.__init__(self)
        self.fila = fila_aptos

    def escalonar(self):
        tempo_aux = []
        processos_pendentes = []
        listaProcessos = copy.deepcopy(self.fila.listaProcessos)
        while True:
            for i in range(len(listaProcessos)):
                if (listaProcessos[i].get_chegada() <= self.tempo
                        and listaProcessos[i].get_tempo_cpu() > 0):
                    processos_pendentes.append(listaProcessos[i])
            if processos_pendentes == []:
                self.tempo = 0
                for i in range(len(listaProcessos) - 1):
                    self.tempo += tempo_aux[i]
                break
            processo_atual = min(processos_pendentes,
                                 key=operator.attrgetter('chegada'))
            self.ordemExecucao.append(processo_atual)
            indice_processo = processo_atual.get_id() - 1
            self.tempo += processo_atual.get_tempo_cpu()
            tempo_aux.append(self.tempo)
            listaProcessos[indice_processo].tempo_cpu = 0
            processos_pendentes = []
        self.media = self.tempo / len(listaProcessos)
        self.geraArquivoAnalise()
        return self.media

    def geraArquivoAnalise(self):
        processos = []
        nome_arquivo = "./gantt/fcfs.txt"
        for i in range(len(self.ordemExecucao)):
            processos.append(
                (self.ordemExecucao[i].get_id(),
                 self.fila.listaProcessos[self.ordemExecucao[i].get_id() -
                                          1].get_tempo_cpu()))
        texto_arquivo = processos
        arquivo = open(nome_arquivo, "w")
        texto = texto_arquivo
        arquivo.write(str(texto))
        arquivo.close()

    def run(self):
        print('Algoritmo FCFS')
        print(f'Media de espera: {self.escalonar()}')


class SJF(threading.Thread):
    tempo = 0
    media = 0.0
    ordemExecucao = []

    def __init__(self, fila_aptos, preemptivo):
        self.preemptivo = preemptivo
        threading.Thread.__init__(self)
        self.fila = fila_aptos

    def escalonar(self):
        if (self.preemptivo):
            processos_pendentes = []
            listaProcessos = copy.deepcopy(self.fila.listaProcessos)
            while True:
                for i in range(len(listaProcessos)):
                    if (listaProcessos[i].get_chegada() <= self.tempo
                            and listaProcessos[i].get_tempo_cpu() > 0):
                        processos_pendentes.append(listaProcessos[i])
                if processos_pendentes == []:
                    break
                self.tempo += 1
                processo_atual = min(processos_pendentes,
                                     key=operator.attrgetter('tempo_cpu'))
                self.ordemExecucao.append(processo_atual)
                indice = processo_atual.get_id() - 1
                listaProcessos[indice].tempo_cpu -= 1
                processos_pendentes = []
            self.media = self.tempo / len(listaProcessos)
            self.geraArquivoAnalise(self.preemptivo)
            listaProcessos = []
            return self.media
        else:
            tempo_aux = []
            processos_pendentes = []
            listaProcessos = copy.deepcopy(self.fila.listaProcessos)
            while True:
                for i in range(len(listaProcessos)):
                    if (listaProcessos[i].get_chegada() <= self.tempo
                            and listaProcessos[i].get_tempo_cpu() > 0):
                        processos_pendentes.append(listaProcessos[i])
                if processos_pendentes == []:
                    self.tempo = 0
                    for i in range(len(listaProcessos) - 1):
                        self.tempo += tempo_aux[i]
                    break
                processo_atual = min(processos_pendentes,
                                     key=operator.attrgetter('tempo_cpu'))
                self.ordemExecucao.append(processo_atual)
                indice_processo = processo_atual.get_id() - 1
                self.tempo += processo_atual.get_tempo_cpu()
                tempo_aux.append(self.tempo)
                listaProcessos[indice_processo].tempo_cpu = 0
                processos_pendentes = []
            self.media = self.tempo / len(listaProcessos)
            self.geraArquivoAnalise(self.preemptivo)
            return self.media

    def geraArquivoAnalise(self, preemptivo):
        processos = []
        if preemptivo:
            nome_arquivo = "./gantt/preemptivo_sjf.txt"
            for i in range(len(self.ordemExecucao)):
                processos.append(self.ordemExecucao[i].get_id())
                chaves_valores = [(k, sum(1 for _ in g))
                                  for k, g in groupby(processos)]
                texto_arquivo = chaves_valores
        else:
            nome_arquivo = "./gantt/nao_preemptivo_sjf.txt"
            for i in range(len(self.ordemExecucao)):
                processos.append(
                    (self.ordemExecucao[i].get_id(),
                     self.fila.listaProcessos[self.ordemExecucao[i].get_id() -
                                              1].get_tempo_cpu()))
            texto_arquivo = processos
        arquivo = open(nome_arquivo, "w")
        texto = texto_arquivo
        arquivo.write(str(texto))
        arquivo.close()

    def run(self):
        print('Algoritmo SJF')
        print(f'Media de espera: {self.escalonar()}')


class Prioridade(threading.Thread):
    tempo = 0
    media = 0.0
    ordemExecucao = []

    def __init__(self, fila_aptos, preemptivo):
        threading.Thread.__init__(self)
        self.preemptivo = preemptivo
        self.fila = fila_aptos

    def escalonar(self):
        if (self.preemptivo):
            processo_anterior = dict()
            resultante_tarefa = dict()
            processos_pendentes = []
            listaProcessos = copy.deepcopy(self.fila.listaProcessos)
            while True:
                for i in range(len(listaProcessos)):
                    if (listaProcessos[i].get_chegada() <= self.tempo
                            and listaProcessos[i].get_tempo_cpu() > 0):
                        processos_pendentes.append(listaProcessos[i])
                if processos_pendentes == []:
                    break
                self.tempo += 1
                processo_atual = min(processos_pendentes,
                                     key=operator.attrgetter('prioridade'))
                self.ordemExecucao.append(processo_atual)
                indice = processo_atual.get_id() - 1
                if indice in processo_anterior:
                    processo_anterior[indice] += 1
                else:
                    processo_anterior[indice] = 1
                resultante_tarefa[indice] = self.tempo - processo_anterior[
                    indice] - processo_atual.get_chegada()
                listaProcessos[indice].tempo_cpu -= 1
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
            listaProcessos = copy.deepcopy(self.fila.listaProcessos)
            while True:
                for i in range(len(listaProcessos)):
                    if (listaProcessos[i].get_chegada() <= self.tempo
                            and listaProcessos[i].get_tempo_cpu() > 0):
                        processos_pendentes.append(listaProcessos[i])
                if processos_pendentes == []:
                    self.tempo = 0
                    for i in range(len(listaProcessos) - 1):
                        self.tempo += tempo_aux[i]
                    break
                processo_atual = min(processos_pendentes,
                                     key=operator.attrgetter('prioridade'))
                self.ordemExecucao.append(processo_atual)
                indice_processo = processo_atual.get_id() - 1
                self.tempo += processo_atual.get_tempo_cpu()
                tempo_aux.append(self.tempo)
                listaProcessos[indice_processo].tempo_cpu = 0
                processos_pendentes = []
            self.media = self.tempo / len(listaProcessos)
            self.geraArquivoAnalise(self.preemptivo)
            return self.media

    def geraArquivoAnalise(self, preemptivo):
        processos = []
        if preemptivo:
            nome_arquivo = "./gantt/preemptivo_prioridade.txt"
            for i in range(len(self.ordemExecucao)):
                processos.append(self.ordemExecucao[i].get_id())
                chaves_valores = [(k, sum(1 for _ in g))
                                  for k, g in groupby(processos)]
                texto_arquivo = chaves_valores
        else:
            nome_arquivo = "./gantt/nao_preemptivo_prioridade.txt"
            for i in range(len(self.ordemExecucao)):
                processos.append((self.ordemExecucao[i].get_id(),
                                  self.fila.listaProcessos[
                                      self.ordemExecucao[i].get_id() -
                                      1].get_tempo_cpu()))
            texto_arquivo = processos
        arquivo = open(nome_arquivo, "w")
        texto = texto_arquivo
        arquivo.write(str(texto))
        arquivo.close()

    def run(self):
        print('Algoritmo Prioridade')
        print(f'Media de espera: {self.escalonar()}')

def main():
    dataSet = pd.read_csv('./csv/processos.csv')
    processos = []
    for row in dataSet.values:
        processos.append(Processo(row[0], row[1], row[2], row[3]))
    fila = FilaAptos()
    for i in range(len(processos)):
        fila.insere_processo(processo=processos[i])

    fila.mostra_processos_lista()

    execucoes = []
    execucoes.append(FCSFS(fila))
    execucoes.append(SJF(fila, True))
    execucoes.append(Prioridade(fila, True))

    for i in range(len(execucoes)):
        execucoes[i].start()
        execucoes[i].join()

main()