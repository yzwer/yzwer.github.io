import whisper
import os
import json
import sys

WAV_PATH = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\GoO-MQcVnI8.wav'
JSON_PATH = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\GoO-MQcVnI8.json'

print('[1/4] Checking audio file...')
if not os.path.exists(WAV_PATH):
    print('ERROR: WAV file not found: ' + WAV_PATH)
    sys.exit(1)
else:
    size_mb = os.path.getsize(WAV_PATH) / (1024 * 1024)
    print('OK: Found WAV file (' + str(round(size_mb, 2)) + ' MB)')

print('\n[2/4] Loading Whisper model (base)...')
try:
    model = whisper.load_model('base')
    print('OK: Model loaded successfully')
except Exception as e:
    print('ERROR: Failed to load model: ' + str(e))
    sys.exit(1)

print('\n[3/4] Starting transcription (language: Chinese)...')
try:
    result = model.transcribe(WAV_PATH, language='zh', fp16=False)
    print('OK: Transcription completed')
except Exception as e:
    print('ERROR: Transcription failed: ' + str(e))
    sys.exit(1)

print('\n[4/4] Saving result to JSON...')
try:
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    size_kb = os.path.getsize(JSON_PATH) / 1024
    print('OK: Saved to ' + JSON_PATH)
    print('    Text segments: ' + str(len(result.get('segments', []))))
    print('    Detected language: ' + str(result.get('language', 'unknown')))
except Exception as e:
    print('ERROR: Failed to save JSON: ' + str(e))
    sys.exit(1)

print('\n=== Whisper transcription completed ===')
print('Output file: ' + JSON_PATH)
print('Next step: Generate WeChat article')
