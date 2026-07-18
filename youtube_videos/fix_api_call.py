import json, urllib.request, sys, re
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
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

token = get_token()
print(f"✅ token 获取成功\n")

# 获取草稿详情
mid = "bvX396z8kF5D2hkDHrmN4GqPC7pQ3bYPo5kDS6MR9AtRJcYSqfNJE1dAg20URBID"
draft = get_draft(token, mid)
item = draft['news_item'][0]

print(f"旧标题: {item['title']}")
print(f"author: {item.get('author', '')}")
print(f"digest: {item.get('digest', '')[:50]}...")
print(f"content长度: {len(item.get('content', ''))}")
print(f"content_source_url: {item.get('content_source_url', '(空)')}")
print(f"thumb_media_id: {item.get('thumb_media_id', '(空)')}")

# 问题可能在于 content_source_url 或 thumb_media_id 为空
# 让我尝试用完整数据更新，但设置 content_source_url 为有效URL

# 先从HTML里找YouTube链接
content = item['content']
youtube_urls = re.findall(r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+', content)
print(f"\n找到的YouTube链接: {youtube_urls[:3]}")

# 构造更新请求
new_title = "巴菲特谢幕秀：后巴菲特时代，伯克希尔还能否续写传奇？"
articles = [{
    "media_id": mid,
    "index": 0,
    "title": new_title,
    "author": item.get('author', 'OpenClaw'),
    "digest": item.get('digest', '巴菲特退休后的首次股东大会，伯克希尔进入后巴菲特时代')[:64],
    "content": item['content'],
    "content_source_url": youtube_urls[0] if youtube_urls else "https://www.youtube.com/",
    "thumb_media_id": item.get('thumb_media_id', '')
}]

print(f"\n正在更新标题为: {new_title}")
url = f"https://api.weixin.qq.com/cgi-bin/draft/update?access_token={token}"
payload = json.dumps({"articles": articles}, ensure_ascii=False).encode('utf-8')
req = urllib.request.Request(url, data=payload, method='POST')
req.add_header('Content-Type', 'application/json; charset=utf-8')

try:
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.loads(r.read().decode())
    print(f"结果: {result}")
except urllib.error.HTTPError as e:
    print(f"HTTP错误: {e.code}")
    print(e.read().decode())
