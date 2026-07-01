import hashlib
import hmac
import os
import time
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

from bot.logging_config import setup_logger

load_dotenv()

logger = setup_logger("client")


class BinanceClient:
    """
    Low-level Binance Futures Testnet client.
    Handles authentication, request signing, and raw HTTP calls.
    No order logic here — just clean API communication.
    """

    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        self.base_url = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

        if not self.api_key or not self.api_secret:
            raise ValueError("API key and secret must be set in .env file")

        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        })

        logger.info("BinanceClient initialized (Testnet)")

    def _sign(self, params: dict) -> dict:
        """
        Adds timestamp + HMAC-SHA256 signature to params.
        Binance requires this for all private endpoints.
        """
        # Step 1: Add current timestamp (Binance rejects requests older than 5 seconds)
        params["timestamp"] = int(time.time() * 1000)

        # Step 2: Convert params to query string e.g. "symbol=BTCUSDT&side=BUY&..."
        query_string = urlencode(params)

        # Step 3: Sign it using your secret key
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        # Step 4: Attach signature to params
        params["signature"] = signature
        return params

    def post(self, endpoint: str, params: dict) -> dict:
        """
        Makes a signed POST request to a private Binance endpoint.
        Used for placing orders.
        """
        signed_params = self._sign(params)
        url = f"{self.base_url}{endpoint}"

        logger.debug(f"POST {url} | params: {self._safe_params(signed_params)}")

        try:
            response = self.session.post(url, data=signed_params)
            result = response.json()
            logger.debug(f"Response: {result}")

            if response.status_code != 200:
                logger.error(f"API error {response.status_code}: {result}")

            return result

        except requests.exceptions.ConnectionError:
            logger.error("Network error: could not connect to Binance Testnet")
            raise
        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    def get(self, endpoint: str, params: dict = None) -> dict:
        """
        Makes a signed GET request.
        Used for checking account info, positions etc.
        """
        params = params or {}
        signed_params = self._sign(params)
        url = f"{self.base_url}{endpoint}"

        logger.debug(f"GET {url} | params: {self._safe_params(signed_params)}")

        try:
            response = self.session.get(url, params=signed_params)
            result = response.json()
            logger.debug(f"Response: {result}")
            return result

        except requests.exceptions.ConnectionError:
            logger.error("Network error: could not connect to Binance Testnet")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    def _safe_params(self, params: dict) -> dict:
        """
        Returns params with signature hidden for safe logging.
        Never log the full signature — it's sensitive.
        """
        safe = params.copy()
        if "signature" in safe:
            safe["signature"] = "***"
        return safe
