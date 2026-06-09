"""Generate the synthetic seed CSVs under warehouse/seeds/.

All data is synthetic and deterministic: a fixed RNG seed (42) produces the same
CSVs on every run. Re-run after changing any constant; commit the result so
`dbt build` works from a clean clone without running this script.

Usage: uv run python scripts/generate_seed.py
"""

from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

SEED = 42
SEEDS_DIR = Path(__file__).resolve().parent.parent / "warehouse" / "seeds"

N_PRODUCTS = 60
N_CUSTOMERS = 400
N_ORDERS = 4000

ORDER_DATE_START = date(2024, 1, 1)
ORDER_DATE_END = date(2025, 12, 31)
SIGNUP_DATE_START = date(2023, 1, 1)

CATEGORIES = {
    "sensors": (18.0, 95.0),
    "controllers": (55.0, 240.0),
    "harnesses": (8.0, 40.0),
    "actuators": (35.0, 160.0),
    "displays": (60.0, 320.0),
    "fasteners": (1.5, 12.0),
}
REGIONS = ("midwest", "northeast", "south", "west")
SEGMENTS = ("smb", "mid_market", "enterprise")
ORDER_STATUSES = ("completed", "completed", "completed", "completed", "returned", "cancelled")

ADJECTIVES = ("amber", "basalt", "cedar", "delta", "ember", "flint", "granite", "harbor")
NOUNS = ("works", "supply", "industrial", "equipment", "systems", "manufacturing", "tooling", "ag")


@dataclass
class Order:
    order_id: int
    customer_id: int
    order_date: date
    status: str
    promised_ship_date: date


def _margin_price(rng: random.Random, lo: float, hi: float) -> tuple[float, float]:
    cost = round(rng.uniform(lo, hi), 2)
    price = round(cost * rng.uniform(1.25, 1.9), 2)
    return cost, price


def write_csv(name: str, header: list[str], rows: list[list[object]]) -> None:
    path = SEEDS_DIR / name
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"wrote {path.relative_to(Path.cwd())} ({len(rows)} rows)")


def main() -> None:
    rng = random.Random(SEED)
    SEEDS_DIR.mkdir(parents=True, exist_ok=True)

    products: list[list[object]] = []
    for pid in range(1, N_PRODUCTS + 1):
        category = rng.choice(sorted(CATEGORIES))
        lo, hi = CATEGORIES[category]
        cost, price = _margin_price(rng, lo, hi)
        products.append([pid, f"{category[:-1]}-{pid:03d}", category, cost, price])
    write_csv(
        "raw_products.csv",
        ["product_id", "product_name", "category", "unit_cost", "unit_price"],
        products,
    )

    signup_span = (ORDER_DATE_END - SIGNUP_DATE_START).days
    customers: list[list[object]] = []
    for cid in range(1, N_CUSTOMERS + 1):
        name = f"{rng.choice(ADJECTIVES)}-{rng.choice(NOUNS)}-{cid:04d}"
        signup = SIGNUP_DATE_START + timedelta(days=rng.randrange(signup_span))
        customers.append([cid, name, rng.choice(REGIONS), rng.choice(SEGMENTS), signup.isoformat()])
    write_csv(
        "raw_customers.csv",
        ["customer_id", "customer_name", "region", "segment", "signup_date"],
        customers,
    )

    order_span = (ORDER_DATE_END - ORDER_DATE_START).days
    orders: list[Order] = []
    for oid in range(1, N_ORDERS + 1):
        # quadratic weighting toward the recent end of the window: order volume grows over time
        offset = int(order_span * (rng.random() ** 0.5))
        order_date = ORDER_DATE_START + timedelta(days=offset)
        orders.append(
            Order(
                order_id=oid,
                customer_id=rng.randint(1, N_CUSTOMERS),
                order_date=order_date,
                status=rng.choice(ORDER_STATUSES),
                promised_ship_date=order_date + timedelta(days=rng.randint(2, 7)),
            )
        )
    orders.sort(key=lambda o: (o.order_date, o.order_id))
    write_csv(
        "raw_orders.csv",
        ["order_id", "customer_id", "order_date", "status", "promised_ship_date"],
        [
            [
                o.order_id,
                o.customer_id,
                o.order_date.isoformat(),
                o.status,
                o.promised_ship_date.isoformat(),
            ]
            for o in orders
        ],
    )

    items: list[list[object]] = []
    item_id = 0
    for o in orders:
        for _ in range(rng.randint(1, 5)):
            item_id += 1
            pid = rng.randint(1, N_PRODUCTS)
            unit_price = float(products[pid - 1][4])
            discount = rng.choice((0.0, 0.0, 0.0, 0.05, 0.1, 0.15))
            items.append([item_id, o.order_id, pid, rng.randint(1, 10), unit_price, discount])
    write_csv(
        "raw_order_items.csv",
        ["order_item_id", "order_id", "product_id", "quantity", "unit_price", "discount"],
        items,
    )

    shipments: list[list[object]] = []
    sid = 0
    for o in orders:
        if o.status == "cancelled":
            continue
        sid += 1
        shipped = o.order_date + timedelta(days=rng.randint(1, 9))
        shipments.append([sid, o.order_id, shipped.isoformat()])
    write_csv("raw_shipments.csv", ["shipment_id", "order_id", "shipped_date"], shipments)


if __name__ == "__main__":
    main()
