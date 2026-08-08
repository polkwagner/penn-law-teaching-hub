#!/usr/bin/env python3
"""Structural checks for the Deputy Dean hub page."""
import pathlib
import re
import sys

HTML = pathlib.Path(__file__).parent / "index.html"

REQUIRED_STRINGS = [
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

BANNED_STRINGS = [
    "ai-teaching-lab.org",
    "polkwagner.github.io",
    "Deputy Dean's Office",
]


def validate() -> None:
    if not HTML.exists():
        sys.exit("FAIL: index.html not found")
    text = HTML.read_text(encoding="utf-8")
    errors = []

    for needle in REQUIRED_STRINGS:
        if needle not in text:
            errors.append(f"missing required string: {needle}")

    for needle in BANNED_STRINGS:
        if needle in text:
            errors.append(f"contains banned string: {needle}")

    # Every new-tab link must carry rel="noopener".
    for anchor in re.findall(r"<a\b[^>]*>", text):
        if 'target="_blank"' in anchor and 'rel="noopener"' not in anchor:
            errors.append(f"target=_blank without rel=noopener: {anchor}")

    if '<link rel="canonical" href="https://pennlawteaching.org/">' not in text:
        errors.append("missing or wrong canonical link")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        sys.exit(1)
    print("hub validation passed")


if __name__ == "__main__":
    validate()
