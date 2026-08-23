#!/usr/bin/env python3
import html
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / "input" / "result.json").read_text(encoding="utf-8"))
required = ["day", "nickname", "title", "result", "learned", "next"]
missing = [key for key in required if not str(data.get(key, "")).strip()]
if missing:
    raise SystemExit("비어 있는 항목: " + ", ".join(missing))
safe = {key: html.escape(str(data[key])) for key in required}
page = f'''<!doctype html><html lang="ko"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{safe['day']} 인증</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#eef2ff;font-family:system-ui,"Apple SD Gothic Neo","Malgun Gothic",sans-serif}}
.card{{width:min(92vw,720px);margin:30px auto;padding:42px;border-radius:32px;background:#111827;color:#fff;box-shadow:0 18px 50px #312e8160}}
.day{{color:#a5b4fc;font-weight:800}}h1{{font-size:clamp(30px,7vw,54px);line-height:1.12;margin:12px 0 30px}}
.box{{padding:18px;margin:14px 0;border-radius:18px;background:#ffffff12}}b{{display:block;color:#c7d2fe;margin-bottom:8px}}p{{font-size:20px;line-height:1.55;margin:0}}.name{{text-align:right;color:#d1d5db;margin-top:24px}}
</style><main class="card"><div class="day">{safe['day']} COMPLETE</div><h1>{safe['title']}</h1>
<div class="box"><b>오늘 만든 것</b><p>{safe['result']}</p></div>
<div class="box"><b>오늘 배운 것</b><p>{safe['learned']}</p></div>
<div class="box"><b>다음에 할 것</b><p>{safe['next']}</p></div>
<p class="name">@{safe['nickname']}</p></main></html>'''
out = root / "output"
out.mkdir(exist_ok=True)
(out / "proof-card.html").write_text(page, encoding="utf-8")
print("완성: output/proof-card.html")
