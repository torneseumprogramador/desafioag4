
import csv
import glob

soIn = glob.glob("arquivos_carga_csv/transaction-in-*.csv")
soOut = glob.glob("arquivos_carga_csv/transaction-out-*.csv")
soCliente = glob.glob("arquivos_carga_csv/clients-*.csv")
count =0
for arq in soIn:    
    # print(arq)
    ficheiro = open(arq, 'r', encoding="utf8")  
    reader = csv.reader(ficheiro)
    for linha in reader:
        count += 1
        print (count)

count2 = 0        
for arq in soOut:
    # print(arq)
    ficheiro = open(arq, 'r', encoding="utf8")
    reader = csv.reader(ficheiro)
    for linha in reader:
        count2 += 1
        print ( count2)

count3 = 0        
for arq in soCliente:
    # print(arq)
    ficheiro = open(arq, 'r', encoding="utf8")
    reader = csv.reader(ficheiro)
    for linha in reader:
        count3 += 1
        print ( count3)     
           
total=count+count2+count3 

print(total)

