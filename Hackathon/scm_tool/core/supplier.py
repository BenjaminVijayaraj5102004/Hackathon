class Supplier:
    def __init__(self, lead_time_days: int = 2):
        self.lead_time = lead_time_days

    def place_order(self, quantity: int, today: int) -> tuple[int, int]:
        delivery_day = today + self.lead_time
        return delivery_day, quantity
