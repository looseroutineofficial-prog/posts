"""
이지컷 Concept2 — WHY 섹션 고화질 GIF 캡처
deviceScaleFactor=3 + 팔레트 256색 풀 품질
"""
from playwright.sync_api import sync_playwright
from PIL import Image
import io, time, os

BASE_DIR = r"C:\Users\ozcre\07-clients\04-루즈루틴\02-tasks\03-content\04-concept2"
OUTPUT   = os.path.join(BASE_DIR, "sections")
os.makedirs(OUTPUT, exist_ok=True)

HTML_PATH = os.path.join(BASE_DIR, "easycut_concept2.html")
URL      = "file:///" + HTML_PATH.replace("\\", "/")
SELECTOR = "section.why-section"

DURATION_SEC = 5
FPS          = 8
FRAME_DELAY  = 1000 // FPS

frames = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(
        viewport={"width": 390, "height": 844},
        device_scale_factor=3
    )
    page.goto(URL, wait_until="networkidle")
    time.sleep(1)

    el = page.locator(SELECTOR).first
    el.scroll_into_view_if_needed()
    time.sleep(1)

    total_frames = DURATION_SEC * FPS
    interval = 1.0 / FPS

    print(f"Capturing {total_frames} frames at {FPS}fps (3x scale)...")
    for i in range(total_frames):
        raw = el.screenshot()
        img = Image.open(io.BytesIO(raw)).convert("RGBA")
        frames.append(img)
        time.sleep(interval)
        if (i + 1) % FPS == 0:
            print(f"  {i+1}/{total_frames} frames")

    browser.close()

out_path = os.path.join(OUTPUT, "03_why_mechanism.gif")
palette_frames = [f.convert("P", palette=Image.ADAPTIVE, colors=256) for f in frames]
palette_frames[0].save(
    out_path,
    save_all=True,
    append_images=palette_frames[1:],
    optimize=False,
    duration=FRAME_DELAY,
    loop=0,
)

size_kb = os.path.getsize(out_path) // 1024
print(f"\n저장 완료 -> {out_path}")
print(f"크기: {size_kb} KB")
