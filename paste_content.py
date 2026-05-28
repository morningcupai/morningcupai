#!/usr/bin/env python3
"""
Paste Claude-generated content into the terminal and have it automatically
split and saved into the correct per-pillar content folder.

Usage:
    python3 paste_content.py
"""

import re
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("AI-Neighbor")

PILLARS = [
    "health-medical",
    "scam-protection",
    "money-retirement",
    "daily-life",
    "family-connection",
    "learning-sharpness",
    "tech-literacy",
    "travel-lifestyle",
]

SECTIONS = [
    "NEWSLETTER",
    "FACEBOOK_POST_1",
    "FACEBOOK_POST_2",
    "FACEBOOK_POST_3",
    "INSTAGRAM_CAPTION",
    "VIDEO_SCRIPT",
    "YOUTUBE_DESCRIPTION",
    "CONTENT_BRIEF",
]

FILENAMES = {
    "NEWSLETTER":          "newsletter.txt",
    "FACEBOOK_POST_1":     "facebook_post_1.txt",
    "FACEBOOK_POST_2":     "facebook_post_2.txt",
    "FACEBOOK_POST_3":     "facebook_post_3.txt",
    "INSTAGRAM_CAPTION":   "instagram_caption.txt",
    "VIDEO_SCRIPT":        "video_script.txt",
    "YOUTUBE_DESCRIPTION": "youtube_description.txt",
    "CONTENT_BRIEF":       "content_brief.txt",
}


# ── helpers ───────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def pick_pillar() -> str:
    print("\nWhich pillar?\n")
    for i, pillar in enumerate(PILLARS, 1):
        print(f"  {i}. {pillar}")
    print()
    while True:
        raw = input("Enter the number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(PILLARS):
            return PILLARS[int(raw) - 1]
        print(f"  Please enter a number between 1 and {len(PILLARS)}.")


def ask_topic() -> str:
    while True:
        topic = input("\nWhat is the topic / subtopic?\n  e.g. Using AI to track medications\n\n  Topic: ").strip()
        if topic:
            return topic
        print("  Topic cannot be empty.")


def read_pasted_content() -> str:
    print('\nPaste your Claude-generated content below.')
    print('When done, type END on a new line and press Enter.\n')
    print("-" * 60)
    lines = []
    try:
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(0)
    print("-" * 60)
    return "\n".join(lines)


# ── parser ────────────────────────────────────────────────────────────────────

def parse_sections(raw: str) -> dict[str, str]:
    # Build a regex that splits on any ###SECTION_NAME### marker
    pattern = r"###(" + "|".join(re.escape(s) for s in SECTIONS) + r")###"
    parts = re.split(pattern, raw)

    # parts is: [pre-text, KEY, content, KEY, content, ...]
    sections: dict[str, str] = {}
    i = 1
    while i < len(parts) - 1:
        key     = parts[i].strip()
        content = parts[i + 1].strip()
        if key in FILENAMES:
            sections[key] = content
        i += 2

    return sections


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print("\n=== The AI Neighbor — Paste Content ===")

    ts     = datetime.now()
    pillar = pick_pillar()
    topic  = ask_topic()
    raw    = read_pasted_content()

    if not raw.strip():
        print("\nNo content detected. Nothing was saved.\n")
        sys.exit(1)

    sections = parse_sections(raw)
    if not sections:
        print("\nNo recognised section headers found.")
        print("Make sure your content uses markers like  ###NEWSLETTER###\n")
        sys.exit(1)

    folder_name = f"{ts.strftime('%Y-%m-%d_%H-%M')}_{slugify(topic)}"
    content_dir = BASE_DIR / pillar / folder_name
    content_dir.mkdir(parents=True, exist_ok=True)

    saved = []
    for key, content in sections.items():
        filename = FILENAMES[key]
        path = content_dir / filename
        path.write_text(content, encoding="utf-8")
        saved.append((filename, path))

    missing = [FILENAMES[s] for s in SECTIONS if s not in sections]

    print(f"\n{'='*60}")
    print(f"  Content package saved!")
    print(f"{'='*60}")
    print(f"\n  Pillar  : {pillar}")
    print(f"  Topic   : {topic}")
    print(f"  Created : {ts.strftime('%Y-%m-%d')} at {ts.strftime('%H:%M')}")
    print(f"\n  Folder  : {content_dir}")
    print(f"\n  Files saved ({len(saved)}):")
    for filename, path in saved:
        print(f"    • {path}")

    if missing:
        print(f"\n  Sections not found in paste ({len(missing)}) — no file created:")
        for filename in missing:
            print(f"    – {filename}")

    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(0)
