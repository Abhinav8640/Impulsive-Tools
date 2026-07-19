"""security_tools.py — passwords, random strings/numbers, all pure Python."""
import re
import secrets
import string

from .base import ToolResult

AMBIGUOUS = "Il1O0"


def password_generator(files, fields):
    try:
        length = int(fields.get("length", "16"))
    except ValueError:
        length = 16
    length = max(4, min(length, 128))

    use_upper = fields.get("upper", "on") == "on"
    use_lower = fields.get("lower", "on") == "on"
    use_digits = fields.get("digits", "on") == "on"
    use_symbols = fields.get("symbols", "on") == "on"
    avoid_ambiguous = fields.get("avoid_ambiguous") == "on"

    pool = ""
    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += "!@#$%^&*()-_=+[]{};:,.?"
    if not pool:
        return ToolResult.error("Select at least one character type.")
    if avoid_ambiguous:
        pool = "".join(c for c in pool if c not in AMBIGUOUS)

    password = "".join(secrets.choice(pool) for _ in range(length))
    return ToolResult.text(password, message="Password generated.")


def _strength_report(password):
    checks = {
        "At least 8 characters": len(password) >= 8,
        "At least 12 characters": len(password) >= 12,
        "Contains a lowercase letter": bool(re.search(r"[a-z]", password)),
        "Contains an uppercase letter": bool(re.search(r"[A-Z]", password)),
        "Contains a digit": bool(re.search(r"\d", password)),
        "Contains a symbol": bool(re.search(r"[^\w\s]", password)),
        "No obvious repeated characters (aaa, 111)": not re.search(r"(.)\1\1", password),
    }
    score = sum(1 for v in checks.values() if v)
    if score <= 2:
        label = "Very Weak"
    elif score <= 4:
        label = "Weak"
    elif score <= 5:
        label = "Good"
    elif score == 6:
        label = "Strong"
    else:
        label = "Very Strong"
    lines = [f"Strength: {label} ({score}/7)", ""]
    for k, v in checks.items():
        lines.append(f"{'✔' if v else '✘'} {k}")
    return "\n".join(lines)


def password_strength_checker(files, fields):
    password = fields.get("password", "")
    if not password:
        return ToolResult.error("Enter a password to check.")
    return ToolResult.text(_strength_report(password))


def random_string_generator(files, fields):
    try:
        length = int(fields.get("length", "12"))
    except ValueError:
        length = 12
    length = max(1, min(length, 512))

    charset = fields.get("charset", "alnum")
    pools = {
        "alnum": string.ascii_letters + string.digits,
        "letters": string.ascii_letters,
        "digits": string.digits,
        "hex": string.digits + "abcdef",
        "all": string.ascii_letters + string.digits + "!@#$%^&*()-_=+",
    }
    pool = pools.get(charset, pools["alnum"])
    result = "".join(secrets.choice(pool) for _ in range(length))
    return ToolResult.text(result, message="Random string generated.")


def random_number_generator(files, fields):
    try:
        low = int(fields.get("min", "1"))
        high = int(fields.get("max", "100"))
    except ValueError:
        return ToolResult.error("Min and max must be whole numbers.")
    if low > high:
        low, high = high, low
    n = secrets.randbelow(high - low + 1) + low
    return ToolResult.text(str(n), message="Random number generated.")
