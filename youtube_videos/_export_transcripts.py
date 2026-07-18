import json, os

vids = ['k1aG0q28Qfg', '_gn03Q1qxtw', 'ExxZ-ug-LFs', 'RYq2pdfv8l0', 's_MKH36lhgg']
BASE = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'
OUT = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\_transcripts'
os.makedirs(OUT, exist_ok=True)

for vid in vids:
    path = f'{BASE}\\{vid}.json'
    with open(path, encoding='utf-8-sig') as f:
        data = json.load(f)
    text = ' '.join([seg['text'].strip() for seg in data['segments']])
    outpath = f'{OUT}\\{vid}_text.txt'
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'{vid}: {len(text)} chars -> {outpath}')