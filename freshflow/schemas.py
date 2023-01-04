from datetime import date
from pydantic import BaseModel
from typing import List, Optional


class Details(BaseModel):
    quantity: float
    unit: str

class Order(BaseModel):
    item_number: int  # uniquely identifies the item
    ordering_day: date  # the day this item can be ordered
    delivery_day: date  # the day this item will be delivered
    sales_price_suggestion: float  # supplier's suggested retail price per unit
    profit_margin: Optional[float]  # profit margin at the sales price suggestion
    purchase_price: float  # supplier official purchase price per unit
    # TODO: covert to list
    item_categories: str  # any of the categories the item is in
    # TODO: covert to list
    labels: str  # a list that can contain any of `new`, `on_sale` and `price_change`, plus all categories extracted from the item name
    # case: Optional[Details]
    order: Optional[Details]
    # inventory: Optional[Details]
    # Internal Data
    sales_quantity: Optional[int]


class Orders(BaseModel):
    orders: List[Order]
