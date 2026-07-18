import json

vids = ['k1aG0q28Qfg', '_gn03Q1qxtw', 'ExxZ-ug-LFs', 'RYq2pdfv8l0', 's_MKH36lhgg']
BASE = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'

results = []
for vid in vids:
    path = f'{BASE}\\{vid}.json'
    # Try both encodings
    data = None
    for enc in ['utf-8-sig', 'utf-8', 'gbk']:
        try:
            with open(path, encoding=enc) as f:
                data = json.load(f)
            break
        except:
            continue
    if data is None:
        results.append(f'{vid}: CANNOT DECODE')
        continue
    text = ' '.join([seg['text'].strip() for seg in data.get('segments', [])])
    results.append(f'{vid} [{len(text)} chars]: {text[:200]}')

for r in results:
    print(r)