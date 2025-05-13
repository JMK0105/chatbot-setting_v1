# 📁 utils/gpt_helper.py
import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text_to_slides(text, instruction):
    messages = [
        {"role": "system", "content": "당신은 교육 세션, 리더십 개발, 조직성과 분석 등 전문 주제를 발표 슬라이드로 설계하는 교육 콘텐츠 디자이너입니다."},
        {"role": "user", "content": f"{instruction}\n\n{text}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=2000
    )
    return response.choices[0].message.content


def parse_structured_slides(gpt_response):
    slides = []
    title_kr_global = ""
    title_en_global = ""
    slide_blocks = gpt_response.strip().split("[슬라이드")
    for block in slide_blocks[1:]:
        title_kr, title_en, content, keywords = "", "", "", ""
        lines = block.splitlines()
        for line in lines:
            if line.startswith("제목:"):
                title_kr = line.replace("제목:", "").strip()
                if not title_kr_global:
                    title_kr_global = title_kr
            elif line.startswith("영문제목:"):
                title_en = line.replace("영문제목:", "").strip()
                if not title_en_global:
                    title_en_global = title_en
            elif line.startswith("내용:"):
                content = line.replace("내용:", "").strip()
            elif line.startswith("키워드:"):
                keywords = line.replace("키워드:", "").strip()
        slides.append({
            "title_kr": title_kr_global,
            "title_en": title_en_global,
            "content": content,
            "keywords": keywords
        })
    return slides
