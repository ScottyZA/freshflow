import sqlite3
from fastapi import FastAPI
from freshflow.schemas import Orders, Order

app = FastAPI()

database = sqlite3.connect('data.db')

cursor = database.cursor()

orders_query = """
SELECT
    DISTINCT
    orderable_items.item_number,
    ordering_day AS deadline,
    delivery_day AS will_arrive_at
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

    for item in query_data:
        orders.append(Order(item_number=item[0]))

    return Orders(orders=orders)
