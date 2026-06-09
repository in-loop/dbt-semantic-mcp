-- Cancelled orders must not ship.
select o.order_id
from {{ ref('fct_orders') }} o
where o.status = 'cancelled' and o.shipped_date is not null
