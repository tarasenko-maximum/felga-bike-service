from playwright.sync_api import sync_playwright
URL = 'https://tarasenko-maximum.github.io/felga-bike-service/'
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width':1440,'height':950})
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(f"{m.type}: {m.text}") if m.type=='error' else None)
    pg.goto(URL, wait_until='networkidle'); pg.wait_for_timeout(1500)
    print('TITLE:', pg.title())
    print('fonts:', pg.evaluate("document.fonts.check('700 40px Unbounded')"), pg.evaluate("document.fonts.check('400 16px Manrope')"))
    pg.screenshot(path='/root/sites/felga/live-hero.png')
    pg.click('button[data-lang="ru"]'); pg.wait_for_timeout(800)
    pg.screenshot(path='/root/sites/felga/live-ru.png')
    print('RU h1:', pg.inner_text('h1').replace('\n',' | '))
    print('cta:', pg.inner_text('.nav-cta'))
    m = b.new_context(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True)
    mp = m.new_page(); mp.goto(URL, wait_until='networkidle'); mp.wait_for_timeout(1200)
    mp.screenshot(path='/root/sites/felga/live-mobile.png')
    b.close()
print('errors:', errs[:10])
