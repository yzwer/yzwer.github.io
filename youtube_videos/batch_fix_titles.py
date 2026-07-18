import re

def fix_html_title(html_file, new_title):
    """修复 HTML 文件的标题（<title> 标签和页面大标题）"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 更新 <title> 标签
    content = re.sub(r'<title>[^<]+</title>', f'<title>{new_title}</title>', content)
    
    # 2. 更新页面大标题（ct-title 类）
    # 先找到当前的标题
    old_title_match = re.search(r'<div class="ct-title">([^<]+)<br>([^<]+)</div>', content)
    if old_title_match:
        # 将新标题分成两行（在合适位置插入 <br>）
        if len(new_title) > 12:
            # 找合适的分割点
            mid = len(new_title) // 2
            for sep in ['：', '—', '，', ' ']:
                idx = new_title.find(sep, mid-3, mid+3)
                if idx > 0:
                    part1 = new_title[:idx+1]
                    part2 = new_title[idx+1:]
                    new_heading = f'{part1}<br>{part2}'
                    break
            else:
                # 没找到合适分隔符，直接中间分割
                part1 = new_title[:mid]
                part2 = new_title[mid:]
                new_heading = f'{part1}<br>{part2}'
        else:
            new_heading = new_title
        
        content = re.sub(
            r'<div class="ct-title">[^<]+<br>[^<]+</div>',
            f'<div class="ct-title">{new_heading}</div>',
            content
        )
    
    # 保存
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

# 修复两个文件
files_to_fix = [
    (r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\4IIJY9Y5L54_wechat_article.html",
     "从国宴座位看懂权力秩序：一场顶级饭局的社交密码"),
    (r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\6PcC0ADq1zo_wechat_article.html",
     "比亚迪股价暴跌背后：特斯拉车主的心跳时刻")
]

for file_path, new_title in files_to_fix:
    try:
        fix_html_title(file_path, new_title)
        print(f'✅ 已修复: {file_path.split("\\")[-1]}')
        print(f'   新标题: {new_title}\n')
    except Exception as e:
        print(f'❌ 修复失败: {e}\n')

print('完成！')
