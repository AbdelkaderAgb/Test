"""Bundle the UI into one self-contained file.

Reads src/index.src.html, embeds the IBM Plex Sans Arabic fonts (src/fonts, from
the @fontsource/ibm-plex-sans-arabic npm package, SIL OFL) as base64, and writes
app/src/main/assets/index.html, which the Android app loads offline.

Run from the project root:  python3 src/build.py
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "index.src.html"
FONTS = ROOT / "src" / "fonts"
OUT = ROOT / "app" / "src" / "main" / "assets" / "index.html"

ARABIC = ("U+0600-06FF,U+0750-077F,U+0870-088E,U+0890-0891,U+0897-08E1,U+08E3-08FF,"
          "U+200C-200E,U+2010-2011,U+204F,U+2E41,U+FB50-FDFF,U+FE70-FE74,U+FE76-FEFC")
LATIN = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,"
         "U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")


def face(subset: str, weight: int, rng: str) -> str:
    data = (FONTS / f"ibm-plex-sans-arabic-{subset}-{weight}-normal.woff2").read_bytes()
    b64 = base64.b64encode(data).decode()
    return ("@font-face{font-family:'Plex Arabic';font-style:normal;font-display:swap;"
            f"font-weight:{weight};src:url(data:font/woff2;base64,{b64}) format('woff2');"
            f"unicode-range:{rng}}}")


def main() -> None:
    css = "\n".join(face(s, w, r) for s, r in (("arabic", ARABIC), ("latin", LATIN))
                    for w in (400, 500, 600, 700))
    html = SRC.read_text(encoding="utf-8")
    assert "/*FONTS*/" in html, "font placeholder missing"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html.replace("/*FONTS*/", css), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
