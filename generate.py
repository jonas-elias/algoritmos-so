import csv
import random

dados = []
for i in range(1, 5):
    id_processo = str(i)
    tempo_cheg = random.randint(1, 19)
    temp_CPU = random.randint(1, 19)
    priori = random.randint(1, 5)
    while True:
        interrupt = False
        for row in dados:
            while (row[3] == priori):
                interrupt = True
                priori = random.randint(1, 5)
        if interrupt != True:
            break
    dados.append([id_processo, tempo_cheg, temp_CPU, priori])

nome_arquivo = "processos.csv"

cabecalho = ["id_processo", "tempo_cheg", "temp_CPU", "priori"]

# Abre o arquivo CSV para escrita
with open(nome_arquivo, mode='w', newline='') as arquivo_csv:
    writer = csv.writer(arquivo_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Escreve o cabeçalho no arquivo CSV
    writer.writerow(cabecalho)

    # Escreve os dados no arquivo CSV
    writer.writerows(dados)

print("Planilha gerada e salva com sucesso!")