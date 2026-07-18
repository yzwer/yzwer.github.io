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
    payload = json.dumps({"media_id": media_id}, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

token = get_token()
print(f"✅ token 获取成功\n")

# 11篇"继续减仓"的 media_id 列表
media_ids = [
    "bvX396z8kF5D2hkDHrmN4GqPC7pQ3bYPo5kDS6MR9AtRJcYSqfNJE1dAg20URBID",
    "bvX396z8kF5D2hkDHrmN4Hxor-enEs2hQR4bATc4FFN7UliwaCVpiT4N3oNyKipa",
    "bvX396z8kF5D2hkDHrmN4NIp0RoU6SPo2PENnRZbmk8CPEA0orCrlydj9c1w5RMI",
    "bvX396z8kF5D2hkDHrmN4F0pEiFjVsRJdwwDv2d6MSsVgvEOHVcyvbObc_7CzKhV",
    "bvX396z8kF5D2hkDHrmN4G9NcNTO9FrnUza8Q7yol3HLZLyRDJqqh4S39psJQdyd",
    "bvX396z8kF5D2hkDHrmN4FleKYbu5Osmjw1HQlFZ6PoAdqz_Ls3EThEvNq4FFmod",
    "bvX396z8kF5D2hkDHrmN4Awt1FJMt0ibP9knxzWvKqcR4IXiru-auNWOkGXttW_s",
    "bvX396z8kF5D2hkDHrmN4MA-ZKNiSfWaUMyxSpHIB7oaDZ6wZ8yJtvdnPlG9z4Bt",
    "bvX396z8kF5D2hkDHrmN4HAnYf6QFGOkdaQ6jXlzJBJJwbQUPtl8nRKqH3-JF_eU",
    "bvX396z8kF5D2hkDHrmN4KFbqqo4oFRQAGDsR5_V8NKs5hOeXGR5TPUzLvj19uGb",
    "bvX396z8kF5D2hkDHrmN4BRpsO-7MDJVGXkI6UHBKYi3fLBOprKkyO-2_rE1k3uW",
    "bvX396z8kF5D2hkDHrmN4CP0ykMXNUELU3AiCW2aPEmyxmEu6f-dNBA0ubw7SAFy",
    "bvX396z8kF5D2hkDHrmN4JHMOsLZA8IA3jVZoa4OHfC8EzC8N6m50OgRn-yDyKaR",
]

print("正在获取13篇草稿的详情...\n")
results = []
for i, mid in enumerate(media_ids):
    try:
        d = get_draft(token, mid)
        content = d.get('content', {})
        for item in content.get('news_item', []):
            title = item['title']
            source_url = item.get('content_source_url', '')
            # 从 source_url 提取 video ID
            video_id = None
            m = re.search(r'youtube\.com/watch\?v=([\w-]+)', source_url)
            if m:
                video_id = m.group(1)
            results.append({
                'index': i+1,
                'media_id': mid,
                'title': title,
                'video_id': video_id,
                'source_url': source_url
            })
            print(f"[{i+1:2d}] title: {title}")
            print(f"     video_id: {video_id}")
            print(f"     media_id: {mid[:30]}...")
            print()
    except Exception as e:
        print(f"[{i+1:2d}] ❌ 获取失败: {e}")
        results.append({'index': i+1, 'media_id': mid, 'title': 'ERROR', 'video_id': None})

# 去重统计
video_ids = list(set([r['video_id'] for r in results if r.get('video_id')]))
print(f"\n去重后共有 {len(video_ids)} 个不同的视频ID:")
for vid in video_ids:
    print(f"  - {vid}")
