import os, re

d = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'
files = sorted([f for f in os.listdir(d) if f.endswith('_wechat_article.html')])
print(f'共 {len(files)} 个文章文件\n')
for f in files:
    path = os.path.join(d, f)
    with open(path, 'r', encoding='utf-8') as fp:
        content = fp.read()
    title_m = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    title = title_m.group(1).strip() if title_m else 'NO TITLE'
    h1 = h1_m.group(1).strip() if h1_m else 'NO H1'
    has_cover = 'og:image' in content or 'cover.jpg' in content
    sections = len(re.findall(r'<h2|<h3', content))
    video_id = f.replace('_wechat_article.html', '')
    print(f'[{video_id}]')
    print(f'  <title>: {title[:60]}')
    print(f'  <h1>:    {h1[:60]}')
    print(f'  章节数: {sections}  |  有封面: {has_cover}')
    print()
