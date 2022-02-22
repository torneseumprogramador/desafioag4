from os.path import exists

def compilaDados (nome_arq, path, n_arq=1):
    arq_comp = open(f"{nome_arq}.csv","a",encoding='ansi')  
    print(f"========= lendo arquivo {n_arq} ========= ")
    
    f = open(f"{path}{n_arq:03}.csv",encoding='ansi')
    for line in f:
          arq_comp.write(line)
    f.close() 
    arq_comp.close()
    
    if exists(f"{path}{n_arq+1:03}.csv"): 
        print(f"{path}{n_arq+1:03}.csv")
        compilaDados(nome_arq, path,n_arq+1) 
    else:
        return

path = "arquivos_fornecidos/transaction-out-" # <===== INSERIR path dos arquivos a serem compilados sem os numeros
nome_arq = "transaction-out"                  # <=====  NOME desejado para o csv compilado

compilaDados(nome_arq, path)

