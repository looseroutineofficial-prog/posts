"""
골든밀크 Post1 — 섹션별 고화질 PNG 캡처
deviceScaleFactor=3 → 1170px (3x Retina)
"""
from playwright.sync_api import sync_playwright
import os, time

BASE_DIR = r"C:\Users\ozcre\07-clients\04-루즈루틴\02-tasks\03-content\06-goldenmilk-post1"
OUTPUT   = os.path.join(BASE_DIR, "sections")
os.makedirs(OUTPUT, exist_ok=True)

HTML_PATH = os.path.join(BASE_DIR, "goldenmilk_post1.html")
URL = "file:///" + HTML_PATH.replace("\\", "/")

SECTIONS = [
    ("section.hero",                          "01_hero",         0),
    ("section:nth-child(2)",                  "02_empathy",      0),
    ("section:nth-child(3)",                  "03_curcumin",     0),
    ("section.twist-section",                 "04_twist",        0),
    ("section:nth-child(5)",                  "05_bromelain",    0),
    ("section:nth-child(6)",                  "06_compare",      0),
    ("section:nth-child(7)",                  "07_synergy",      0),
    ("section.reviews",                       "08_reviews",      0),
    ("section.product-section",               "09_product",      0),
    ("section.cta-section",                   "10_cta",          0),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(
        viewport={"width": 390, "height": 844},
        device_scale_factor=3,
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
    print("done ->", OUTPUT)
