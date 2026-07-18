import json, urllib.request, sys, re
sys.stdout.reconfigure(encoding='utf-8')

APPID = "wxabc1784dbf87c3de"
SECRET = "10d4335f33efcb36d3f27551870595d5"

url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
with urllib.request.urlopen(url, timeout=10) as r:
    d = json.loads(r.read().decode())
token = d['access_token']

# 11篇"继续减仓"的 media_id
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
]

print("正在分析11篇问题草稿...\n")

video_id_counts = {}
for i, mid in enumerate(media_ids):
    try:
        url = f"https://api.weixin.qq.com/cgi-bin/draft/get?access_token={token}"
        payload = json.dumps({"media_id": mid}).encode('utf-8')
        req = urllib.request.Request(url, data=payload, method='POST')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode())
        
        content = ''
        for item in d.get('news_item', []):
            content += item.get('content', '')
        
        # 从HTML里找YouTube链接
        video_ids = re.findall(r'youtube\.com/watch\?v=([\w-]+)', content)
        video_ids = list(set(video_ids))
        
        print(f"[{i+1:2d}] media_id: {mid[:30]}...")
        print(f"     找到视频ID: {video_ids}")
        
        for vid in video_ids:
            video_id_counts[vid] = video_id_counts.get(vid, 0) + 1
        
    except Exception as e:
        print(f"[{i+1:2d}] ❌ 错误: {e}")

print("\n" + "="*50)
print(f"去重后共有 {len(video_id_counts)} 个不同的视频:")
for vid, count in video_id_counts.items():
    print(f"  {vid} → 出现 {count} 次")
