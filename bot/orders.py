from bot.client import BinanceClient
from bot.logging_config import setup_logger
from bot.validators import ValidationError, validate_order_inputs

logger = setup_logger("orders")

ORDER_ENDPOINT = "/fapi/v1/order"


def place_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str = None
) -> dict:
    """
    Main function to place a MARKET or LIMIT order.
    Validates inputs → builds params → calls API → prints result.
    """

    # Step 1: Validate all inputs first
    try:
        validated = validate_order_inputs(symbol, side, order_type, quantity, price)
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        print(f"\n❌ Input error: {e}\n")
        return {}

    # Step 2: Build params for Binance API
    params = {
        "symbol":   validated["symbol"],
        "side":     validated["side"],
        "type":     validated["order_type"],
        "quantity": validated["quantity"],
    }

    # LIMIT orders need price + timeInForce
    if validated["order_type"] == "LIMIT":
        params["price"] = validated["price"]
        params["timeInForce"] = "GTC"  # Good Till Cancelled

    # Step 3: Print order summary before sending
    _print_order_summary(params)

    # Step 4: Send to Binance
    logger.info(f"Placing {params['type']} {params['side']} order for {params['symbol']}")

    try:
        client = BinanceClient()
        response = client.post(ORDER_ENDPOINT, params)
    except Exception as e:
        logger.error(f"Failed to place order: {e}")
        print(f"\n❌ Failed to reach Binance: {e}\n")
        return {}

    # Step 5: Handle response
    if "code" in response and response["code"] != 200:
        _print_failure(response)
        return response

    _print_success(response)
    return response


def _print_order_summary(params: dict):
    """Prints a clean summary of what we're about to send."""
    print("\n" + "=" * 45)
    print("         ORDER REQUEST SUMMARY")
    print("=" * 45)
    print(f"  Symbol     : {params['symbol']}")
    print(f"  Side       : {params['side']}")
    print(f"  Type       : {params['type']}")
    print(f"  Quantity   : {params['quantity']}")
    if "price" in params:
        print(f"  Price      : {params['price']}")
    if "timeInForce" in params:
        print(f"  TimeInForce: {params['timeInForce']}")
    print("=" * 45)


def _print_success(response: dict):
    """Prints clean order response details on success."""
    print("\n" + "=" * 45)
    print("         ✅ ORDER PLACED SUCCESSFULLY")
    print("=" * 45)
    print(f"  Order ID     : {response.get('orderId', 'N/A')}")
    print(f"  Symbol       : {response.get('symbol', 'N/A')}")
    print(f"  Status       : {response.get('status', 'N/A')}")
    print(f"  Side         : {response.get('side', 'N/A')}")
    print(f"  Type         : {response.get('type', 'N/A')}")
    print(f"  Quantity     : {response.get('origQty', 'N/A')}")
    print(f"  Executed Qty : {response.get('executedQty', 'N/A')}")
    print(f"  Avg Price    : {response.get('avgPrice', 'N/A')}")
    print("=" * 45 + "\n")
    logger.info(f"Order placed successfully — ID: {response.get('orderId')}, Status: {response.get('status')}")


def _print_failure(response: dict):
    """Prints error details when Binance rejects the order."""
    print("\n" + "=" * 45)
    print("         ❌ ORDER FAILED")
    print("=" * 45)
    print(f"  Error Code : {response.get('code', 'N/A')}")
    print(f"  Message    : {response.get('msg', 'N/A')}")
    print("=" * 45 + "\n")
    logger.error(f"Order rejected by Binance — code: {response.get('code')}, msg: {response.get('msg')}")