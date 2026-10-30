"""Turn every novel2/chNN_popo.txt into docs/audio/eNN.mp3 (skip existing) and update episodes.json."""
import glob, json, os, re, subprocess, sys
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
SRC = os.path.expanduser("~/.gemini/jetski/brain/9ddac055-6c3d-4b59-b184-5e8f8f7c2fd8/novel2")
CN = "零一二三四五六七八九"
def cn(n): return CN[n] if n < 10 else ("十" + (CN[n % 10] if n % 10 else "") if n < 20 else CN[n // 10] + "十" + (CN[n % 10] if n % 10 else ""))
eps = json.load(open("episodes.json", encoding="utf-8")) if os.path.exists("episodes.json") else []
have = {e["file"] for e in eps}
base = datetime(2026, 10, 30, 12, tzinfo=timezone(timedelta(hours=8)))
for txt in sorted(glob.glob(f"{SRC}/ch[0-9][0-9]_popo.txt")):
    n = int(re.search(r"ch(\d+)_popo", txt).group(1))
    md = open(txt.replace("_popo.txt", ".md"), encoding="utf-8").read()
    m = re.search(r"^## (.+)$", md, re.M); title = m.group(1).strip() if m else f"第{cn(n)}章"
    name = title.split("　", 1)[-1]
    f = f"e{n:02d}.mp3"
    mp3 = f"docs/audio/{f}"
    stale = os.path.exists(mp3) and os.path.getmtime(txt) > os.path.getmtime(mp3) + 60
    if stale: os.remove(mp3)  # chapter text was edited after the audio was made: regenerate
    if f not in have or not os.path.exists(mp3):
        if not os.path.exists(mp3):
            subprocess.run([sys.executable, "-u", "tools/tts.py", txt, f"docs/audio/{f}",
                            f"執刑者。{title.replace('　', '，')}。", f"{title.split('　')[0]}，完。感謝收聽執刑者。"], check=True)
        if f not in have:
            eps.append({"n": n, "season": 1, "file": f, "title": f"執刑者｜{title}",
                        "summary": f"《執刑者》{title}。18 禁：含暴力血腥內容。",
                        "pub": format_datetime(base + timedelta(minutes=n))})
            have.add(f)
        json.dump(sorted(eps, key=lambda e: e["n"]), open("episodes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("done", f, flush=True)
