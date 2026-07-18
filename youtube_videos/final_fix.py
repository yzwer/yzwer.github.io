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

def delete_draft(token, media_id):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/delete?access_token={token}"
    payload = json.dumps({"media_id": media_id}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def create_draft(token, title, content, thumb_media_id, source_url=''):
    article = {
        "title": title,
        "author": "OpenClaw",
        "digest": title[:50],
        "content": content,
        "content_source_url": source_url,
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    payload = json.dumps({"articles": [article]}, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

token = get_token()
print(f"✅ token 获取成功\n")

# 获取第一篇草稿（提取 thumb_media_id 和 content）
mid = "bvX396z8kF5D2hkDHrmN4GqPC7pQ3bYPo5kDS6MR9AtRJcYSqfNJE1dAg20URBID"
print(f"正在读取旧草稿...")
draft = get_draft(token, mid)
item = draft['news_item'][0]
content = item['content']
thumb_media_id = item.get('thumb_media_id', '')

print(f"✅ 内容获取成功（{len(content)} 字符）")
print(f"✅ 封面ID: {thumb_media_id}\n")

# 生成新标题
new_title = "巴菲特谢幕：后巴菲特时代，伯克希尔的变与不变"
print(f"新标题: {new_title}\n")

# 创建新草稿（使用相同的封面ID）
print("正在创建新草稿...")
result = create_draft(token, new_title, content, thumb_media_id, source_url="https://www.youtube.com/watch?v=ExxZ-ug-LFs")
if 'media_id' in result:
    new_mid = result['media_id']
    print(f"✅ 新草稿创建成功！media_id: {new_mid}\n")
    
    # 删除旧草稿
    print("正在删除11篇旧草稿...")
    old_mids = [
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
    
    success = 0
    for m in old_mids:
        try:
            r = delete_draft(token, m)
            if r.get('errcode') == 0:
                success += 1
                print(f"  ✅ 已删除: {m[:40]}...")
        except Exception as e:
            print(f"  ❌ 删除失败: {m[:40]}... ({e})")
    
    print(f"\n✅ 完成！删除了 {success}/11 篇旧草稿")
    print(f"✅ 新草稿 media_id: {new_mid}")
    print(f"\n请去微信公众平台查看新草稿：《{new_title}》")
else:
    print(f"❌ 创建失败: {result}")
