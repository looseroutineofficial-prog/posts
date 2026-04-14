"""
NMN Post1 — 섹션별 고화질 PNG 캡처
deviceScaleFactor=3 → 1170px (3x Retina)
"""
from playwright.sync_api import sync_playwright
import os, time

BASE_DIR = r"C:\Users\ozcre\07-clients\04-루즈루틴\02-tasks\03-content\05-nmn-post1"
OUTPUT   = os.path.join(BASE_DIR, "sections")
os.makedirs(OUTPUT, exist_ok=True)

HTML_PATH = os.path.join(BASE_DIR, "nmn_post1.html")
URL = "file:///" + HTML_PATH.replace("\\", "/")

# (selector, name, nth_index)  — nth_index: 같은 selector 중 몇 번째 (0부터)
SECTIONS = [
    ("section.hero",                 "01_hero",         0),
    ("section:nth-child(2)",         "02_symptoms",     0),
    ('section[style*="cream2"]',     "03_nad_graph",    0),
    ("section:nth-child(4)",         "04_mechanism",    0),
    ('section[style*="cream2"]',     "05_product",      1),
    ("section.reviews",              "06_reviews",      0),
    ("section.product-section",      "07_product_spec", 0),
    ("section.cta-section",          "08_cta",          0),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(
        viewport={"width": 390, "height": 844},
        device_scale_factor=3
    )
    page.goto(URL, wait_until="networkidle")
    time.sleep(2)

    for selector, name, nth in SECTIONS:
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
    print("\n완료! ->", OUTPUT)
