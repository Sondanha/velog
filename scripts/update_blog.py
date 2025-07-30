# feedparser: RSS 피드 파싱을 위한 외부 라이브러리
    # RSS 피드란? 
    # 블로그 글 등의 새 콘텐츠를 자동으로 외부로 전달하기 위한 XML 형식의 표준 데이터입니다. 
    # 이를 이용하면 자동 수집, 알림, 백업 등이 가능
    # 이 피드는 자동화된 프로그램(예: Feed Reader, 봇, 백엔드 등)이 읽을 수 있도록 구조화되어 있으며,
    # 웹사이트가 새글 올릴 때마다 RSS 피드가 업데이트
import feedparser 
import os         
import re

VELG_FEED_URL = "https://velog.io/rss/son-dan-ha" # Velog RSS 피드 주소
OUTPUT_DIR = "posts" # 마크다운 파일들을 저장할 디렉토리

# 제목 -> 파일명 (안전하게 바꾸려면 정규식으로 정리)
def slugify(title):
    # 영문자, 숫자, 하이픈 이외의 문자 모두 하이픈 대체 
    # 양쪽 하이픈 제거 후 소문자 변환
    return re.sub(r'[^\w\-]+', '-', title).strip('-').lower()

def main():
    # RSS 피드를 파싱하여 파이썬 객체로 변환
    feed = feedparser.parse(VELG_FEED_URL)

    if not os.path.exists(OUTPUT_DIR): # 출력 디렉토리가 존재하지 않으면,
        os.makedirs(OUTPUT_DIR)        # 새로 생성

    # 피드 항목(entries)을 순회하며 각 포스트를 파일로 저장
    for entry in feed.entries: 
        title = entry.title          # 포스트 제목
        published = entry.published  # 작성일자
        content = entry.summary      # Velog는 summary 필드에 HTML 본문이 들어있음
        link = entry.link            # 원문 링크

        # 파일 이름 생성: 제목을 슬러그 형태로 바꾸고 확장자는 .md
        filename = f"{slugify(title)}.md" # 제목 -> 파일명 함수 사용
        filepath = os.path.join(OUTPUT_DIR, filename)

        # 마크다운 형식으로 파일 작성
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"📅 {published}\n\n")
            f.write(f"🔗 [원문 링크]({link})\n\n")
            f.write("---\n\n")
            f.write(content)           # 본문 (HTML 형식 포함)

    print("✅ Velog posts updated!")

if __name__ == "__main__":
    main()
