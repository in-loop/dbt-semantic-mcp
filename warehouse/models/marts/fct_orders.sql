-- Order-grain fact, all statuses. order_revenue is the gross line total
-- regardless of status; revenue metrics filter to completed orders in
-- fct_order_items.
with line_totals as (
    select
        order_id,
        round(sum(line_revenue), 2) as order_revenue,
        round(sum(line_cost), 2) as order_cost,
        count(*) as item_count
    from {{ ref('int_order_items_pricing') }}
    group by 1
),

first_orders as (
    select
        order_id,
        row_number() over (
            partition by customer_id
            order by order_date, order_id
        ) = 1 as is_first_order
    from {{ ref('stg_orders') }}
    where status != 'cancelled'
)

select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.promised_ship_date,
    s.shipped_date,
    s.shipped_date is not null
        and s.shipped_date <= o.promised_ship_date as is_on_time,
    coalesce(f.is_first_order, false) as is_first_order,
    t.order_revenue,
    t.order_cost,
    t.item_count
from {{ ref('stg_orders') }} o
left join {{ ref('stg_shipments') }} s using (order_id)
left join first_orders f using (order_id)
join line_totals t using (order_id)
