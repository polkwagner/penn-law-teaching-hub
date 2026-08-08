#!/usr/bin/env python3
"""Structural checks for the Deputy Dean hub site."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
INDEX = ROOT / "index.html"
LICENSE = ROOT / "license.html"

INDEX_REQUIRED = [
    "https://pedagogy.pennlawteaching.org",
    "https://resources.pennai.law/",
    "https://pennai.law/toolkit/",
    "assets/penn-shield.png",
    "Academic Affairs &amp; Innovation",
    "EB+Garamond",
    "DM+Sans",
    "--navy: #011F5B",
    "--cream: #FAF8F3",
]

LICENSE_REQUIRED = [
    "creativecommons.org/licenses/by/4.0/",
    "apache.org/licenses/LICENSE-2.0",
    "pennlawteaching.org",
]

# Penn WCAG 2.2 AA baseline — every page carries these.
ACCESSIBILITY_REQUIRED = [
    ('<html lang="en">', "page language"),
    ('class="skip-link" href="#main"', "skip link"),
    ('id="main"', "main landmark"),
    ("tabindex=\"-1\"", "focusable main target"),
    (":focus-visible", "visible focus indicator"),
    ("prefers-reduced-motion", "reduced-motion support"),
    ("accessibility.web-resources.upenn.edu", "accessibility contact"),
]

# Every page links to the license and shows the copyright line.
FOOTER_REQUIRED = [
    'href="license.html"',
    "CC BY 4.0",
    "The Trustees of the University of Pennsylvania",
]

BANNED = [
    "ai-teaching-lab.org",
    "polkwagner.github.io",
    "Deputy Dean's Office",
]


def check(path: pathlib.Path, required: list, errors: list) -> str:
    if not path.exists():
        errors.append(f"{path.name} not found")
        return ""
    text = path.read_text(encoding="utf-8")

    for needle in required:
        if needle not in text:
            errors.append(f"{path.name}: missing {needle}")

    for needle, label in ACCESSIBILITY_REQUIRED:
        if needle not in text:
            errors.append(f"{path.name}: missing {label} ({needle})")

    for needle in FOOTER_REQUIRED:
        if needle not in text:
            errors.append(f"{path.name}: footer missing {needle}")

    for needle in BANNED:
        if needle in text:
            errors.append(f"{path.name}: contains banned string {needle}")

    for anchor in re.findall(r"<a\b[^>]*>", text):
        if 'target="_blank"' in anchor and 'rel="noopener"' not in anchor:
            errors.append(f"{path.name}: target=_blank without rel=noopener: {anchor}")

    # Decorative vs meaningful images both need an alt attribute.
    for img in re.findall(r"<img\b[^>]*>", text):
        if "alt=" not in img:
            errors.append(f"{path.name}: img without alt: {img}")

    return text


def validate() -> None:
    errors: list = []

    index_text = check(INDEX, INDEX_REQUIRED, errors)
    check(LICENSE, LICENSE_REQUIRED, errors)

    if index_text and '<link rel="canonical" href="https://pennlawteaching.org/">' not in index_text:
        errors.append("index.html: missing or wrong canonical link")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        sys.exit(1)
    print("hub validation passed (index.html, license.html)")


if __name__ == "__main__":
    validate()
