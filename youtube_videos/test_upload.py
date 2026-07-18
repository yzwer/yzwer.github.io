import requests, json, re, os

APPID = 'wxabc1784dbf87c3de'
APPSECRET = '10d4335f33efcb36d3f27551870595d5'
WORK_DIR = r'C:\Users\11132\.qclaw\workspace-yw3plsutb1jupnif\youtube_videos'
vid = 'DqDUrNyLxZM'

# get token
for i in range(3):
    try:
        r = requests.get(f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}', timeout=10, proxies={'http': None, 'https': None})
        token = r.json()['access_token']
        break
    except:
        import time; time.sleep(5)

# upload cover
cover = os.path.join(WORK_DIR, f'{vid}_cover.jpg')
with open(cover, 'rb') as f:
    r = requests.post(f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=thumb', files={'media': ('cover.jpg', f, 'image/jpeg')}, timeout=30, proxies={'http': None, 'https': None})
thumb_id = r.json()['media_id']
print('thumb:', thumb_id)

# read article
with open(os.path.join(WORK_DIR, f'{vid}_wechat_article.html'), 'r', encoding='utf-8') as f:
    content = f.read()

# test different title lengths
test_titles = ['跨境券商重罚', '跨境券商被重罚', '跨境券商末路']
for title in test_titles:
    byte_len = len(title.encode('utf-8'))
    print(f'Testing: {title} ({byte_len} bytes)')
    articles = [{'title': title, 'author': '', 'content': content, 'digest': 'test', 'thumb_media_id': thumb_id, 'content_source_url': '', 'show_cover_pic': 1}]
    r = requests.post(f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}', json={'articles': articles}, timeout=30, proxies={'http': None, 'https': None})
    result = r.json()
    print('Result:', json.dumps(result, ensure_ascii=False))
    if 'media_id' in result:
        print('SUCCESS!')
        break
