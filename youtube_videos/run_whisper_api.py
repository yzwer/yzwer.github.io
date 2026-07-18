import whisper
import os
import json
import sys

# 绝对路径配置
WAV_PATH = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\GoO-MQcVnI8.wav'
JSON_PATH = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\GoO-MQcVnI8.json'

print('[1/3] 检查音频文件...')
if not os.path.exists(WAV_PATH):
    print(f'ERROR: WAV file not found: {WAV_PATH}')
    sys.exit(1)
else:
    size_mb = os.path.getsize(WAV_PATH) / (1024 * 1024)
    print(f'OK: Found WAV file ({size_mb:.2f} MB)')

print('\n[2/3] 加载 Whisper 模型 (base)...')
try:
    model = whisper.load_model('base')
    print('OK: Model loaded successfully')
except Exception as e:
    print(f'ERROR: Failed to load model: {e}')
    sys.exit(1)

print('\n[3/3] 开始转录 (语言: 中文)...')
try:
    # 使用绝对路径，指定中文语言
    result = model.transcribe(WAV_PATH, language='zh', fp16=False)
    print('OK: Transcription completed')
except Exception as e:
    print(f'ERROR: Transcription failed: {e}')
    sys.exit(1)

print('\n保存结果到 JSON...')
try:
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    size_kb = os.path.getsize(JSON_PATH) / 1024
    print(f'OK: Saved to {JSON_PATH} ({size_kb:.2f} KB)')
    print(f'   - Text segments: {len(result.get("segments", []))}')
    print(f'   - Detected language: {result.get("language", "unknown")}')
except Exception as e:
    print(f'ERROR: Failed to save JSON: {e}')
    sys.exit(1)

print('\n=== 完成 ===')
print('Whisper 转录成功！可以生成公众号文章了。')
