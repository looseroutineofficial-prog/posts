"""
WHY 섹션 애니메이션 GIF 캡처
"""
from playwright.sync_api import sync_playwright
from PIL import Image
import io, time, os

OUTPUT = r"C:\Users\ozcre\07-clients\04-루즈루틴\02-tasks\03-content\04-output\sections"
URL = "http://localhost:8768/easycut_concept1_v2.html"

SELECTOR = "section.why-section"
DURATION_SEC = 4      # 총 녹화 시간
FPS = 8               # 초당 프레임
FRAME_DELAY = 1000 // FPS  # ms per frame (GIF용)

frames = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto(URL, wait_until="networkidle")
    time.sleep(0.5)

    el = page.locator(SELECTOR).first
    el.scroll_into_view_if_needed()
    time.sleep(0.5)  # GIF 애니메이션 시작 대기

    total_frames = DURATION_SEC * FPS
    interval = 1.0 / FPS

    print(f"Capturing {total_frames} frames at {FPS}fps...")
    for i in range(total_frames):
        raw = el.screenshot()
        img = Image.open(io.BytesIO(raw)).convert("RGBA")
        frames.append(img)
        time.sleep(interval)
        if (i + 1) % FPS == 0:
            print(f"  {i+1}/{total_frames}")

    browser.close()

# GIF 저장
out_path = os.path.join(OUTPUT, "03_why_mechanism.gif")
# 팔레트로 변환해서 용량 절감
palette_frames = [f.convert("P", palette=Image.ADAPTIVE, colors=128) for f in frames]
palette_frames[0].save(
    out_path,
    save_all=True,
    append_images=palette_frames[1:],
    optimize=True,
    duration=FRAME_DELAY,
    loop=0,
)
print(f"Saved -> {out_path}")
size_kb = os.path.getsize(out_path) // 1024
print(f"Size: {size_kb} KB")
