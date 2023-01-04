from pydantic import BaseModel
from typing import List


class Order(BaseModel):
    item_number: int  # uniquely identifies the item
    # ordering_day: datetime.date  # the day this item can be ordered
    # delivery_day: datetime.date  # the day this item will be delivered
    # sales_price_suggestion: float  # supplier's suggested retail price per unit
    # profit_margin: float  # profit margin at the sales price suggestion
    # purchase_price: float  # supplier official purchase price per unit
    # item_categories: List[str]  # any of the categories the item is in
    # labels: List[str]  # a list that can contain any of `new`, `on_sale` and `price_change`, plus all categories extracted from the item name
    # case: {
    #   quantity: float  # represents how many items (in `case.unit`) a case contains
    #   unit: str  # the unit of the `case.quantity`
    # },
    # order: {
    #   quantity: int  # represents how many items (in `order.unit`) the user should order given the formula below (look below)
    #   unit: str  # the unit of the `order.quantity` (it's always 'CS')
    # },
    # inventory: {
    #   quantity: float  # the inventory quantity of the item that day
    #   unit: str  # the unit of that quantity
    # }

class Orders(BaseModel):
    orders: List[Order]
