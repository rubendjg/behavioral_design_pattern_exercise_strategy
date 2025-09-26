from __future__ import annotations
from domain.pricing import PricingStrategy, NoDiscount, PercentageDiscount, BulkItemDiscount, CompositeStrategy


def choose_strategy(kind: str, **kwargs) -> PricingStrategy:
    # TODO: Implement strategy selection logic based on the 'kind' parameter
    # Should support: "none", "percent", "bulk", "composite"
    # Each strategy type needs different parameters from **kwargs
    # Return the appropriate strategy instance or raise an error for unknown types
    if (kind == "none"):
        return NoDiscount()
    elif(kind == "percent"):
        return PercentageDiscount(kwargs['percent'])
    elif(kind == "bulk"):
        return BulkItemDiscount(kwargs['sku'], kwargs['threshold'], kwargs['per_item_off'])
    elif(kind == "composite"):
        return CompositeStrategy([PercentageDiscount(kwargs['percent']),BulkItemDiscount(kwargs['sku'], kwargs['threshold'], kwargs['per_item_off'])])
    else:
        raise IOError('Parameter not supported')
