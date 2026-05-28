#!/usr/bin/env python3
"""
Interactive tool: paste your newsletter content in the terminal and save it
to the correct AI-Neighbor subfolder automatically.

Usage:
    python3 new_issue.py
"""

import re
import sys
from datetime import date
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


def create_folders() -> None:
    for pillar in PILLARS:
        for channel in ["newsletters", "facebook", "instagram", "video-scripts"]:
            (BASE_DIR / pillar / channel).mkdir(parents=True, exist_ok=True)


def slugify(text: str) -> str:
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def pick_pillar() -> str:
    print("\nWhich pillar does this issue belong to?\n")
    for i, pillar in enumerate(PILLARS, 1):
        print(f"  {i}. {pillar}")
    print()

    while True:
        raw = input("Enter the number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(PILLARS):
            return PILLARS[int(raw) - 1]
        print(f"  Please enter a number between 1 and {len(PILLARS)}.")


def read_pasted_content() -> str:
    print("\nPaste your newsletter content below.")
    print("When finished, press Enter then Ctrl+D (Mac/Linux) or Ctrl+Z + Enter (Windows).\n")
    print("-" * 60)

    try:
        content = sys.stdin.read()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(0)

    print("-" * 60)
    return content.strip()


def main() -> None:
    print("\n=== The AI Neighbor — New Issue ===")

    create_folders()

    content = read_pasted_content()
    if not content:
        print("\nNo content detected. Nothing was saved.\n")
        sys.exit(1)

    pillar = pick_pillar()

    topic = input("\nWhat is the topic name for this issue?\n  e.g. Using AI to track medications\n\n  Topic: ").strip()
    if not topic:
        print("\nTopic cannot be empty. Nothing was saved.\n")
        sys.exit(1)

    today = date.today().strftime("%Y-%m-%d")
    filename = f"{today}_{pillar}_{slugify(topic)}.txt"
    dest = BASE_DIR / pillar / "newsletters" / filename

    dest.write_text(content, encoding="utf-8")

    print(f"\nSaved successfully!")
    print(f"  File   : {filename}")
    print(f"  Folder : {dest.parent}")
    print(f"  Path   : {dest}\n")


if __name__ == "__main__":
    main()
