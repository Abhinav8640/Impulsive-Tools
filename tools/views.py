import base64
import importlib

from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .tools_data import (
    CATEGORIES, TOOLS, TOOLS_BY_SLUG, FIELDS_BY_SLUG,
    tools_for_category, popular_tools, recent_tools,
)

FAQ_ITEMS = [
    ("Is Impulsive Tools free to use?", "Yes — every tool on this site is free, with no sign-up required."),
    ("Do you store the files I upload?", "Uploaded files are processed in memory to generate your result and are not kept afterwards."),
    ("Can I use these tools on mobile?", "Yes, the whole site is responsive and works on phones, tablets and desktops."),
    ("Some tools say 'Coming Soon' — when will they launch?", "Those tools are on the roadmap and will go live as they're built out."),
    ("Who built this?", "Impulsive Tools is an independent project developed by Abhinav Tripathi."),
    ("How do I report a bug or request a tool?", "Use the Contact page, or reach out via the GitHub link in the footer."),
]


def home(request):
    context = {
        "popular_tools": popular_tools(8),
        "recent_tools": recent_tools(8),
        "categories": list(CATEGORIES.values()),
        "faq_preview": FAQ_ITEMS[:4],
    }
    return render(request, "tools/home.html", context)


def category_list(request):
    return render(request, "tools/categories.html", {"categories": list(CATEGORIES.values())})


def category_detail(request, category_slug):
    if category_slug not in CATEGORIES:
        raise Http404("Category not found")
    context = {
        "category": CATEGORIES[category_slug],
        "tools": tools_for_category(category_slug),
    }
    return render(request, "tools/category.html", context)


def _resolve_handler(dotted_path):
    module_path, func_name = dotted_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, func_name)


@require_http_methods(["GET", "POST"])
def tool_detail(request, tool_slug):
    tool = TOOLS_BY_SLUG.get(tool_slug)
    if not tool:
        raise Http404("Tool not found")

    category = CATEGORIES[tool["category"]]
    related = [t for t in tools_for_category(tool["category"]) if t["slug"] != tool_slug][:4]

    context = {
        "tool": tool,
        "category": category,
        "related_tools": related,
        "fields": FIELDS_BY_SLUG.get(tool_slug, []),
        "result": None,
        "download_uri": None,
        "is_file_kind": tool.get("kind") in ("file", "form"),
    }

    if request.method == "POST" and tool["status"] == "live" and tool["handler"]:
        handler = _resolve_handler(tool["handler"])
        result = handler(request.FILES, request.POST)
        context["result"] = result
        if result.ok and result.file_bytes:
            b64 = base64.b64encode(result.file_bytes).decode("ascii")
            context["download_uri"] = f"data:{result.content_type};base64,{b64}"

    return render(request, "tools/tool.html", context)


def about(request):
    return render(request, "tools/about.html")


def contact(request):
    return render(request, "tools/contact.html")


def faq(request):
    return render(request, "tools/faq.html", {"faq_items": FAQ_ITEMS})


def privacy(request):
    return render(request, "tools/privacy.html")


def terms(request):
    return render(request, "tools/terms.html")


def search(request):
    query = request.GET.get("q", "").strip().lower()
    results = []
    if query:
        results = [t for t in TOOLS if query in t["name"].lower() or query in t["description"].lower()]
    return render(request, "tools/search_results.html", {"query": query, "results": results})


def handler404(request, exception):
    return render(request, "404.html", status=404)
