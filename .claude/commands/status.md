---
description: Print a one-screen health check of the paper-tracker pipeline (recent runs, cache sizes, env vars, scheduled tasks).
---

Print a tight at-a-glance status of the system — useful before running `/daily` manually, or to confirm the scheduled tasks did their job overnight.

## What to show

Read `python_path` from `config.yaml`. Run a single inline Python snippet that gathers everything in one shot, and print its output verbatim. Do NOT spawn subagents — `/status` is purely informational.

```
<python_path> -c "
import json, os, glob
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('.')

# 1. State
try:
    s = json.loads((ROOT/'papers/state.json').read_text(encoding='utf-8'))
    last_d = s.get('last_daily') or '(never)'
    last_w = s.get('last_weekly') or '(never)'
    last_m = s.get('last_monthly') or '(never)'
    seen = len(s.get('seen_ids', []))
    seen_dois = len(s.get('seen_dois', []))
except Exception as e:
    last_d = last_w = last_m = '(error)'
    seen = seen_dois = 0

# 2. Cache sizes
def count(pattern):
    return len(glob.glob(str(ROOT/pattern)))
notes = count('papers/notes/*.md')
fulltext = count('papers/fulltext/*.pdf')
daily = count('papers/daily/*.md')
weekly = count('papers/weekly/*.md')
monthly = count('papers/monthly/*.md')
raw = count('papers/raw/*.json')

# 3. Recent runs
runs_path = ROOT/'papers/runs.jsonl'
recent = []
if runs_path.exists():
    lines = runs_path.read_text(encoding='utf-8').splitlines()[-5:]
    for line in lines:
        try:
            recent.append(json.loads(line))
        except Exception:
            pass

# 4. Env vars (without leaking values)
def have(var):
    if os.environ.get(var):
        return True
    env_file = ROOT/'.env'
    if env_file.exists():
        for ln in env_file.read_text(encoding='utf-8').splitlines():
            if ln.startswith(f'{var}=') and ln.split('=',1)[1].strip().strip(chr(34)).strip(chr(39)) not in ('', f'your_{var.lower()}_here'):
                return True
    return False
smtp_ok = have('SMTP_PASSWORD')
els_key = have('ELSEVIER_API_KEY')
els_ins = have('ELSEVIER_INSTTOKEN')

# Render
print(f'last_daily   : {last_d}')
print(f'last_weekly  : {last_w}')
print(f'last_monthly : {last_m}')
print(f'seen_ids     : {seen}')
print(f'seen_dois    : {seen_dois}')
print()
print(f'cache:  notes={notes}  fulltext={fulltext}  raw={raw}')
print(f'        daily={daily}  weekly={weekly}  monthly={monthly}')
print()
print(f'env: SMTP={\"OK\" if smtp_ok else \"missing\"}  '
      f'ELSEVIER_API_KEY={\"OK\" if els_key else \"missing\"}  '
      f'ELSEVIER_INSTTOKEN={\"OK\" if els_ins else \"missing (teaser only)\"}')
print()
if recent:
    print('recent runs:')
    for r in recent:
        ts = r.get('timestamp','?')[:16].replace('T',' ')
        print(f'  {ts} {r.get(\"type\",\"?\"):<8} {r.get(\"date\",\"?\"):<10}'
              f' fetched={r.get(\"fetched\",0):<4} filt={r.get(\"filtered\",0):<4}'
              f' notes={r.get(\"summarized\",0):<3} pdf={r.get(\"fulltext_downloaded\",0):<3}'
              f' email={r.get(\"email_status\",\"?\")}')
else:
    print('recent runs: (none yet)')
"
```

## After printing the status, also check Windows Task Scheduler

Run:

```
schtasks /query /tn "PaperTracker-Daily" /fo LIST 2>&1
schtasks /query /tn "PaperTracker-Weekly" /fo LIST 2>&1
schtasks /query /tn "PaperTracker-Monthly" /fo LIST 2>&1
```

Pluck the `Status:`, `Next Run Time:`, and `Last Result:` fields from each, and print a one-liner per task. If a task is missing (`ERROR: The system cannot find the file specified`), print "(not scheduled)".

## Final report shape (target)

```
Paper Tracker — status

last_daily   : 2026-04-28
last_weekly  : (never)
last_monthly : (never)
seen_ids     : 446
seen_dois    : 446

cache:  notes=8  fulltext=8  raw=2
        daily=1  weekly=0  monthly=0

env: SMTP=OK  ELSEVIER_API_KEY=OK  ELSEVIER_INSTTOKEN=missing (teaser only)

recent runs:
  2026-04-28 09:23 daily    2026-04-28 fetched=505  filt=158 notes=10 pdf=8  email=sent

scheduled:
  PaperTracker-Daily   : Ready, next 2026-04-29 01:00, last result OK
  PaperTracker-Weekly  : (not scheduled)
  PaperTracker-Monthly : (not scheduled)
```

Be terse — one screen, no commentary, no markdown headers.
