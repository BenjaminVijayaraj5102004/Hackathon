from collections import deque
from .supplier import Supplier
from .inventory import Inventory
from .forecast import ForecastModel


class SupplyChainEngine:
    """
    Pure logic engine — no print statements, no plots, no input().
    All methods return plain Python dicts consumed by tool wrappers.
    """

    def __init__(
        self,
        product: str,
        initial_stock: int,
        reorder_point: int,
        cost_price: float,
        selling_price: float,
        lead_time_days: int,
        forecast_window: int,
    ):
        self.day = 1
        self.selling_price = selling_price
        self.total_profit = 0.0

        self.supplier = Supplier(lead_time_days=lead_time_days)
        self.inventory = Inventory(product, initial_stock, reorder_point, cost_price)
        self.forecast = ForecastModel(window=forecast_window)

        # History log
        self.log: list[dict] = []
        self.total_sales = 0
        self.total_lost = 0

    # ── Core Operations ──────────────────────────────────────────

    def process_day(self, demand: int) -> dict:
        opening_stock = self.inventory.stock
        deliveries_received = []

        # Receive pending deliveries due today
        while (self.inventory.pending_orders and
               self.inventory.pending_orders[0][0] == self.day):
            _, qty = self.inventory.pending_orders.popleft()
            self.inventory.receive(qty)
            deliveries_received.append(qty)

        sold, lost = self.inventory.sell(demand)

        revenue = sold * self.selling_price
        cost = sold * self.inventory.cost_price
        profit = revenue - cost
        self.total_profit += profit
        self.total_sales += sold
        self.total_lost += lost

        self.forecast.update(demand)
        predicted = self.forecast.predict()

        reorder_placed = False
        reorder_qty = None
        delivery_day = None

        if self.inventory.needs_reorder():
            reorder_qty = max(predicted * 2, 20)
            delivery_day, qty = self.supplier.place_order(reorder_qty, self.day)
            self.inventory.pending_orders.append((delivery_day, qty))
            reorder_placed = True

        result = {
            "day": self.day,
            "opening_stock": opening_stock,
            "demand": demand,
            "sold": sold,
            "lost_sales": lost,
            "closing_stock": self.inventory.stock,
            "revenue": revenue,
            "cost": cost,
            "profit": profit,
            "total_profit": self.total_profit,
            "predicted_next_demand": predicted,
            "reorder_placed": reorder_placed,
            "reorder_quantity": reorder_qty,
            "delivery_expected_day": delivery_day,
            "deliveries_received": deliveries_received,
        }

        self.log.append(result)
        self.day += 1
        return result

    def skip_holiday(self) -> dict:
        result = {
            "day": self.day,
            "message": "Holiday — store closed, day skipped",
        }
        self.day += 1
        return result

    def get_status(self) -> dict:
        return {
            "day": self.day,
            "product": self.inventory.product,
            "current_stock": self.inventory.stock,
            "reorder_point": self.inventory.reorder_point,
            "cost_price": self.inventory.cost_price,
            "selling_price": self.selling_price,
            "lead_time_days": self.supplier.lead_time,
            "total_profit": self.total_profit,
            "pending_orders": [
                {"delivery_day": d, "quantity": q}
                for d, q in self.inventory.pending_orders
            ],
            "forecast_history": self.forecast.history,
            "predicted_next_demand": self.forecast.predict(),
        }

    def get_summary(self) -> dict:
        return {
            "total_days_operated": len(self.log),
            "total_profit": self.total_profit,
            "total_sales": self.total_sales,
            "total_lost_sales": self.total_lost,
            "days": self.log,
        }
