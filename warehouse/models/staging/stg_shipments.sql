select
    shipment_id,
    order_id,
    shipped_date
from {{ ref('raw_shipments') }}
