import subprocess, sys, os

VID = 'GoO-MQcVnI8'
INPUT_VIDEO = f'{VID}.mp4'
OUTPUT_AUDIO = f'{VID}.wav'

print(f'Extracting audio from: {INPUT_VIDEO}')
print(f'Output: {OUTPUT_AUDIO}')

# 使用 ffmpeg 提取音频
cmd = [
    'ffmpeg',
    '-i', INPUT_VIDEO,
    '-vn',                      # 不要视频
    '-acodec', 'pcm_s16le',   # PCM 16-bit
    '-ar', '16000',            # 采样率 16kHz
    '-ac', '1',                # 单声道
    '-y',                      # 覆盖输出文件
    OUTPUT_AUDIO
]

print(f'Command: {" ".join(cmd)}')
print('Running ffmpeg...')

result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

if result.returncode == 0:
    print('Audio extraction successful!')
    if os.path.exists(OUTPUT_AUDIO):
        size = os.path.getsize(OUTPUT_AUDIO) / (1024 * 1024)
        print(f'Audio file size: {size:.2f} MB')
    else:
        print('Warning: WAV file not found after extraction')
else:
    print(f'ffmpeg failed with return code: {result.returncode}')
    # ffmpeg 输出通常在 stderr
    if result.stderr:
        # 只显示最后 500 字符
        print(f'FFmpeg stderr (last 500 chars): ...{result.stderr[-500:]}')
    sys.exit(1)
