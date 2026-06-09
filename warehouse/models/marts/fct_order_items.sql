-- Order-line fact, completed orders only (the revenue business rule:
-- returned and cancelled orders do not count toward revenue metrics).
select
    order_item_id,
    order_id,
    product_id,
    customer_id,
    order_date,
    quantity,
    unit_price,
    discount,
    line_revenue,
    line_cost,
    round(line_revenue - line_cost, 2) as gross_profit
from {{ ref('int_order_items_pricing') }}
where order_status = 'completed'
