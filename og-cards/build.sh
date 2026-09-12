#!/bin/bash
# Gera os cards de preview Open Graph (1200x630) a partir dos HTMLs deste diretório.
#
#   bash og-cards/build.sh og-metanfetamina   -> site/metanfetamina/og-metanfetamina-v1.png
#   bash og-cards/build.sh og-home            -> site/og-home-v1.png
#
# Renderiza a 2x (2400x1260) no Chrome headless e reduz para 1200x630 —
# é o que mantém o texto nítido na miniatura do WhatsApp.
set -e

NAME="${1:?informe o nome do card: og-metanfetamina | og-home}"
DIR="$(cd "$(dirname "$0")" && pwd)"
REPO="$(dirname "$DIR")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

case "$NAME" in
  og-metanfetamina) OUT="$REPO/site/metanfetamina/og-metanfetamina-v1.png" ;;
  og-home)          OUT="$REPO/site/og-home-v1.png" ;;
  *) echo "card desconhecido: $NAME"; exit 1 ;;
esac

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

"$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-first-run \
  --user-data-dir="$TMP/prof" --window-size=1200,630 --force-device-scale-factor=2 \
  --screenshot="$TMP/shot.png" "file://$DIR/$NAME.html" >/dev/null 2>&1 &
CHROME_PID=$!

for _ in $(seq 1 30); do
  [ -f "$TMP/shot.png" ] && break
  sleep 2
done
kill "$CHROME_PID" 2>/dev/null || true

[ -f "$TMP/shot.png" ] || { echo "FALHOU: o Chrome não gerou o screenshot"; exit 1; }

sips --resampleWidth 1200 "$TMP/shot.png" --out "$OUT" >/dev/null
# Recompressão lossless (pixels idênticos, ~20% menor): parte do build,
# para o card continuar reproduzível byte a byte.
python3 -c "from PIL import Image; im = Image.open('$OUT'); im.save('$OUT', optimize=True)"
echo "gerado: $OUT"
sips -g pixelWidth -g pixelHeight "$OUT" | tail -2
