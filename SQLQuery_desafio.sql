USE Desafio

-- Teste: Marca a diferença em minutos em relação transação anterior
-- Deu certo, mas nao consegui aplicar o filtro WHERE minute_diff<=3
select cliente_id,valor,data,
datediff(MINUTE, lag(data,1) over (partition by cliente_id order by data asc), data) as 'minute_diff'
from transactionout

-- Como nao consegui aplicar filtro criei uma nova tabela que apresenta os dados do cliente (necessário para 
-- comunicação após encontrar a fraude) e a coluna minute_diff
CREATE TABLE rastreio(
	cliente_id int FOREIGN KEY REFERENCES clientes(id),
	nome varchar(50),
	email varchar(100),
	telefone varchar(50),
	transOut_id int FOREIGN KEY REFERENCES transactionout(id),
	valor money,
	data datetime,
	minute_diff int
	)

select * from rastreio

-- inserindo os dados na tabela
INSERT INTO rastreio (
	Cliente_ID, nome, email, telefone, 
	transOut_id, valor, data, minute_diff)
SELECT
	tout.cliente_id, c.Nome,  c.Email, c.Telefone,
	tout.id as transOut_id, tout.valor, tout.data, 
	datediff(MINUTE, lag(data,1) over (partition by cliente_id order by data asc), data) as minute_diff
from transactionout tout
inner join clientes C ON c.id = tout.cliente_id

-- Agora consigo identificar, foram 15 clientes fraudados
select * from rastreio
where minute_diff<=3

--  parei aqui, tentando fazer um grouo by por cliente somando o total fraudado, mas nenhum desses 2 selects funcionou
SELECT r.cliente_id, r.nome, r.email, r.telefone, 
	sum(r.valor) as Valor_Total_Fraudado 
from rastreio r
where minute_diff<=3
group by r.nome 

SELECT c.id, c.nome, c.email, c.telefone, 
	   sum(r.valor) as Valor_Total_Fraudado  
from clientes c
inner join rastreio r on r.Cliente_ID = c.id
group by c.id
having minute_diff<=3
