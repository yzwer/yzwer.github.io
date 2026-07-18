# -*- coding: utf-8 -*-
import subprocess, json, sys, time
sys.stdout.reconfigure(encoding='utf-8')

cmd = ['yt-dlp', '--flat-playlist', '-J', 'https://www.youtube.com/@sunriches/videos']
for attempt in range(3):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if r.returncode == 0 or r.stdout:
            data = json.loads(r.stdout)
            entries = data.get('entries', [])
            if entries:
                latest = entries[0]
                print(f"LATEST_ID={latest.get('id','')}")
                print(f"LATEST_TITLE={latest.get('title','')}")
                for i, e in enumerate(entries[:3]):
                    print(f"  [{i+1}] {e.get('id','')} - {e.get('title','')}")
            break
        else:
            print(f'Attempt {attempt+1} stderr: {r.stderr[:200]}')
    except Exception as e:
        print(f'Attempt {attempt+1} error: {e}')
    if attempt < 2:
        time.sleep([5,15][attempt])
else:
    print('FAILED')
