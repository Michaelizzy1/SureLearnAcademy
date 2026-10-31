"""SEO helpers: JSON-LD structured data builders and sitemap/robots support."""
import json

from django.conf import settings
from django.utils.safestring import mark_safe


def absolute(path):
    """Build an absolute URL on the canonical domain."""
    return settings.SITE_URL.rstrip("/") + path


def ld_json(*blocks):
    """Render one or more dicts as <script type="application/ld+json"> tags (safe against </script>)."""
    out = []
    for data in blocks:
        payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
        out.append(f'<script type="application/ld+json">{payload}</script>')
    return mark_safe("\n".join(out))


def organization_schema():
    return {
        "@context": "https://schema.org",
        "@type": ["EducationalOrganization", "LocalBusiness"],
        "@id": absolute("/#organization"),
        "name": settings.SITE_NAME,
        "url": absolute("/"),
        "logo": absolute("/static/assets/logo.png"),
        "image": absolute("/static/assets/og-default.png"),
        "description": (
            "One-on-one private and home lessons in Abuja and Nasarawa, Nigeria: "
            "SSCE and JAMB exam prep, web development, programming, AI and creative skills."
        ),
        "email": settings.CONTACT_EMAIL,
        "telephone": settings.CONTACT_PHONE,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Abuja",
            "addressRegion": "FCT",
            "addressCountry": "NG",
        },
        "areaServed": [
            {"@type": "City", "name": "Abuja"},
            {"@type": "AdministrativeArea", "name": "Nasarawa"},
            {"@type": "Place", "name": "Mararaba"},
            {"@type": "Place", "name": "New Nyanya"},
            {"@type": "Place", "name": "Masaka"},
        ],
        "knowsAbout": [
            "SSCE preparation", "JAMB UTME preparation", "Web development",
            "Programming", "Artificial intelligence", "Graphics design", "UI/UX design",
        ],
    }


def website_schema():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": absolute("/#website"),
        "url": absolute("/"),
        "name": settings.SITE_NAME,
        "publisher": {"@id": absolute("/#organization")},
        "inLanguage": "en-NG",
    }


def breadcrumb_schema(*crumbs):
    """crumbs: (name, path) tuples, starting with Home."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": name, "item": absolute(path)}
            for i, (name, path) in enumerate(crumbs, start=1)
        ],
    }


def faq_schema(pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }
