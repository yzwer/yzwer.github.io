import subprocess
import os

VID = "GoO-MQcVnI8"
MP4_PATH = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\GoO-MQcVnI8.mp4'
WAV_PATH = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\GoO-MQcVnI8.wav'

print('[1/2] Extracting audio...')
cmd = [
    'ffmpeg', '-i', MP4_PATH,
    '-vn', '-acodec', 'pcm_s16le',
    '-ar', '16000', '-ac', '1',
    WAV_PATH, '-y'
]

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0 and os.path.exists(WAV_PATH):
    size_mb = os.path.getsize(WAV_PATH) / (1024 * 1024)
    print('OK: Audio extracted successfully')
    print(f'    Size: {size_mb:.2f} MB')
    print(f'    Path: {WAV_PATH}')
else:
    print('ERROR: Audio extraction failed')
    print(f'    Return code: {result.returncode}')
    print(f'    stderr (last 500 chars): {result.stderr[-500:]}')
    exit(1)

print('\n[2/2] Verifying file...')
if os.path.exists(WAV_PATH):
    print('OK: WAV file is ready')
    print('Next step: Run Whisper transcription')
else:
    print('ERROR: WAV file not found!')
    exit(1)
