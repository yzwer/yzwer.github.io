# -*- coding: utf-8 -*-
"""Check @sunriches channel for new videos"""
import subprocess, json, sys, os

cmd = ['yt-dlp', '--flat-playlist', '-J', 'https://www.youtube.com/@sunriches/videos']
print(f'Running: {" ".join(cmd)}')
sys.stdout.flush()

for attempt in range(3):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            entries = data.get('entries', [])
            if entries:
                latest = entries[0]
                vid = latest.get('id', '')
                title = latest.get('title', '')
                print(f'Latest video: {vid} - {title}')
                print(f'Total entries: {len(entries)}')
                # Also list top 3
                for i, e in enumerate(entries[:3]):
                    print(f'  [{i+1}] {e.get("id","")} - {e.get("title","")}')
            else:
                print('No entries found')
            break
        else:
            print(f'Attempt {attempt+1} failed: {result.stderr[:200]}')
    except subprocess.TimeoutExpired:
        print(f'Attempt {attempt+1} timed out')
    except Exception as e:
        print(f'Attempt {attempt+1} error: {e}')
    
    if attempt < 2:
        import time
        wait = [5, 15, 30][attempt]
        print(f'Retrying in {wait}s...')
        time.sleep(wait)
else:
    print('All 3 attempts failed')
