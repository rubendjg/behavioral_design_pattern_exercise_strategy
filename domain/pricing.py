from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class LineItem:
    sku: str
    qty: int
    unit_price: float


class PricingStrategy(ABC):
    # TODO: Define the common interface for all pricing strategies.
    # This should include a method that takes pricing parameters and returns a calculated value.
    @abstractmethod
    def apply(self, subtotal, items):
        pass


class NoDiscount(PricingStrategy):
    # TODO: Implement a strategy that returns the original value without changes
    def apply(self, subtotal, items):
        return(subtotal)



class PercentageDiscount(PricingStrategy):
    def __init__(self, percent: float) -> None:
        # TODO: Store the percentage value and validate it's in the correct range
        if (0 <= percent <= 100):
            self.percent = percent
        else:
            raise IOError('Value is not in the correct range')
    def apply(self, subtotal, items):
        # TODO: Implement the main calculation method that reduces the input by a percentage
        return(subtotal * (100 - self.percent)/100)


class BulkItemDiscount(PricingStrategy):
    """If any single item's quantity >= threshold, apply a per-item discount for that SKU."""
    def __init__(self, sku: str, threshold: int, per_item_off: float) -> None:
        # TODO: Store the parameters needed to identify items and calculate 
        self.sku = sku
        self.threshold = threshold
        self.per_item_off = per_item_off

    def apply(self, subtotal, items):
        # TODO: Implement logic to iterate through items and apply reductions based on quantity thresholds
        for item in items:
            if item.qty >= self.threshold:
                subtotal = subtotal - (item.qty * item.unit_price)
                subtotal = subtotal + (item.qty * (item.unit_price - self.per_item_off))
        
        return subtotal


class CompositeStrategy(PricingStrategy):
    """Compose multiple strategies; apply in order."""
    def __init__(self, strategies: list[PricingStrategy]) -> None:
        # TODO: Store the collection of strategies to be applied sequentially
        self.strategies = strategies

    def apply(self, subtotal, items):
        # TODO: Implement method that applies each strategy in sequence, using the output of one as input to the next
        for strategy in self.strategies:
           subtotal = strategy.apply(subtotal, items)

        return subtotal


def compute_subtotal(items: list[LineItem]) -> float:
    return round(sum(it.unit_price * it.qty for it in items), 2)
