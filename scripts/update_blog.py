import os         
import re
import requests

# 설정 항목
USERNAME = "son-dan-ha"  # Velog 사용자명 (@ 없이)
GRAPHQL_ENDPOINT = "https://v2.velog.io/graphql"
OUTPUT_DIR = "posts"   # 글을 저장할 폴더 이름

# 글 목록을 요청하는 GraphQL 쿼리 문자열
    # query 키워드를 사용하여 데이터를 조회함. 쿼리 이름은 'Posts'.
    # '$username'은 외부에서 넘겨줄 사용자 이름(변수)이며, 타입은 String이고 반드시 있어야 함!!
    # 'posts'는 서버에서 제공하는 Query 타입의 필드.
    # 'username'이라는 인자를 통해 특정 사용자의 글 목록을 요청함.
    # 서버에서 각 글의 다음 필드(title,url_slug,released_at)를 반환하도록 요청
POSTS_QUERY = """
query Posts($username: String!) {
  posts(username: $username) {
    title
    url_slug
    released_at
  }
}
"""

# 본문을 요청하는 GraphQL 쿼리 문자열
    # query 키워드를 사용하여 특정 글의 본문을 조회함. 쿼리 이름은 'Post'
    # 'post'는 서버에서 제공하는 Query 필드.
    # username과 url_slug를 전달하여 특정 글 하나를 식별함.
    # 'body' -> 글의 전체 본문 (Markdown 형식)
POST_BODY_QUERY = """
query Post($username: String!, $url_slug: String!) {
  post(username: $username, url_slug: $url_slug) {
    body
  }
}
"""

# 파일명에 적합한 문자열 생성
def slugify(text):
    # 공백과 슬래시(/)를 하이픈(-)으로 바꾸고 소문자로 변환
    return text.replace(" ", "-").replace("/", "-").lower()

# 글 목록 가져오기
def fetch_posts(username):
    # Velog GraphQL API에 글 목록을 요청하는 POST 요청을 보냄
    res = requests.post(
        GRAPHQL_ENDPOINT, # 요청을 보낼 Velog GraphQL 서버 주소
        json={
          "query": POSTS_QUERY, 
          "variables": {"username": username}}, # 사용자명을 변수로 전달
        headers={"Content-Type": "application/json"}, # 요청 헤더 설정
    )
    res.raise_for_status()  # 요청이 실패하면 예외를 발생시킴
    
    # JSON 응답에서 글 목록 데이터만 추출하여 반환
    return res.json()["data"]["posts"]

# 글 본문 가져오기(마크다운)
def fetch_post_body(username, slug):
    # Velog GraphQL API에 특정 글의 본문(body)을 요청하는 POST 요청 수행
    res = requests.post(
        GRAPHQL_ENDPOINT,
        json={
            "query": POST_BODY_QUERY,
            "variables": {
              "username": username, 
              "url_slug": slug}, # 글의 고유 URL 슬러그
        },
        headers={"Content-Type": "application/json"}, 
    )
    # 요청이 실패(200이 아님)한 경우 상세 정보 출력
    if res.status_code != 200:
        print("❌ GraphQL 요청 실패:")              
        print("Status Code:", res.status_code)      # HTTP 상태 코드 출력
        print("Response:", res.text)                # 서버 응답 본문 출력     
        print("Username:", username, "Slug:", slug) # 요청에 사용된 값 출력

    res.raise_for_status() 
  
    # JSON 응답에서 글의 본문(body)을 추출하여 반환 (Markdown 형식)
    return res.json()["data"]["post"]["body"]


# 마크다운 파일로 저장하기
def save_as_markdown(posts, username):
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # posts/ 디렉토리 생성 (없으면 새로)

    for post in posts:
        title = post["title"]
        slug = post["url_slug"]
        # print(f"처리 중: {title} ({slug})")
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


# 실행
if __name__ == "__main__":
    posts = fetch_posts(USERNAME)      # 글 목록에 이름 넣고
    save_as_markdown(posts, USERNAME)  # 해당 내용을 저장
