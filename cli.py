import argparse
import sys

from bot.orders import place_order


def build_parser() -> argparse.ArgumentParser:
    """Defines all CLI arguments and their rules."""

    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  Market BUY:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

  Limit SELL:
    python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3000
        """
    )

    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading pair (e.g. BTCUSDT, ETHUSDT)"
    )

    parser.add_argument(
        "--side",
        required=True,
        choices=["BUY", "SELL"],
        type=str.upper,
        help="Order side: BUY or SELL"
    )

    parser.add_argument(
        "--type",
        required=True,
        choices=["MARKET", "LIMIT"],
        type=str.upper,
        dest="order_type",
        help="Order type: MARKET or LIMIT"
    )

    parser.add_argument(
        "--quantity",
        required=True,
        help="Order quantity (e.g. 0.001)"
    )

    parser.add_argument(
        "--price",
        required=False,
        default=None,
        help="Limit price — required for LIMIT orders only"
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Extra check: price required for LIMIT
    if args.order_type == "LIMIT" and args.price is None:
        parser.error("--price is required for LIMIT orders")

    place_order(
        symbol=args.symbol,
        side=args.side,
        order_type=args.order_type,
        quantity=args.quantity,
        price=args.price
    )


if __name__ == "__main__":
    main()