from playwright.sync_api import sync_playwright

JS = """() => {
    return [...document.querySelectorAll('img')].map((img, i) => ({
        i: i,
        src: img.getAttribute('src'),
        currentSrc: img.currentSrc,
        complete: img.complete,
        naturalWidth: img.naturalWidth,
        ok: img.complete && img.naturalWidth > 0,
        cls: img.className,
        parent: img.parentElement ? img.parentElement.className : ''
    }))
}"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for path in ['/garden-town.html', '/masoom-shah-road.html', '/railway-road.html', '/']:
        page = browser.new_page(viewport={'width': 1920, 'height': 1000})
        page.goto('https://cuts-curves-ten.vercel.app' + path, wait_until='networkidle')
        page.wait_for_timeout(500)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
        imgs = page.evaluate(JS)
        broken = [i for i in imgs if not i['ok']]
        print(path, '- total:', len(imgs), 'broken:', len(broken))
        for b in broken:
            print('  [%d] src=%s currentSrc=%s cls=%s parent=%s' % (b['i'], b['src'], b['currentSrc'], b['cls'], b['parent']))
        page.close()
    browser.close()
