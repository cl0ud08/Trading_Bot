from bot.logging_config import setup_logger

logger = setup_logger("validators")

# Valid values Binance Futures accepts
VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


class ValidationError(Exception):
    """Raised when user input fails validation."""
    pass


def validate_symbol(symbol: str) -> str:
    """
    Symbol must be a non-empty uppercase string.
    e.g. BTCUSDT, ETHUSDT
    """
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol cannot be empty")

    symbol = symbol.strip().upper()

    if len(symbol) < 5:
        raise ValidationError(f"Invalid symbol '{symbol}' — must be at least 5 characters (e.g. BTCUSDT)")

    logger.debug(f"Symbol validated: {symbol}")
    return symbol


def validate_side(side: str) -> str:
    """
    Side must be BUY or SELL.
    """
    if not side:
        raise ValidationError("Side cannot be empty")

    side = side.strip().upper()

    if side not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}' — must be BUY or SELL")

    logger.debug(f"Side validated: {side}")
    return side


def validate_order_type(order_type: str) -> str:
    """
    Order type must be MARKET or LIMIT.
    """
    if not order_type:
        raise ValidationError("Order type cannot be empty")

    order_type = order_type.strip().upper()

    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(f"Invalid order type '{order_type}' — must be MARKET or LIMIT")

    logger.debug(f"Order type validated: {order_type}")
    return order_type


def validate_quantity(quantity: str) -> float:
    """
    Quantity must be a positive number.
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid quantity '{quantity}' — must be a number (e.g. 0.01)")

    if qty <= 0:
        raise ValidationError(f"Quantity must be greater than 0, got {qty}")

    logger.debug(f"Quantity validated: {qty}")
    return qty


def validate_price(price: str) -> float:
    """
    Price must be a positive number.
    Only required for LIMIT orders.
    """
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid price '{price}' — must be a number (e.g. 50000.5)")

    if p <= 0:
        raise ValidationError(f"Price must be greater than 0, got {p}")

    logger.debug(f"Price validated: {p}")
    return p


def validate_order_inputs(symbol, side, order_type, quantity, price=None) -> dict:
    """
    Master validator — runs all checks and returns clean validated values.
    Call this once before placing any order.
    """
    logger.debug("Validating order inputs...")

    validated = {
        "symbol":     validate_symbol(symbol),
        "side":       validate_side(side),
        "order_type": validate_order_type(order_type),
        "quantity":   validate_quantity(quantity),
    }

    # Price is only required for LIMIT orders
    if validated["order_type"] == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders")
        validated["price"] = validate_price(price)
    else:
        if price is not None:
            logger.debug("Price ignored for MARKET order")

    logger.info(f"Inputs validated: {validated}")
    return validated