"""Thermostat helpers, hardened against invalid input (Lab 7 fuzzing fixes).

Each function returns None when the input is missing or malformed instead of
raising, so callers can check the result and re-prompt.
"""
import math


def parse_setpoint(text):
    """Parse '21.5C' / '70F' into Celsius (1 d.p.). Returns None if invalid."""
    if not isinstance(text, str):
        return None
    text = text.strip()
    if len(text) < 2:
        return None
    unit = text[-1].upper()
    if unit not in ("C", "F"):
        return None
    try:
        value = float(text[:-1])
    except ValueError:
        return None
    if not math.isfinite(value):
        return None
    if unit == "F":
        value = (value - 32) * 5 / 9
    return round(value, 1)


def average_temperature(readings_csv):
    """Average of comma-separated readings. Returns None if invalid/empty."""
    if not isinstance(readings_csv, str):
        return None
    parts = [p.strip() for p in readings_csv.split(",")]
    if not parts or any(p == "" for p in parts):
        return None
    try:
        values = [float(p) for p in parts]
    except ValueError:
        return None
    if not all(math.isfinite(v) for v in values):
        return None
    result = sum(values) / len(values)
    return result if math.isfinite(result) else None


def schedule_slot(time_text):
    """Label an 'HH:MM' time as 'night MM' (before 06:00) or 'day MM'."""
    if not isinstance(time_text, str):
        return None
    parts = time_text.strip().split(":")
    if len(parts) != 2:
        return None
    try:
        hour, minute = int(parts[0]), int(parts[1])
    except ValueError:
        return None
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None
    period = "night" if hour < 6 else "day"
    return f"{period} {minute:02d}"


def main():
    """Interactive demo."""
    print("==== Running parse_setpoint ====")
    result = parse_setpoint(input("Enter a setpoint (e.g. 21.5C or 70F): "))
    print("Setpoint in Celsius:", result if result is not None else "Invalid input")

    print("\n==== Running average_temperature ====")
    result = average_temperature(
        input("Enter sensor readings as CSV (e.g. 20.5,21,22.5): "))
    print("Average Temperature:", result if result is not None else "Invalid input")

    print("\n==== Running schedule_slot ====")
    result = schedule_slot(input("Enter a time as HH:MM (e.g. 07:30): "))
    print("Schedule Slot:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
