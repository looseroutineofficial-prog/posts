"""
이지컷 HTML 섹션별 PNG 캡처
"""
from playwright.sync_api import sync_playwright
import os, time

OUTPUT = r"C:\Users\ozcre\07-clients\04-루즈루틴\02-tasks\03-content\04-output\sections"
os.makedirs(OUTPUT, exist_ok=True)

URL = "http://localhost:8768/easycut_concept1_v2.html"

# 섹션 selector → 파일명
SECTIONS = [
    ("section.hero",                        "01_hero"),
    ("section.story",                        "02_story_timeline"),
    ("section.why-section",                 "03_why_mechanism"),
    ('section.story[style*="cream2"]',      "04_featured_reviews"),
    ("section.solution-section",            "05_ingredients"),
    (".proof-bar",                           "06_social_proof"),
    ("section.reviews-section",             "07_reviews"),
    ("section.product-section",             "08_product"),
    ("section.cta-section",                 "09_cta"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844})  # iPhone 14 크기
    page.goto(URL, wait_until="networkidle")
    time.sleep(1)

    for selector, name in SECTIONS:
        try:
            el = page.locator(selector).first
            el.wait_for(timeout=5000)
            path = os.path.join(OUTPUT, f"{name}.png")
            el.screenshot(path=path)
            print(f"OK {name}.png")
        except Exception as e:
            print(f"FAIL {name} - {e}")

    browser.close()
    print("\n완료! →", OUTPUT)
