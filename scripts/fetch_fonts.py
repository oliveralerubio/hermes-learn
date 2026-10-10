#!/usr/bin/env python3
# hermes-learn: descarga fuentes de Google Fonts a ~/Explicaciones/.lib/fonts (offline) y genera fonts.css
import os, re, urllib.request
OUT = os.path.join(os.environ.get("EXPLICAR_DIR", os.path.expanduser("~/Explicaciones")), ".lib", "fonts")
os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
FAMS = ["Inter:wght@400..800", "Fraunces:opsz,wght@9..144,400..800", "Space+Grotesk:wght@400..700",
        "Caveat:wght@500..700", "Nunito:wght@400..800", "Lora:wght@400..700",
        "Bricolage+Grotesque:opsz,wght@12..96,400..800"]
url = "https://fonts.googleapis.com/css2?" + "&".join("family=" + f for f in FAMS) + "&display=swap"
css = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read().decode()
blocks = re.findall(r"/\* ([\w-]+) \*/\s*(@font-face\s*\{.*?\})", css, re.S)
keep, n = [], 0
for subset, block in blocks:
    if subset not in ("latin", "latin-ext"):
        continue
    fam = re.search(r"font-family: '([^']+)'", block).group(1)
    style = re.search(r"font-style: (\w+)", block).group(1)
    m = re.search(r"url\((https://\S+?)\)", block)
    if not m: continue
    src = m.group(1)
    name = f"{fam.replace(' ', '')}-{style}-{subset}.woff2"
    path = os.path.join(OUT, name)
    if not os.path.exists(path):
        urllib.request.urlretrieve(src, path); n += 1
    keep.append(block.replace(src, "fonts/" + name))
open(os.path.join(OUT, "..", "fonts.css"), "w").write("\n".join(keep) + "\n")
print(f"{len(keep)} @font-face, {n} archivos nuevos")
