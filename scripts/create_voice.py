#!/usr/bin/env python3
"""Crea una voz propia con Gemini Voice design y la guarda en la config de hermes-learn.

Uso:
  GEMINI_API_KEY=... scripts/create_voice.py                      # voz por defecto (profe joven, es-MX)
  scripts/create_voice.py "descripción en inglés de la voz" es-ES female

Escucha la muestra en ./voz_preview.wav. El id (voice_...) se guarda como
EXPLICAR_VOICE en ~/.config/hermes-learn/config. Las voces caducan tras 1 año sin uso.
"""
import base64, json, os, sys, urllib.request

DEFAULT = ("A bright, articulate young woman around 18 speaking neutral Latin American Spanish with a clear "
           "Mexico City dubbing-studio accent; clear mid-high voice with crisp diction, intelligent and slightly "
           "self-assured, warm and patient when explaining, like a top student helping a friend understand.")

desc = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
lang = sys.argv[2] if len(sys.argv) > 2 else "es-MX"
gender = sys.argv[3] if len(sys.argv) > 3 else "female"
key = os.environ.get("GEMINI_API_KEY") or sys.exit("Falta GEMINI_API_KEY")

body = {"store": True, "voice": {"model": "gemini-3.8-flash-tts", "type": "prompted",
        "display_name": "hermes-learn profe", "gender": gender, "language_code": lang,
        "prompted": {"input": desc}}}
req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/voices",
                             data=json.dumps(body).encode(), method="POST",
                             headers={"x-goog-api-key": key, "Content-Type": "application/json"})
r = json.load(urllib.request.urlopen(req, timeout=120))
vid = r["id"]
if r.get("sample_audio", {}).get("data"):
    open("voz_preview.wav", "wb").write(base64.b64decode(r["sample_audio"]["data"]))
    print("Muestra: ./voz_preview.wav")

cdir = os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")), "hermes-learn")
os.makedirs(cdir, exist_ok=True)
cf = os.path.join(cdir, "config")
lines = [l for l in (open(cf).read().splitlines() if os.path.exists(cf) else []) if not l.startswith("EXPLICAR_VOICE=")]
lines.append(f"EXPLICAR_VOICE={vid}")
open(cf, "w").write("\n".join(lines) + "\n")
print(f"Voz creada: {vid} (caduca {r.get('expire_time', '?')[:10]}) → guardada en {cf}")
