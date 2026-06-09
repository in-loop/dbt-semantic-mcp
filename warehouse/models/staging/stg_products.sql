select
    product_id,
    product_name,
    category,
    unit_cost,
    unit_price
from {{ ref('raw_products') }}
