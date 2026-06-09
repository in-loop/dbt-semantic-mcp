-- fct_orders.order_revenue must equal the sum of its lines in
-- int_order_items_pricing (all statuses). Returns mismatched orders.
with line_sums as (
    select order_id, round(sum(line_revenue), 2) as line_total
    from {{ ref('int_order_items_pricing') }}
    group by 1
)

select o.order_id, o.order_revenue, l.line_total
from {{ ref('fct_orders') }} o
join line_sums l using (order_id)
where abs(o.order_revenue - l.line_total) > 0.01
