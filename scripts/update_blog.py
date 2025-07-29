import feedparser
import os
import re

VELG_FEED_URL = "https://velog.io/rss/son-dan-ha"
OUTPUT_DIR = "posts"

def slugify(title):
    return re.sub(r'[^\w\-]+', '-', title).strip('-').lower()

def main():
    feed = feedparser.parse(VELG_FEED_URL)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for entry in feed.entries:
        title = entry.title
        published = entry.published
        content = entry.summary  # Velog RSS는 content:encoded가 아닌 summary에 HTML 포함
        link = entry.link
        filename = f"{slugify(title)}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"📅 {published}\n\n")
            f.write(f"🔗 [원문 링크]({link})\n\n")
            f.write("---\n\n")
            f.write(content)

    print("✅ Velog posts updated!")

if __name__ == "__main__":
    main()
