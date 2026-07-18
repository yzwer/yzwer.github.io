import json, sys

vids = ['k1aG0q28Qfg', '_gn03Q1qxtw', 'ExxZ-ug-LFs', 'RYq2pdfv8l0', 's_MKH36lhgg']
BASE = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'

for vid in vids:
    path = f'{BASE}\\{vid}.json'
    with open(path, 'rb') as f:
        raw = f.read()
    # Try UTF-8 first, then GBK
    for enc in ['utf-8', 'gbk', 'latin-1']:
        try:
            data = json.loads(raw.decode(enc, errors='replace'))
            break
        except:
            continue
    text = ' '.join([seg['text'].strip() for seg in data.get('segments', [])])
    print(f'=== {vid} ({len(text)} chars) ===')
    print(text[:800])
    print()