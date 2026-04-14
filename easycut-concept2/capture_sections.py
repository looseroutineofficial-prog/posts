"""
이지컷 Concept2 — 섹션별 고화질 PNG 캡처
deviceScaleFactor=3 → 실제 출력 1170px (3x Retina)
"""
from playwright.sync_api import sync_playwright
import os, time

BASE_DIR = r"C:\Users\ozcre\07-clients\04-루즈루틴\02-tasks\03-content\04-concept2"
OUTPUT   = os.path.join(BASE_DIR, "sections")
os.makedirs(OUTPUT, exist_ok=True)

HTML_PATH = os.path.join(BASE_DIR, "easycut_concept2.html")
URL = "file:///" + HTML_PATH.replace("\\", "/")

SECTIONS = [
    ("section.hero",                              "01_hero"),
    ("section.story",                             "02_story"),
    ("section.why-section",                       "03_why"),
    ("section.pivot-section",                     "04_pivot_reviews"),
    ("section.solution-section",                  "05_solution"),
    ('section.story[style*="cream2"]',            "06_product_features"),
    (".proof-bar",                                "07_social_proof"),
    ("section.reviews-section",                   "08_reviews"),
    ("section.product-section",                   "09_product"),
    ("section.cta-section",                       "10_cta"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(
        viewport={"width": 390, "height": 844},
        device_scale_factor=3
    )
    page.goto(URL, wait_until="networkidle")
    time.sleep(1.5)

    for selector, name in SECTIONS:
        try:
            el = page.locator(selector).first
            el.wait_for(timeout=5000)
            el.scroll_into_view_if_needed()
            time.sleep(0.3)
            path = os.path.join(OUTPUT, f"{name}.png")
            el.screenshot(path=path)
            size_kb = os.path.getsize(path) // 1024
            print(f"OK  {name}.png  ({size_kb} KB)")
        except Exception as e:
            print(f"FAIL {name} - {e}")

    browser.close()
    print("\n완료! ->", OUTPUT)
