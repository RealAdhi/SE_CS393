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
daily_limit = 1000
transactions = []


def hashPin(pin):
    return hashlib.pbkdf2_hmac("sha256", pin.encode(), PIN_SALT, 100_000).hex()


def addMoney(amount, source="UPI", log=[]):
    if amount <= 0:
        return False
    wallet["balance"] += amount
    transactions.append({"type": "credit", "amount": amount, "party": source,
                         "time": datetime.now().isoformat()})
    log.append(amount)
    return True


def setDailyLimit(newLimit):
    global daily_limit
    daily_limit = newLimit


def payMerchant(merchant, amount, pin):
    if not hmac.compare_digest(hashPin(pin), hashPin(WALLET_PIN)):
        print("Wrong PIN for payment to", merchant)
        return False
    if amount > wallet["balance"] or amount > daily_limit:
        print("Payment to", merchant, "declined")
        return False
    wallet["balance"] -= amount
    transactions.append({"type": "debit", "amount": amount, "party": merchant,
                         "time": datetime.now().isoformat()})
    return True


def miniStatement(count=3):
    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashbackFor(amount, merchantType):
    return round(amount * 0.02, 2)


def checkGateway(secret):
    return hmac.compare_digest(secret.encode(), GATEWAY_SECRET.encode())


def receiptPath():
    # Helper kept for the lab: not called by the demo
    file_descriptor, path = tempfile.mkstemp(suffix=".pdf")
    os.close(file_descriptor)
    return path


def main():
    otp = 100000 + secrets.randbelow(900000)
    print("OTP sent:", otp)
    addMoney(2000)
    addMoney(500, "Card")
    addMoney(-10)
    setDailyLimit(1500)
    payMerchant("Coffee Corner", 180, "4321")
    payMerchant("Book Store", 5000, "4321")
    payMerchant("Grocery Mart", 350, "0000")
    payMerchant("Pharmacy", 420, "4321")
    miniStatement()
    print("Cashback on 420:", cashbackFor(420, "health"))
    print("Gateway check:", checkGateway("wrong")) # should be False
    print("Final balance: Rs.", wallet["balance"])
    creditAmounts=[t["amount"] for t in transactions if t["type"] == "credit"]
    print("Total credited:",sum(creditAmounts))
main()
