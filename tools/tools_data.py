"""
tools_data.py
=============
Single source of truth for every category and tool on Impulsive Tool.

The whole site is template-driven: nothing here needs a database row.
To add a new tool, add one dict to TOOLS below and point `handler` at a
function in tools/tool_logic/ (or leave handler=None for a "Coming Soon"
tool that still gets a full page, just with no processing wired up yet).

Each tool dict:
    slug        - URL segment, must be unique site-wide
    name        - display name
    category    - must match a key in CATEGORIES
    description - one-line summary for cards / meta description
    icon        - a short emoji/glyph used as a lightweight icon (no external
                  icon font dependency, keeps the project self-contained)
    kind        - 'file' | 'form' | 'client'
                  file   -> tool takes an uploaded file, handled server-side
                  form   -> tool takes text/number inputs, handled server-side
                  client -> tool runs entirely in the browser (JS), e.g. GPA
                            calculators, counters, timers
    handler     - dotted path to the processing function (file/form tools) or
                  None for tools that are UI-ready but not wired up yet
    status      - 'live' | 'soon'   (drives the "Coming Soon" badge/behaviour)
"""

CATEGORIES = {
    "pdf": {
        "name": "PDF Tools",
        "slug": "pdf",
        "icon": "📄",
        "description": "Convert, merge, split, compress and protect PDF files.",
    },
    "student": {
        "name": "Student Tools",
        "slug": "student",
        "icon": "🎓",
        "description": "GPA/CGPA calculators, attendance tracking and study timers.",
    },
    "social": {
        "name": "Social Media Tools",
        "slug": "social",
        "icon": "📣",
        "description": "Hashtags, captions and titles for every platform.",
    },
    "security": {
        "name": "Security Tools",
        "slug": "security",
        "icon": "🔐",
        "description": "Passwords, random data and QR codes.",
    },
    "resume": {
        "name": "Resume Tools",
        "slug": "resume",
        "icon": "📝",
        "description": "Score your resume and check ATS compatibility.",
    },
    "qr-barcode": {
        "name": "QR & Barcode Tools",
        "slug": "qr-barcode",
        "icon": "▦",
        "description": "Generate and scan QR codes and barcodes for anything.",
    },
}

TOOLS = [
    # ---------------------------------------------------------------- PDF --
    {"slug": "pdf-to-word", "name": "PDF to Word", "category": "pdf",
     "description": "Convert a PDF into an editable Word document.",
     "icon": "📄", "kind": "file", "handler": None, "status": "soon"},
    {"slug": "word-to-pdf", "name": "Word to PDF", "category": "pdf",
     "description": "Convert a Word document into a PDF.",
     "icon": "📄", "kind": "file", "handler": None, "status": "soon"},
    {"slug": "pdf-to-excel", "name": "PDF to Excel", "category": "pdf",
     "description": "Pull tables out of a PDF into a spreadsheet.",
     "icon": "📄", "kind": "file", "handler": None, "status": "soon"},
    {"slug": "excel-to-pdf", "name": "Excel to PDF", "category": "pdf",
     "description": "Convert a spreadsheet into a PDF.",
     "icon": "📄", "kind": "file", "handler": None, "status": "soon"},
    {"slug": "pdf-to-powerpoint", "name": "PDF to PowerPoint", "category": "pdf",
     "description": "Convert PDF pages into an editable slide deck.",
     "icon": "📄", "kind": "file", "handler": None, "status": "soon"},
    {"slug": "powerpoint-to-pdf", "name": "PowerPoint to PDF", "category": "pdf",
     "description": "Convert a slide deck into a PDF.",
     "icon": "📄", "kind": "file", "handler": None, "status": "soon"},
    {"slug": "pdf-to-jpg", "name": "PDF to JPG", "category": "pdf",
     "description": "Turn every page of a PDF into a JPG image.",
     "icon": "🖼️", "kind": "file", "handler": "tools.tool_logic.pdf_tools.pdf_to_jpg", "status": "live"},
    {"slug": "jpg-to-pdf", "name": "JPG to PDF", "category": "pdf",
     "description": "Combine one or more images into a single PDF.",
     "icon": "🖼️", "kind": "file", "handler": "tools.tool_logic.pdf_tools.jpg_to_pdf", "status": "live"},
    {"slug": "merge-pdf", "name": "Merge PDF", "category": "pdf",
     "description": "Combine multiple PDFs into one file, in order.",
     "icon": "📎", "kind": "file", "handler": "tools.tool_logic.pdf_tools.merge_pdf", "status": "live"},
    {"slug": "split-pdf", "name": "Split PDF", "category": "pdf",
     "description": "Pull a page range out of a PDF into its own file.",
     "icon": "✂️", "kind": "file", "handler": "tools.tool_logic.pdf_tools.split_pdf", "status": "live"},
    {"slug": "compress-pdf", "name": "Compress PDF", "category": "pdf",
     "description": "Shrink a PDF's file size for easier sharing.",
     "icon": "🗜️", "kind": "file", "handler": "tools.tool_logic.pdf_tools.compress_pdf", "status": "live"},
    {"slug": "rotate-pdf", "name": "Rotate PDF", "category": "pdf",
     "description": "Rotate every page of a PDF by 90, 180 or 270°.",
     "icon": "🔄", "kind": "file", "handler": "tools.tool_logic.pdf_tools.rotate_pdf", "status": "live"},
    {"slug": "protect-pdf", "name": "Protect PDF", "category": "pdf",
     "description": "Lock a PDF behind a password.",
     "icon": "🔒", "kind": "file", "handler": "tools.tool_logic.pdf_tools.protect_pdf", "status": "live"},
    {"slug": "unlock-pdf", "name": "Unlock PDF", "category": "pdf",
     "description": "Remove a known password from a PDF.",
     "icon": "🔓", "kind": "file", "handler": "tools.tool_logic.pdf_tools.unlock_pdf", "status": "live"},
    {"slug": "ocr-pdf", "name": "OCR PDF", "category": "pdf",
     "description": "Make a scanned PDF's text searchable and selectable.",
     "icon": "🔎", "kind": "file", "handler": None, "status": "soon"},

    # ------------------------------------------------------------ Student --
    {"slug": "gpa-calculator", "name": "GPA Calculator", "category": "student",
     "description": "Work out your GPA from course grades and credits.",
     "icon": "🎓", "kind": "client", "handler": None, "status": "live"},
    {"slug": "cgpa-calculator", "name": "CGPA Calculator", "category": "student",
     "description": "Work out your CGPA across semesters.",
     "icon": "🎓", "kind": "client", "handler": None, "status": "live"},
    {"slug": "percentage-calculator", "name": "Percentage Calculator", "category": "student",
     "description": "Convert marks obtained into a percentage.",
     "icon": "🧮", "kind": "client", "handler": None, "status": "live"},
    {"slug": "percentage-to-cgpa", "name": "Percentage to CGPA", "category": "student",
     "description": "Convert a percentage score into an equivalent CGPA.",
     "icon": "🧮", "kind": "client", "handler": None, "status": "live"},
    {"slug": "cgpa-to-percentage", "name": "CGPA to Percentage", "category": "student",
     "description": "Convert a CGPA score into an equivalent percentage.",
     "icon": "🧮", "kind": "client", "handler": None, "status": "live"},
    {"slug": "attendance-calculator", "name": "Attendance Calculator", "category": "student",
     "description": "Check your attendance percentage and safe skips.",
     "icon": "📅", "kind": "client", "handler": None, "status": "live"},
    {"slug": "study-timer", "name": "Study Timer (Pomodoro)", "category": "student",
     "description": "A focus timer with work and break intervals.",
     "icon": "⏱️", "kind": "client", "handler": None, "status": "live"},
    {"slug": "citation-generator", "name": "Citation Generator", "category": "student",
     "description": "Generate APA, MLA and Chicago style citations.",
     "icon": "📚", "kind": "client", "handler": None, "status": "live"},

    # ------------------------------------------------------------- Social --
    {"slug": "hashtag-generator", "name": "Hashtag Generator", "category": "social",
     "description": "Generate relevant hashtags from a topic or caption.",
     "icon": "#️⃣", "kind": "form", "handler": "tools.tool_logic.text_tools.hashtag_generator", "status": "live"},
    {"slug": "caption-generator", "name": "Caption Generator", "category": "social",
     "description": "Generate short caption ideas from a topic.",
     "icon": "💬", "kind": "form", "handler": "tools.tool_logic.text_tools.caption_generator", "status": "live"},
    {"slug": "youtube-title-generator", "name": "YouTube Title Generator", "category": "social",
     "description": "Generate click-worthy YouTube title ideas.",
     "icon": "▶️", "kind": "form", "handler": "tools.tool_logic.text_tools.youtube_title_generator", "status": "live"},
    {"slug": "youtube-description-generator", "name": "YouTube Description Generator", "category": "social",
     "description": "Generate a starter description for your video.",
     "icon": "▶️", "kind": "form", "handler": "tools.tool_logic.text_tools.youtube_description_generator", "status": "live"},
    {"slug": "youtube-tag-generator", "name": "YouTube Tag Generator", "category": "social",
     "description": "Generate a set of tags for a video topic.",
     "icon": "▶️", "kind": "form", "handler": "tools.tool_logic.text_tools.youtube_tag_generator", "status": "live"},
    {"slug": "instagram-bio-generator", "name": "Instagram Bio Generator", "category": "social",
     "description": "Generate short, punchy Instagram bio ideas.",
     "icon": "📸", "kind": "form", "handler": "tools.tool_logic.text_tools.instagram_bio_generator", "status": "live"},
    {"slug": "linkedin-headline-generator", "name": "LinkedIn Headline Generator", "category": "social",
     "description": "Generate a professional LinkedIn headline.",
     "icon": "💼", "kind": "form", "handler": "tools.tool_logic.text_tools.linkedin_headline_generator", "status": "live"},
    {"slug": "tweet-formatter", "name": "Tweet Formatter", "category": "social",
     "description": "Split long text into a numbered tweet thread.",
     "icon": "🐦", "kind": "form", "handler": "tools.tool_logic.text_tools.tweet_formatter", "status": "live"},
    {"slug": "character-counter", "name": "Character Counter", "category": "social",
     "description": "Count characters, words and sentences live.",
     "icon": "🔢", "kind": "client", "handler": None, "status": "live"},
    {"slug": "thumbnail-downloader", "name": "Thumbnail Downloader", "category": "social",
     "description": "Grab a YouTube video's thumbnail in full resolution.",
     "icon": "🖼️", "kind": "form", "handler": "tools.tool_logic.text_tools.thumbnail_downloader", "status": "live"},

    # ----------------------------------------------------------- Security --
    {"slug": "password-generator", "name": "Password Generator", "category": "security",
     "description": "Generate a strong, random password.",
     "icon": "🔑", "kind": "form", "handler": "tools.tool_logic.security_tools.password_generator", "status": "live"},
    {"slug": "password-strength-checker", "name": "Password Strength Checker", "category": "security",
     "description": "Check how strong a password is and why.",
     "icon": "💪", "kind": "form", "handler": "tools.tool_logic.security_tools.password_strength_checker", "status": "live"},
    {"slug": "random-string-generator", "name": "Random String Generator", "category": "security",
     "description": "Generate a random string with a custom charset.",
     "icon": "🔤", "kind": "form", "handler": "tools.tool_logic.security_tools.random_string_generator", "status": "live"},
    {"slug": "random-number-generator", "name": "Random Number Generator", "category": "security",
     "description": "Generate a random number within a range.",
     "icon": "🎲", "kind": "form", "handler": "tools.tool_logic.security_tools.random_number_generator", "status": "live"},
    {"slug": "qr-code-generator", "name": "QR Code Generator", "category": "security",
     "description": "Turn any text or link into a QR code.",
     "icon": "▦", "kind": "form", "handler": "tools.tool_logic.qr_tools.qr_generic", "status": "live"},
    # {"slug": "qr-code-reader", "name": "QR Code Reader", "category": "security",
    #  "description": "Upload a QR code image and read its contents.",
    #  "icon": "🔍", "kind": "file", "handler": "tools.tool_logic.qr_tools.qr_reader", "status": "live"},

    # ------------------------------------------------------------ Resume --
    {"slug": "resume-ats-checker", "name": "Resume ATS Checker", "category": "resume",
     "description": "Check resume formatting for ATS compatibility.",
     "icon": "📝", "kind": "file", "handler": "tools.tool_logic.resume_tools.ats_checker", "status": "live"},
    {"slug": "resume-score", "name": "Resume Score", "category": "resume",
     "description": "Score a resume against a target job description.",
     "icon": "📝", "kind": "file", "handler": "tools.tool_logic.resume_tools.resume_score", "status": "live"},

    # -------------------------------------------------------- QR/Barcode --
    {"slug": "wifi-qr-generator", "name": "Wi-Fi QR Generator", "category": "qr-barcode",
     "description": "Generate a QR code that connects to your Wi-Fi.",
     "icon": "📶", "kind": "form", "handler": "tools.tool_logic.qr_tools.qr_wifi", "status": "live"},
    {"slug": "contact-qr-generator", "name": "Contact QR Generator", "category": "qr-barcode",
     "description": "Generate a QR code that saves a contact card.",
     "icon": "👤", "kind": "form", "handler": "tools.tool_logic.qr_tools.qr_contact", "status": "live"},
    {"slug": "email-qr-generator", "name": "Email QR Generator", "category": "qr-barcode",
     "description": "Generate a QR code that opens a pre-filled email.",
     "icon": "✉️", "kind": "form", "handler": "tools.tool_logic.qr_tools.qr_email", "status": "live"},
    {"slug": "sms-qr-generator", "name": "SMS QR Generator", "category": "qr-barcode",
     "description": "Generate a QR code that opens a pre-filled text.",
     "icon": "💬", "kind": "form", "handler": "tools.tool_logic.qr_tools.qr_sms", "status": "live"},
    {"slug": "whatsapp-qr-generator", "name": "WhatsApp QR Generator", "category": "qr-barcode",
     "description": "Generate a QR code that opens a WhatsApp chat.",
     "icon": "💚", "kind": "form", "handler": "tools.tool_logic.qr_tools.qr_whatsapp", "status": "live"},
    {"slug": "phone-qr-generator", "name": "Phone Number QR Generator", "category": "qr-barcode",
     "description": "Generate a QR code that dials a phone number.",
     "icon": "📞", "kind": "form", "handler": "tools.tool_logic.qr_tools.qr_phone", "status": "live"},
    {"slug": "url-qr-generator", "name": "URL QR Generator", "category": "qr-barcode",
     "description": "Generate a QR code that opens a link.",
     "icon": "🔗", "kind": "form", "handler": "tools.tool_logic.qr_tools.qr_url", "status": "live"},
    {"slug": "gmaps-qr-generator", "name": "Google Maps QR Generator", "category": "qr-barcode",
     "description": "Generate a QR code that opens a map location.",
     "icon": "📍", "kind": "form", "handler": "tools.tool_logic.qr_tools.qr_gmaps", "status": "live"},
    {"slug": "event-qr-generator", "name": "Event QR Generator", "category": "qr-barcode",
     "description": "Generate a QR code that adds a calendar event.",
     "icon": "📆", "kind": "form", "handler": "tools.tool_logic.qr_tools.qr_event", "status": "live"},
    {"slug": "barcode-generator", "name": "Barcode Generator", "category": "qr-barcode",
     "description": "Generate a Code128 barcode from any text.",
     "icon": "▥", "kind": "form", "handler": "tools.tool_logic.qr_tools.barcode_generic", "status": "live"},
    # {"slug": "barcode-scanner", "name": "Barcode Scanner", "category": "qr-barcode",
    #  "description": "Upload a barcode image and read its value.",
    #  "icon": "🔍", "kind": "file", "handler": "tools.tool_logic.qr_tools.barcode_scanner", "status": "live"},
    {"slug": "isbn-barcode-generator", "name": "ISBN Barcode Generator", "category": "qr-barcode",
     "description": "Generate an ISBN-13 barcode for a book.",
     "icon": "📖", "kind": "form", "handler": "tools.tool_logic.qr_tools.barcode_isbn", "status": "live"},
    {"slug": "upc-ean-barcode-generator", "name": "UPC/EAN Barcode Generator", "category": "qr-barcode",
     "description": "Generate a UPC-A or EAN-13 barcode.",
     "icon": "🏷️", "kind": "form", "handler": "tools.tool_logic.qr_tools.barcode_upc_ean", "status": "live"},
]

# ---------------------------------------------------------------------------
# Form field specs for 'file' and 'form' kind tools. tool.html renders these
# generically so every tool shares one template — add a tool above, then a
# matching field list here (or leave a 'file' tool with no extra fields).
#
# Field dict keys: name, label, type, required(optional bool), placeholder,
# options (for select, list of (value,label)), default, accept (for file),
# multiple (bool, for multi-file upload), hint (optional helper text)
# ---------------------------------------------------------------------------
FIELDS_BY_SLUG = {
    # ---- PDF -------------------------------------------------------------
    "pdf-to-jpg": [
        {"name": "file", "label": "PDF file", "type": "file", "accept": ".pdf", "required": True},
    ],
    "jpg-to-pdf": [
        {"name": "file", "label": "Images", "type": "file", "accept": "image/*", "multiple": True, "required": True,
         "hint": "Upload one or more images — they'll appear in the PDF in the order selected."},
    ],
    "merge-pdf": [
        {"name": "file", "label": "PDF files", "type": "file", "accept": ".pdf", "multiple": True, "required": True,
         "hint": "Upload two or more PDFs — they'll be merged in the order selected."},
    ],
    "split-pdf": [
        {"name": "file", "label": "PDF file", "type": "file", "accept": ".pdf", "required": True},
        {"name": "start_page", "label": "Start page", "type": "number", "placeholder": "1", "attrs": "data-split-start"},
        {"name": "end_page", "label": "End page", "type": "number", "placeholder": "e.g. 5", "attrs": "data-split-end"},
    ],
    "compress-pdf": [
        {"name": "file", "label": "PDF file", "type": "file", "accept": ".pdf", "required": True},
    ],
    "rotate-pdf": [
        {"name": "file", "label": "PDF file", "type": "file", "accept": ".pdf", "required": True},
        {"name": "angle", "label": "Rotation angle", "type": "select", "default": "90", "attrs": "data-rotate-angle",
         "options": [("90", "90°"), ("180", "180°"), ("270", "270°")]},
    ],
    "protect-pdf": [
        {"name": "file", "label": "PDF file", "type": "file", "accept": ".pdf", "required": True},
        {"name": "password", "label": "New password", "type": "password", "required": True},
    ],
    "unlock-pdf": [
        {"name": "file", "label": "PDF file", "type": "file", "accept": ".pdf", "required": True},
        {"name": "password", "label": "Current password", "type": "password", "required": True},
    ],

    # ---- Social ------------------------------------------------------------
    "hashtag-generator": [
        {"name": "topic", "label": "Topic or caption", "type": "text", "placeholder": "e.g. weekend hiking trip", "required": True},
    ],
    "caption-generator": [
        {"name": "topic", "label": "Topic", "type": "text", "placeholder": "e.g. sunset at the beach", "required": True},
        {"name": "tone", "label": "Tone", "type": "select", "default": "casual",
         "options": [("casual", "Casual"), ("funny", "Funny"), ("inspirational", "Inspirational"), ("professional", "Professional")]},
    ],
    "youtube-title-generator": [
        {"name": "topic", "label": "Video topic", "type": "text", "placeholder": "e.g. learning Python in 30 days", "required": True},
    ],
    "youtube-description-generator": [
        {"name": "topic", "label": "Video topic", "type": "text", "placeholder": "e.g. learning Python in 30 days", "required": True},
        {"name": "keywords", "label": "Key topics covered (optional)", "type": "text", "placeholder": "e.g. variables, loops, functions"},
    ],
    "youtube-tag-generator": [
        {"name": "topic", "label": "Video topic", "type": "text", "placeholder": "e.g. learning Python in 30 days", "required": True},
    ],
    "instagram-bio-generator": [
        {"name": "niche", "label": "Niche or interests", "type": "text", "placeholder": "e.g. travel photography", "required": True},
    ],
    "linkedin-headline-generator": [
        {"name": "role", "label": "Job title / role", "type": "text", "placeholder": "e.g. Software Engineer", "required": True},
        {"name": "skills", "label": "Key skills (optional)", "type": "text", "placeholder": "e.g. Python, Django, React"},
    ],
    "tweet-formatter": [
        {"name": "text", "label": "Long text to split into a thread", "type": "textarea", "required": True},
    ],
    "thumbnail-downloader": [
        {"name": "url", "label": "YouTube video URL or ID", "type": "text", "placeholder": "https://youtu.be/...", "required": True},
    ],

    # ---- Security ------------------------------------------------------------
    "password-generator": [
        {"name": "length", "label": "Length", "type": "number", "default": "16"},
        {"name": "upper", "label": "Include uppercase (A-Z)", "type": "checkbox", "default": True},
        {"name": "lower", "label": "Include lowercase (a-z)", "type": "checkbox", "default": True},
        {"name": "digits", "label": "Include digits (0-9)", "type": "checkbox", "default": True},
        {"name": "symbols", "label": "Include symbols (!@#...)", "type": "checkbox", "default": True},
        {"name": "avoid_ambiguous", "label": "Avoid ambiguous characters (Il1O0)", "type": "checkbox", "default": False},
    ],
    "password-strength-checker": [
        {"name": "password", "label": "Password to check", "type": "password", "required": True},
    ],
    "random-string-generator": [
        {"name": "length", "label": "Length", "type": "number", "default": "12"},
        {"name": "charset", "label": "Character set", "type": "select", "default": "alnum",
         "options": [("alnum", "Letters + digits"), ("letters", "Letters only"), ("digits", "Digits only"), ("hex", "Hex"), ("all", "Letters + digits + symbols")]},
    ],
    "random-number-generator": [
        {"name": "min", "label": "Minimum", "type": "number", "default": "1"},
        {"name": "max", "label": "Maximum", "type": "number", "default": "100"},
    ],
    "qr-code-generator": [
        {"name": "text", "label": "Text or link", "type": "text", "placeholder": "https://example.com", "required": True},
    ],
    "qr-code-reader": [
        {"name": "file", "label": "QR code image", "type": "file", "accept": "image/*", "required": True},
    ],

    # ---- Resume ------------------------------------------------------------
    "resume-ats-checker": [
        {"name": "file", "label": "Resume (PDF)", "type": "file", "accept": ".pdf", "required": True},
    ],
    "resume-score": [
        {"name": "file", "label": "Resume (PDF)", "type": "file", "accept": ".pdf", "required": True},
        {"name": "job_description", "label": "Target job description (optional)", "type": "textarea",
         "hint": "Paste a job posting to get a keyword-match score against it."},
    ],

    # ---- QR & Barcode ------------------------------------------------------
    "wifi-qr-generator": [
        {"name": "ssid", "label": "Network name (SSID)", "type": "text", "required": True},
        {"name": "password", "label": "Password", "type": "password"},
        {"name": "security", "label": "Security type", "type": "select", "default": "WPA",
         "options": [("WPA", "WPA/WPA2"), ("WEP", "WEP"), ("nopass", "None (open network)")]},
        {"name": "hidden", "label": "Hidden network", "type": "checkbox", "default": False},
    ],
    "contact-qr-generator": [
        {"name": "name", "label": "Full name", "type": "text", "required": True},
        {"name": "phone", "label": "Phone", "type": "tel"},
        {"name": "email", "label": "Email", "type": "email"},
        {"name": "org", "label": "Organization", "type": "text"},
    ],
    "email-qr-generator": [
        {"name": "to", "label": "Recipient email", "type": "email", "required": True},
        {"name": "subject", "label": "Subject", "type": "text"},
        {"name": "body", "label": "Body", "type": "textarea"},
    ],
    "sms-qr-generator": [
        {"name": "number", "label": "Phone number", "type": "tel", "required": True},
        {"name": "message", "label": "Message", "type": "textarea"},
    ],
    "whatsapp-qr-generator": [
        {"name": "number", "label": "WhatsApp number (with country code)", "type": "tel", "required": True, "placeholder": "919876543210"},
        {"name": "message", "label": "Pre-filled message (optional)", "type": "textarea"},
    ],
    "phone-qr-generator": [
        {"name": "number", "label": "Phone number", "type": "tel", "required": True},
    ],
    "url-qr-generator": [
        {"name": "url", "label": "URL", "type": "url", "placeholder": "https://example.com", "required": True},
    ],
    "gmaps-qr-generator": [
        {"name": "place", "label": "Place name / address", "type": "text", "placeholder": "e.g. India Gate, Delhi"},
        {"name": "lat", "label": "Latitude (optional)", "type": "text", "placeholder": "28.6129"},
        {"name": "lng", "label": "Longitude (optional)", "type": "text", "placeholder": "77.2295"},
    ],
    "event-qr-generator": [
        {"name": "title", "label": "Event title", "type": "text", "required": True},
        {"name": "start", "label": "Start (YYYYMMDDTHHMMSS)", "type": "text", "placeholder": "20260901T090000", "required": True},
        {"name": "end", "label": "End (YYYYMMDDTHHMMSS)", "type": "text", "placeholder": "20260901T170000", "required": True},
        {"name": "location", "label": "Location (optional)", "type": "text"},
    ],
    "barcode-generator": [
        {"name": "text", "label": "Text / number to encode", "type": "text", "required": True},
    ],
    "barcode-scanner": [
        {"name": "file", "label": "Barcode image", "type": "file", "accept": "image/*", "required": True},
    ],
    "isbn-barcode-generator": [
        {"name": "isbn", "label": "ISBN (10 or 13 digits)", "type": "text", "required": True, "placeholder": "9780134685991"},
    ],
    "upc-ean-barcode-generator": [
        {"name": "code", "label": "Code", "type": "text", "required": True, "placeholder": "012345678905"},
        {"name": "kind", "label": "Symbology", "type": "select", "default": "ean13",
         "options": [("ean13", "EAN-13"), ("upca", "UPC-A"), ("ean8", "EAN-8")]},
    ],
}

TOOLS_BY_SLUG = {t["slug"]: t for t in TOOLS}


def tools_for_category(category_slug):
    return [t for t in TOOLS if t["category"] == category_slug]


def category_tool_counts():
    counts = {c: 0 for c in CATEGORIES}
    for t in TOOLS:
        counts[t["category"]] = counts.get(t["category"], 0) + 1
    return counts


def popular_tools(limit=8):
    """A hand-picked 'popular' shelf — first N live tools across categories."""
    live = [t for t in TOOLS if t["status"] == "live"]
    return live[:limit]


def recent_tools(limit=8):
    """Most recently added tools — last N in catalog order."""
    return TOOLS[-limit:][::-1]
