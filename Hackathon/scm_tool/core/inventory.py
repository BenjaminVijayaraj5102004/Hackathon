from collections import deque


class Inventory:
    def __init__(self, product: str, stock: int, reorder_point: int, cost_price: float):
        self.product = product
        self.stock = stock
        self.reorder_point = reorder_point
        self.cost_price = cost_price
        self.pending_orders: deque[tuple[int, int]] = deque()

    def receive(self, qty: int) -> None:
        self.stock += qty

    def sell(self, demand: int) -> tuple[int, int]:
        sold = min(demand, self.stock)
        lost = demand - sold
        self.stock -= sold
        return sold, lost

    def needs_reorder(self) -> bool:
        return self.stock <= self.reorder_point
