class ForecastModel:
    def __init__(self, window: int = 3):
        self.window = window
        self.history: list[int] = []

    def update(self, demand: int) -> None:
        self.history.append(demand)

    def predict(self) -> int:
        if not self.history:
            return 0
        data = self.history[-self.window:]
        return int(sum(data) / len(data))
