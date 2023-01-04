import sqlite3
from datetime import datetime
from fastapi import FastAPI
from freshflow.schemas import Orders, Order

app = FastAPI()

# This factory will be used to convert data from a Sqlite query to a Pydantic Model
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

database = sqlite3.connect('data.db')
database.row_factory = dict_factory
cursor = database.cursor()

orders_query = """
SELECT
    DISTINCT
    orderable_items.item_number,
    ordering_day,
    delivery_day,
    suggested_retail_price AS sales_price_suggestion,
    orderable_items.purchase_price,
    item_categories,
    tags AS labels,
    sales_predictions.sales_quantity
FROM orderable_items
LEFT JOIN inventory
ON orderable_items.item_number = inventory.item_number
AND DATE(inventory.day) = ordering_day
LEFT JOIN order_intake
ON orderable_items.item_number = order_intake.item_number
AND DATE(order_intake.day) = delivery_day
LEFT JOIN sales_predictions
ON orderable_items.item_number = sales_predictions.item_number
AND DATE(sales_predictions.day) = delivery_day;
"""

cursor.execute(orders_query)

query_data = cursor.fetchall()

database.commit()
database.close()

@app.get("/", response_model=Orders)
async def root():

    orders = []

    # With more time, I would make this loop more testable by seperating functions into their own utils file.
    for item in query_data:
        order = Order.parse_obj(item)
        order.profit_margin = order.sales_price_suggestion - order.purchase_price

        # TODO: calculate the case, order and inventory data, ran out of time :(

        orders.append(order)

    # TODO: exclude 'sales_quantity' in response data (this was going to be used to calculate case quantity)
    return Orders(orders=orders)
