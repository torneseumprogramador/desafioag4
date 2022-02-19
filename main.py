from os.path import exists
import time

def lerDados(id = 1, count = 0):
    clientes = open("clientes.csv", "a")
    file1 = open(f'arquivos_carga_csv/clients-00{id}.csv', 'r' ,encoding='utf-8', errors='ignore')
    print(f"======== lendo arquivo clients-00{id}.csv =====")
    time.sleep(2)
    count = 0
    while True:
        count += 1
        line = file1.readline()
        if not line:
            break
        clientes.write(line)
    file1.close()

    if exists(f"arquivos_carga_csv/clients-00{(id + 1)}.csv"):
        lerDados(id+1, count)

lerDados()