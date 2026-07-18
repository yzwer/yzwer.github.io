import json

with open(r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\whisper_result.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Language:", data.get("language", "unknown"))
print("Segments:", len(data.get("segments", [])))
print()

for seg in data["segments"]:
    start_t = seg["start"]
    end_t = seg["end"]
    text = seg["text"].strip()
    if text:
        m_s, s_s = divmod(int(start_t), 60)
        m_e, s_e = divmod(int(end_t), 60)
        print(f"[{m_s:02d}:{s_s:02d} - {m_e:02d}:{s_e:02d}] {text}")
