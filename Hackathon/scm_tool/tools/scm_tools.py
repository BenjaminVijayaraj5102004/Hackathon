import csv
import io
from typing import Union

from ..core.engine import SupplyChainEngine
from ..schemas.models import (
    EmptyInput,
    InitStoreInput,
    ProcessDayInput,
    DayResult,
    HolidayResult,
    StoreStatus,
    SummaryReport,
    ToolError,
)

# ── Singleton engine instance (reset via init_store) ─────────────
_engine: SupplyChainEngine | None = None


def _get_engine() -> SupplyChainEngine | None:
    return _engine


# ─────────────────────────────────────────────────────────────────
# Tool 1: init_store
# ─────────────────────────────────────────────────────────────────
def init_store(params: InitStoreInput) -> Union[StoreStatus, ToolError]:
    """
    Initialize (or reset) the supply chain store with given config.
    Must be called before any other tool.
    """
    global _engine
    try:
        _engine = SupplyChainEngine(
            product=params.product,
            initial_stock=params.initial_stock,
            reorder_point=params.reorder_point,
            cost_price=params.cost_price,
            selling_price=params.selling_price,
            lead_time_days=params.lead_time_days,
            forecast_window=params.forecast_window,
        )
        return StoreStatus(**_engine.get_status())
    except Exception as e:
        return ToolError(error=str(e))


# ─────────────────────────────────────────────────────────────────
# Tool 2: process_day
# ─────────────────────────────────────────────────────────────────
def process_day(params: ProcessDayInput) -> Union[DayResult, ToolError]:
    """
    Run one business day with the given customer demand.
    Handles deliveries, sales, forecasting, and auto-reorder.
    """
    global _engine
    if _engine is None:
        return ToolError(error="Store not initialised. Call init_store() first.")
    try:
        result = _engine.process_day(params.demand)
        return DayResult(**result)
    except Exception as e:
        return ToolError(error=str(e))
    

# ─────────────────────────────────────────────────────────────────
# Tool 3: holiday
# ─────────────────────────────────────────────────────────────────
def skip_holiday(params: EmptyInput = None) -> Union[HolidayResult, ToolError]: #
    """
    Mark the current day as a holiday and advance to the next day.
    """
    global _engine
    if _engine is None:
        return ToolError(error="Store not initialised. Call init_store() first.") #
    try:
        result = _engine.skip_holiday() #
        return HolidayResult(**result) #
    except Exception as e:
        return ToolError(error=str(e)) #
# ─────────────────────────────────────────────────────────────────
# Tool 4: status
# ─────────────────────────────────────────────────────────────────
def get_status(params: EmptyInput = None) -> Union[StoreStatus, ToolError]: #
    """
    Return the current live state of the store.
    """
    global _engine
    if _engine is None:
        return ToolError(error="Store not initialised. Call init_store() first.") #
    try:
        return StoreStatus(**_engine.get_status()) #
    except Exception as e:
        return ToolError(error=str(e)) #

# ─────────────────────────────────────────────────────────────────
# Tool 5: summary
# ─────────────────────────────────────────────────────────────────
def get_summary(params: EmptyInput = None) -> Union[SummaryReport, ToolError]: #
    """
    Return a full summary report of all days operated so far.
    """
    global _engine
    if _engine is None:
        return ToolError(error="Store not initialised. Call init_store() first.") #
    try:
        return SummaryReport(**_engine.get_summary()) #
    except Exception as e:
        return ToolError(error=str(e)) #

# ─────────────────────────────────────────────────────────────────
# Tool 6: export_csv
# ─────────────────────────────────────────────────────────────────
def export_csv(filepath: str = "scm_report.csv") -> Union[dict, ToolError]:
    """
    Export the full day-by-day log to a CSV file.
    Returns the filepath and row count on success.
    """
    global _engine
    if _engine is None:
        return ToolError(error="Store not initialised. Call init_store() first.")
    try:
        log = _engine.log
        if not log:
            return ToolError(error="No data to export yet. Process at least one day.")

        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Day", "Sales", "Lost Sales", "Profit", "Inventory"])
            for row in log:
                writer.writerow([
                    row["day"],
                    row["sold"],
                    row["lost_sales"],
                    row["profit"],
                    row["closing_stock"],
                ])

        return {"success": True, "filepath": filepath, "rows_written": len(log)}
    except Exception as e:
        return ToolError(error=str(e))
#────────────────────────────────────────────────────────────────
# Tool 7 : expiry detector
#_________________________________________________________________
