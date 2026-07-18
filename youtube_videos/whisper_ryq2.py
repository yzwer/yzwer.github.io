# -*- coding: utf-8 -*-
"""Run Whisper on RYq2pdfv8l0.wav"""
import subprocess, sys, os, time

wav = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'RYq2pdfv8l0.wav')
out_dir = os.path.dirname(os.path.abspath(__file__))
cmd = ['whisper', wav, '--model', 'base', '--language', 'zh',
       '--output_format', 'json', '--output_dir', out_dir]

print(f'Running Whisper on {os.path.basename(wav)} (15min audio)')
print(f'Cmd: {" ".join(cmd)}')
sys.stdout.flush()

for attempt in range(3):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            # Check output
            json_file = os.path.join(out_dir, 'RYq2pdfv8l0.json')
            if os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf-8') as f:
                    import json
                    data = json.load(f)
                text = data.get('text', '')
                segments = data.get('segments', [])
                print(f'Transcription SUCCESS!')
                print(f'Total text length: {len(text)} chars')
                print(f'Segments: {len(segments)}')
                # Show first 500 chars
                print(f'Preview: {text[:500]}')
                if len(text) > 500:
                    print(f'...(truncated)...')
                break
            else:
                print(f'Whisper succeeded but JSON not found at {json_file}')
        else:
            print(f'Attempt {attempt+1} failed. stderr: {result.stderr[:300]}')
    except subprocess.TimeoutExpired:
        print(f'Attempt {attempt+1} timed out after 600s')
    except Exception as e:
        print(f'Attempt {attempt+1} error: {e}')
    
    if attempt < 2:
        wait = [5, 15][attempt]
        print(f'Retrying in {wait}s...')
        time.sleep(wait)
else:
    print('All 3 attempts failed')
