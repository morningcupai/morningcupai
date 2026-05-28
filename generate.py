#!/usr/bin/env python3
"""
Reads draft_input.txt and saves it to the correct AI-Neighbor subfolder.

Usage:
    python3 generate.py --pillar health-medical --topic "Using AI to track medications"
"""

import argparse
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

DRAFT_FILE = Path("draft_input.txt")

SAMPLE_TEMPLATE = """\
SUBJECT LINE: {subject}

OPENING HOOK:
{opening_hook}

MAIN TOPIC:
{main_topic}

YOUR TAKEAWAY:
{takeaway}

THIS WEEK'S PROMPT:
{prompt}

SCAM WATCH:
{scam_watch}

WARM CLOSING:
{closing}

Your AI Neighbor
"""


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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Save draft_input.txt into the correct AI-Neighbor subfolder."
    )
    parser.add_argument(
        "--pillar",
        required=True,
        choices=PILLARS,
        metavar="PILLAR",
        help="Content pillar: " + ", ".join(PILLARS),
    )
    parser.add_argument(
        "--topic",
        required=True,
        help='Topic name (e.g. "Using AI to track medications")',
    )
    args = parser.parse_args()

    create_folders()

    # If no draft file exists, create a starter template and exit
    if not DRAFT_FILE.exists():
        DRAFT_FILE.write_text(SAMPLE_TEMPLATE, encoding="utf-8")
        print(f"\nNo {DRAFT_FILE} found — a starter template has been created.")
        print(f"Fill it in, then run this command again.\n")
        sys.exit(0)

    content = DRAFT_FILE.read_text(encoding="utf-8").strip()
    if not content:
        print(f"\nError: {DRAFT_FILE} is empty. Add your newsletter content and try again.\n")
        sys.exit(1)

    today = date.today().strftime("%Y-%m-%d")
    filename = f"{today}_{args.pillar}_{slugify(args.topic)}.txt"
    dest = BASE_DIR / args.pillar / "newsletters" / filename

    dest.write_text(content, encoding="utf-8")

    print(f"\nNewsletter saved:")
    print(f"  {dest}\n")


if __name__ == "__main__":
    main()
