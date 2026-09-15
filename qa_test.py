"""Comprehensive visual/QA test for cuts-curves-ten.vercel.app - 7 pages x 4 viewports."""
from playwright.sync_api import sync_playwright
import json

BASE = "https://cuts-curves-ten.vercel.app"
PAGES = {
    "/": "Home",
    "/garden-town.html": "Garden Town",
    "/masoom-shah-road.html": "Masoom Shah Road",
    "/railway-road.html": "Railway Road",
    "/about.html": "About",
    "/privacy.html": "Privacy",
    "/404.html": "404",
}
VIEWPORTS = {'mobile320': (320, 780), 'mobile390': (390, 844), 'tablet768': (768, 1024), 'desktop1920': (1920, 1000)}

GREEN, RED, YELLOW = '\033[92m', '\033[91m', '\033[93m'
RESET = '\033[0m'

def report(f):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for page_path, page_name in PAGES.items():
            for vp_name, (w, h) in VIEWPORTS.items():
                page = browser.new_page(viewport={'width': w, 'height': h})
                console_errors = []
                page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
                failed_requests = []
                page.on('requestfailed', lambda req: failed_requests.append(req.url))

                url = BASE + page_path
                try:
                    r = page.goto(url, wait_until='networkidle', timeout=20000)
                    page.wait_for_timeout(800)
                except Exception as e:
                    f.write(f"[FAIL] {page_name} {vp_name}: load error {e}\n")
                    page.close()
                    continue

                status = r.status if r else 999
                try:
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(1200)
                    for _ in range(3):
                        page.evaluate("window.scrollBy(0, -400)")
                        page.wait_for_timeout(120)
                except Exception:
                    pass
                doc = page.evaluate("""() => ({
                    scrollW: document.documentElement.scrollWidth,
                    winW: window.innerWidth,
                    imgs: [...document.images].map(i => ({
                        src: i.currentSrc || i.src,
                        ok: i.complete && i.naturalWidth > 0,
                        nw: i.naturalWidth
                    })),
                    cardsOverflow: [...document.querySelectorAll('.card,.branch,.pane')].map(c => ({w: c.scrollWidth, cw: c.clientWidth})).filter(x => x.w > x.cw + 1).length,
                    h1: document.querySelector('h1')?.textContent?.trim() || '',
                    title: document.title
                })""")
                no_overflow = doc['scrollW'] <= doc['winW']
                broken = [i['src'] for i in doc['imgs'] if not i['ok']]
                real_console_errors = [e for e in console_errors if 'favicon' not in e]

                ok = status == 200 and no_overflow and not broken and not real_console_errors
                flag = GREEN + "OK " + RESET if ok else RED + "FAIL" + RESET
                f.write(f"{flag} {page_name:18s} {vp_name:12s} status={status} overflow={'NO' if no_overflow else 'YES'} brokenImg={len(broken)} consoleErr={len(real_console_errors)}\n")
                if broken:
                    for b in broken:
                        f.write("         broken: " + b[:100] + "\n")
                if real_console_errors:
                    for e in real_console_errors[:3]:
                        f.write("         console: " + e[:100] + "\n")
                results.append({'page': page_name, 'vp': vp_name, 'ok': ok})
                page.close()

        # Interaction tests (desktop)
        f.write("\n=== INTERACTION TESTS (desktop 1280x900) ===\n")
        page = browser.new_page(viewport={'width': 1280, 'height': 900})
        page.goto(BASE + "/", wait_until='networkidle')
        page.wait_for_timeout(800)

        # Fee tabs on home
        try:
            tabs = page.locator('.fee-tab, [data-tab], .tab')
            f.write(f"Fee tabs found: {tabs.count()}\n")
        except Exception as e:
            f.write(f"Fee tabs err: {e}\n")

        # Lightbox on home gallery (if any)
        gal_imgs = page.locator('.gal img, .gallery img')
        if gal_imgs.count() > 0:
            try:
                gal_imgs.first.click()
                page.wait_for_timeout(400)
                lb = page.locator('.lb, .lightbox, [class*=lightbox], [id*=lightbox]')
                f.write(f"Lightbox detected: {lb.count() > 0}\n")
                if lb.count() > 0:
                    page.keyboard.press('Escape')
                    page.wait_for_timeout(300)
                    f.write(f"Lightbox closed via Esc: {lb.first.is_visible() == False}\n")
            except Exception as e:
                f.write(f"Lightbox test err: {e}\n")

        # Branch page fee structure (masoom)
        page.goto(BASE + "/masoom-shah-road.html", wait_until='networkidle')
        page.wait_for_timeout(600)
        fee_blocks = page.locator('.fee-block')
        f.write(f"Masoom fee blocks: {fee_blocks.count()}\n")
        wa_links = page.locator("a[href*='wa.me']")
        f.write(f"Masoom WhatsApp links: {wa_links.count()}\n")

        # Reviews sections
        page.goto(BASE + "/", wait_until='networkidle')
        page.wait_for_timeout(600)
        reviews = page.locator('.rev .rv, .reviews .rv, [class*=review]')
        f.write(f"Home review cards: {reviews.count()}\n")

        # Mobile menu
        page.set_viewport_size({'width': 390, 'height': 844})
        page.goto(BASE + "/", wait_until='networkidle')
        page.wait_for_timeout(600)
        try:
            menu_btn = page.locator('button[aria-label*=menu], .menu-btn, #menu-btn, [id*=menu]')
            if menu_btn.count() > 0:
                menu_btn.first.click()
                page.wait_for_timeout(400)
                menu_visible = page.evaluate("getComputedStyle(document.body).overflow")
                f.write(f"Mobile menu opens, body overflow lock: {menu_visible}\n")
        except Exception as e:
            f.write(f"Mobile menu test err: {e}\n")

        page.close()

        # Screenshots for visual review
        f.write("\n=== SCREENSHOTS SAVED ===\n")
        for page_path, page_name in PAGES.items():
            pg = browser.new_page(viewport={'width': 390, 'height': 844})
            pg.goto(BASE + page_path, wait_until='networkidle')
            pg.wait_for_timeout(500)
            pg.screenshot(path=f"C:\\Users\\chzar\\cuts-curves\\qa\\{page_name}-390.png", full_page=False)
            pg.close()
        # Desktop home
        pg = browser.new_page(viewport={'width': 1920, 'height': 1000})
        pg.goto(BASE + "/", wait_until='networkidle')
        pg.wait_for_timeout(700)
        pg.screenshot(path="C:\\Users\\chzar\\cuts-curves\\qa\\Home-desktop.png", full_page=True)
        pg.close()

        browser.close()

    passed = sum(1 for r in results if r['ok'])
    f.write(f"\n=== SUMMARY: {passed}/{len(results)} combos passed ===\n")

with open(r"C:\Users\chzar\cuts-curves\qa\QA-REPORT.txt", "w", encoding="utf-8") as f:
    report(f)
print("QA report written")