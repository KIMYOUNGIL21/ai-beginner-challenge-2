"""Subtitle rendering for build.py.

Two backends, picked automatically:
  ass  -- ffmpeg's libass filter, when this ffmpeg was built with it
  png  -- Pillow-rendered transparent overlays, composited with `overlay`

Homebrew's ffmpeg 9 ships without libass/freetype, so the png backend is the
one that actually runs on a stock macOS setup.
"""
import os
import subprocess
import sys

MAX_CAPTION_CHARS = 18   # ~2 lines of Korean at this size
MAX_CAPTION_SECS = 2.4

KOREAN_FONTS = [
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
    "/Library/Fonts/NanumGothic.ttf",
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
]


def have_libass():
    try:
        out = subprocess.run(["ffmpeg", "-hide_banner", "-filters"],
                             capture_output=True, text=True).stdout
    except FileNotFoundError:
        sys.exit("ffmpeg not found on PATH")
    return any(line.split()[1:2] == ["ass"] for line in out.splitlines() if line.split())


def find_font():
    for p in KOREAN_FONTS:
        if os.path.exists(p):
            return p
    sys.exit("no Korean font found; install one or add its path to KOREAN_FONTS")


def group_captions(words):
    """Chunk words into cues, never spanning a sentence boundary."""
    cues, cur = [], []
    for w in words:
        if cur:
            same = w["sentence"] == cur[0]["sentence"]
            text = " ".join(x["text"] for x in cur + [w])
            span = w["end"] - cur[0]["start"]
            if not same or len(text) > MAX_CAPTION_CHARS or span > MAX_CAPTION_SECS:
                cues.append(cur)
                cur = []
        cur.append(w)
    if cur:
        cues.append(cur)
    return [{"text": " ".join(x["text"] for x in c),
             "start": c[0]["start"], "end": c[-1]["end"]} for c in cues]


# ---------------------------------------------------------------- ass backend

ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,{font},{size},&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,7,3,2,80,80,{mv},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def _ts(t):
    h, rem = divmod(max(t, 0), 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def _filter_path(path):
    p = os.path.abspath(path)
    for ch in ("\\", ":", "'", "[", "]", ","):
        p = p.replace(ch, "\\" + ch)
    return p


def build_ass(cues, workdir, w, h, size, margin_v):
    path = os.path.join(workdir, "subs.ass")
    lines = [ASS_HEAD.format(w=w, h=h, font="Apple SD Gothic Neo",
                             size=size, mv=margin_v)]
    for c in cues:
        lines.append(f"Dialogue: 0,{_ts(c['start'])},{_ts(c['end'])},Main,,0,0,0,,"
                     + c["text"].replace("\n", " "))
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return [f"[0:v]ass=filename={_filter_path(path)}[vout]"], []


# ---------------------------------------------------------------- png backend

def build_png(cues, workdir, w, h, size, margin_v, fps=30):
    """Render cues into ONE transparent overlay video, composited in one pass.

    Chaining N overlay filters (one per cue) would both blow up the filter
    graph and force ffmpeg to walk every full frame N times. Instead the cues
    are laid onto a single alpha track via the concat demuxer, so the main
    encode does exactly one overlay.

    Returns (filter_chain_parts, extra_ffmpeg_inputs).
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        sys.exit("subtitles need either a libass-enabled ffmpeg or Pillow.\n"
                 "  fix: python3 -m venv .venv && .venv/bin/pip install pillow\n"
                 "  then run build.py with .venv/bin/python")

    if not cues:
        return ["[0:v]null[vout]"], []

    font = ImageFont.truetype(find_font(), size)
    cue_dir = os.path.join(workdir, "cues")
    os.makedirs(cue_dir, exist_ok=True)

    blank = os.path.join(cue_dir, "blank.png")
    Image.new("RGBA", (w, h), (0, 0, 0, 0)).save(blank)

    max_w = w - 160  # 80px side margins
    pngs = []
    for i, c in enumerate(cues):
        # Greedy wrap on spaces; Korean captions rarely exceed two lines here.
        lines, cur = [], ""
        for word in c["text"].split():
            trial = f"{cur} {word}".strip()
            if cur and font.getbbox(trial)[2] > max_w:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        if cur:
            lines.append(cur)

        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        lh = int(size * 1.25)
        y = h - margin_v - lh * len(lines)
        for ln in lines:
            tw = d.textbbox((0, 0), ln, font=font)[2]
            # stroke_width gives the same read as an ASS outline over busy video
            d.text(((w - tw) // 2, y), ln, font=font, fill=(255, 255, 255, 255),
                   stroke_width=6, stroke_fill=(0, 0, 0, 230))
            y += lh
        png = os.path.join(cue_dir, f"{i:04d}.png")
        img.save(png)
        pngs.append(png)

    # Timeline of (image, duration) covering gaps with the blank frame.
    timeline, t = [], 0.0
    for c, png in zip(cues, pngs):
        if c["start"] > t + 1e-3:
            timeline.append((blank, c["start"] - t))
        timeline.append((png, max(c["end"] - c["start"], 1.0 / fps)))
        t = c["end"]

    listing = os.path.join(cue_dir, "timeline.txt")
    with open(listing, "w") as f:
        for img, dur in timeline:
            f.write(f"file '{os.path.abspath(img)}'\nduration {dur:.3f}\n")
        f.write(f"file '{os.path.abspath(timeline[-1][0])}'\n")  # concat quirk

    track = os.path.join(workdir, "subs.mov")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", listing, "-fps_mode", "cfr", "-r", str(fps),
                    "-c:v", "qtrle", "-pix_fmt", "argb", track], check=True)

    # input 0 = video, input 1 = narration, input 2 = this overlay track
    return ["[0:v][2:v]overlay=0:0:shortest=0[vout]"], ["-i", track]
