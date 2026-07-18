# -*- coding: utf-8 -*-
import subprocess, json, sys, time
sys.stdout.reconfigure(encoding='utf-8')
cmd = ['yt-dlp','--flat-playlist','-J','https://www.youtube.com/@sunriches/videos']
for i in range(3):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        data = json.loads(r.stdout)
        entries = data.get('entries', [])
        if entries:
            for e in entries[:3]:
                print(f"{e.get('id','')} | {e.get('title','')}")
        break
    except Exception as e:
        print(f'Attempt {i+1} error: {e}')
        if i < 2: time.sleep([5,15][i])
else:
    print('FAILED')
