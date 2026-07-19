"""
resume_tools.py
================
Heuristic resume analysis — no external AI call, so it's instant and free.
Extracts text from an uploaded PDF (pypdf) and runs a rule-based checklist.
For .docx uploads it falls back to a friendly error asking for PDF, since
parsing docx well needs an extra dependency out of scope for this pass.
"""
import re

from pypdf import PdfReader

from .base import ToolResult, first_uploaded_file

SECTION_HEADERS = ["experience", "education", "skills", "projects", "summary", "certifications"]
ACTION_VERBS = ["led", "built", "created", "designed", "managed", "improved", "launched",
                "developed", "implemented", "increased", "reduced", "optimized", "achieved"]
CONTACT_PATTERNS = {
    "email": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "phone": r"(\+?\d[\d\s().-]{8,}\d)",
}


def _extract_text(f):
    name = getattr(f, "name", "")
    if name.lower().endswith(".pdf"):
        reader = PdfReader(f)
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    raise ValueError("Please upload your resume as a PDF for accurate analysis.")


def ats_checker(files, fields):
    f = first_uploaded_file(files)
    if not f:
        return ToolResult.error("Upload your resume (PDF).")
    try:
        text = _extract_text(f)
    except ValueError as exc:
        return ToolResult.error(str(exc))
    if not text.strip():
        return ToolResult.error("Couldn't extract text — this may be a scanned/image-based PDF, which ATS software also struggles with. Try exporting a text-based PDF.")

    lower = text.lower()
    checks = []

    has_email = bool(re.search(CONTACT_PATTERNS["email"], text))
    checks.append(("Includes an email address", has_email))

    has_phone = bool(re.search(CONTACT_PATTERNS["phone"], text))
    checks.append(("Includes a phone number", has_phone))

    found_sections = [s for s in SECTION_HEADERS if s in lower]
    checks.append((f"Has clear section headers ({', '.join(found_sections) or 'none found'})", len(found_sections) >= 3))

    word_count = len(text.split())
    checks.append((f"Reasonable length ({word_count} words)", 250 <= word_count <= 1200))

    has_bullets = ("•" in text) or bool(re.search(r"^\s*[-*]\s", text, re.MULTILINE))
    checks.append(("Uses bullet points", has_bullets))

    verb_hits = sum(1 for v in ACTION_VERBS if v in lower)
    checks.append((f"Uses action verbs ({verb_hits} found)", verb_hits >= 3))

    has_tables_risk = text.count("\t") > 20
    checks.append(("Avoids complex tables/columns that confuse ATS parsers", not has_tables_risk))

    passed = sum(1 for _, ok in checks if ok)
    score_pct = round(passed / len(checks) * 100)

    lines = [f"ATS Compatibility Score: {score_pct}%  ({passed}/{len(checks)} checks passed)", ""]
    for label, ok in checks:
        lines.append(f"{'✔' if ok else '✘'} {label}")
    lines.append("")
    lines.append("Note: this is a heuristic check based on common ATS parsing pitfalls, not a guarantee of how any specific ATS will score your resume.")
    return ToolResult.text("\n".join(lines))


def resume_score(files, fields):
    f = first_uploaded_file(files)
    job_desc = fields.get("job_description", "").strip()
    if not f:
        return ToolResult.error("Upload your resume (PDF).")
    try:
        text = _extract_text(f)
    except ValueError as exc:
        return ToolResult.error(str(exc))
    if not text.strip():
        return ToolResult.error("Couldn't extract text from that PDF.")

    lower = text.lower()
    lines = []

    if job_desc:
        jd_words = set(re.findall(r"[a-z][a-z+#.-]{2,}", job_desc.lower()))
        jd_words -= {"and", "the", "with", "for", "you", "your", "our", "will", "are", "this"}
        matched = sorted(w for w in jd_words if w in lower)
        match_pct = round(len(matched) / max(1, len(jd_words)) * 100)
        lines.append(f"Keyword match vs. job description: {match_pct}% ({len(matched)}/{len(jd_words)} terms found)")
        missing = sorted(jd_words - set(matched))[:15]
        if missing:
            lines.append(f"Missing keywords to consider adding: {', '.join(missing)}")
        lines.append("")

    verb_hits = sum(1 for v in ACTION_VERBS if v in lower)
    numbers_hits = len(re.findall(r"\b\d+%?\b", text))
    word_count = len(text.split())

    base_score = 40
    base_score += min(20, verb_hits * 3)
    base_score += min(20, numbers_hits)
    base_score += 10 if 250 <= word_count <= 1200 else 0
    if job_desc:
        base_score = round(base_score * 0.6 + match_pct * 0.4)
    base_score = min(100, base_score)

    lines.insert(0, f"Overall Resume Score: {base_score}/100")
    lines.insert(1, "")
    lines.append(f"Action verbs used: {verb_hits}")
    lines.append(f"Quantified results (numbers/%): {numbers_hits} — quantifying impact strongly helps recruiters and ATS.")
    lines.append(f"Word count: {word_count}")

    return ToolResult.text("\n".join(lines))
