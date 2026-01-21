# DeepSeek-OCR: Contextual Optical Compression 논문리뷰

📅 2026-01-20T14:43:16.113Z

🔗 [원문 링크](https://velog.io/@son-dan-ha/DeepSeek-OCR-Contextual-Optical-Compression-논문리뷰)

---

![](https://velog.velcdn.com/images/son-dan-ha/post/a53de6ed-9442-4538-88a5-1cdd07ac2c65/image.png)
# 1. Introduction

DeepSeek-OCR 논문은 기존 **OCR 및 VLM 기반** 문서 이해 모델들이 **시각 토큰 수**가 과도하게 많다는 문제의식에서 출발한다. 고해상도 문서 이미지를 그대로 토큰화하면, 모델은 불필요한 시각 정보까지 처리해야 하고 이는 곧 <u>비용 증가</u>와 <u>추론 지연</u>으로 이어진다.

저자들은 이 문제를 단순히 “모델을 더 크게” 혹은 “토큰을 줄이자”로 접근하지 않는다. 대신, **문맥적으로 중요한 시각 정보만 남기고 나머지는 압축**할 수 있지 않을까? 라는 질문을 던진다.

이 부분을 읽으면서 나는 기존 OCR 파이프라인이 사실상 **이미지 → 텍스트 변환**에만 집중해 왔고, 이미지 자체를 정보 압축의 대상으로 본 **시각은 상대적으로 적었다**는 점을 다시 생각하게 됐다.

<br><br>

---
