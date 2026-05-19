#!/usr/bin/env python3
"""
Patch script per RAPTOR nav - aggiungi NASDAQ 100 + A/D BREADTH
Esegui nella cartella del repo stoxx600:
  python3 patch_raptor_nav.py
"""
import os

BREADTH = '''    <a href="breadth.html" style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:11px;letter-spacing:1px;padding:3px 10px;border-radius:3px;text-decoration:none;background:var(--surface3);color:var(--text2);border:1px solid var(--border);">&#128200; A/D BREADTH</a>'''

NDX = '''    <a href="nasdaq100.html" style="font-family:'Rajdhani',sans-serif;font-weight:700;font-size:11px;letter-spacing:1px;padding:3px 10px;border-radius:3px;text-decoration:none;background:var(--surface3);color:var(--text2);border:1px solid var(--border);">&#128202; NASDAQ 100</a>'''

def patch(filename, old, new):
    if not os.path.exists(filename):
        print(f"SKIP: {filename} non trovato")
        return
    txt = open(filename, encoding="utf-8").read()
    if old not in txt:
        print(f"SKIP: {filename} — pattern non trovato (già patchato?)")
        return
    open(filename, "w", encoding="utf-8").write(txt.replace(old, new, 1))
    print(f"OK: {filename}")

# nasdaq100.html — aggiungi breadth dopo NASDAQ 100 (attivo)
patch("nasdaq100.html",
    '>&#128202; NASDAQ 100</a>\n  </div>',
    f'>&#128202; NASDAQ 100</a>\n{BREADTH}\n  </div>')

# sp500.html — aggiungi NASDAQ + breadth dopo S&P 500 (attivo)
patch("sp500.html",
    '>&#127482;&#127480; S&amp;P 500</a>\n  </div>',
    f'>&#127482;&#127480; S&amp;P 500</a>\n{NDX}\n{BREADTH}\n  </div>')

# index.html — aggiungi NASDAQ + breadth dopo S&P 500
patch("index.html",
    '>&#127482;&#127480; S&amp;P 500</a>\n  </div>',
    f'>&#127482;&#127480; S&amp;P 500</a>\n{NDX}\n{BREADTH}\n  </div>')

print("\nFatto. Ora fai git add -A && git commit -m \'nav: aggiunti NASDAQ 100 e A/D Breadth\' && git push")
