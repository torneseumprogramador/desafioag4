SELECT sdiff.cliente_id
  , sdiff.valor
  , sdiff.data
  , sdiff.transOut_id
  , sdiff.second_diff
FROM (
	  select cliente_id, valor, data, id as transOut_id,
	datediff(SECOND, lag(data,1) over (partition by cliente_id order by data asc), data) as 'second_diff'
	from transactionout
) sdiff
WHERE sdiff.second_diff<120
order by cliente_id

