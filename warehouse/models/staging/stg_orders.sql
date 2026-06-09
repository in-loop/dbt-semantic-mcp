select
    order_id,
    customer_id,
    order_date,
    status,
    promised_ship_date
from {{ ref('raw_orders') }}
