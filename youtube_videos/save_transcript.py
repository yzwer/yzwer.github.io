import json

# Read the whisper result
with open(r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\whisper_result.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert Traditional Chinese to Simplified Chinese
try:
    from opencc import OpenCC
    cc = OpenCC("t2s")
    convert = cc.convert
except ImportError:
    # Manual common conversion as fallback
    print("opencc not available, using raw text")
    convert = lambda x: x

# Build SRT content
srt_lines = []
txt_lines = []
for i, seg in enumerate(data["segments"], 1):
    text = seg["text"].strip()
    if not text:
        continue
    text = convert(text)
    
    start_t = seg["start"]
    end_t = seg["end"]
    
    # Format SRT timestamps
    def fmt_time(t):
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = int(t % 60)
        ms = int((t - int(t)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    
    srt_lines.append(f"{i}")
    srt_lines.append(f"{fmt_time(start_t)} --> {fmt_time(end_t)}")
    srt_lines.append(text)
    srt_lines.append("")
    
    m_s, s_s = divmod(int(start_t), 60)
    m_e, s_e = divmod(int(end_t), 60)
    txt_lines.append(f"[{m_s:02d}:{s_s:02d} - {m_e:02d}:{s_e:02d}] {text}")

# Save SRT
srt_content = convert("\n".join(srt_lines))
srt_path = r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\sojKNj_uXYU.srt"
with open(srt_path, "w", encoding="utf-8") as f:
    f.write(srt_content)

# Save TXT
txt_content = convert("\n".join(txt_lines))
txt_path = r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\sojKNj_uXYU_transcript.txt"
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(txt_content)

# Save full text
full_text = convert(data["text"].strip())
full_path = r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\sojKNj_uXYU_fulltext.txt"
with open(full_path, "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"SRT saved: {srt_path}")
print(f"TXT saved: {txt_path}")
print(f"Full text saved: {full_path}")
print(f"Total segments: {len(data['segments'])}")
print(f"Full text length: {len(full_text)} chars")
