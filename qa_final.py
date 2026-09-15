from playwright.sync_api import sync_playwright

results = []
JS = """() => ({
    scrollW: document.documentElement.scrollWidth,
    winW: window.innerWidth,
    h1: (document.querySelector('h1') || {}).textContent || '',
    imgsLoaded: [...document.querySelectorAll('img')].filter(i => i.complete && i.naturalWidth > 0).length,
    imgsTotal: document.querySelectorAll('img').length,
    emptySrc: [...document.querySelectorAll("img[src='']")].length,
    noOverflow: document.documentElement.scrollWidth <= window.innerWidth
})"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    pages = [('Home','/'), ('Garden','/garden-town.html'), ('Masoom','/masoom-shah-road.html'), ('Railway','/railway-road.html'), ('About','/about.html'), ('Privacy','/privacy.html'), ('404','/404.html')]
    viewports = [('320x780',(320,780)),('390x844',(390,844)),('768x1024',(768,1024)),('1920x1000',(1920,1000))]
    for pg_name, pg_path in pages:
        for vp_name, (w, h) in viewports:
            page = browser.new_page(viewport={'width':w, 'height':h})
            try:
                page.goto('https://cuts-curves-ten.vercel.app'+pg_path, wait_until='networkidle', timeout=15000)
                page.wait_for_timeout(400)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(800)
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(300)
                doc = page.evaluate(JS)
                real_broken = doc['imgsTotal'] - doc['imgsLoaded'] - doc['emptySrc']
                status = 'OK' if doc['noOverflow'] and real_broken <= 0 else 'FAIL'
                results.append({'page': pg_name, 'vp': vp_name, 'status': status, 'overflow': doc['noOverflow'], 'imgs': '%d/%d' % (doc['imgsLoaded'], doc['imgsTotal']), 'emptySrc': doc['emptySrc'], 'realBroken': real_broken})
            except Exception as e:
                results.append({'page': pg_name, 'vp': vp_name, 'status': 'ERROR', 'error': str(e)[:50]})
            page.close()
    browser.close()

print('%-12s %-10s %-5s %-9s %-6s %-6s' % ('PAGE', 'VIEWPORT', 'PASS', 'IMAGES', 'EMPTY', 'REALBK'))
print('-' * 64)
ok_count = sum(1 for r in results if r['status'] == 'OK')
for r in results:
    flag = 'YES' if r['status'] == 'OK' else 'NO'
    print('%-12s %-10s %-5s %-9s %-6s %-6s' % (r['page'], r['vp'], flag, r.get('imgs','?'), r.get('emptySrc','?'), r.get('realBroken','?')))
print('-' * 64)
print('TOTAL: %d/%d PASSED' % (ok_count, len(results)))
