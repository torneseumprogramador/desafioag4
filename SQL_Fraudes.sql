SELECT sdiff.cliente_id
  , sdiff.valor
  , sdiff.data
  , sdiff.transOut_id
  , sdiff.minute_diff
FROM (
	  select cliente_id, valor, data, id as transOut_id,
	datediff(MINUTE, lag(data,1) over (partition by cliente_id order by data asc), data) as 'minute_diff'
	from transactionout
) sdiff
WHERE sdiff.minute_diff<2
order by cliente_id

