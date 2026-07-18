import sys, json, os
from faster_whisper import WhisperModel

# Usage: python whisper_transcribe.py <wav> <json_out> <model> <lang>
# Args from run_pipeline.py: "<wav>" "<video_id>.json" base zh
wav_path = sys.argv[1] if len(sys.argv) > 1 else "LOXQXHHRUvU.wav"
json_path = sys.argv[2] if len(sys.argv) > 2 else "LOXQXHHRUvU.json"
model_name = sys.argv[3] if len(sys.argv) > 3 else "base"
lang = sys.argv[4] if len(sys.argv) > 4 else "en"

# Derive transcript txt path from json path (same basename)
txt_path = os.path.splitext(json_path)[0] + "_transcript.txt"

print(f"Loading model '{model_name}' for lang '{lang}'...", flush=True)
model = WhisperModel(model_name, device="cpu", compute_type="int8")
print("Transcribing...", flush=True)
segments, info = model.transcribe(wav_path, language=lang, task="transcribe")
print(f"Detected language: {info.language} (prob={info.language_probability:.2f})", flush=True)

text_parts = []
segs_out = []
for seg in segments:
    text_parts.append(seg.text)
    segs_out.append({"start": round(seg.start, 2), "end": round(seg.end, 2), "text": seg.text})

text = "\n".join(text_parts)
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(text)
result = {"text": text, "segments": segs_out, "language": info.language}
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"Done: {len(text)} chars, {len(segs_out)} segments -> {json_path}", flush=True)
