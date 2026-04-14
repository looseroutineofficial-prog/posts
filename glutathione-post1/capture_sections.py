"""
글루타치온 Post1 — 섹션별 고화질 PNG 캡처
deviceScaleFactor=3 → 1170px (3x Retina)
"""
from playwright.sync_api import sync_playwright
import os, time

BASE_DIR = r"C:\Users\ozcre\07-clients\04-루즈루틴\02-tasks\03-content\08-glutathione-post1"
OUTPUT   = os.path.join(BASE_DIR, "sections")
os.makedirs(OUTPUT, exist_ok=True)

HTML_PATH = os.path.join(BASE_DIR, "glutathione_post1.html")
URL = "file:///" + HTML_PATH.replace("\\", "/")

# (selector, nth, name)  — section:nth-child(4) GIF은 capture_gif_sections.py에서 처리
SECTIONS = [
    ("section.hero",            0, "01_hero"),
    ("section:nth-child(2)",    0, "02_cause"),
    ("section:nth-child(3)",    0, "03_intro"),
    # section:nth-child(4) = 메커니즘 GIF → capture_gif_sections.py
    ("section:nth-child(5)",    0, "05_white_tomato"),
    ("section:nth-child(6)",    0, "06_hangover"),
    ("section:nth-child(7)",    0, "07_reduced_compare"),
    ("section.reviews",         0, "08_reviews"),
    ("section.product-section", 0, "09_product"),
    ("section.cta-section",     0, "10_cta"),
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
