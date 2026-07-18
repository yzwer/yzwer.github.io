import json, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')

APPID = "wxabc1784dbf87c3de"
SECRET = "10d4335f33efcb36d3f27551870595d5"

def get_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
    with urllib.request.urlopen(url, timeout=10) as r:
        d = json.loads(r.read().decode())
    return d['access_token']

def get_draft(token, media_id):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/get?access_token={token}"
    payload = json.dumps({"media_id": media_id}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def update_draft_title(token, media_id, new_title, author="OpenClaw", digest="", content_source_url=""):
    """只更新标题，保留原有内容"""
    # 先获取原草稿内容
    draft = get_draft(token, media_id)
    news_item = draft.get('news_item', [{}])[0]
    
    # 保留原有内容，只改标题
    original_content = news_item.get('content', '')
    original_thumb = news_item.get('thumb_media_id', '')
    
    article = {
        "media_id": media_id,
        "index": 0,
        "title": new_title,
        "author": author,
        "digest": digest if digest else news_item.get('digest', ''),
        "content": original_content,
        "content_source_url": content_source_url if content_source_url else news_item.get('content_source_url', ''),
        "thumb_media_id": original_thumb
    }
    
    url = f"https://api.weixin.qq.com/cgi-bin/draft/update?access_token={token}"
    payload = json.dumps({"articles": [article]}, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

token = get_token()
print(f"✅ token 获取成功\n")

# 11篇草稿的 media_id
media_ids = [
    "bvX396z8kF5D2hkDHrmN4GqPC7pQ3bYPo5kDS6MR9AtRJcYSqfNJE1dAg20URBID",
    "bvX396z8kF5D2hkDHrmN4Hxor-enEs2hQR4bATc4FFN7UliwaCVpiT4N3oNyKipa",
    # ... 先处理第一篇测试
]

# 测试：读取第一篇草稿内容，生成新标题
mid = media_ids[0]
print(f"正在处理: {mid[:30]}...")
draft = get_draft(token, mid)
content = draft['news_item'][0]['content']
old_title = draft['news_item'][0]['title']

print(f"旧标题: {old_title}")
print(f"内容长度: {len(content)} 字符")

# 从内容中提取关键信息来生成标题
# 简单提取前500字符的中文内容
import re
text_content = re.sub(r'<[^>]+>', '', content[:2000])
print(f"\n内容预览:\n{text_content[:300]}...\n")

# TODO: 根据内容生成新标题
# 暂时用一个示例标题
new_title = "巴菲特退休后的第一次股东会：伯克希尔的后巴菲特时代开局"
print(f"新标题: {new_title}")

# 更新标题
result = update_draft_title(token, mid, new_title)
print(f"\n更新结果: {result}")
