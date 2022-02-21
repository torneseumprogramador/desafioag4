import pyodbc 
import csv
import glob
import datetime

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
        
username = 'sa' 
password = 'erica@123'
connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=localhost, 1433;'
                      'Database=Desafio;'
                      'UID='+username+';'
                      'PWD='+ password+';'
                    #   'Trusted_Connection=yes;'
                      )
cursor = connection.cursor()
query = '''
		CREATE TABLE clientes (
			id int primary key,
			nome nvarchar(50),
			email nvarchar(100),
            data_cadastro datetime,
            telefone nvarchar(50)
			)
               '''
cursor.execute(query)
query2 = '''
        CREATE TABLE transactionin (
			id int primary key,
            cliente_id int FOREIGN KEY REFERENCES clientes(id),
			valor float,
            data datetime
			)    
                '''
cursor.execute(query2)
query3 = '''
        CREATE TABLE transactionout (
			id int primary key,
            cliente_id int FOREIGN KEY REFERENCES clientes(id),
			valor float,
            data datetime
			)
                '''
cursor.execute(query3)

# Inserindo as linhas dos arquivos do cliente na Tabela
for arq in soCliente: 
    # print(arq)
    ficheiro = open(arq, 'r', encoding="utf8")
    reader = csv.reader(ficheiro)
    for linha in reader:
        if 'id;nome' in linha[0]: continue
        quebralinha=linha[0].split(';')
        date_time_obj = datetime.datetime.strptime( quebralinha[3], '%Y-%m-%d %H:%M:%S %z')
        cursor.execute('''
                    INSERT INTO clientes (id, nome, email, data_cadastro, telefone)
                    VALUES (?,?,?,?,?)
                    ''',
                   quebralinha[0], 
                   quebralinha[1], 
                   quebralinha[2], 
                   date_time_obj, 
                   quebralinha[4],
                    )
connection.commit()

