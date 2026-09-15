from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for pg in ['/garden-town.html', '/masoom-shah-road.html', '/railway-road.html', '/']:
        page = browser.new_page(viewport={'width':1920,'height':1000})
        page.goto('https://cuts-curves-ten.vercel.app'+pg, wait_until='networkidle')
        page.wait_for_timeout(500)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
        result = page.evaluate("""() => {
            return [...document.querySelectorAll('img')].map((i,idx) => ({
                idx: idx,
                src: i.src || '(empty)',
                ok: i.complete && i.naturalWidth > 0,
                w: i.naturalWidth,
                lazy: i.loading
            }))
        }""")
        broken = [i for i in result if not i['ok']]
        print(pg, '- total imgs:', len(result), 'broken:', len(broken))
        for b in broken:
            print('  [%d] src=%s loaded=%s lazy=%s' % (b['idx'], b['src'], b['w'], b['lazy']))
        page.close()
    browser.close()
