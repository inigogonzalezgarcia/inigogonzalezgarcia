"""Keeps the profile current: the counts at the top of README.md, the roadmap chart (assets/roadmap.svg) and its interactive
version (docs/index.html, served by GitHub Pages).

The chart has the days from `start` to `end` on the X axis (months above, days below) and the toolbox areas on the Y axis.
Every repo sits in its area on the date of its blog post; planned repos are dashed until their post exists; a red line marks
today (Europe/Madrid). Sources: the blog posts in the website repo (src/posts.py: number, repo and date), the toolbox sections
of this README (which area each repo belongs to and its name) and roadmap.json (dates, areas and names of the planned repos).
Standard library only. Run by .github/workflows/update-readme.yml every few hours; `python scripts/update_readme.py` locally
(`--today=YYYY-MM-DD` and a local posts.py path are accepted for testing)."""
from __future__ import annotations

import html
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
MONTHS = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
e = html.escape


def read_posts(url: str, local: str | None) -> dict[str, tuple[str, date]]:
    text = Path(local).read_text(encoding="utf-8") if local else urllib.request.urlopen(url, timeout=30).read().decode("utf-8")
    out = {n: (repo, date.fromisoformat(d)) for n, repo, d in
           re.findall(r'dict\(n="(\d+)", repo="([^"]+)", date="(\d{4}-\d{2}-\d{2})"', text)}
    if len(out) < 10:
        raise SystemExit(f"only {len(out)} posts read from {local or url}: not touching anything")
    return out


def read_toolbox(readme: str, areas: list[dict]) -> dict[str, tuple[str, str]]:
    """Repo number -> (area label, tool name), from the <details> sections of the README."""
    out = {}
    for summary, body in re.findall(r"<summary><b>(.*?)</b>.*?</summary>(.*?)</details>", readme, re.S):
        area = next((a["label"] for a in areas if summary.startswith(a["match"])), None)
        if not area:
            continue
        for n, name in re.findall(r"^\| (\d\d) \| \[([^\]]+)\]", body, re.M):
            out[n] = (area, name)
    return out


def model(cfg: dict, posts: dict, toolbox: dict, today: date) -> dict:
    start, end = date.fromisoformat(cfg["start"]), date.fromisoformat(cfg["end"])
    days = [start + timedelta(i) for i in range((end - start).days + 1)]
    shown = {n: v for n, v in posts.items() if v[1] <= today}
    plan = {p["n"]: p for p in cfg["planned"]}
    cells: dict[tuple[str, date], list[dict]] = {}
    for n, (repo, d) in sorted(shown.items()):
        if not start <= d <= end:
            continue
        fallback = (plan[n]["area"], plan[n]["name"]) if n in plan else (cfg["areas"][-1]["label"], repo)
        area, name = toolbox.get(n, fallback)
        cells.setdefault((area, d), []).append({"n": n, "name": name, "url": f'{cfg["blog"]}{repo}.html', "planned": False})
    pending = [p for p in cfg["planned"] if p["n"] not in shown]
    for p in pending:
        d = date.fromisoformat(p["date"])
        if start <= d <= end:
            cells.setdefault((p["area"], d), []).append({"n": p["n"], "name": p["name"], "url": "", "planned": True})
    left = [p for p in pending if date.fromisoformat(p["date"]) <= end]
    in_range = sum(1 for _, d in shown.values() if start <= d <= end)
    return {"start": start, "end": end, "days": days, "today": today, "cells": cells, "shown": shown, "left": left,
            "in_range": in_range, "areas": cfg["areas"]}


def svg(m: dict) -> str:
    LW, CW, MH, DH, RH, PAD = 210, 12, 26, 18, 30, 12
    days, areas = m["days"], m["areas"]
    gx, gy = LW, MH + DH + 8
    W, H = LW + CW * len(days) + PAD, gy + RH * len(areas) + 40
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" rx="10" fill="#ffffff"/>']
    for i, d in enumerate(days):
        x = gx + i * CW
        if d.weekday() >= 5:
            o.append(f'<rect x="{x}" y="{gy}" width="{CW}" height="{RH * len(areas)}" fill="#f6f8fa"/>')
        if d.day == 1 or i == 0:
            o.append(f'<text x="{x + 2}" y="{MH - 8}" font-size="15" font-weight="700" fill="#1f2328">{MONTHS[d.month]}</text>')
            if i:
                o.append(f'<line x1="{x}" y1="{MH - 22}" x2="{x}" y2="{gy + RH * len(areas)}" stroke="#8c959f" stroke-width="1"/>')
        o.append(f'<text x="{x + CW / 2}" y="{MH + DH - 4}" font-size="8.5" text-anchor="middle" fill="{"#8c959f" if d.weekday() >= 5 else "#59636e"}">{d.day}</text>')
    for r, a in enumerate(areas):
        y = gy + r * RH
        o.append(f'<line x1="{PAD}" y1="{y}" x2="{W - PAD}" y2="{y}" stroke="#d1d9e0" stroke-width="1"/>')
        o.append(f'<rect x="{PAD}" y="{y + RH / 2 - 5}" width="10" height="10" rx="2" fill="{a["color"]}"/>')
        o.append(f'<text x="{PAD + 16}" y="{y + RH / 2 + 5}" font-size="14" fill="#1f2328">{e(a["label"])}</text>')
        for i, d in enumerate(days):
            items = m["cells"].get((a["label"], d))
            if not items:
                continue
            x, cx = gx + i * CW + 1, gx + i * CW + CW / 2
            if all(it["planned"] for it in items):
                o.append(f'<rect x="{x + 0.5}" y="{y + 6.5}" width="{CW - 3}" height="{RH - 13}" rx="2" fill="none" stroke="{a["color"]}" stroke-width="1.5" stroke-dasharray="2 2"/>')
            else:
                o.append(f'<rect x="{x}" y="{y + 6}" width="{CW - 2}" height="{RH - 12}" rx="2" fill="{a["color"]}"/>')
                if len(items) > 1:
                    o.append(f'<text x="{cx}" y="{y + RH / 2 + 3.5}" font-size="9" font-weight="700" text-anchor="middle" fill="#ffffff">{len(items)}</text>')
    o.append(f'<line x1="{PAD}" y1="{gy + RH * len(areas)}" x2="{W - PAD}" y2="{gy + RH * len(areas)}" stroke="#d1d9e0" stroke-width="1"/>')
    t = m["today"]
    if m["start"] <= t <= m["end"]:
        x = gx + (t - m["start"]).days * CW + CW / 2
        o.append(f'<line x1="{x}" y1="{MH - 22}" x2="{x}" y2="{gy + RH * len(areas) + 6}" stroke="#cf222e" stroke-width="2"/>')
        o.append(f'<text x="{x}" y="{gy + RH * len(areas) + 20}" font-size="12" font-weight="700" text-anchor="middle" fill="#cf222e">Today · {t.day} {MONTHS[t.month][:3]}</text>')
    ly = H - 10
    o.append(f'<rect x="{PAD}" y="{ly - 10}" width="10" height="10" rx="2" fill="#57606a"/><text x="{PAD + 15}" y="{ly}" font-size="12" fill="#59636e">published (a number = several that day)</text>')
    o.append(f'<rect x="{PAD + 280}" y="{ly - 10}" width="10" height="10" rx="2" fill="none" stroke="#57606a" stroke-dasharray="2 2"/><text x="{PAD + 295}" y="{ly}" font-size="12" fill="#59636e">planned</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Roadmap · Iñigo González</title>
<meta name="description" content="Every open-source IT tool by Iñigo González on the day its post went out, by area, from __START__ to __END__.">
<style>
:root{--bg:#ffffff;--ink:#1f2328;--muted:#59636e;--line:#d1d9e0;--wk:#f6f8fa;--hi:#fff8c5;--today:#cf222e;--card:#ffffff}
@media (prefers-color-scheme:dark){:root{--bg:#0d1117;--ink:#e6edf3;--muted:#9198a1;--line:#30363d;--wk:#161b22;--hi:#3b2f00;--today:#ff7b72;--card:#161b22}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 -apple-system,Segoe UI,Helvetica,Arial,sans-serif}
main{max-width:1500px;margin:0 auto;padding:28px 16px 48px}h1{font-size:24px;margin:0 0 6px}p.lead{color:var(--muted);margin:0 0 18px}
a{color:#2f81f7}.wrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--card)}
table{border-collapse:separate;border-spacing:0;font-size:12px}th,td{padding:0;text-align:center}
th.area{position:sticky;left:0;z-index:2;background:var(--card);text-align:left;padding:0 12px;white-space:nowrap;font-weight:600;min-width:190px;border-right:1px solid var(--line)}
th.area i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:8px;vertical-align:-1px}
thead th{background:var(--card)}thead tr.m th{font-size:13px;font-weight:700;text-align:left;padding:8px 6px 2px;border-left:1px solid var(--line)}
thead tr.d th{font-weight:400;color:var(--muted);width:24px;min-width:24px;padding:2px 0 6px;font-size:11px;position:relative}
thead tr.d th.we,td.we{background:var(--wk)}td{height:34px;border-top:1px solid var(--line);position:relative}
td .b{position:absolute;inset:7px 3px;border-radius:3px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:10px}
td .b.p{background:none!important;border:1.5px dashed}td.has{cursor:pointer}
.hl{background:var(--hi)!important}th.hl{color:var(--ink)!important}td.cur{outline:2px solid var(--ink);outline-offset:-2px}
td.today::after,th.today::after{content:"";position:absolute;top:0;bottom:-1px;left:50%;width:2px;margin-left:-1px;background:var(--today);pointer-events:none}
thead tr.d th.today{color:var(--today);font-weight:700}
#tip{position:fixed;z-index:9;pointer-events:none;background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px 10px;font-size:12px;box-shadow:0 6px 18px rgba(0,0,0,.18);max-width:320px;display:none}
#tip b{display:block;margin-bottom:2px}#tip span{color:var(--muted)}#tip ul{margin:4px 0 0;padding-left:16px}
.legend{display:flex;gap:18px;flex-wrap:wrap;color:var(--muted);margin:12px 2px 0;font-size:12px}.legend i{display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:6px;vertical-align:-2px}
.legend .t{width:2px;background:var(--today)}footer{color:var(--muted);margin-top:22px;font-size:12px}
</style></head><body><main>
<h1>Roadmap · __START__ – __END__</h1>
<p class="lead">__COUNT__ Hover a cell to see the date and the area; click it to open the post. Data from <a href="__BLOG__">the blog</a>, updated every few hours.</p>
<div class="wrap"><table id="g">__TABLE__</table></div>
<div class="legend"><span><i style="background:#57606a"></i>published (a number = several that day)</span><span><i style="border:1.5px dashed #57606a"></i>planned</span><span><i class="t"></i>today</span></div>
<footer><a href="https://github.com/inigogonzalezgarcia">github.com/inigogonzalezgarcia</a> · <a href="https://inigogonzalezgarcia.github.io">inigogonzalezgarcia.github.io</a></footer>
</main><div id="tip"></div>
<script>
const DATA=__DATA__;
const g=document.getElementById('g'),tip=document.getElementById('tip');
// today's line from the visitor's clock in Madrid time, so it moves even between updates
const madrid=new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Madrid',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
g.querySelectorAll('[data-d="'+madrid+'"]').forEach(el=>el.classList.add('today'));
let cur=null;
function clear(){g.querySelectorAll('.hl,.cur').forEach(el=>el.classList.remove('hl','cur'))}
g.addEventListener('mouseover',ev=>{const td=ev.target.closest('td[data-d]');if(!td||td===cur)return;cur=td;clear();
 const d=td.dataset.d,r=td.parentElement;td.classList.add('cur');r.querySelector('th').classList.add('hl');
 g.querySelectorAll('[data-d="'+d+'"]').forEach(el=>{if(el!==td)el.classList.add('hl')});
 const items=DATA[td.dataset.k]||[],dt=new Date(d+'T12:00:00');
 tip.innerHTML='<b>'+dt.toLocaleDateString('en-GB',{weekday:'long',day:'numeric',month:'long',year:'numeric'})+'</b><span>'+r.dataset.a+'</span>'+
  (items.length?'<ul>'+items.map(i=>'<li>'+i.n+' · '+i.name+(i.planned?' <span>(planned)</span>':'')+'</li>').join('')+'</ul>':'');
 tip.style.display='block'});
g.addEventListener('mousemove',ev=>{const w=tip.offsetWidth,h=tip.offsetHeight;let x=ev.clientX+14,y=ev.clientY+14;
 if(x+w>innerWidth-8)x=ev.clientX-w-14;if(y+h>innerHeight-8)y=ev.clientY-h-14;tip.style.left=x+'px';tip.style.top=y+'px'});
g.addEventListener('mouseleave',()=>{tip.style.display='none';clear();cur=null});
g.addEventListener('click',ev=>{const td=ev.target.closest('td[data-k]');if(!td)return;const it=(DATA[td.dataset.k]||[]).filter(i=>i.url);
 if(it.length)location.href=it[0].url});
</script></body></html>
"""


def page(m: dict, cfg: dict) -> str:
    days, areas = m["days"], m["areas"]
    data, rows = {}, []
    head_m, i = ['<tr class="m"><th class="area" rowspan="2">Area</th>'], 0
    while i < len(days):
        j = i
        while j + 1 < len(days) and days[j + 1].month == days[i].month:
            j += 1
        head_m.append(f'<th colspan="{j - i + 1}">{MONTHS[days[i].month]} {days[i].year}</th>')
        i = j + 1
    head_m.append("</tr>")
    head_d = ['<tr class="d">'] + [f'<th data-d="{d.isoformat()}" title="{DOW[d.weekday()]} {d.day} {MONTHS[d.month]}"'
                                    f'{" class=we" if d.weekday() >= 5 else ""}>{d.day}</th>' for d in days] + ["</tr>"]
    for a in areas:
        tds = []
        for d in days:
            items = m["cells"].get((a["label"], d))
            cls = ["we"] if d.weekday() >= 5 else []
            attrs = f'data-d="{d.isoformat()}"'
            inner = ""
            if items:
                k = f'{a["label"]}|{d.isoformat()}'
                data[k] = items
                attrs += f' data-k="{e(k)}"'
                planned = all(it["planned"] for it in items)
                if not planned:
                    cls.append("has")
                label = str(len(items)) if len(items) > 1 else ""
                inner = (f'<div class="b{" p" if planned else ""}" style="background:{a["color"]};border-color:{a["color"]};'
                         f'color:{"#fff" if not planned else a["color"]}">{label}</div>')
            klass = f' class="{" ".join(cls)}"' if cls else ""
            tds.append(f"<td {attrs}{klass}>{inner}</td>")
        rows.append(f'<tr data-a="{e(a["label"])}"><th class="area"><i style="background:{a["color"]}"></i>{e(a["label"])}</th>{"".join(tds)}</tr>')
    table = "<thead>" + "".join(head_m) + "".join(head_d) + "</thead><tbody>" + "".join(rows) + "</tbody>"
    fmt = lambda d: f"{d.day} {MONTHS[d.month]} {d.year}"
    count = f'{m["in_range"]} repos published since {fmt(m["start"])}' + (f', {len(m["left"])} still to come.' if m["left"] else ".")
    return (PAGE.replace("__TABLE__", table).replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
            .replace("__START__", fmt(m["start"])).replace("__END__", fmt(m["end"])).replace("__COUNT__", e(count)).replace("__BLOG__", cfg["blog"]))


def badge(label: str, message: str, color: str) -> str:
    esc = lambda t: urllib.parse.quote(t.replace("-", "--").replace("_", "__").replace(" ", "_"), safe="_")
    return f'<img src="https://img.shields.io/badge/{esc(label)}-{esc(message)}-{color}?style=for-the-badge" alt="{label}: {message}">'


def blocks(m: dict, cfg: dict) -> tuple[str, str]:
    start, end, today, shown, left = m["start"], m["end"], m["today"], m["shown"], m["left"]
    plan = f"🗓️ **{len(left)} more** before the end of {end.year}" if left else f"✅ **{end.year}** roadmap complete"
    counts = (f"| 🧰 **{len(shown)}** open-source projects | {plan} | "
              "🎮 **1** free IT support simulator |\n|:---:|:---:|:---:|")
    parts = [f"### 🗺️ Roadmap to the end of {end.year}", "",
             f"Every repo on the day its post went out on [the blog]({cfg['blog']}), by area. **{m['in_range']}** published since "
             f"{start.day} {MONTHS[start.month]}" + (f", {len(left)} still to come" if left else "") + ". The red line is today; the chart updates itself.", "",
             f'<a href="{cfg["page"]}"><img src="assets/roadmap.svg" alt="Roadmap: every repo by area and day, from {start.day} {MONTHS[start.month]} '
             f'to {end.day} {MONTHS[end.month]} {end.year}" width="100%"></a>', "",
             '<p align="center"><sub>Click the chart for the interactive version: hover a cell to see the date and the area, click it to open the post.</sub></p>', ""]
    badges = []
    y, mo = start.year, start.month
    while (y, mo) <= (end.year, end.month):
        done = sum(1 for _, d in shown.values() if (d.year, d.month) == (y, mo))
        todo = sum(1 for p in left if date.fromisoformat(p["date"]).timetuple()[:2] == (y, mo))
        if todo:
            msg = f"{done} built · {todo} to go" if done else f"{todo} planned"
            color = "e36209" if (y, mo) == (today.year, today.month) else "8b949e"
        elif done:
            msg, color = f"{done} tools ✓", "2ea44f"
        else:
            y, mo = (y + 1, 1) if mo == 12 else (y, mo + 1)
            continue
        badges.append(badge(MONTHS[mo], msg, color))
        y, mo = (y + 1, 1) if mo == 12 else (y, mo + 1)
    parts += ['<p align="center">'] + badges + ["</p>", ""]
    if left:
        parts += ["| # | Coming | The question it answers | When |", "|---|---|---|---|"]
        for p in sorted(left, key=lambda p: (p["date"], p["n"])):
            d = date.fromisoformat(p["date"])
            parts.append(f"| {p['n']} | **{p['name']}** | {p['question']} | {d.day} {MONTHS[d.month][:3]} |")
    return counts, "\n".join(parts).rstrip()


def replace(text: str, name: str, body: str) -> str:
    pat = re.compile(rf"(<!-- {name}:START -->\n).*?(\n<!-- {name}:END -->)", re.S)
    if not pat.search(text):
        raise SystemExit(f"marker {name} not found in README.md")
    return pat.sub(lambda mm: mm.group(1) + "\n" + body + "\n" + mm.group(2), text)


def write(path: Path, text: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    cfg = json.loads((ROOT / "roadmap.json").read_text(encoding="utf-8"))
    today = datetime.now(ZoneInfo(cfg.get("timezone", "UTC"))).date()
    args = sys.argv[1:]
    if args and args[0].startswith("--today="):
        today = date.fromisoformat(args.pop(0).split("=", 1)[1])
    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    m = model(cfg, read_posts(cfg["posts_url"], args[0] if args else None), read_toolbox(readme, cfg["areas"]), today)
    counts, roadmap = blocks(m, cfg)
    outputs = ((readme_path, replace(replace(readme, "COUNTS", counts), "ROADMAP", roadmap)),
               (ROOT / "assets" / "roadmap.svg", svg(m)), (ROOT / "docs" / "index.html", page(m, cfg)))
    changed = [p for p, t in outputs if write(p, t)]
    print("updated: " + ", ".join(p.relative_to(ROOT).as_posix() for p in changed) if changed else "everything already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
