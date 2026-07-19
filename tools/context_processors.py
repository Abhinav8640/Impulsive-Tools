from django.conf import settings
from .tools_data import CATEGORIES, category_tool_counts


def branding(request):
    """Site-wide branding constants, available as {{ site_name }} etc. everywhere."""
    return {
        "site_name": settings.SITE_NAME,
        "site_tagline": settings.SITE_TAGLINE,
        "site_developer": settings.SITE_DEVELOPER,
        "site_github": settings.SITE_GITHUB,
        "site_linkedin": settings.SITE_LINKEDIN,
        "site_contact_email": settings.SITE_CONTACT_EMAIL,
        "current_year": 2026,
    }


def tool_categories(request):
    """Category list + counts for the navbar mega-menu and footer."""
    counts = category_tool_counts()
    categories = []
    for slug, data in CATEGORIES.items():
        categories.append({**data, "count": counts.get(slug, 0)})
    return {"nav_categories": categories}
