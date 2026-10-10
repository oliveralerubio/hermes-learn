#!/usr/bin/env bash
# hermes-learn — instalador
# Copia los scripts a ~/.local/bin y descarga las librerías del HTML para que
# funcione sin internet. No toca tu config de Hyprland: mira hypr/ para eso.
set -euo pipefail
cd "$(dirname "$0")"

BIN="${BIN_DIR:-$HOME/.local/bin}"
OUT="${EXPLICAR_DIR:-$HOME/Explicaciones}"
LIB="$OUT/.lib"
mkdir -p "$BIN" "$LIB"

say() { printf '\033[1;35m▸\033[0m %s\n' "$*"; }

# Dependencias
missing=()
for c in hermes chromium wl-paste curl python3 pw-cat; do command -v "$c" >/dev/null || missing+=("$c"); done
command -v magick >/dev/null || echo "  (opcional) falta imagemagick: las capturas no se reducirán"
if ((${#missing[@]})); then
  echo "Faltan: ${missing[*]}"
  echo "  hermes   → https://hermes-agent.nousresearch.com"
  echo "  wl-paste → wl-clipboard · pw-cat → pipewire"
  exit 1
fi

say "Instalando scripts en $BIN"
install -m 755 bin/explicar bin/explicar-voz "$BIN/"

say "Descargando librerías en $LIB"
dl() { [[ -s $LIB/$2 ]] || curl -fsSL -o "$LIB/$2" "$1"; }
dl https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js mermaid.min.js
dl https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/highlight.min.js hljs.js
dl https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/styles/github-dark.min.css hljs-dark.css
dl https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/styles/github.min.css hljs-light.css
[[ -s $LIB/fonts.css ]] || EXPLICAR_DIR="$OUT" python3 scripts/fetch_fonts.py

CONF="${XDG_CONFIG_HOME:-$HOME/.config}/hermes-learn/config"
if [[ ! -f $CONF ]]; then
  mkdir -p "$(dirname "$CONF")"
  cp config.example "$CONF"
  say "Config de ejemplo en $CONF"
fi

cat <<EOF

Listo. Siguientes pasos:
  1. Pon tu GEMINI_API_KEY en $CONF (o en tu entorno) para la voz.
     Opcional: crea tu voz con  scripts/create_voice.py
  2. Atajo de teclado, p. ej. Hyprland (Lua):
       o.bind("SUPER + SHIFT + E", "Explicar portapapeles", "explicar")
     y la regla de ventana flotante de hypr/ventana-flotante.lua
  3. Copia algo y pulsa el atajo.  Sin voz:  EXPLICAR_VOZ=0 explicar
EOF
