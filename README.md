# 📝 Velog Backup Automation with GitHub Actions

이 저장소는 [Velog](https://velog.io)에서 작성한 게시글을  
GraphQL API를 통해 자동으로 수집하고,  
마크다운(.md) 형식으로 저장소에 커밋하는 자동화 시스템입니다.

> Velog 블로그 글 → GitHub `posts/` 폴더에 자동 저장 (이미지 제외)  
> 매일 오전 9시에 GitHub Actions로 자동 실행됩니다.

---

## ✅ 기능 소개

- 📥 Velog GraphQL API로 내 글 목록 및 본문 수집
- 📄 각 글을 마크다운 파일로 저장 (`posts/` 디렉토리)
- 🔁 GitHub Actions로 매일 자동 실행 및 커밋
- 🕹 수동 실행도 가능 (workflow_dispatch)

---

## 🛠 사용 기술

- Python (requests)
- GitHub Actions (자동화 스케줄링)
- GraphQL (Velog 비공식 API 활용)

---

## 📁 디렉토리 구조
```
.
├── posts/ # Velog에서 가져온 마크다운 파일 저장 경로
├── scripts/
│ └── update_blog.py # 자동 수집 및 저장 스크립트
└── .github/workflows/
  └── update.yml # GitHub Actions 워크플로우 설정
```
---

## ⚙️ 자동화 주기 설정

- `update.yml` 내 cron 스케줄:
  - 매일 오전 9시 (KST) 실행
  - 필요 시 수동 실행 가능 (Actions 탭 → Run workflow)

---

## 🔐 GitHub Token 설정 방법

1. [Personal Access Token (classic)](https://github.com/settings/tokens) 생성  
   권한: `repo`
2. 해당 토큰을 저장소 → Settings → `Actions > Secrets`에 등록  
   이름: `GH_PAT`

---

## 📌 참고사항

- 현재는 글 본문만 수집하며, 이미지 렌더링은 마크다운 형식(`body`) 기준입니다.
- Velog GraphQL API는 비공식 API로, 스키마 변경 시 수정이 필요할 수 있습니다.

---

## 👤 작성자

- GitHub: [@Sondanha](https://github.com/Sondanha)
- Velog: [@sksmsdbs](https://velog.io/@son-dan-ha)
