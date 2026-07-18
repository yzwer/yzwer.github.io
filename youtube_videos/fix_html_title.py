import re

HTML_FILE = r"C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos\sojKNj_uXYU_wechat_article.html"

# Read file
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Generate self-created title based on content
# Article is about: Hantavirus outbreak on Antarctic cruise ship, 30-60% mortality rate, human-to-human transmission controversy
new_title = "南极游轮病毒事件调查：汉坦病毒的真相与误读"

# Update <title> tag
content = re.sub(r'<title>[^<]+</title>', f'<title>{new_title}</title>', content)

# Update cover heading (ct-title class) - handle the <br> tag
old_heading_pattern = r'<div class="ct-title">[^<]+<br>[^<]+</div>'
# The original heading was: "死亡率60%、唯一人传人<br>这艘南极游轮碰上了最凶险的病毒"
# Replace with new title (may need to split if too long)
if len(new_title) > 15:
    # Split into two parts for better display
    mid = len(new_title) // 2
    # Find a good break point (space or punctuation)
    for sep in ['：', '—', '，', ' ']:
        idx = new_title.find(sep, mid-5, mid+5)
        if idx > 0:
            part1 = new_title[:idx+1]
            part2 = new_title[idx+1:]
            new_heading = f'{part1}<br>{part2}'
            break
    else:
        part1 = new_title[:mid]
        part2 = new_title[mid:]
        new_heading = f'{part1}<br>{part2}'
else:
    new_heading = new_title

content = re.sub(r'<div class="ct-title">[^<]+<br>[^<]+</div>', 
                f'<div class="ct-title">{new_heading}</div>', 
                content)

# Save
with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print('Title updated successfully!')
print(f'New title: {new_title}')
print(f'File: {HTML_FILE}')
