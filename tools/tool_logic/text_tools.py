"""
text_tools.py
=============
Rule-based generators for the Social Media Tools category. These don't call
an external AI API — they use templates and light heuristics, so they run
instantly and for free. Swap the internals for a real LLM call later if
you want richer output (see README section 'Upgrading the generators').
"""
import re
import urllib.parse

import requests

from .base import ToolResult

STOPWORDS = {"the", "a", "an", "of", "and", "or", "for", "to", "in", "on", "with", "is", "my", "your"}


def _keywords(topic, limit=6):
    words = re.findall(r"[A-Za-z0-9]+", topic.lower())
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    seen, out = set(), []
    for w in words:
        if w not in seen:
            seen.add(w)
            out.append(w)
        if len(out) >= limit:
            break
    return out or ["content"]


def hashtag_generator(files, fields):
    topic = fields.get("topic", "").strip()
    if not topic:
        return ToolResult.error("Enter a topic or caption.")
    kws = _keywords(topic, limit=8)
    base = [f"#{w}" for w in kws]
    extras = ["#trending", "#viral", "#explorepage", "#instagood", "#reels", f"#{''.join(kws[:2])}"]
    tags = list(dict.fromkeys(base + extras))[:15]
    return ToolResult.text(" ".join(tags), message="Hashtags generated.")


def caption_generator(files, fields):
    topic = fields.get("topic", "").strip()
    tone = fields.get("tone", "casual")
    if not topic:
        return ToolResult.error("Enter a topic.")
    templates = {
        "casual": [
            f"Just another day with {topic}. 🌤️",
            f"{topic} kind of mood today.",
            f"Can't stop thinking about {topic}.",
        ],
        "funny": [
            f"{topic}? Say less. 😂",
            f"Me pretending I have my life together while thinking about {topic}.",
            f"Plot twist: it's always about {topic}.",
        ],
        "inspirational": [
            f"Every {topic} moment is a step forward. ✨",
            f"Chasing {topic}, one day at a time.",
            f"{topic} taught me more than I expected.",
        ],
        "professional": [
            f"Reflecting on {topic} and what it means for what's next.",
            f"Excited to share this update on {topic}.",
            f"A few thoughts on {topic}.",
        ],
    }
    options = templates.get(tone, templates["casual"])
    return ToolResult.text("\n\n".join(options), message="Captions generated.")


def youtube_title_generator(files, fields):
    topic = fields.get("topic", "").strip()
    if not topic:
        return ToolResult.error("Enter a video topic.")
    title = topic.title()
    ideas = [
        f"{title} — Everything You Need to Know",
        f"I Tried {title} So You Don't Have To",
        f"The Truth About {title}",
        f"{title}: A Complete Beginner's Guide",
        f"Why {title} Actually Matters in 2026",
    ]
    return ToolResult.text("\n".join(ideas), message="Titles generated.")


def youtube_description_generator(files, fields):
    topic = fields.get("topic", "").strip()
    keywords = fields.get("keywords", "").strip()
    if not topic:
        return ToolResult.error("Enter a video topic.")
    kw_line = f"\n\nTopics covered: {keywords}" if keywords else ""
    desc = (
        f"In this video, we dive into {topic} — what it is, why it matters, "
        f"and how you can get the most out of it.{kw_line}\n\n"
        f"👍 If this helped, leave a like and subscribe for more content on {topic}.\n"
        f"💬 Drop a comment with your thoughts or questions below."
    )
    return ToolResult.text(desc, message="Description generated.")


def youtube_tag_generator(files, fields):
    topic = fields.get("topic", "").strip()
    if not topic:
        return ToolResult.error("Enter a video topic.")
    kws = _keywords(topic, limit=6)
    tags = set(kws)
    tags.update([topic.lower(), f"{topic.lower()} tutorial", f"{topic.lower()} 2026", f"how to {topic.lower()}"])
    return ToolResult.text(", ".join(sorted(tags)), message="Tags generated.")


def instagram_bio_generator(files, fields):
    niche = fields.get("niche", "").strip()
    if not niche:
        return ToolResult.error("Enter your niche or interests.")
    ideas = [
        f"{niche} enthusiast 🌟 | Sharing my journey, one post at a time",
        f"📍 Living the {niche} life | DM for collabs",
        f"{niche.title()} • Creator • Always learning",
    ]
    return ToolResult.text("\n\n".join(ideas), message="Bio ideas generated.")


def linkedin_headline_generator(files, fields):
    role = fields.get("role", "").strip()
    skills = fields.get("skills", "").strip()
    if not role:
        return ToolResult.error("Enter your job title or role.")
    skill_part = f" | {skills}" if skills else ""
    ideas = [
        f"{role}{skill_part}",
        f"{role} — helping teams build better products",
        f"Aspiring {role} | Open to opportunities{skill_part}",
    ]
    return ToolResult.text("\n\n".join(ideas), message="Headlines generated.")


def tweet_formatter(files, fields):
    text = fields.get("text", "").strip()
    if not text:
        return ToolResult.error("Paste the text you want to split into a thread.")
    limit = 270
    words = text.split()
    chunks, current = [], ""
    for w in words:
        if len(current) + len(w) + 1 > limit:
            chunks.append(current.strip())
            current = w
        else:
            current += (" " if current else "") + w
    if current:
        chunks.append(current.strip())
    total = len(chunks)
    thread = "\n\n".join(f"{i+1}/{total} {c}" for i, c in enumerate(chunks))
    return ToolResult.text(thread, message=f"Split into a {total}-tweet thread.")


def _extract_youtube_id(url_or_id):
    url_or_id = url_or_id.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url_or_id):
        return url_or_id
    parsed = urllib.parse.urlparse(url_or_id)
    if "youtu.be" in parsed.netloc:
        return parsed.path.lstrip("/")
    qs = urllib.parse.parse_qs(parsed.query)
    if "v" in qs:
        return qs["v"][0]
    if "/shorts/" in parsed.path:
        return parsed.path.split("/shorts/")[-1].split("/")[0]
    return None


def thumbnail_downloader(files, fields):
    link = fields.get("url", "").strip()
    if not link:
        return ToolResult.error("Paste a YouTube video URL or ID.")
    video_id = _extract_youtube_id(link)
    if not video_id:
        return ToolResult.error("Could not find a video ID in that URL.")
    from .base import save_output
    for quality in ("maxresdefault", "sddefault", "hqdefault"):
        img_url = f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"
        try:
            resp = requests.get(img_url, timeout=8)
            if resp.status_code == 200 and len(resp.content) > 500:
                return save_output(resp.content, f"{video_id}-thumbnail.jpg", "image/jpeg",
                                    message=f"Fetched {quality} thumbnail.")
        except requests.RequestException:
            continue
    return ToolResult.error("Couldn't fetch a thumbnail for that video.")
