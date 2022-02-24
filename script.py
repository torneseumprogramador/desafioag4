import pyodbc 
import csv
import glob
import datetime

def createTransactionTables(nome):
    cursor.execute(f'''
            CREATE TABLE {nome} (
                id int primary key,
                cliente_id int FOREIGN KEY REFERENCES clientes(id), 			
                valor money,
                data datetime,            
                )
                ''')


def createTables():
    
    cursor.execute('''
		CREATE TABLE clientes (
			id int primary key,
			nome nvarchar(50),
			email nvarchar(100),
            data_cadastro datetime,
            telefone nvarchar(50),
			)
               ''')
    
    createTransactionTables('transactionin')
    createTransactionTables('transactionout')


def inserirClientes(clientearq):
    for arq in clientearq: 
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
    
    
def inserirTransacoes(transacoes, tabela):
    for arq in transacoes: 
        # print(arq)
        ficheiro = open(arq, 'r', encoding="utf8")
        reader = csv.reader(ficheiro)
        for linha in reader:
            if 'id;cliente_id' in linha[0]: continue
            quebralinha=linha[0].split(';')
            date_time_obj = datetime.datetime.strptime(quebralinha[3], '%Y-%m-%d %H:%M:%S %z')
            try:
                cursor.execute(f'''
                        INSERT INTO {tabela} (id, cliente_id, valor, data)
                        VALUES (?,?,?,?)
                        ''',
                    quebralinha[0], 
                    quebralinha[1], 
                    quebralinha[2], 
                    date_time_obj                 
                        )
            except: print(f"Nao existe cliente de ID: {quebralinha[1]}")           

    connection.commit()
     
#### -------------------------------

connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                    'Server=DESKTOP-PO3SOQV;'
                    'Database=Desafio;'
                    'Trusted_Connection=yes;')
cursor = connection.cursor()


def main():
    soIn = glob.glob("arquivos_carga_csv/transaction-in-*.csv")
    soOut = glob.glob("arquivos_carga_csv/transaction-out-*.csv")
    soCliente = glob.glob("arquivos_carga_csv/clients-*.csv") 

    createTables()
    inserirClientes(soCliente)
    inserirTransacoes(soIn, 'transactionin')
    inserirTransacoes(soOut, 'transactionout')

main()