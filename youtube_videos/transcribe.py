import whisper
import json
import time

print("Loading Whisper base model...")
model = whisper.load_model("base")
print("Model loaded. Starting transcription...")

start = time.time()
result = model.transcribe(
    r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\sojKNj_uXYU.wav",
    language="zh",
    verbose=False
)
elapsed = time.time() - start
print(f"Transcription completed in {elapsed:.1f}s")
print(f"Detected language: {result.get('language', 'unknown')}")

# Save full result
with open(r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\whisper_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# Print transcript
print("\n=== TRANSCRIPT ===")
for seg in result["segments"]:
    start_t = seg["start"]
    end_t = seg["end"]
    text = seg["text"].strip()
    if text:
        m_s, s_s = divmod(int(start_t), 60)
        m_e, s_e = divmod(int(end_t), 60)
        print(f"[{m_s:02d}:{s_s:02d} - {m_e:02d}:{s_e:02d}] {text}")
print("=== END ===")
