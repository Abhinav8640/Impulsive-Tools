"""
base.py
=======
Small shared helpers used by every tool_logic module so handlers stay
short and consistent.
"""
import base64
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ToolResult:
    """The result of running a tool.

    ok=True + file_bytes  -> a downloadable file is offered to the user
    ok=True + text_result -> a plain text / HTML snippet is shown inline
    ok=False + message    -> an error message is shown to the user
    """
    ok: bool
    message: str = ""
    file_bytes: Optional[bytes] = None
    file_name: str = ""
    content_type: str = "application/octet-stream"
    text_result: str = ""
    # base64 data-URI, used for instantly previewing generated images (QR/barcode)
    preview_data_uri: str = ""

    @staticmethod
    def error(message):
        return ToolResult(ok=False, message=message)

    @staticmethod
    def text(text_result, message=""):
        return ToolResult(ok=True, text_result=text_result, message=message)

    @staticmethod
    def file(file_bytes, file_name, content_type, message="", preview_data_uri=""):
        return ToolResult(
            ok=True,
            file_bytes=file_bytes,
            file_name=file_name,
            content_type=content_type,
            message=message,
            preview_data_uri=preview_data_uri,
        )


def save_output(data_bytes, file_name, content_type, message=""):
    """Wrap raw bytes for download. Images also get an inline base64 preview."""
    preview = ""
    if content_type.startswith("image/"):
        b64 = base64.b64encode(data_bytes).decode("ascii")
        preview = f"data:{content_type};base64,{b64}"
    return ToolResult.file(data_bytes, file_name, content_type, message, preview)


def first_uploaded_file(files):
    """Return the first uploaded file under 'file', or None."""
    return files.get("file")


def unique_name(prefix, ext):
    return f"{prefix}-{uuid.uuid4().hex[:10]}.{ext}"
