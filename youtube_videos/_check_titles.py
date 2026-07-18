import json, os

BASE = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'
vids = ['k1aG0q28Qfg', '_gn03Q1qxtw', 'ExxZ-ug-LFs', 'RYq2pdfv8l0', 's_MKH36lhgg']

for vid in vids:
    info_path = os.path.join(BASE, vid + '_info.json')
    if os.path.exists(info_path):
        with open(info_path, encoding='utf-8-sig') as f:
            info = json.load(f)
        title = info.get('title', 'N/A')
        print(f'{vid}: {title}')
    else:
        print(f'{vid}: no info.json')