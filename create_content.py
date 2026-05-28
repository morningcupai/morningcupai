#!/usr/bin/env python3
"""
Creates a master content folder for one newsletter issue, pre-populated
with structured templates for every channel.

Usage:
    python3 create_content.py
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


def header(title: str, pillar: str, topic: str, ts: datetime) -> str:
    created = ts.strftime("%Y-%m-%d at %H:%M")
    return (
        f"================================\n"
        f"{title}\n"
        f"================================\n"
        f"Created: {created}\n"
        f"Pillar: {pillar}\n"
        f"Topic: {topic}\n"
        f"--------------------------------\n"
    )


# ── templates ─────────────────────────────────────────────────────────────────

def content_brief(pillar: str, topic: str, ts: datetime) -> str:
    return (
        header("CONTENT BRIEF", pillar, topic, ts) +
        "Key Message: [write the core message here]\n"
        "Target Emotion: [what should the reader feel?]\n"
        "Notes: [any additional notes]\n"
        "================================\n"
    )


def newsletter(pillar: str, topic: str, ts: datetime) -> str:
    return (
        header("THE AI COMPANION — NEWSLETTER DRAFT", pillar, topic, ts) +
        "SUBJECT LINE:\n"
        "[write your subject line here — curiosity driven, plain English, no clickbait]\n"
        "\n"
        "OPENING HOOK:\n"
        "[write 2 to 3 warm sentences here — like writing to a friend]\n"
        "\n"
        "MAIN TOPIC:\n"
        "[write 300 to 400 words here — one clear idea, plain English, one practical takeaway at the end]\n"
        "\n"
        "THIS WEEKS PROMPT:\n"
        "[write a copy-paste prompt the reader can drop directly into ChatGPT or Claude]\n"
        "\n"
        "SCAM WATCH:\n"
        "[write 2 to 3 sentences about a current AI scam or risk relevant to adults 55+]\n"
        "\n"
        "CLOSING:\n"
        "[write a warm encouraging closing paragraph]\n"
        "Your AI Neighbor\n"
        "================================\n"
    )


def facebook_post(pillar: str, topic: str, ts: datetime, num: int) -> str:
    angle_note = {
        2: " — different angle from post 1",
        3: " — different angle from posts 1 and 2",
    }.get(num, "")
    return (
        header(f"FACEBOOK POST {num}", pillar, topic, ts) +
        "HOOK:\n"
        f"[write an attention grabbing first line{angle_note}]\n"
        "\n"
        "BODY:\n"
        "[write 2 to 3 sentences expanding on the hook]\n"
        "\n"
        "CTA:\n"
        "[soft call to action to join the newsletter]\n"
        "================================\n"
    )


def instagram_caption(pillar: str, topic: str, ts: datetime) -> str:
    return (
        header("INSTAGRAM CAPTION", pillar, topic, ts) +
        "HOOK LINE:\n"
        "[write one punchy opening line]\n"
        "\n"
        "BODY:\n"
        "[write 3 to 4 warm sentences]\n"
        "\n"
        "HASHTAGS:\n"
        "[write 10 to 15 relevant hashtags for adults 55+ interested in AI and technology]\n"
        "================================\n"
    )


def video_script(pillar: str, topic: str, ts: datetime) -> str:
    return (
        header("VIDEO SCRIPT — 60 SECONDS", pillar, topic, ts) +
        "OPEN (5 seconds):\n"
        "[write a hook that grabs attention immediately]\n"
        "\n"
        "MAIN TIP (40 seconds):\n"
        "[write the core tip in plain conversational language — one clear actionable idea]\n"
        "\n"
        "CTA (15 seconds):\n"
        "[soft invite to join the free newsletter — where to find it]\n"
        "================================\n"
    )


def youtube_description(pillar: str, topic: str, ts: datetime) -> str:
    return (
        header("YOUTUBE DESCRIPTION", pillar, topic, ts) +
        "VIDEO TITLE:\n"
        "[write an SEO friendly title for adults 55+ searching for AI help]\n"
        "\n"
        "DESCRIPTION:\n"
        "[write 150 words in plain English describing what this video covers]\n"
        "\n"
        "TAGS:\n"
        "[write 15 to 20 relevant search tags]\n"
        "\n"
        "END SCREEN CTA:\n"
        "[write a short subscribe and newsletter CTA]\n"
        "================================\n"
    )


# ── file map ──────────────────────────────────────────────────────────────────

def build_files(pillar: str, topic: str, ts: datetime) -> dict[str, str]:
    return {
        "content_brief.txt":     content_brief(pillar, topic, ts),
        "newsletter.txt":        newsletter(pillar, topic, ts),
        "facebook_post_1.txt":   facebook_post(pillar, topic, ts, 1),
        "facebook_post_2.txt":   facebook_post(pillar, topic, ts, 2),
        "facebook_post_3.txt":   facebook_post(pillar, topic, ts, 3),
        "instagram_caption.txt": instagram_caption(pillar, topic, ts),
        "video_script.txt":      video_script(pillar, topic, ts),
        "youtube_description.txt": youtube_description(pillar, topic, ts),
    }


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print("\n=== The AI Neighbor — Create Content Package ===")

    ts     = datetime.now()
    pillar = pick_pillar()
    topic  = ask_topic()

    folder_name = f"{ts.strftime('%Y-%m-%d_%H-%M')}_{slugify(topic)}"
    content_dir = BASE_DIR / pillar / folder_name
    content_dir.mkdir(parents=True, exist_ok=True)

    files = build_files(pillar, topic, ts)
    for filename, body in files.items():
        (content_dir / filename).write_text(body, encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"  Content package created!")
    print(f"{'='*60}")
    print(f"\n  Pillar  : {pillar}")
    print(f"  Topic   : {topic}")
    print(f"  Created : {ts.strftime('%Y-%m-%d')} at {ts.strftime('%H:%M')}")
    print(f"\n  Folder  : {content_dir}")
    print(f"\n  Files:")
    for filename in files:
        print(f"    • {content_dir / filename}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(0)
