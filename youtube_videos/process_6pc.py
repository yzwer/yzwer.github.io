# -*- coding: utf-8 -*-
"""Extract audio and run Whisper for 6PcC0ADq1zo"""
import subprocess, sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'
vid = '6PcC0ADq1zo'
mp4 = os.path.join(base, f'{vid}.mp4')
wav = os.path.join(base, f'{vid}.wav')
json_out = os.path.join(base, f'{vid}.json')

# Step 1: ffmpeg extract audio
print(f'[1/2] Extracting audio from {vid}.mp4 ...')
sys.stdout.flush()
for attempt in range(3):
    r = subprocess.run(['ffmpeg','-y','-i',mp4,'-vn','-acodec','pcm_s16le','-ar','16000','-ac','1',wav],
                       capture_output=True, text=True, timeout=120)
    if os.path.exists(wav) and os.path.getsize(wav) > 1000:
        print(f'  Audio OK: {os.path.getsize(wav)//1024}KB')
        break
    print(f'  Attempt {attempt+1} failed, retrying...')
    time.sleep(5)
else:
    print('FATAL: ffmpeg failed')
    sys.exit(1)

# Step 2: Whisper transcription
print(f'[2/2] Running Whisper (base model, zh) ...')
sys.stdout.flush()
for attempt in range(3):
    r = subprocess.run(['whisper', wav, '--model','base','--language','zh',
                        '--output_format','json','--output_dir',base],
                       capture_output=True, text=True, timeout=900)
    if os.path.exists(json_out) and os.path.getsize(json_out) > 100:
        with open(json_out,'r',encoding='utf-8') as f:
            d = json.load(f)
        text = d.get('text','')
        segs = d.get('segments',[])
        print(f'  Whisper OK! {len(segs)} segments, {len(text)} chars')
        print(f'  Preview: {text[:200]}')
        break
    print(f'  Attempt {attempt+1} failed (returncode={r.returncode}), stderr: {r.stderr[:200]}')
    if attempt < 2:
        time.sleep([5,15][attempt])
else:
    print('FATAL: Whisper failed after 3 attempts')
    sys.exit(1)

print('DONE')
