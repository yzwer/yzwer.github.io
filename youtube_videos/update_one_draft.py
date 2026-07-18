import json, urllib.request, sys, re
sys.stdout.reconfigure(encoding='utf-8')

APPID = "wxabc1784dbf87c3de"
SECRET = "10d4335f33efcb36d3f27551870595d5"

def get_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
    with urllib.request.urlopen(url, timeout=10) as r:
        d = json.loads(r.read().decode())
    return d['access_token']

def get_draft_content(token, media_id):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/get?access_token={token}"
    payload = json.dumps({"media_id": media_id}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def update_draft(token, media_id, new_title):
    # 先获取原草稿的完整信息
    draft = get_draft_content(token, media_id)
    item = draft['news_item'][0]
    
    # 构造更新请求（必须包含所有字段）
    articles = [{
        "media_id": media_id,
        "index": 0,
        "title": new_title,
        "author": item.get('author', ''),
        "digest": item.get('digest', ''),
        "content": item.get('content', ''),
        "content_source_url": item.get('content_source_url', ''),
        "thumb_media_id": item.get('thumb_media_id', '')
    }]
    
    url = f"https://api.weixin.qq.com/cgi-bin/draft/update?access_token={token}"
    payload = json.dumps({"articles": articles}, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

token = get_token()
print(f"✅ token 获取成功\n")

# 获取第一篇草稿的内容来分析
mid = "bvX396z8kF5D2hkDHrmN4GqPC7pQ3bYPo5kDS6MR9AtRJcYSqfNJE1dAg20URBID"
print(f"正在分析草稿: {mid[:40]}...")

draft = get_draft_content(token, mid)
content = draft['news_item'][0]['content']
old_title = draft['news_item'][0]['title']

print(f"旧标题: {old_title}\n")

# 从HTML中提取纯文本（去掉标签）
text = re.sub(r'<[^>]+>', ' ', content)
text = re.sub(r'\s+', ' ', text).strip()
print(f"内容预览（前500字）:\n{text[:500]}\n")

# 根据内容生成新标题
new_title = "巴菲特谢幕秀：后巴菲特时代，伯克希尔还能否续写传奇？"
print(f"✅ 新标题: {new_title}\n")

# 更新标题
print("正在更新草稿标题...")
result = update_draft(token, mid, new_title)
print(f"更新结果: {result}")
