"""qr_tools.py — QR code + barcode generation and scanning."""
import io

import barcode
from barcode.writer import ImageWriter
import qrcode
from PIL import Image
# from pyzbar.pyzbar import decode as zbar_decode

from .base import ToolResult, first_uploaded_file, save_output


# --------------------------------------------------------------------- QR --
def _make_qr(data):
    qr = qrcode.QRCode(border=2, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0A0D13", back_color="white").convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def qr_generic(files, fields):
    text = fields.get("text", "").strip()
    if not text:
        return ToolResult.error("Enter the text or link to encode.")
    return save_output(_make_qr(text), "qr-code.png", "image/png", message="QR code generated.")


def qr_wifi(files, fields):
    ssid = fields.get("ssid", "").strip()
    password = fields.get("password", "").strip()
    security = fields.get("security", "WPA")
    hidden = "true" if fields.get("hidden") == "on" else "false"
    if not ssid:
        return ToolResult.error("Enter a Wi-Fi network name (SSID).")
    payload = f"WIFI:T:{security};S:{ssid};P:{password};H:{hidden};;"
    return save_output(_make_qr(payload), "wifi-qr.png", "image/png", message="Scan to join Wi-Fi.")


def qr_contact(files, fields):
    name = fields.get("name", "").strip()
    phone = fields.get("phone", "").strip()
    email = fields.get("email", "").strip()
    org = fields.get("org", "").strip()
    if not name:
        return ToolResult.error("Enter a contact name.")
    payload = (
        "BEGIN:VCARD\nVERSION:3.0\n"
        f"N:{name}\nFN:{name}\n"
        + (f"ORG:{org}\n" if org else "")
        + (f"TEL:{phone}\n" if phone else "")
        + (f"EMAIL:{email}\n" if email else "")
        + "END:VCARD"
    )
    return save_output(_make_qr(payload), "contact-qr.png", "image/png", message="Scan to save contact.")


def qr_email(files, fields):
    to = fields.get("to", "").strip()
    subject = fields.get("subject", "").strip()
    body = fields.get("body", "").strip()
    if not to:
        return ToolResult.error("Enter a recipient email address.")
    payload = f"mailto:{to}?subject={subject}&body={body}"
    return save_output(_make_qr(payload), "email-qr.png", "image/png", message="Scan to compose email.")


def qr_sms(files, fields):
    number = fields.get("number", "").strip()
    message = fields.get("message", "").strip()
    if not number:
        return ToolResult.error("Enter a phone number.")
    payload = f"SMSTO:{number}:{message}"
    return save_output(_make_qr(payload), "sms-qr.png", "image/png", message="Scan to send text.")


def qr_whatsapp(files, fields):
    number = fields.get("number", "").strip()
    message = fields.get("message", "").strip()
    if not number:
        return ToolResult.error("Enter a WhatsApp number with country code.")
    digits = "".join(c for c in number if c.isdigit())
    payload = f"https://wa.me/{digits}"
    if message:
        payload += f"?text={message}"
    return save_output(_make_qr(payload), "whatsapp-qr.png", "image/png", message="Scan to open WhatsApp chat.")


def qr_phone(files, fields):
    number = fields.get("number", "").strip()
    if not number:
        return ToolResult.error("Enter a phone number.")
    return save_output(_make_qr(f"tel:{number}"), "phone-qr.png", "image/png", message="Scan to call.")


def qr_url(files, fields):
    url = fields.get("url", "").strip()
    if not url:
        return ToolResult.error("Enter a URL.")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return save_output(_make_qr(url), "url-qr.png", "image/png", message="Scan to open link.")


def qr_gmaps(files, fields):
    place = fields.get("place", "").strip()
    lat = fields.get("lat", "").strip()
    lng = fields.get("lng", "").strip()
    if lat and lng:
        payload = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
    elif place:
        payload = f"https://www.google.com/maps/search/?api=1&query={place}"
    else:
        return ToolResult.error("Enter a place name, or both latitude and longitude.")
    return save_output(_make_qr(payload), "gmaps-qr.png", "image/png", message="Scan to open in Maps.")


def qr_event(files, fields):
    title = fields.get("title", "").strip()
    start = fields.get("start", "").strip()  # YYYYMMDDTHHMMSS
    end = fields.get("end", "").strip()
    location = fields.get("location", "").strip()
    if not title or not start or not end:
        return ToolResult.error("Enter a title, start time and end time.")
    payload = (
        "BEGIN:VEVENT\n"
        f"SUMMARY:{title}\n"
        f"DTSTART:{start}\nDTEND:{end}\n"
        + (f"LOCATION:{location}\n" if location else "")
        + "END:VEVENT"
    )
    return save_output(_make_qr(payload), "event-qr.png", "image/png", message="Scan to add to calendar.")


def qr_reader(files, fields):
    try:
        from pyzbar.pyzbar import decode
    except ImportError:
        return ToolResult.error(
            "QR Scanner is unavailable because the ZBar library is not installed on this server."
        )

    f = first_uploaded_file(files)
    if not f:
        return ToolResult.error("Upload a QR code image.")

    try:
        img = Image.open(f)
        results = decode(img)
    except Exception as exc:
        return ToolResult.error(f"Could not read the image: {exc}")

    if not results:
        return ToolResult.error("No QR code was found in that image.")

    decoded = "\n".join(
        r.data.decode("utf-8", errors="replace") for r in results
    )

    return ToolResult.text(decoded, message="QR code decoded.")


# ---------------------------------------------------------------- Barcode --
def _make_barcode(kind, value):
    writer = ImageWriter()
    writer.set_options({"write_text": True, "quiet_zone": 4})
    bc_class = barcode.get_barcode_class(kind)
    bc = bc_class(value, writer=writer)
    buf = io.BytesIO()
    bc.write(buf)
    return buf.getvalue()


def barcode_generic(files, fields):
    text = fields.get("text", "").strip()
    if not text:
        return ToolResult.error("Enter the text/number to encode.")
    try:
        data = _make_barcode("code128", text)
    except Exception as exc:
        return ToolResult.error(f"Could not generate that barcode: {exc}")
    return save_output(data, "barcode.png", "image/png", message="Barcode generated.")


def barcode_isbn(files, fields):
    isbn = fields.get("isbn", "").strip().replace("-", "").replace(" ", "")
    if not isbn:
        return ToolResult.error("Enter an ISBN (10 or 13 digits).")
    try:
        data = _make_barcode("isbn13" if len(isbn) >= 13 else "isbn10", isbn)
    except Exception as exc:
        return ToolResult.error(f"Could not generate that ISBN barcode: {exc}")
    return save_output(data, "isbn-barcode.png", "image/png", message="ISBN barcode generated.")


def barcode_upc_ean(files, fields):
    code = fields.get("code", "").strip().replace(" ", "")
    kind = fields.get("kind", "ean13")
    if not code:
        return ToolResult.error("Enter a UPC/EAN number.")
    try:
        data = _make_barcode(kind, code)
    except Exception as exc:
        return ToolResult.error(f"Could not generate that barcode: {exc}")
    return save_output(data, f"{kind}-barcode.png", "image/png", message="Barcode generated.")


def barcode_scanner(files, fields):
    try:
        from pyzbar.pyzbar import decode
    except ImportError:
        return ToolResult.error(
            "Barcode Scanner is unavailable because the ZBar library is not installed on this server."
        )

    f = first_uploaded_file(files)
    if not f:
        return ToolResult.error("Upload a barcode image.")

    try:
        img = Image.open(f)
        results = decode(img)
    except Exception as exc:
        return ToolResult.error(f"Could not read the image: {exc}")

    if not results:
        return ToolResult.error("No barcode was found in that image.")

    lines = [
        f"{r.type}: {r.data.decode('utf-8', errors='replace')}"
        for r in results
    ]

    return ToolResult.text("\n".join(lines), message="Barcode decoded.")
