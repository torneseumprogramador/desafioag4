import pyodbc
import pandas as pd

# Importando CSV
data = pd.read_csv (r'clientes.csv',delimiter=';')   
df = pd.DataFrame(data)
print(df)
df= df.sort_values(by='id') 
df['data_cadastro'] = pd.to_datetime(df['data_cadastro']) # convertendo o varchar em datetime

# Coenctando com o SQL Server
driver='{ODBC Driver 17 for SQL Server}'
server = 'localhost, 1433'
database = 'Desafio' 
username = 'sa' 
password = 'erica@123'
connection = pyodbc.connect('Driver='+driver+';' 
                            'Server='+server+';'
                            'Database='+database+';'
                            'UID='+username+';'
                            'PWD='+ password)
cursor = connection.cursor()

# Criando a Tabela
cursor.execute('''
		CREATE TABLE clientes (
			id int primary key,
			nome nvarchar(50),
			email nvarchar(100),
            data_cadastro datetime,
            telefone nvarchar(50),
			)
               ''')

# Inserindo o DataFrame na Tabela
for row in df.itertuples():
    cursor.execute('''
                INSERT INTO clientes (id, nome, email, data_cadastro, telefone)
                VALUES (?,?,?,?,?)
                ''',
                row.id, 
                row.nome,
                row.email,
                row.data_cadastro,
                row.telefone
                )
connection.commit()