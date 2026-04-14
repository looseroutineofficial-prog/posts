"""
글루타치온 Post1 — GIF 섹션 캡처 (10MB 이하)
04_mechanism (VB4 메커니즘 GIF)
deviceScaleFactor=2 → 780px
"""
from playwright.sync_api import sync_playwright
from PIL import Image
import io, time, os

BASE_DIR = r"C:\Users\ozcre\07-clients\04-루즈루틴\02-tasks\03-content\08-glutathione-post1"
OUTPUT   = os.path.join(BASE_DIR, "sections")
os.makedirs(OUTPUT, exist_ok=True)

HTML_PATH = os.path.join(BASE_DIR, "glutathione_post1.html")
URL = "file:///" + HTML_PATH.replace("\\", "/")

# (selector, nth, name, duration_sec, fps)
GIF_SECTIONS = [
    ("section:nth-child(4)", 0, "04_mechanism", 4, 8),
]

with sync_playwright() as p:
    browser = p.chromium.launch()

    for selector, nth, name, duration_sec, fps in GIF_SECTIONS:
        page = browser.new_page(
            viewport={"width": 390, "height": 844},
            device_scale_factor=2,
        )
        page.goto(URL, wait_until="networkidle")
        time.sleep(1.5)

        el = page.locator(selector).nth(nth)
        el.wait_for(timeout=5000)
        el.scroll_into_view_if_needed()
        time.sleep(1.0)

        total_frames = duration_sec * fps
        interval = 1.0 / fps
        frame_delay_ms = 1000 // fps

        frames = []
        for i in range(total_frames):
            raw = el.screenshot()
            img = Image.open(io.BytesIO(raw)).convert("RGBA")
            frames.append(img)
            time.sleep(interval)

        page.close()

        out_path = os.path.join(OUTPUT, f"{name}.gif")
        palette_frames = [f.convert("P", palette=Image.ADAPTIVE, colors=128) for f in frames]
        palette_frames[0].save(
            out_path,
            save_all=True,
            append_images=palette_frames[1:],
            optimize=True,
            duration=frame_delay_ms,
            loop=0,
        )
        size_kb = os.path.getsize(out_path) // 1024
        size_mb = size_kb / 1024
        status = "OK" if size_mb < 10 else "WARNING >10MB"
        print(f"{status}  {name}.gif  ({size_mb:.1f} MB)")

    browser.close()
    print("done ->", OUTPUT)
