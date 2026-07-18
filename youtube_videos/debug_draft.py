import json, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')

APPID = "wxabc1784dbf87c3de"
SECRET = "10d4335f33efcb36d3f27551870595d5"

url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
with urllib.request.urlopen(url, timeout=10) as r:
    d = json.loads(r.read().decode())
token = d['access_token']
print(f"✅ token obtained\n")

# Try to get one draft detail
media_id = "bvX396z8kF5D2hkDHrmN4GqPC7pQ3bYPo5kDS6MR9AtRJcYSqfNJE1dAg20URBID"
url = f"https://api.weixin.qq.com/cgi-bin/draft/get?access_token={token}"
payload = json.dumps({"media_id": media_id}).encode('utf-8')
req = urllib.request.Request(url, data=payload, method='POST')
req.add_header('Content-Type', 'application/json')
with urllib.request.urlopen(req, timeout=30) as r:
    resp = r.read().decode()
    print("API Response:")
    print(resp[:500])
    print("\n...")
    d = json.loads(resp)
    print(f"\nKeys in response: {list(d.keys())}")
    if 'news_item' in d:
        for item in d['news_item']:
            print(f"Title: {item.get('title')}")
            print(f"Source URL: {item.get('content_source_url')}")
