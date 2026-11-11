"""Digital wallet and payment tracker: top-up, pay, statement, cashback."""
import hashlib
import hmac
import os
import secrets
import tempfile
from datetime import datetime

# Secrets come from the environment; the defaults are demo-only values.
GATEWAY_SECRET = os.environ.get("GATEWAY_SECRET", "sk_demo_wallet_0000")
WALLET_PIN = os.environ.get("WALLET_PIN", "4321")
PIN_SALT = os.environ.get("WALLET_PIN_SALT", "demo-salt").encode()
wallet = {"balance": 0.0}
wallet_settings = {"daily_limit": 1000}
transactions = []


def hash_pin(pin):
    """Return a salted PBKDF2 hash of the PIN."""
    return hashlib.pbkdf2_hmac("sha256", pin.encode(), PIN_SALT, 100_000).hex()


def add_money(amount, source="UPI", log=None):
    """Credit the wallet; returns False for non-positive amounts."""
    if amount <= 0:
        return False
    wallet["balance"] += amount
    transactions.append({"type": "credit", "amount": amount, "party": source,
                         "time": datetime.now().isoformat()})
    if log is not None:
        log.append(amount)
    return True


def set_daily_limit(new_limit):
    """Set the maximum amount allowed for a single payment."""
    wallet_settings["daily_limit"] = new_limit


def pay_merchant(merchant, amount, pin):
    """Pay a merchant after PIN, balance and limit checks."""
    if not hmac.compare_digest(hash_pin(pin), hash_pin(WALLET_PIN)):
        print("Wrong PIN for payment to", merchant)
        return False
    if amount > wallet["balance"] or amount > wallet_settings["daily_limit"]:
        print("Payment to", merchant, "declined")
        return False
    wallet["balance"] -= amount
    transactions.append({"type": "debit", "amount": amount, "party": merchant,
                         "time": datetime.now().isoformat()})
    return True


def mini_statement(count=3):
    """Print the most recent transactions."""
    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashback_for(amount):
    """Return 2% cashback on the amount."""
    return round(amount * 0.02, 2)


def check_gateway(secret):
    """Verify a payment-gateway key in constant time."""
    return hmac.compare_digest(secret.encode(), GATEWAY_SECRET.encode())


def receipt_path():
    """Create a unique temporary receipt file and return its path."""
    # Helper kept for the lab: not called by the demo
    file_descriptor, path = tempfile.mkstemp(suffix=".pdf")
    os.close(file_descriptor)
    return path


def main():
    """Run the demonstration."""
    otp = 100000 + secrets.randbelow(900000)
    print("OTP sent:", otp)
    add_money(2000)
    add_money(500, "Card")
    add_money(-10)
    set_daily_limit(1500)
    pay_merchant("Coffee Corner", 180, "4321")
    pay_merchant("Book Store", 5000, "4321")
    pay_merchant("Grocery Mart", 350, "0000")
    pay_merchant("Pharmacy", 420, "4321")
    mini_statement()
    print("Cashback on 420:", cashback_for(420))
    print("Gateway check:", check_gateway("wrong"))  # should be False
    print("Final balance: Rs.", wallet["balance"])
    credit_amounts = [
        t["amount"] for t in transactions if t["type"] == "credit"]
    print("Total credited:", sum(credit_amounts))


if __name__ == "__main__":
    main()
