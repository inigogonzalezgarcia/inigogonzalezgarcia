"""Keeps the profile README current: the counts at the top and the day-by-day roadmap calendar.

Reads the blog posts from the website repo (src/posts.py: number, repo and date of every post) and the planned repos from
roadmap.json, and rewrites the parts of README.md between the COUNTS and ROADMAP markers. A repo shows up on the calendar on
the date of its post as soon as the post is in the website repo; a planned repo stays marked 🗓️ until then. Today is marked 📍.
Standard library only. Run by .github/workflows/update-readme.yml every few hours; `python scripts/update_readme.py` locally."""
from __future__ import annotations

import calendar
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
MONTHS = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def posts(url: str, local: str | None) -> dict[str, tuple[str, date]]:
    text = Path(local).read_text(encoding="utf-8") if local else urllib.request.urlopen(url, timeout=30).read().decode("utf-8")
    out = {}
    for n, repo, d in re.findall(r'dict\(n="(\d+)", repo="([^"]+)", date="(\d{4}-\d{2}-\d{2})"', text):
        out[n] = (repo, date.fromisoformat(d))
    if len(out) < 10:
        raise SystemExit(f"only {len(out)} posts read from {local or url}: not touching the README")
    return out


def badge(label: str, message: str, color: str, alt: str) -> str:
    esc = lambda t: urllib.parse.quote(t.replace("-", "--").replace("_", "__").replace(" ", "_"), safe="_")
    return f'<img src="https://img.shields.io/badge/{esc(label)}-{esc(message)}-{color}?style=for-the-badge" alt="{alt}">'


def build(cfg: dict, published: dict[str, tuple[str, date]], today: date) -> tuple[str, str]:
    start, end = date.fromisoformat(cfg["start"]), date.fromisoformat(cfg["end"])
    shown = {n: v for n, v in published.items() if v[1] <= today}
    by_day: dict[date, list[tuple[str, str]]] = {}
    for n, (repo, d) in shown.items():
        by_day.setdefault(d, []).append((n, repo))
    pending = [p for p in cfg["planned"] if p["n"] not in shown]
    plan_day: dict[date, list[str]] = {}
    for p in pending:
        plan_day.setdefault(date.fromisoformat(p["date"]), []).append(p["n"])
    in_range = [n for n, (_, d) in shown.items() if start <= d <= end]
    left = [p for p in pending if date.fromisoformat(p["date"]) <= end]

    counts = (f"| 🧰 **{len(shown)}** open-source projects | 🗓️ **{len(left)} more** before the end of {end.year} | "
              "🎮 **1** free IT support simulator | 📈 **1** educational investing lab |\n|:---:|:---:|:---:|:---:|")

    def cell(d: date) -> str:
        head = f"📍&nbsp;**{d.day}**" if d == today else f"**{d.day}**"
        items = [f'[{n}]({cfg["blog"]}{repo}.html "{repo}")' for n, repo in sorted(by_day.get(d, []))]
        items += [f"🗓️&nbsp;{n}" for n in sorted(plan_day.get(d, []))]
        return head + ("<br>" + " ".join(items) if items else "")

    parts = [f"### 🗺️ Roadmap to the end of {end.year}", "",
             f"Every repo sits on the date of its post on [the blog]({cfg['blog']}). **{len(in_range)}** published since "
             f"{start.day} {MONTHS[start.month]}" + (f"; 🗓️ marks the {len(left)} still to come." if left else ".")
             + f" 📍 is today. This calendar updates itself.", ""]
    badges = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        done = sum(1 for _, (_, d) in shown.items() if (d.year, d.month) == (y, m))
        todo = sum(1 for p in left if date.fromisoformat(p["date"]).timetuple()[:2] == (y, m))
        sub = f"{done} published" + (f" · {todo} planned" if todo else "")
        rows = ["| Mon | Tue | Wed | Thu | Fri | Sat | Sun |", "|:---:|:---:|:---:|:---:|:---:|:---:|:---:|"]
        for week in calendar.Calendar(0).monthdatescalendar(y, m):
            rows.append("| " + " | ".join(cell(d) if d.month == m else " " for d in week) + " |")
        parts += [f"**{MONTHS[m]} {y}** · {sub}", ""] + rows + [""]
        msg, color = (f"{done} tools ✓", "2ea44f") if not todo and (y, m) < (today.year, today.month) else \
                     (f"{done} built · {todo} to go" if done else f"{todo} planned", "e36209" if (y, m) == (today.year, today.month) else "8b949e")
        if not todo and (y, m) >= (today.year, today.month):
            msg, color = f"{done} built", "2ea44f" if done else "8b949e"
        badges.append(badge(MONTHS[m], msg, color, f"{MONTHS[m]}: {msg}"))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    parts += ["<sub>Click a number to read its post.</sub>", "", '<p align="center">'] + badges + ["</p>", ""]
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
    return pat.sub(lambda m: m.group(1) + "\n" + body + "\n" + m.group(2), text)


def main() -> int:
    cfg = json.loads((ROOT / "roadmap.json").read_text(encoding="utf-8"))
    today = datetime.now(ZoneInfo(cfg.get("timezone", "UTC"))).date()
    if len(sys.argv) > 1 and sys.argv[1].startswith("--today="):
        today = date.fromisoformat(sys.argv.pop(1).split("=", 1)[1])
    local = sys.argv[1] if len(sys.argv) > 1 else None
    counts, roadmap = build(cfg, posts(cfg["posts_url"], local), today)
    readme = ROOT / "README.md"
    old = readme.read_text(encoding="utf-8")
    new = replace(replace(old, "COUNTS", counts), "ROADMAP", roadmap)
    if new != old:
        readme.write_text(new, encoding="utf-8")
        print("README updated")
    else:
        print("README already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
