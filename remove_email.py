# -*- coding: utf-8 -*-
import re

files = ['index.html','garden-town.html','masoom-shah-road.html','railway-road.html','about.html','privacy.html','404.html']

for f in files:
    p = r'C:\Users\chzar\cuts-curves\\' + f
    s = open(p, encoding='utf-8').read()
    orig = s

    # 1. Branch page Email buttons (mailto with visible "Email")
    s = re.sub(r'\s*<a class="btn btn-ghost"[^>]*href="mailto:[^"]*"[^>]*>Email</a>', '', s)

    # 2. Home .msg email link (mailto with visible info@...)
    s = re.sub(r'\s*<a class="msg"[^>]*href="mailto:[^"]*"[^>]*>info@[^<]*</a>', '', s)

    # 3. About page email paragraph
    s = re.sub(r'\s*<p style="margin-top:12px"><a href="mailto:[^"]*"[^>]*>info@[^<]*</a></p>', '', s)

    # 4. Bare email links (footer + hero stray): <a href="mailto:info@...">info@...</a>
    s = re.sub(r'\s*<a href="mailto:[^"]*"[^>]*>info@cutsandcurvesgym\.com</a>', '', s)

    # 5. Privacy page email li
    s = re.sub(r'\s*<li>Email: info@[^<]*</li>', '', s)

    open(p, 'w', encoding='utf-8').write(s)
    n = orig.count('cutsandcurvesgym.com') - s.count('cutsandcurvesgym.com')
    print(f, 'removed', n)