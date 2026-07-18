# -*- coding: utf-8 -*-
import subprocess, sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8')
base = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'
vid = 'aOuFC_wWJo8'
mp4 = os.path.join(base, f'{vid}.mp4')
wav = os.path.join(base, f'{vid}.wav')
json_out = os.path.join(base, f'{vid}.json')

print('[1/2] Extracting audio...')
sys.stdout.flush()
for i in range(3):
    subprocess.run(['ffmpeg','-y','-i',mp4,'-vn','-acodec','pcm_s16le','-ar','16000','-ac','1',wav],
                   capture_output=True, text=True, timeout=120)
    if os.path.exists(wav) and os.path.getsize(wav) > 1000:
        print(f'  Audio OK: {os.path.getsize(wav)//1024}KB')
        break
    print(f'  Attempt {i+1} failed')
    time.sleep(5)
else:
    print('FATAL: ffmpeg failed'); sys.exit(1)

print('[2/2] Running Whisper...')
sys.stdout.flush()
for i in range(3):
    r = subprocess.run(['whisper',wav,'--model','base','--language','zh',
                        '--output_format','json','--output_dir',base],
                       capture_output=True, text=True, timeout=900)
    if os.path.exists(json_out) and os.path.getsize(json_out) > 100:
        with open(json_out,'r',encoding='utf-8') as f:
            d = json.load(f)
        print(f'  Whisper OK! {len(d.get("segments",[]))} segments, {len(d.get("text",""))} chars')
        print(f'  Preview: {d["text"][:200]}')
        break
    print(f'  Attempt {i+1} failed (rc={r.returncode})')
    if i < 2: time.sleep([5,15][i])
else:
    print('FATAL: Whisper failed'); sys.exit(1)

print('DONE')
