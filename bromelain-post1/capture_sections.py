"""
브로멜라인 Post1 — 섹션별 고화질 PNG 캡처
deviceScaleFactor=3 → 1170px (3x Retina)
"""
from playwright.sync_api import sync_playwright
import os, time

BASE_DIR = r"C:\Users\ozcre\07-clients\04-루즈루틴\02-tasks\03-content\07-bromelain-post1"
OUTPUT   = os.path.join(BASE_DIR, "sections")
os.makedirs(OUTPUT, exist_ok=True)

HTML_PATH = os.path.join(BASE_DIR, "bromelain_post1.html")
URL = "file:///" + HTML_PATH.replace("\\", "/")

# (selector, nth, name)  — 8번째 섹션(메커니즘)은 GIF로 별도 캡처
SECTIONS = [
    ("section.hero",          0, "01_hero"),
    ("section:nth-child(2)",  0, "02_pain_prep"),
    ("section:nth-child(3)",  0, "03_pain_calorie"),
    ("section:nth-child(4)",  0, "04_pain_taste"),
    ("section:nth-child(5)",  0, "05_pineapple_hook"),
    ("section:nth-child(6)",  0, "06_pineapple_stem"),
    ("section:nth-child(7)",  0, "07_pineapple_heat"),
    # section:nth-child(8) = 메커니즘 → capture_gif_sections.py 에서 처리
    ("section:nth-child(9)",  0, "09_compare"),
    ("section:nth-child(10)", 0, "10_quercetin"),
    ("section.reviews",       0, "11_reviews"),
    ("section.product-section", 0, "12_product"),
    ("section.cta-section",   0, "13_cta"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(
        viewport={"width": 390, "height": 844},
        device_scale_factor=3,
    )
    page.goto(URL, wait_until="networkidle")
    time.sleep(2)

    for selector, nth, name in SECTIONS:
        try:
            el = page.locator(selector).nth(nth)
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
    print("done ->", OUTPUT)
