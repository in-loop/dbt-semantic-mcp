select
    customer_id,
    customer_name,
    region,
    segment,
    signup_date
from {{ ref('stg_customers') }}
