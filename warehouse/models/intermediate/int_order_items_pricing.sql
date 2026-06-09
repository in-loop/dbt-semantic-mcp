-- Line-level pricing: revenue, cost, and margin per order item.
select
    i.order_item_id,
    i.order_id,
    i.product_id,
    o.customer_id,
    o.order_date,
    o.status as order_status,
    i.quantity,
    i.unit_price,
    i.discount,
    round(i.quantity * i.unit_price * (1 - i.discount), 2) as line_revenue,
    round(i.quantity * p.unit_cost, 2) as line_cost
from {{ ref('stg_order_items') }} i
join {{ ref('stg_orders') }} o using (order_id)
join {{ ref('stg_products') }} p using (product_id)
