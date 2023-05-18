import csv
import random

dados = []
for i in range(1, 5):
    id_processo = str(i)
    if i == 1:
        tempo_chegada = 0
        temp_cpu = 0
        while temp_cpu <= 4:
            temp_cpu = random.randint(5, 19)    
    else:
        tempo_chegada = random.randint(0, 4)
        temp_cpu = random.randint(5, 19)
    prioridade = random.randint(1, 5)
    while True:
        interrupt = False
        for row in dados:
            while (row[3] == prioridade):
                interrupt = True
                prioridade = random.randint(1, 5)
        if interrupt != True:
            break
    dados.append([id_processo, tempo_chegada, temp_cpu, prioridade])

nome_arquivo = "processos.csv"

cabecalho = ["id_processo", "tempo_chegada", "tempo_cpu", "prioridade"]

with open(nome_arquivo, mode='w', newline='') as arquivo_csv:
    writer = csv.writer(arquivo_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(cabecalho)
    writer.writerows(dados)

print("Planilha gerada e salva com sucesso!")