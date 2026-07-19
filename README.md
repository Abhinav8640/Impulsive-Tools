# Impulsive Tools

A dark, modern, multi-tool utility website built with Django, HTML5, CSS3 and
vanilla JS — PDF tools, student calculators, social media generators,
security utilities, resume checkers, and QR/barcode tools, all served from
one reusable template.

Developed by **Abhinav Tripathi**.

## Quick start

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

**System dependency:** a couple of tools (QR/barcode scanning) use `pyzbar`,
which needs the `libzbar0` system library.
- Ubuntu/Debian: `sudo apt-get install libzbar0`
- macOS: `brew install zbar`
- Windows: pyzbar ships the DLL it needs, no extra step required.

## Project structure

```
impulsive_tool/          Django project settings & root URLconf
tools/                    The single Django app powering the whole site
  tools_data.py            Catalog: every category, tool, and form field spec
  views.py                 Home / category / tool / static-page views
  context_processors.py    Injects branding + nav categories into every template
  tool_logic/               Server-side processing for each "live" tool
    base.py                  Shared ToolResult helper
    pdf_tools.py              Merge/Split/Compress/Rotate/Protect/Unlock/PDF<->JPG
    qr_tools.py                QR + barcode generation and scanning
    security_tools.py          Password/random string/random number
    text_tools.py               Social media generators + thumbnail downloader
    resume_tools.py              ATS checker + resume score (heuristic, no AI call)
  templates/tools/
    base.html                 Navbar, footer, back-to-top — shared shell
    home.html, category.html, tool.html, about.html, contact.html, ...
    client_widgets/            Pure-JS tools (GPA calc, Pomodoro timer, etc.)
    partials/result.html        Swapped in via AJAX after a tool runs
  static/tools/
    css/  style.css navbar.css footer.css cards.css tool.css responsive.css
    js/   main.js navbar.js search.js upload.js pdf.js
```

## How the "one template, many tools" system works

Every tool page renders from **`tools/tool.html`**. Which form fields it shows
comes from `FIELDS_BY_SLUG` in `tools_data.py`; which Python function
processes the submission comes from the tool's `handler` path. To add a new
tool:

1. Add an entry to `TOOLS` in `tools_data.py` (slug, name, category, icon,
   kind, handler, status).
2. If it takes input, add a matching field list to `FIELDS_BY_SLUG`.
3. Write the processing function in the right `tool_logic/*.py` file. It
   takes `(files, fields)` and returns a `ToolResult` (see `tool_logic/base.py`).
4. That's it — no new template, no new URL route needed.

Client-side-only tools (calculators, timers, counters) skip steps 2–3 and
instead get a small HTML/JS file in `templates/tools/client_widgets/<slug>.html`.

## What's fully working vs. "Coming Soon"

Most tools (PDF merge/split/compress/rotate/protect/unlock, PDF↔JPG,
QR/barcode generation & scanning, all calculators, password/random
generators, social media text generators, resume ATS checker/score) work
end-to-end with real processing.

A handful of the heaviest conversions are marked `status: "soon"` in
`tools_data.py` and show a "Coming Soon" panel instead of a form:
PDF↔Word, PDF↔Excel, PDF↔PowerPoint, and OCR PDF. These need a document
conversion engine (e.g. LibreOffice headless) or an OCR engine (e.g.
Tesseract) wired up as a background job — a good next step once you're
ready to deploy somewhere with those binaries available. To wire one up,
set `"status": "live"` and point `"handler"` at a new function in
`tool_logic/pdf_tools.py`.

## Notes

- Uploaded files are processed in memory and not saved to disk; results are
  streamed back as a base64 download link, so there's nothing to clean up.
- The social media "generators" (hashtags, captions, titles, etc.) are
  rule-based/template-based so they run instantly with no API key. Swap the
  internals of `tool_logic/text_tools.py` for a real LLM call if you want
  richer output later.
- Branding (site name, developer, social links, contact email) lives in
  `impulsive_tool/settings.py` under the "Site-wide branding constants"
  section — change it there and it updates everywhere via the
  `branding` context processor.
