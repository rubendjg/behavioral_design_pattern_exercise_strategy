import argparse
import json
from domain.pricing import LineItem, compute_subtotal
from application.bootstrap import choose_strategy


def parse_items(items_json: str) -> list[LineItem]:
    raw = json.loads(items_json)
    items = [LineItem(**obj) for obj in raw]
    return items

def main() -> None:
    parser = argparse.ArgumentParser(description="Pricing CLI (Strategy Pattern)")
    parser.add_argument("--items", type=str, required=True,
                        help='JSON list of items: [{"sku":"A","qty":2,"unit_price":10.0}, ...]')
    parser.add_argument("--strategy", type=str, default="none",
                        choices=["none", "percent", "bulk", "composite"],
                        help="Strategy kind")
    parser.add_argument("--percent", type=float, default=0.0, help="Percent discount for 'percent' or 'composite'")
    parser.add_argument("--sku", type=str, default="", help="SKU for bulk/composite")
    parser.add_argument("--threshold", type=int, default=0, help="Qty threshold for bulk/composite")
    parser.add_argument("--per-item-off", type=float, default=0.0, dest="per_item_off",
                        help="Per item discount for bulk/composite")
    args = parser.parse_args()

    items = parse_items(args.items)
    subtotal = compute_subtotal(items)
    values = vars(args)
    

    # TODO: Get the appropriate strategy using choose_strategy function
    strategy = choose_strategy(values['strategy'], **values)
    # TODO: Apply the strategy to calculate the final total
    final_price = strategy.apply(subtotal, items)
    # TODO: Display the results (subtotal, strategy used, and final total)
    print(f"Subtotal: {subtotal:.2f}")
    print(f"Strategy: {values['strategy']}")
    print(f"Total: {final_price:.2f}")
    # TODO: Calculate and print the final total
    return final_price


if __name__ == "__main__":
    main()
