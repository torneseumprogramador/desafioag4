import pyodbc 
import csv
import glob
import datetime

soIn = glob.glob("arquivos_carga_csv/transaction-in-*.csv")
soOut = glob.glob("arquivos_carga_csv/transaction-out-*.csv")
soCliente = glob.glob("arquivos_carga_csv/clients-*.csv")

connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=DESKTOP-PO3SOQV;'
                      'Database=Desafio;'
                      'Trusted_Connection=yes;')
cursor = connection.cursor()

cursor.execute('''
		CREATE TABLE clientes (
			id int primary key,
			nome nvarchar(50),
			email nvarchar(100),
            data_cadastro datetime,
            telefone nvarchar(50),
			)
               ''')

for arq in soCliente: 
    # print(arq)
    ficheiro = open(arq, 'r', encoding="utf8")
    reader = csv.reader(ficheiro)
    for linha in reader:
        if 'id;nome' in linha[0]: continue
        quebralinha=linha[0].split(';')
        date_time_obj = datetime.datetime.strptime(quebralinha[3], '%Y-%m-%d %H:%M:%S %z')
        
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

        
cursor.execute('''
		CREATE TABLE transactionin (
			id int primary key,
            cliente_id int FOREIGN KEY REFERENCES clientes(id), 			
			valor money,
            data datetime,            
			)
               ''')

# Inserindo as linhas dos arquivos transaction in 
count = 0
for arq in soIn: 
    # print(arq)
    ficheiro = open(arq, 'r', encoding="utf8")
    reader = csv.reader(ficheiro)
    for linha in reader:
        if 'id;cliente_id' in linha[0]: continue
        quebralinha=linha[0].split(';')
        date_time_obj = datetime.datetime.strptime(quebralinha[3], '%Y-%m-%d %H:%M:%S %z')
        try:
            cursor.execute('''
                    INSERT INTO transactionin (id, cliente_id, valor, data)
                    VALUES (?,?,?,?)
                    ''',
                   quebralinha[0], 
                   quebralinha[1], 
                   quebralinha[2], 
                   date_time_obj,                    
                    ) 
        except: 
            count+=1
            print(f"Trans-In: Erro ({count}) Não existe cliente com esse ID")       
        
cursor.execute('''
CREATE TABLE transactionout (
    id int primary key,
    cliente_id int FOREIGN KEY REFERENCES clientes(id), 			
    valor money,
    data datetime,            
    )
        ''')        
        # Inserindo as linhas dos arquivos transaction OUT
count = 0
for arq in soOut: 
    # print(arq)
    ficheiro = open(arq, 'r', encoding="utf8")
    reader = csv.reader(ficheiro)
    for linha in reader:
        if 'id;cliente_id' in linha[0]: continue
        quebralinha=linha[0].split(';')
        date_time_obj = datetime.datetime.strptime(quebralinha[3], '%Y-%m-%d %H:%M:%S %z')
        try:
            cursor.execute('''
                    INSERT INTO transactionout (id, cliente_id, valor, data)
                    VALUES (?,?,?,?)
                    ''',
                   quebralinha[0], 
                   quebralinha[1], 
                   quebralinha[2], 
                   date_time_obj                 
                    )
        except: 
            count+=1
            print(f"Trans-Out: Erro ({count}) Não existe cliente com esse ID")                  
connection.commit()

