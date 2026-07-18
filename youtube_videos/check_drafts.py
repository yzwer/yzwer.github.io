import json, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')

APPID = "wxabc1784dbf87c3de"
SECRET = "10d4335f33efcb36d3f27551870595d5"

# 获取 token
url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
with urllib.request.urlopen(url, timeout=10) as r:
    d = json.loads(r.read().decode())
if 'errcode' in d:
    print(f"❌ Token error: {d}")
    sys.exit(1)
token = d['access_token']
print(f"✅ token 获取成功\n")

# 获取草稿列表（最多100条）
url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={token}"
payload = json.dumps({"offset": 0, "count": 20, "no_content": 1}, ensure_ascii=False).encode('utf-8')
req = urllib.request.Request(url, data=payload, method='POST')
req.add_header('Content-Type', 'application/json; charset=utf-8')
with urllib.request.urlopen(req, timeout=30) as r:
    d = json.loads(r.read().decode())

print(f"草稿箱总数: {d.get('total_count', '?')}")
print(f"本次返回: {len(d.get('item', []))} 条\n")
print("=" * 50)
for item in d.get('item', []):
    media_id = item['media_id']
    content = item['content']
    for article in content.get('news_item', []):
        title = article['title']
        print(f"title: {title}")
        print(f"  media_id: {media_id}")
        print(f"  url: {article.get('url', 'N/A')}")
        print()
