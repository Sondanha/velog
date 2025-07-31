import os         
import re
import requests

# ===[ 설정 항목 ]===
USERNAME = "son-dan-ha"  # Velog 사용자명 (@ 없이)
GRAPHQL_ENDPOINT = "https://v2.velog.io/graphql"
OUTPUT_DIR = "posts"   # 글을 저장할 폴더 이름


# ===[ GraphQL 쿼리: 글 목록 (제목, 슬러그, 날짜) 요청 ]===
POSTS_QUERY = """
query Posts($username: String!) {
  posts(username: $username) {
    title
    url_slug
    released_at
  }
}
"""

# ===[ GraphQL 쿼리: 개별 글의 전체 본문(HTML 포함) 요청 ]===
POST_BODY_QUERY = """
query Post($username: String!, $url_slug: String!) {
  post(username: $username, url_slug: $url_slug) {
    body_html
  }
}
"""

# ===[ 파일명으로 사용할 수 있도록 슬러그 처리 ]===
def slugify(text):
    return text.replace(" ", "-").replace("/", "-").lower()

# ===[ GraphQL로 글 목록 가져오기 ]===
def fetch_posts(username):
    res = requests.post(
        GRAPHQL_ENDPOINT,
        json={"query": POSTS_QUERY, "variables": {"username": username}},
        headers={"Content-Type": "application/json"},
    )
    res.raise_for_status()
    return res.json()["data"]["posts"]


# ===[ GraphQL로 개별 글 본문(HTML) 가져오기 ]===
def fetch_post_body(username, slug):
    res = requests.post(
        GRAPHQL_ENDPOINT,
        json={
            "query": POST_BODY_QUERY,
            "variables": {"username": username, "url_slug": slug},
        },
        headers={"Content-Type": "application/json"},
    )

    if res.status_code != 200:
        print("❌ GraphQL 요청 실패:")
        print("Status Code:", res.status_code)
        print("Response:", res.text)
        print("Username:", username, "Slug:", slug)

    res.raise_for_status()
    return res.json()["data"]["post"]["body_html"]



# ===[ 마크다운 파일로 저장하기 ]===
def save_as_markdown(posts, username):
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # posts/ 디렉토리 생성 (없으면 새로)

    for post in posts:
        title = post["title"]
        slug = post["url_slug"]
        print(f"📄 처리 중: {title} ({slug})")
        date = post["released_at"]
        url = f"https://velog.io/@{username}/{slug}"

        # 개별 글 본문 HTML 가져오기
        try:
            body_html = fetch_post_body(username, slug)
        except Exception as e:
            print(f"⚠️ {slug} 가져오기 실패: {e}")
            continue

        # 저장할 파일 경로 생성
        filename = f"{slugify(slug)}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)

        # 마크다운 형식으로 저장 (HTML 포함)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")               # 제목
            f.write(f"📅 {date}\n\n")               # 작성일
            f.write(f"🔗 [원문 링크]({url})\n\n")   # 링크
            f.write("---\n\n")
            f.write(body_html)                       # HTML 본문 (이미지 포함)

    print(f"✅ {len(posts)} posts saved to ./{OUTPUT_DIR}")


# ===[ 실행 진입점 ]===
if __name__ == "__main__":
    posts = fetch_posts(USERNAME)               # Velog 글 목록 불러오기
    save_as_markdown(posts, USERNAME)           # 글마다 마크다운 파일로 저장

if __name__ == "__main__":
    main()
