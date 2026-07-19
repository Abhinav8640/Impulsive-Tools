"""
pdf_tools.py
============
Server-side PDF processing. All functions share one signature:

    handler(files, fields) -> ToolResult

`files`  is a QueryDict-like mapping of uploaded files (request.FILES)
`fields` is a dict of plain form fields (request.POST)

They return a ToolResult (see tools/tool_logic/base.py) describing either
a downloadable file or an error message to show the user.
"""
import io
import zipfile

from pypdf import PdfReader, PdfWriter
from PIL import Image
import fitz  # PyMuPDF

from .base import ToolResult, first_uploaded_file, save_output


def merge_pdf(files, fields):
    uploads = files.getlist("file")
    if len(uploads) < 2:
        return ToolResult.error("Upload at least two PDF files to merge.")
    writer = PdfWriter()
    try:
        for f in uploads:
            reader = PdfReader(f)
            for page in reader.pages:
                writer.add_page(page)
    except Exception as exc:
        return ToolResult.error(f"Could not read one of the PDFs: {exc}")

    buf = io.BytesIO()
    writer.write(buf)
    return save_output(buf.getvalue(), "merged.pdf", "application/pdf")


def split_pdf(files, fields):
    f = first_uploaded_file(files)
    if not f:
        return ToolResult.error("Upload a PDF to split.")
    start = fields.get("start_page", "").strip()
    end = fields.get("end_page", "").strip()
    try:
        reader = PdfReader(f)
        total = len(reader.pages)
        start_i = max(1, int(start)) if start else 1
        end_i = min(total, int(end)) if end else total
        if start_i > end_i:
            return ToolResult.error("Start page must be before end page.")
        writer = PdfWriter()
        for i in range(start_i - 1, end_i):
            writer.add_page(reader.pages[i])
    except ValueError:
        return ToolResult.error("Page numbers must be whole numbers.")
    except Exception as exc:
        return ToolResult.error(f"Could not read the PDF: {exc}")

    buf = io.BytesIO()
    writer.write(buf)
    return save_output(buf.getvalue(), f"split_p{start_i}-{end_i}.pdf", "application/pdf")


def compress_pdf(files, fields):
    f = first_uploaded_file(files)
    if not f:
        return ToolResult.error("Upload a PDF to compress.")
    try:
        reader = PdfReader(f)
        writer = PdfWriter()
        for page in reader.pages:
            page.compress_content_streams()  # lossless stream compression
            writer.add_page(page)
        writer.add_metadata(reader.metadata or {})
        writer.compress_identical_objects()
    except Exception as exc:
        return ToolResult.error(f"Could not compress the PDF: {exc}")

    buf = io.BytesIO()
    writer.write(buf)
    return save_output(buf.getvalue(), "compressed.pdf", "application/pdf")


def rotate_pdf(files, fields):
    f = first_uploaded_file(files)
    if not f:
        return ToolResult.error("Upload a PDF to rotate.")
    try:
        angle = int(fields.get("angle", "90"))
    except ValueError:
        angle = 90
    if angle not in (90, 180, 270):
        angle = 90
    try:
        reader = PdfReader(f)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page.rotate(angle))
    except Exception as exc:
        return ToolResult.error(f"Could not rotate the PDF: {exc}")

    buf = io.BytesIO()
    writer.write(buf)
    return save_output(buf.getvalue(), f"rotated_{angle}.pdf", "application/pdf")


def protect_pdf(files, fields):
    f = first_uploaded_file(files)
    password = fields.get("password", "").strip()
    if not f:
        return ToolResult.error("Upload a PDF to protect.")
    if not password:
        return ToolResult.error("Enter a password to lock the PDF with.")
    try:
        reader = PdfReader(f)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(password)
    except Exception as exc:
        return ToolResult.error(f"Could not protect the PDF: {exc}")

    buf = io.BytesIO()
    writer.write(buf)
    return save_output(buf.getvalue(), "protected.pdf", "application/pdf")


def unlock_pdf(files, fields):
    f = first_uploaded_file(files)
    password = fields.get("password", "").strip()
    if not f:
        return ToolResult.error("Upload a PDF to unlock.")
    try:
        reader = PdfReader(f)
        if reader.is_encrypted:
            ok = reader.decrypt(password)
            if not ok:
                return ToolResult.error("That password did not unlock the PDF.")
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
    except Exception as exc:
        return ToolResult.error(f"Could not unlock the PDF: {exc}")

    buf = io.BytesIO()
    writer.write(buf)
    return save_output(buf.getvalue(), "unlocked.pdf", "application/pdf")


def pdf_to_jpg(files, fields):
    f = first_uploaded_file(files)
    if not f:
        return ToolResult.error("Upload a PDF to convert.")
    try:
        data = f.read()
        doc = fitz.open(stream=data, filetype="pdf")
        if len(doc) == 0:
            return ToolResult.error("The PDF has no pages.")
        if len(doc) == 1:
            pix = doc[0].get_pixmap(dpi=150)
            return save_output(pix.tobytes("jpg"), "page-1.jpg", "image/jpeg")
        # multiple pages -> zip of JPGs
        zbuf = io.BytesIO()
        with zipfile.ZipFile(zbuf, "w", zipfile.ZIP_DEFLATED) as zf:
            for i, page in enumerate(doc, start=1):
                pix = page.get_pixmap(dpi=150)
                zf.writestr(f"page-{i}.jpg", pix.tobytes("jpg"))
        return save_output(zbuf.getvalue(), "pages.zip", "application/zip")
    except Exception as exc:
        return ToolResult.error(f"Could not convert the PDF: {exc}")


def jpg_to_pdf(files, fields):
    uploads = files.getlist("file")
    if not uploads:
        return ToolResult.error("Upload one or more images to convert.")
    try:
        images = []
        for f in uploads:
            img = Image.open(f).convert("RGB")
            images.append(img)
        buf = io.BytesIO()
        images[0].save(buf, format="PDF", save_all=True, append_images=images[1:])
    except Exception as exc:
        return ToolResult.error(f"Could not read one of the images: {exc}")
    return save_output(buf.getvalue(), "images.pdf", "application/pdf")
