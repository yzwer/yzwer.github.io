import os, re

HTML_DIR = r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos"

print("正在检查所有 HTML 文件的标题...\n")
print("=" * 60)

html_files = [f for f in os.listdir(HTML_DIR) if f.endswith('_wechat_article.html')]
print(f"找到 {len(html_files)} 个 HTML 文件\n")

results = []
for fname in sorted(html_files):
    fpath = os.path.join(HTML_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 <title> 标签内容
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1) if title_match else 'NO TITLE'
    
    # 提取视频ID
    video_id = fname.replace('_wechat_article.html', '')
    
    results.append((video_id, title, fname))

# 按视频ID排序输出
print(f"{'视频ID':<20} {':':<60}")
print("=" * 60)
for video_id, title, fname in results:
    print(f"{video_id}")
    print(f"  标题: {title}\n")

print("=" * 60)
print(f"共 {len(results)} 个文件")
